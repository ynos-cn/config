from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from utils.base_delete import delete_model_instances
from utils.base_query import (
    delete_user_organizations,
    get_all_parent_orgs,
    get_filter,
    get_sorter,
    get_sorter_sql,
    get_user_organizations,
    getBaseParams,
)
from utils.utils import (
    format_datetime,
    json_response,
    new_call_id,
)
from ..models import EnvInfo, CustomUser, Project, ProjectSerializer, RoleRelation
from rest_framework.parsers import JSONParser
from utils.decorators import GET, POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q
from django.db import transaction, connection, DatabaseError, connections
from ..utils import EnvironmentType


@POST("create")
@auth_user()
def create(request: HttpRequest):
    """
    创建项目优化版（全SQL实现）
    优化点：
    1. 全面改用原生SQL提升性能
    2. 增强事务管理
    3. 防御性编程强化
    4. 精细化错误处理
    """
    print("\n")
    logger.info("============= 进入 创建项目 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 1. 参数解析与校验 ==========================
        body = JSONParser().parse(request)
        logger.info(f"请求参数: {body}")

        # 必填字段校验
        app_name = body.get("appName")
        project_managers = body.get("projectManagers")
        if not app_name:
            return JsonResponse(
                json_response(code=400, msg="项目名称不能为空", success=False),
                status=400,
            )
        if not project_managers:
            return JsonResponse(
                json_response(code=400, msg="负责人不能为空", success=False), status=400
            )

        # 获取用户信息
        org_id = request.user.get("orgId")
        org_name = body.get("orgName", "")
        user_name = request.user.get("username", "")

        # ========================== 2. 项目名称唯一性校验 ==========================
        with connections["config_db"].cursor() as cursor:
            check_project_sql = f"""
            SELECT COUNT(*) 
            FROM {Project._meta.db_table} 
            WHERE app_name = %s 
              AND org_id = %s 
              AND (is_delete IS NULL OR is_delete != 1)  -- 添加 is_delete 条件
            """
            cursor.execute(check_project_sql, [app_name, org_id])
            if cursor.fetchone()[0] > 0:
                return JsonResponse(
                    json_response(
                        code=400, msg=f"{app_name} 项目名称已存在", success=False
                    ),
                    status=400,
                )

        # ========================== 3. 创建项目事务 ==========================
        with transaction.atomic(using="config_db"):
            with connections["config_db"].cursor() as cursor:
                try:
                    # ------------------- 3.1 生成项目ID -------------------
                    app_id = new_call_id("-")

                    # ------------------- 3.2 插入项目主数据 -------------------
                    insert_project_sql = f"""
                    INSERT INTO {Project._meta.db_table} 
                    (app_name, app_id, project_managers, description, 
                     pull_switch, env_switch, creator, updater, org_id, org_name, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        insert_project_sql,
                        [
                            app_name,
                            app_id,
                            project_managers,
                            body.get("description", ""),
                            body.get("pullSwitch", 1),
                            body.get("envSwitch", 0),
                            user_name,
                            user_name,
                            org_id,
                            org_name,
                            format_datetime(),
                        ],
                    )
                    logger.info(f"创建项目成功 | 项目ID: {app_id}")

                    # ------------------- 3.3 创建默认环境 -------------------
                    insert_env_sql = f"""
                    INSERT INTO {EnvInfo._meta.db_table} 
                    (app_id, env_type, env_name, env_desc)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(
                        insert_env_sql,
                        [app_id, EnvironmentType.PRODUCTION.value, "Default", ""],
                    )
                    env_id = cursor.lastrowid
                    logger.info(f"创建默认环境成功 | 环境ID: {env_id}")

                    # ------------------- 3.4 创建默认用户 -------------------
                    insert_user_sql = f"""
                    INSERT INTO {CustomUser._meta.db_table} 
                    (app_id, user_name, user_id, secret_key, enable_status)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    user_id = new_call_id()
                    secret_key = new_call_id()
                    cursor.execute(
                        insert_user_sql,
                        [app_id, "Config_default", user_id, secret_key, 1],
                    )
                    logger.info(f"创建默认用户成功 | 用户ID: {user_id}")

                    # ================== 4. 查询并返回结果 ==================
                    # 查询项目详情
                    select_project_sql = f"""
                    SELECT id, app_name, app_id, project_managers, description, pull_switch, env_switch, creator, updater, org_id, org_name, update_time
                    FROM {Project._meta.db_table} 
                    WHERE app_id = %s
                    """
                    cursor.execute(select_project_sql, [app_id])
                    project_data = cursor.fetchone()

                    # 转换为字典格式
                    project_dict = {
                        "id": project_data[0],
                        "appName": project_data[1],
                        "appId": project_data[2],
                        "projectManagers": project_data[3],
                        "description": project_data[4],
                        "pullSwitch": project_data[5],
                        "envSwitch": project_data[6],
                        "creator": project_data[7],
                        "updater": project_data[8],
                        "orgId": project_data[9],
                        "orgName": project_data[10],
                        "updateTime": project_data[11],
                    }

                    return JsonResponse(
                        json_response(
                            code=200,
                            msg=f"{app_name} 项目创建成功",
                            data=project_dict,
                            success=True,
                        )
                    )

                except DatabaseError as e:
                    logger.error(f"数据库操作失败 | SQL: {cursor._last_executed}")
                    raise
                except Exception as e:
                    logger.error(f"事务执行失败: {str(e)}")
                    raise

    except DatabaseError as db_err:
        logger.error(f"数据库错误 | 类型: {type(db_err)} | 错误: {str(db_err)}")
        return JsonResponse(
            json_response(code=500, msg="数据库操作失败", success=False), status=500
        )
    except Exception as e:
        logger.error(f"系统异常 | 类型: {type(e)} | 错误: {str(e)}", exc_info=True)
        return JsonResponse(
            json_response(code=500, msg="服务器内部错误", success=False), status=500
        )


@POST("update")
@auth_user()
def update(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 修改项目 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    id = body.get("id")
    app_name = body.get("appName")
    org_id = request.user.get("orgId")

    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    try:
        with transaction.atomic():
            # 检查项目名称是否已存在（如果提供了新名称）
            if app_name:
                if (
                    Project.objects.using("config_db")
                    .filter(app_name=app_name)
                    .exclude(id=id)
                    .exclude(org_id=org_id)
                    .exclude(is_delete=1)
                    .exists()
                ):
                    return JsonResponse(
                        json_response(
                            code=400, msg=f"{app_name} 项目名称已存在", success=False
                        ),
                        status=400,
                    )

            # 准备更新数据
            update_data = {
                "update_time": format_datetime(),  # 使用Django提供的timezone.now()
                "updater": request.user.get("username"),
            }
            # 只更新提供的字段
            update_fields = {
                "app_name": "appName",
                "project_managers": "projectManagers",
                "description": "description",
                "pull_switch": "pullSwitch",
                "env_switch": "envSwitch",
            }

            for db_field, request_field in update_fields.items():
                if request_field in body:
                    update_data[db_field] = body[request_field]

            # 执行更新
            updated_rows = (
                Project.objects.using("config_db").filter(id=id).update(**update_data)
            )
            if updated_rows == 0:
                return JsonResponse(
                    json_response(code=400, msg="项目不存在或未修改", success=False),
                    status=400,
                )

            # 再次获取项目以获取更新后的数据（如果需要完整的数据）
            project = Project.objects.using("config_db").get(id=id)
            serializer = ProjectSerializer(project)

            return JsonResponse(
                json_response(
                    msg=f"{project.app_name} 项目修改成功",
                    data=serializer.data,
                    success=True,
                ),
                safe=False,
            )
    except Project.DoesNotExist:
        return JsonResponse(
            json_response(code=400, msg="项目不存在", success=False), status=400
        )
    except Exception as e:
        logger.error(f"修改失败: {e}")
        return JsonResponse(
            json_response(code=500, msg="修改失败", success=False), status=500
        )


@GET("id/<str:id>")
@auth_user()
def get_id(request: HttpRequest, id: str):
    print(f"\n")
    logger.info("============= 进入 项目详情 =============")
    logger.info(f"操作人: {request.user}")

    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    try:
        record = Project.objects.using("config_db").filter(id=id).first()
        if not record:
            return JsonResponse(
                json_response(code=400, msg="项目不存在", success=False), status=400
            )

        serializer = ProjectSerializer(record, many=False)
        return JsonResponse(
            json_response(
                msg=f"{record.app_name} 项目详情",
                data=serializer.data,
                success=True,
            ),
            safe=False,
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=500, msg="查询失败", success=False), status=500
        )


@POST("find")
@auth_user()
def find(request: HttpRequest):
    """
    项目查询接口（SQL优化版）
    优化内容：
    1. 原生SQL实现复杂查询
    2. 多表关联权限控制
    3. 机构层级权限处理
    4. 防御性分页参数处理
    """
    print("\n")
    logger.info("============= 项目查询流程 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 参数解析 ==========================
        body = JSONParser().parse(request)
        logger.info(f"原始请求参数: {body}")

        # 分页参数处理
        page = max(1, int(body.get("page", 1)))
        limit = max(1, int(body.get("limit", 10)))

        # 排序处理
        order_by = get_sorter_sql(body, {"create_time": "p"})

        # ========================== 权限参数准备 ==========================
        current_user = request.user.get("username")
        current_org_id = request.user.get("orgId")
        allowed_org_ids = get_all_parent_orgs(
            current_org_id
        )  # 获取当前机构及所有父机构ID

        # ========================== SQL构建 ==========================
        base_query = f"""
        SELECT 
            p.id,
            p.app_name,
            p.app_id,
            p.project_managers,
            p.description,
            p.create_time,
            p.update_time
        FROM {Project._meta.db_table} p
        WHERE p.is_delete IS NULL
        """

        # 基础条件列表
        conditions = []
        params = []

        # -------------------------- 关键词搜索 --------------------------
        if body.get("keywords"):
            keywords = f"%{body['keywords']}%"
            search_fields = ["app_name", "app_id", "description"]
            search_conds = " OR ".join([f"{field} LIKE %s" for field in search_fields])
            conditions.append(f"({search_conds})")
            params.extend([keywords] * len(search_fields))

        # -------------------------- 权限过滤条件 --------------------------
        permission_condition = f"""
        p.creator = '{current_user}'
        OR p.project_managers REGEXP '\\b{current_user}\\b'
        OR EXISTS (
            SELECT 1
            FROM {RoleRelation._meta.db_table} rr
            WHERE rr.app_id = p.app_id
            AND (
                /* 用户类型权限 */
                (rr.user_type = 1 
                 AND rr.username_list LIKE %s)
                OR
                /* 机构类型权限 */
                (rr.user_type = 2 
                 AND rr.org_list IN ({','.join(['%s']*len(allowed_org_ids))}))
            )
        )
        """
        conditions.append(permission_condition)
        params.append(f"%{current_user}%")
        params.extend(allowed_org_ids)

        # 组合所有条件
        if conditions:
            base_query += " AND (" + " AND ".join(conditions) + ")"

        # 排序处理
        if order_by:
            base_query += f" {order_by}"

        # 分页处理 如果 limit 为 -1 则不进行分页
        if body.get("limit") != -1:
            base_query += f" LIMIT {limit} OFFSET {(page-1)*limit}"

        # ========================== 执行查询 ==========================
        with connections["config_db"].cursor() as cursor:
            try:
                # 总数查询
                count_sql = f"SELECT COUNT(*) FROM ({base_query}) AS total"
                cursor.execute(count_sql, params)
                total = cursor.fetchone()[0]

                # 数据查询
                cursor.execute(base_query, params)
                results = cursor.fetchall()

            except DatabaseError as e:
                logger.error(f"SQL执行失败: {cursor._last_executed} | 错误: {str(e)}")
                return JsonResponse(
                    json_response(code=500, msg="数据库查询失败", success=False),
                    status=500,
                )

        # ========================== 结果处理 ==========================
        project_list = []
        for row in results:
            project_list.append(
                {
                    "id": row[0],
                    "appName": row[1],
                    "appId": row[2],
                    "projectManagers": row[3],
                    "description": row[4],
                    "createTime": format_datetime(row[5]),
                    "updateTime": format_datetime(row[6]),
                }
            )

        return JsonResponse(
            json_response(code=200, msg="查询成功", data=project_list, total=total),
            safe=False,
        )

    except Exception as e:
        logger.error(f"系统异常: {str(e)}", exc_info=True)
        return JsonResponse(
            json_response(code=500, msg="服务器内部错误", success=False), status=500
        )


@DELETE("delete")
@auth_user()
def delete(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 项目删除 =============")
    logger.info(f"操作人: {request.user}")

    ids = JSONParser().parse(request)
    logger.info(f"获取到的参数: {ids}")

    if ids:
        try:
            length = delete_model_instances(
                Project,
                ids,
                db="config_db",
            )
            if length >= len(ids):
                return JsonResponse(
                    json_response(
                        code=200, msg="删除成功", data=len(ids), success=True
                    ),
                )
            else:
                return JsonResponse(
                    json_response(
                        code=500,
                        msg=f"删除成功{length}个，删除失败{len(ids) - length}个",
                        data=length,
                        success=False,
                    ),
                    status=500,
                )
        except Exception as e:
            logger.error(f"删除失败: {e}")
            return JsonResponse(
                json_response(code=500, msg="删除失败", success=False), status=500
            )

    return JsonResponse(
        json_response(code=400, msg="删除失败 请提供需要删除的id", success=True),
        status=400,
    )

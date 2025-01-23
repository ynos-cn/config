from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from utils.base_delete import delete_model_instances
from utils.base_query import (
    delete_user_organizations,
    get_filter,
    get_sorter,
    get_user_organizations,
    getBaseParams,
)
from utils.utils import (
    format_datetime,
    json_response,
    new_call_id,
)
from ..models import EnvInfo, CustomUser, Project, ProjectSerializer
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
    print(f"\n")
    logger.info("============= 进入 项目查询 =============")
    logger.info(f"操作人: {request.user}")

    # 获取查询参数
    body = JSONParser().parse(request)
    logger.info(f"获取到的参数: {body}")

    # 处理分页参数
    limit = body.get("limit", 10)
    page = body.get("page", 1)

    # 排序
    sorter = get_sorter(body)

    if body.get("body") != None:
        logger.info(f"body = {body.get('body')}")
        query_data = get_filter(
            body.get("body"), ["app_name", "app_id", "project_managers", "description"]
        )
    else:
        query_data = Q()
    query_data &= ~Q(is_delete="1")

    # 获取当前登录用户
    current_user = request.user.get("username")
    current_depart_id = request.user.get("orgId")

    # 构建新的查询条件
    # 1. creator 是当前登录人 或 project_managers 中包含当前登录人
    # 添加 creator 条件
    query_data &= Q(creator=current_user)
    # 处理 project_managers 条件
    # 使用正则表达式确保匹配整个单词
    query_data |= Q(project_managers__iregex=r"\b" + current_user + r"\b")

    # 2. 或者 role 表中 app_id 与项目 app_id 相等且 persons 中包含当前登录人；或者当前登录人的组织在 depart_ids 中
    # 假设 Role 模型中有一个 'app_id' 和 'persons' 字段
    # query_data |= Q(
    #     id__in=Role.objects.filter(
    #         app_id=OuterRef("id"), persons__contains=current_user
    #     ).values("app_id")
    # )
    # query_data |= Q(depart_ids__contains=current_depart_id)

    try:
        logger.info(f"查询条件 = {query_data}")

        # 查询用户 进行分页查询
        record = Project.objects.using("config_db").filter(query_data).order_by(*sorter)
        total = record.count()

        if limit != -1:
            paginator = Paginator(record, limit)
            record = paginator.get_page(page)

        list_data = ProjectSerializer(record, many=True)
        # 返回数据
        return JsonResponse(
            json_response(msg="查询成功", data=list_data.data, total=total), safe=False
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=500, msg="查询失败", success=False), status=500
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

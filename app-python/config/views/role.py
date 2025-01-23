from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from utils.base_delete import delete_model_instances
from utils.base_query import (
    delete_user_organizations,
    get_filter,
    get_user_organizations,
    getBaseParams,
)
from utils.utils import (
    format_datetime,
    json_response,
    new_call_id,
)
from ..models import (
    RoleInfo,
    RoleInfoSerializer,
    RoleRelation,
    Project,
    RoleRelationSerializer,
)
from rest_framework.parsers import JSONParser
from utils.decorators import GET, POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q
from django.db import transaction, connection, DatabaseError
import json
from typing import Dict, Any, Union, Tuple
from ..utils import PermissionType
from django.core.serializers.json import DjangoJSONEncoder


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 创建角色 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    app_id = body.get("appId")  # 项目ID
    object = body.get("object", "*")  # 分组
    name = body.get("name")  # 角色名称
    permission_types = body.get("permissionTypes")  # 权限类型
    persons = body.get("persons")  # 人员
    env_names = body.get("envNames")  # 环境
    if permission_types is None:
        return JsonResponse(
            json_response(code=400, msg="请分配权限类型", success=False), status=400
        )
    if persons is None:
        return JsonResponse(
            json_response(code=400, msg="请提供人员列表", success=False), status=400
        )
    if app_id is None:
        return JsonResponse(
            json_response(code=400, msg="项目ID不能为空", success=False), status=400
        )
    if env_names is None:
        return JsonResponse(
            json_response(code=400, msg="请提供环境类型", success=False), status=400
        )
    if name is None:
        return JsonResponse(
            json_response(code=400, msg="请提供角色名", success=False), status=400
        )

    try:
        with transaction.atomic():
            # 根据appid判断项目是否存在
            current_user = request.user.get("username")
            query_data = Q()
            query_data &= Q(app_id=app_id)
            query_data &= Q(creator=current_user)
            # 处理 project_managers 条件
            # 使用正则表达式确保匹配整个单词
            query_data |= Q(project_managers__iregex=r"\b" + current_user + r"\b")

            if (
                not Project.objects.using("config_db")
                .filter(query_data)
                .exclude(is_delete=1)
                .exists()
            ):
                return JsonResponse(
                    json_response(
                        code=400, msg=f"{app_id} 项目ID不存在", success=False
                    ),
                    status=400,
                )

            # 开始创建角色
            # 判断 permission_types 是否为列表 如果是列表则合并分号分隔
            if isinstance(permission_types, list):
                permission_types = ",".join(map(str, permission_types))

            if isinstance(env_names, list):
                env_names = ",".join(map(str, env_names))

            role_data = {
                "app_id": app_id,
                "name": name,
                "object": object,
                "permission_types": permission_types,
                "env_names": env_names,
            }

            role = RoleInfo.objects.using("config_db").create(**role_data)

            # 使用sql模型批量插入
            sql = f"""
            INSERT INTO {RoleRelation._meta.db_table} (app_id, user_type, role_id, username_list, org_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            # 准备数据，注意处理可能的None值
            data = [
                (
                    app_id,
                    person["type"],
                    role.id,
                    person["names"] or "",  # 如果没有用户名列表，使用空字符串
                    (
                        person.get("orgId") if person["type"] == 2 is not None else None
                    ),  # 注意处理None值
                )
                for person in persons
            ]

            try:
                with connection.cursor() as cursor:
                    # 使用 executemany 来批量执行
                    cursor.execute("USE config_db;")
                    cursor.executemany(sql, data)
            except Exception as e:
                logger.error(f"批量插入失败: {e}")
                # 这里可以选择回滚当前事务，或者其他异常处理
                # 删除已创建的角色
                RoleInfo.objects.using("config_db").filter(id=role.id).delete()
                transaction.rollback()
                raise

            role_list = get_role_data(role_id=role.id)

            return JsonResponse(
                json_response(
                    msg=f"创建成功",
                    data=role_list,
                    success=True,
                ),
                safe=False,
            )
    except Exception as e:
        logger.error(f"创建失败: {e}")
        # 这里可以选择回滚当前事务，或者其他异常处理
        RoleInfo.objects.using("config_db").filter(id=role.id).delete()
        transaction.rollback()
        return JsonResponse(
            json_response(code=500, msg="创建失败", success=False), status=500
        )


@POST("find")
@auth_user()
def find(request: HttpRequest):
    logger.info("============= 进入角色查询 =============")
    logger.info(f"操作人: {request.user}")

    # 获取查询参数
    body = JSONParser().parse(request)
    logger.info(f"获取到的参数: {body}")

    if body.get("body") != None:
        app_id = body.get("body").get("appId")

    # 处理分页参数
    limit = body.get("limit", 10)
    page = body.get("page", 1)

    # 校验 app_id 是否为空
    if not app_id:
        return JsonResponse(
            json_response(code=400, msg="appId 不能为空", success=False), status=400
        )

    try:
        # 调用 get_role_data 方法进行查询
        roles, total = get_role_data(app_id=app_id, page=page, limit=limit)

        logger.info(f"角色查询成功: {roles}")
        return JsonResponse(
            json_response(msg="查询成功", data=roles, total=total), status=200
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=500, msg="查询失败", success=False), status=500
        )


from django.http import HttpRequest, JsonResponse
from django.db import transaction, connection, DatabaseError
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser
from ..models import RoleInfo, RoleRelation, Project
from utils.decorators import DELETE, auth_user
from utils.log import logger
from utils.utils import json_response
from typing import Dict, Any, Union, Tuple
import json
from ..utils import PermissionType


# ---------------------------- 角色删除方法优化 ----------------------------
@DELETE("delete")
@auth_user()
def delete(request: HttpRequest):
    """
    批量删除角色及关联数据（支持事务回滚）
    优化要点：
    1. 动态表名获取
    2. 精细化事务控制
    3. 部分删除结果反馈
    4. 防御性编程增强
    """
    logger.info("============= 进入角色删除流程 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ---------------------------- 1. 参数解析与校验 ----------------------------
        ids = JSONParser().parse(request)
        logger.debug(f"原始请求参数: {ids}")

        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            logger.warning(f"参数类型错误 | 输入: {type(ids)}")
            return JsonResponse(
                json_response(code=400, msg="请求参数必须是整数列表", success=False),
                status=400,
            )

        total_ids = len(ids)

        if total_ids == 0:
            return JsonResponse(
                json_response(code=400, msg="至少需要提供一个角色ID", success=False),
                status=400,
            )

        # ---------------------------- 2. 动态获取表名 ----------------------------
        role_table = RoleInfo._meta.db_table
        relation_table = RoleRelation._meta.db_table
        logger.debug(f"动态表名 | 主表: {role_table} | 关联表: {relation_table}")

        # ---------------------------- 3. 事务执行 ----------------------------
        deleted_count = 0
        try:
            with transaction.atomic(using="config_db"):  # 明确指定数据库
                with connection.cursor() as cursor:
                    cursor.execute("USE config_db;")  # 指定数据库
                    # ---------------------------- 3.1 删除关联数据 ----------------------------
                    delete_relation_sql = f"""
                    DELETE FROM {relation_table}
                    WHERE role_id IN %s
                    """
                    logger.debug(f"执行关联表删除SQL: {delete_relation_sql}")
                    cursor.execute(delete_relation_sql, [tuple(ids)])
                    logger.info(f"删除关联数据影响行数: {cursor.rowcount}")

                    # ---------------------------- 3.2 删除主表数据 ----------------------------
                    delete_role_sql = f"""
                    DELETE FROM {role_table}
                    WHERE id IN %s
                    """
                    logger.debug(f"执行主表删除SQL: {delete_role_sql}")
                    cursor.execute(delete_role_sql, [tuple(ids)])
                    deleted_count = cursor.rowcount
                    logger.info(f"删除主数据影响行数: {deleted_count}")

        except DatabaseError as e:
            logger.error(f"数据库操作失败 | 错误详情: {str(e)}")
            raise

        # ---------------------------- 4. 处理删除结果 ----------------------------
        if deleted_count == total_ids:
            logger.info(f"全部删除成功 | 预期: {total_ids} 实际: {deleted_count}")
            return JsonResponse(
                json_response(
                    code=200,
                    msg="删除成功",
                    data=deleted_count,
                    success=True,
                )
            )
        else:
            logger.warning(
                f"部分删除成功 | 成功: {deleted_count} 失败: {total_ids - deleted_count}"
            )
            return JsonResponse(
                json_response(
                    code=500,
                    msg=f"删除成功{deleted_count}个，删除失败{total_ids - deleted_count}个",
                    data=deleted_count,
                    success=False,
                ),
                status=500,  # 重要变更：部分成功返回500
            )

    except DatabaseError as db_err:
        logger.critical(f"数据库严重错误 | 类型: {type(db_err)} | 错误: {str(db_err)}")
        return JsonResponse(
            json_response(code=500, msg="数据库操作失败", success=False), status=500
        )
    except Exception as e:
        logger.error(f"系统异常 | 类型: {type(e)} | 错误: {str(e)}", exc_info=True)
        return JsonResponse(
            json_response(code=500, msg="服务器内部错误", success=False), status=500
        )


def get_role_data(
    role_id: Union[int, None] = None,
    app_id: Union[str, None] = None,
    page: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> Tuple[Dict[str, Any], int]:
    """
    获取角色数据，支持分页。

    :param role_id: 角色ID（可选）
    :param app_id: 应用ID（可选）
    :param page: 当前页码（可选，默认查询全部）
    :param limit: 每页条数（可选，默认查询全部）
    :return: 返回角色数据和总条数
    """

    if not role_id and not app_id:
        raise ValueError("必须提供role_id或app_id")

    conditions = []
    params = []
    if role_id:
        conditions.append("r.id = %s")
        params.append(role_id)
    if app_id:
        conditions.append("r.app_id = %s")
        params.append(app_id)
    where_clause = " AND ".join(conditions)

    # 查询总数
    count_sql = f"""
    SELECT 
        COUNT(DISTINCT r.id)
    FROM 
        {RoleInfo._meta.db_table} r
    LEFT JOIN 
        {RoleRelation._meta.db_table} rr ON r.id = rr.role_id
    WHERE 
        {where_clause};
    """

    # 数据查询 SQL
    data_sql = f"""
    SELECT 
        r.id,
        r.name,
        r.object,
        r.app_id,
        r.permission_types,
        r.env_names,
        GROUP_CONCAT(
            CONCAT(
                '{{"type":', CAST(rr.user_type AS SIGNED), ',',
                '"names":"', rr.username_list, '"',
                CASE WHEN rr.org_id IS NOT NULL THEN CONCAT(',"orgId":', CAST(rr.org_id AS SIGNED)) ELSE '' END,
                '}}'
            ) SEPARATOR ','
        ) AS persons
    FROM 
        {RoleInfo._meta.db_table} r
    LEFT JOIN 
        {RoleRelation._meta.db_table} rr ON r.id = rr.role_id
    WHERE 
        {where_clause}
    GROUP BY 
        r.id, r.name, r.object, r.app_id, r.permission_types, r.env_names
    """

    # 如果传入分页参数，则加上 LIMIT 和 OFFSET
    if page is not None and limit is not None:
        offset = (page - 1) * limit
        data_sql += f" LIMIT {limit} OFFSET {offset};"

    try:
        with connection.cursor() as cursor:
            # 查询总数
            cursor.execute("USE config_db;")
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]

            # 查询数据
            cursor.execute(data_sql, params)
            results = cursor.fetchall()

        # 处理结果
        role_data_list = []
        for result in results:
            role_data = {
                "id": result[0],
                "name": result[1],
                "object": result[2],
                "appId": result[3],
                "permissionTypes": [],
                "envNames": [],
                "persons": [],
            }

            # 处理 permissionTypes
            try:
                role_data["permissionTypes"] = [
                    PermissionType(int(permission)).name
                    for permission in result[4].split(";")
                    if permission
                ]
            except ValueError:
                role_data["permissionTypes"] = result[4].split(";")
                logger.error(f"转换角色的权限类型时出错 {role_id or app_id}")

            # 处理 envNames
            role_data["envNames"] = [
                env_name for env_name in result[5].split(";") if env_name
            ]

            # 处理 persons
            try:
                role_data["persons"] = json.loads(f"[{result[6]}]") if result[6] else []
            except json.JSONDecodeError:
                role_data["persons"] = [{"error": "解析失败"}]
                logger.error(f"解析角色的人员数据时出错 {role_id or app_id}")

            role_data_list.append(role_data)

        return role_data_list, total

    except DatabaseError as db_err:
        logger.error(f"发生数据库错误: {str(db_err)}")
        raise db_err
    except Exception as e:
        logger.error(f"发生意外错误: {str(e)}")
        raise e

from django.http import HttpRequest, JsonResponse
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
from utils.decorators import POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q
from django.db import transaction, connection, DatabaseError, connections
import json
from typing import Dict, Any, Union, Tuple, List
from ..utils import PermissionType
import re


@POST("create")
@auth_user()
def create(request: HttpRequest):
    """
    创建角色优化版（全SQL实现）
    优化点：
    1. 全面改用原生SQL提升性能
    2. 增强参数校验和类型检查
    3. 改进事务管理
    4. 防御性编程强化
    5. 精细化错误处理
    """
    print("\n")
    logger.info("============= 角色创建流程 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 1. 参数解析与校验 ==========================
        body = JSONParser().parse(request)
        logger.info(f"请求参数: {body}")

        # 参数校验（增强版）
        required_fields = {
            "appId": (body.get("appId"), "项目ID不能为空"),
            "name": (body.get("name"), "角色名称不能为空"),
            "permissionTypes": (body.get("permissionTypes"), "请分配权限类型"),
            "persons": (body.get("persons"), "请提供人员列表"),
            "envNames": (body.get("envNames"), "请提供环境类型"),
        }

        errors = []
        for field, (value, msg) in required_fields.items():
            if not value:
                errors.append(msg)
        if errors:
            return JsonResponse(
                json_response(code=400, msg=", ".join(errors), success=False),
                status=400,
            )

        # 参数类型强制转换
        app_id = str(body["appId"])
        name = str(body["name"])
        object = str(body.get("object", "*"))
        permission_types = body["permissionTypes"]
        env_names = body["envNames"]
        persons = body["persons"]

        # ========================== 2. 项目存在性校验 ==========================
        current_user = request.user.get("username", "")
        project_table = Project._meta.db_table

        with connections["config_db"].cursor() as cursor:
            # 使用原生SQL进行存在性校验
            check_project_sql = f"""
            SELECT COUNT(*) 
            FROM {project_table} 
            WHERE app_id = %s 
              AND (is_delete IS NULL OR is_delete != 1)  -- 添加 is_delete 条件
              AND (
                creator = %s 
                OR project_managers REGEXP %s
              )
            """
            # 构建正则表达式确保精确匹配
            safe_user = re.escape(current_user)  # 转义用户输入
            regex_pattern = r"\b{}\b".format(safe_user)  # 使用 \b 匹配单词边界
            cursor.execute(check_project_sql, [app_id, current_user, regex_pattern])
            if cursor.fetchone()[0] == 0:
                return JsonResponse(
                    json_response(
                        code=400, msg=f"项目{app_id}不存在或无权操作", success=False
                    ),
                    status=400,
                )

        # ========================== 3. 创建角色事务 ==========================
        with transaction.atomic(using="config_db"):
            with connections["config_db"].cursor() as cursor:
                try:
                    # ------------------- 3.1 插入角色主数据 -------------------
                    role_table = RoleInfo._meta.db_table
                    insert_role_sql = f"""
                    INSERT INTO {role_table} 
                    (app_id, name, object, permission_types, env_names)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    # 处理列表类型字段
                    perm_str = (
                        ";".join(map(str, permission_types))
                        if isinstance(permission_types, list)
                        else ""
                    )
                    env_str = (
                        ";".join(map(str, env_names))
                        if isinstance(env_names, list)
                        else ""
                    )

                    cursor.execute(
                        insert_role_sql, [app_id, name, object, perm_str, env_str]
                    )
                    role_id = cursor.lastrowid  # 获取自增ID
                    logger.info(f"创建角色成功 | ID: {role_id}")

                    # ------------------- 3.2 批量插入关联数据 -------------------
                    if not isinstance(persons, list):
                        raise ValueError("人员列表格式错误")

                    relation_table = RoleRelation._meta.db_table
                    insert_relation_sql = f"""
                    INSERT INTO {relation_table} 
                    (app_id, user_type, role_id, username_list, org_list)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    # 构建参数列表（防御性处理）
                    params = []
                    for person in persons:
                        if not isinstance(person, dict):
                            continue

                        p_type = person.get("type")
                        names = person.get("names", "")
                        org_list = person.get("orgIds")

                        # 类型校验
                        if p_type not in [1, 2]:
                            raise ValueError(f"无效的用户类型: {p_type}")

                        # 机构ID校验（当类型为机构时必填）
                        if p_type == 2 and not org_list:
                            raise ValueError("机构类型必须提供orgIds")

                        params.append(
                            (
                                app_id,
                                p_type,
                                role_id,
                                (
                                    ",".join(names)
                                    if isinstance(names, list)
                                    else str(names)
                                ),
                                org_list,
                            )
                        )

                    if not params:
                        raise ValueError("有效人员数据为空")

                    cursor.executemany(insert_relation_sql, params)
                    logger.info(f"插入关联数据成功 | 数量: {len(params)}")

                    # ================== 4. 查询并返回结果 ==================
                    # 使用单独的连接查询结果，避免事务锁定
                    role_data, total = get_role_data_sql(role_id=role_id)

                    return JsonResponse(
                        json_response(
                            code=200, msg="创建成功", data=role_data, success=True
                        ),
                        status=200,
                    )

                except DatabaseError as e:
                    logger.error(f"数据库操作失败 | SQL: {cursor._last_executed}")
                    raise
                except ValueError as e:
                    logger.warning(f"参数验证失败: {str(e)}")
                    return JsonResponse(
                        json_response(code=400, msg=str(e), success=False), status=400
                    )

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


@POST("find")
@auth_user()
def find(request: HttpRequest):
    print("\n")
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
        # 调用 get_role_data_sql 方法进行查询
        roles, total = get_role_data_sql(app_id=app_id, page=page, limit=limit)

        logger.info(f"角色查询成功: {roles}")
        return JsonResponse(
            json_response(msg="查询成功", data=roles, total=total), status=200
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=500, msg="查询失败", success=False), status=500
        )


@POST("update")
@auth_user()
def update(request: HttpRequest):
    """
    更新角色信息
    支持更新的字段：
    - name: 角色名称
    - permissionTypes: 权限类型
    - envNames: 环境类型
    - object: 分组
    - persons: 人员列表（每次更新都会覆盖旧数据）
    """
    print("\n")
    logger.info("============= 角色更新流程 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 1. 参数解析与校验 ==========================
        body = JSONParser().parse(request)
        logger.info(f"请求参数: {body}")

        # 必填字段校验
        required_fields = {
            "id": (body.get("id"), "角色ID不能为空"),
            "persons": (body.get("persons"), "人员列表不能为空"),
            "app_id": (body.get("appId"), "appId不能为空"),
        }
        errors = []
        for field, (value, msg) in required_fields.items():
            if not value:
                errors.append(msg)
        if errors:
            return JsonResponse(
                json_response(code=400, msg=", ".join(errors), success=False),
                status=400,
            )

        # 参数提取
        role_id = int(body["id"])  # 角色ID
        name = body.get("name")  # 角色名称（可选）
        permission_types = body.get("permissionTypes")  # 权限类型（可选）
        env_names = body.get("envNames")  # 环境类型（可选）
        object = body.get("object")  # 分组（可选）
        persons = body["persons"]  # 人员列表（必填）
        app_id = body["appId"]  # AppId（必填）

        # ========================== 2. 角色存在性校验 ==========================
        role_table = RoleInfo._meta.db_table
        with connections["config_db"].cursor() as cursor:
            check_role_sql = f"""
            SELECT COUNT(*) 
            FROM {role_table} 
            WHERE id = %s 
            """
            cursor.execute(check_role_sql, [role_id])
            if cursor.fetchone()[0] == 0:
                return JsonResponse(
                    json_response(
                        code=404, msg=f"角色ID {role_id} 不存在", success=False
                    ),
                    status=404,
                )

        # ========================== 3. 更新角色事务 ==========================
        with transaction.atomic(using="config_db"):
            with connections["config_db"].cursor() as cursor:
                try:
                    # ------------------- 3.1 构建更新字段 -------------------
                    update_fields = []
                    update_params = []

                    if name is not None:
                        update_fields.append("name = %s")
                        update_params.append(str(name))

                    if permission_types is not None:
                        perm_str = (
                            ";".join(map(str, permission_types))
                            if isinstance(permission_types, list)
                            else str(permission_types)
                        )
                        update_fields.append("permission_types = %s")
                        update_params.append(perm_str)

                    if env_names is not None:
                        env_str = (
                            ";".join(map(str, env_names))
                            if isinstance(env_names, list)
                            else str(env_names)
                        )
                        update_fields.append("env_names = %s")
                        update_params.append(env_str)

                    if object is not None:
                        update_fields.append("object = %s")
                        update_params.append(str(object))

                    # ------------------- 3.2 更新角色主数据 -------------------
                    if update_fields:
                        update_sql = f"""
                        UPDATE {role_table} 
                        SET {", ".join(update_fields)} 
                        WHERE id = %s
                        """
                        update_params.append(role_id)  # 添加角色ID作为WHERE条件
                        cursor.execute(update_sql, update_params)
                        logger.info(
                            f"更新角色成功 | ID: {role_id} | 影响行数: {cursor.rowcount}"
                        )

                    # ------------------- 3.3 更新人员列表 -------------------
                    relation_table = RoleRelation._meta.db_table

                    # 删除旧的关联数据
                    delete_relation_sql = f"""
                    DELETE FROM {relation_table} 
                    WHERE role_id = %s
                    """
                    cursor.execute(delete_relation_sql, [role_id])
                    logger.info(f"删除旧的人员列表成功 | 影响行数: {cursor.rowcount}")

                    # 插入新的关联数据
                    if isinstance(persons, list) and persons:
                        insert_relation_sql = f"""
                        INSERT INTO {relation_table} 
                        (app_id, user_type, role_id, username_list, org_list)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        # 构建参数列表
                        params = []
                        for person in persons:
                            if not isinstance(person, dict):
                                continue

                            p_type = person.get("type")
                            names = person.get("names", "")
                            org_list = person.get("orgIds")

                            # 类型校验
                            if p_type not in [1, 2]:
                                raise ValueError(f"无效的用户类型: {p_type}")

                            # 机构ID校验（当类型为机构时必填）
                            if p_type == 2 and not org_list:
                                raise ValueError("机构类型必须提供orgIds")

                            params.append(
                                (
                                    app_id,
                                    p_type,
                                    role_id,
                                    (
                                        ",".join(names)
                                        if isinstance(names, list)
                                        else str(names)
                                    ),
                                    org_list,
                                )
                            )

                        if params:
                            cursor.executemany(insert_relation_sql, params)
                            logger.info(f"插入新的人员列表成功 | 数量: {len(params)}")

                    # ------------------- 3.4 查询并返回更新后的角色数据 -------------------
                    role_data, total = get_role_data_sql(role_id=role_id)

                    return JsonResponse(
                        json_response(
                            code=200, msg="更新成功", data=role_data, success=True
                        ),
                        status=200,
                    )

                except DatabaseError as e:
                    logger.error(f"数据库操作失败 | SQL: {cursor._last_executed}")
                    raise
                except ValueError as e:
                    logger.warning(f"参数验证失败: {str(e)}")
                    return JsonResponse(
                        json_response(code=400, msg=str(e), success=False), status=400
                    )

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


def get_role_data_sql(
    role_id: Union[int, None] = None,
    app_id: Union[str, None] = None,
    page: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> Tuple[List[Dict[str, Any]], int]:
    """
    获取角色数据（支持分页）优化版
    主要优化点：
    1. 精确SQL日志记录
    2. 强化分页参数处理
    3. 增强类型校验
    4. 完善异常处理
    """
    # ========================== 参数校验 ==========================
    if not role_id and not app_id:
        raise ValueError("必须提供 role_id 或 app_id 至少一个参数")

    # ========================== SQL构建 ==========================
    role_table = RoleInfo._meta.db_table
    relation_table = RoleRelation._meta.db_table
    conditions = []
    params = []

    # 构建WHERE条件
    if role_id:
        if not isinstance(role_id, int):
            raise TypeError("role_id 必须为整数")
        conditions.append("r.id = %s")
        params.append(role_id)

    if app_id:
        if not isinstance(app_id, str):
            raise TypeError("app_id 必须为字符串")
        conditions.append("r.app_id = %s")
        params.append(app_id)

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # ------------------------- 总数查询SQL -------------------------
    count_sql = f"""
    SELECT COUNT(DISTINCT r.id)
    FROM {role_table} r
    {where_clause}
    """

    # ------------------------- 数据查询SQL -------------------------
    data_sql = f"""
    SELECT 
        r.id,
        r.name,
        r.object,
        r.app_id,
        r.permission_types,
        r.env_names,
        COALESCE(
            GROUP_CONCAT(
                CONCAT(
                    '{{"type":', rr.user_type, ',',
                    '"names":"', REPLACE(rr.username_list, '"', '\\"'), '"',
                    CASE WHEN rr.org_list IS NOT NULL 
                        THEN CONCAT(',"orgIds":"', REPLACE(rr.org_list, '"', '\\"'), '"')  # 新增双引号包裹
                        ELSE '' END,
                    '}}'
                ) 
                ORDER BY rr.user_type
                SEPARATOR ','
            ), 
            ''
        ) AS persons
    FROM {role_table} r
    LEFT JOIN {relation_table} rr ON r.id = rr.role_id
    {where_clause}
    GROUP BY r.id
    """

    # ========================== 分页处理 ==========================
    if page is not None and limit is not None:
        try:
            page = max(1, int(page))
            limit = max(1, min(int(limit), 1000))  # 限制最大1000条/页
            data_sql += f" LIMIT {limit} OFFSET {(page - 1) * limit}"
        except (TypeError, ValueError) as e:
            logger.warning(
                f"分页参数转换失败 page={page} limit={limit}，将返回全部数据"
            )
    else:
        logger.debug("未提供分页参数，返回全部数据")

    # ========================== 执行查询 ==========================
    try:
        with connections["config_db"].cursor() as cursor:
            # ------------------------- 执行总数查询 -------------------------
            logger.debug(f"执行COUNT SQL: {count_sql} 参数: {params}")
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]

            # ------------------------- 执行数据查询 -------------------------
            logger.debug(f"执行DATA SQL: {data_sql} 参数: {params}")
            cursor.execute(data_sql, params)
            results = cursor.fetchall()

            # ====================== 结果处理 ======================
            role_list = []
            for row in results:
                try:
                    role_data = process_row_data(row)
                    role_list.append(role_data)
                except Exception as e:
                    logger.error(f"行数据处理失败: {str(e)}", exc_info=True)
                    continue

            return role_list, total

    except DatabaseError as e:
        # 获取最后执行的SQL语句
        last_sql = getattr(cursor, "_last_executed", "unknown_sql")
        logger.error(
            f"数据库查询失败 | SQL: {last_sql} | 参数: {params} | 错误: {str(e)}"
        )
        raise RuntimeError("数据库操作失败，请检查查询参数") from e

    except Exception as e:
        logger.error(f"系统异常: {str(e)}", exc_info=True)
        raise RuntimeError("数据处理失败，请联系管理员") from e


def process_row_data(row) -> Dict[str, Any]:
    """处理单行结果数据"""
    # 基础字段处理
    role_data = {
        "id": row[0],
        "name": row[1],
        "object": row[2],
        "appId": row[3],
        "permissionTypes": [],
        "envNames": [],
        "persons": [],
    }

    # 权限类型处理
    if perms := row[4]:
        try:
            role_data["permissionTypes"] = [
                PermissionType(int(p.strip())).name
                for p in perms.split(";")
                if p.strip()
            ]
        except ValueError as e:
            logger.error(f"权限类型转换失败: {perms} | 错误: {str(e)}")
            role_data["permissionTypes"] = perms.split(";")

    # 环境处理
    if envs := row[5]:
        role_data["envNames"] = [e.strip() for e in envs.split(";") if e.strip()]

    # 人员数据处理
    if persons_str := row[6]:
        try:
            # 双重转义处理特殊字符
            safe_json_str = persons_str.replace("\\", "\\\\")
            role_data["persons"] = json.loads(f"[{safe_json_str}]")
        except json.JSONDecodeError as e:
            logger.error(f"人员数据解析失败: {persons_str} | 错误: {str(e)}")
            role_data["persons"] = [{"error": "数据解析失败"}]

    return role_data

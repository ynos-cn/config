from django.http import HttpRequest, JsonResponse
from utils.utils import (
    format_datetime,
    json_response,
    new_call_id,
)
from utils.base_delete import delete_model_instances
from utils.base_query import get_sorter_sql
from ..models import CustomUser, Project
from rest_framework.parsers import JSONParser
from utils.decorators import POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q
from django.db import transaction, DatabaseError, connections
import re


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print("\n")
    logger.info("============= 创建自定义用户 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 1. 参数解析与校验 ==========================
        body = JSONParser().parse(request)
        logger.info(f"请求参数: {body}")

        # 参数校验（增强版）
        required_fields = {
            "user_name": (body.get("userName"), "用户名不能为空"),
            "app_id": (body.get("appId"), "项目ID不能为空"),
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
        user_name = str(body["userName"])

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

        # ========================== 3. 创建自定义用户事务 ==========================
        with transaction.atomic(using="config_db"):
            with connections["config_db"].cursor() as cursor:
                try:
                    # ------------------- 3.1 插入自定义用户数据 -------------------
                    custom_user_table = CustomUser._meta.db_table
                    insert_role_sql = f"""
                    INSERT INTO {custom_user_table} 
                    (app_id, user_name, user_id, secret_key, enable_status, create_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    cursor.execute(
                        insert_role_sql,
                        [
                            app_id,
                            user_name,
                            new_call_id(),
                            new_call_id(),
                            1,
                            format_datetime(),
                        ],
                    )
                    user_id = cursor.lastrowid  # 获取自增ID
                    logger.info(f"创建自定义用户成功 | ID: {user_id}")

                    # ------------------- 3.2 插入成功后返回数据 -------------------
                    # 查询项目详情
                    select_custom_user_sql = f"""
                    SELECT app_id, user_name, user_id, secret_key, enable_status, create_time
                    FROM {CustomUser._meta.db_table} 
                    WHERE id = %s
                    """
                    cursor.execute(select_custom_user_sql, [user_id])
                    user_data = cursor.fetchone()

                    # 转换为字典格式
                    custom_user_dict = {
                        "appId": user_data[0],
                        "userName": user_data[1],
                        "userId": user_data[2],
                        "secretKey": user_data[3],
                        "enableStatus": user_data[4],
                    }

                    return JsonResponse(
                        json_response(
                            code=200,
                            msg="创建成功",
                            data=custom_user_dict,
                            success=True,
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
    logger.info("============= 进入自定义用户查询 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 参数解析 ==========================
        body = JSONParser().parse(request)
        logger.info(f"原始请求参数: {body}")

        # 分页参数处理
        page = int(body.get("page", 1))
        limit = int(body.get("limit", 10))

        # 排序处理
        order_by = get_sorter_sql(body)

        # ========================== SQL构建 ==========================
        base_query = f"""
        SELECT id, app_id, user_name, user_id, secret_key, enable_status, create_time
        FROM {CustomUser._meta.db_table} p
        WHERE p.app_id = %s
        """

        # 基础条件列表
        conditions = []
        params = []
        body = body.get("body", {})
        if body.get("appId"):
            params.append(body["appId"])

        # -------------------------- 关键词搜索 --------------------------
        if body.get("keywords"):
            keywords = f"%{body['keywords']}%"
            search_fields = ["app_name", "app_id", "description"]
            search_conds = " OR ".join([f"{field} LIKE %s" for field in search_fields])
            conditions.append(f"({search_conds})")
            params.extend([keywords] * len(search_fields))

        # 组合所有条件
        if len(conditions) > 0:
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
                    "appId": row[1],
                    "userName": row[2],
                    "userId": row[3],
                    "secretKey": row[4],
                    "enableStatus": row[5],
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


@POST("updateStatus")
@auth_user()
def update_status(request: HttpRequest):
    print("\n")
    logger.info("============= 更新状态 =============")
    logger.info(f"操作人: {request.user}")

    try:
        # ========================== 1. 参数解析与校验 ==========================
        body = JSONParser().parse(request)
        logger.info(f"请求参数: {body}")

        # 必填字段校验
        required_fields = {
            "id": (body.get("id"), "角色ID不能为空"),
            "enable_status": (str(body.get("enableStatus")), "状态不能为空"),
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
        id = int(body["id"])
        enable_status = body.get("enableStatus")
        app_id = body["appId"]  # AppId（必填）

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

        # ========================== 3. 存在性校验 ==========================
        c_user_table = CustomUser._meta.db_table
        with connections["config_db"].cursor() as cursor:
            check_role_sql = f"""
            SELECT COUNT(*)
            FROM {c_user_table}
            WHERE id = %s
            """
            cursor.execute(check_role_sql, [id])
            if cursor.fetchone()[0] == 0:
                return JsonResponse(
                    json_response(code=404, msg=f"用户ID {id} 不存在", success=False),
                    status=404,
                )

        # ========================== 4. 更新事务 ==========================
        with transaction.atomic(using="config_db"):
            with connections["config_db"].cursor() as cursor:
                try:
                    # ------------------- 4.1 更新主数据 -------------------
                    update_sql = f"""
                    UPDATE {c_user_table}
                    SET enable_status = %s
                    WHERE id = %s
                    """
                    cursor.execute(update_sql, [enable_status, id])
                    logger.info(f"更新成功 | ID: {id} | 影响行数: {cursor.rowcount}")

                    # ------------------- 4.2 修改成功后返回数据 -------------------
                    # 查询项目详情
                    select_sql = f"""
                    SELECT app_id, user_name, user_id, secret_key, enable_status, create_time
                    FROM {CustomUser._meta.db_table} 
                    WHERE id = %s
                    """
                    cursor.execute(select_sql, [id])
                    user_data = cursor.fetchone()

                    # 转换为字典格式
                    data_dict = {
                        "appId": user_data[0],
                        "userName": user_data[1],
                        "userId": user_data[2],
                        "secretKey": user_data[3],
                        "enableStatus": user_data[4],
                    }

                    return JsonResponse(
                        json_response(
                            code=200, msg="更新成功", data=data_dict, success=True
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


@DELETE("delete")
@auth_user()
def delete(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 自定义用户删除 =============")
    logger.info(f"操作人: {request.user}")

    ids = JSONParser().parse(request)
    logger.info(f"获取到的参数: {ids}")

    if ids:
        try:
            length = delete_model_instances(
                CustomUser, ids, db="config_db", soft_delete=False
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

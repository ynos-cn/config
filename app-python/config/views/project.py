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
from ..models import EnvInfo, CustomUser, Project, ProjectSerializer
from rest_framework.parsers import JSONParser
from utils.decorators import GET, POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q
from django.db import transaction
from ..utils import EnvironmentType


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 创建项目 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    app_name = body.get("appName")
    project_managers = body.get("projectManagers")
    org_id = request.user.get("orgId")
    org_name = body.get("orgName")

    if not app_name:
        return JsonResponse(
            json_response(code=400, msg="项目名称不能为空", success=False), status=400
        )
    if not project_managers:
        return JsonResponse(
            json_response(code=400, msg="负责人不能为空", success=False), status=400
        )

    try:
        with transaction.atomic():
            # 检查项目名称是否已存在
            if (
                Project.objects.using("default")
                .filter(app_name=app_name, org_id=org_id)
                .exclude(is_delete=1)
                .exists()
            ):
                return JsonResponse(
                    json_response(
                        code=400, msg=f"{app_name} 项目名称已存在", success=False
                    ),
                    status=400,
                )

            user_name = request.user.get("username")
            app_id = new_call_id("-")
            data = {
                "app_name": app_name,
                "app_id": app_id,
                "project_managers": project_managers,
                "description": body.get("description", ""),
                "pull_switch": body.get("pullSwitch", 1),
                "env_switch": body.get("envSwitch", 0),
                "creator": user_name,
                "updater": user_name,
                "org_id": org_id,
                "org_name": org_name,
            }

            project = Project.objects.using("default").create(**data)
            serializer = ProjectSerializer(project)

            # 创建默认环境
            env_data = {
                "app_id": app_id,
                "env_type": EnvironmentType.PRODUCTION,
                "env_name": "Default",
                "env_desc": "",
            }
            env_info = EnvInfo.objects.using("default").create(**env_data)

            # 创建默认自定义用户
            custom_user_data = {
                "app_id": app_id,
                "user_name": "Config_default",
                "user_id": new_call_id(),
                "secret_key": new_call_id(),
                "enable_status": 1,
            }
            c_user = CustomUser.objects.using("default").create(**custom_user_data)
            logger.info(f"创建默认自定义用户成功,项目ID: {app_id}, 用户ID: {c_user.id}")

            logger.info(f"创建默认环境成功,项目ID: {app_id}, 环境ID: {env_info.id}")

        # 成功响应
        return JsonResponse(
            json_response(
                msg=f"{app_name} 项目创建成功", data=serializer.data, success=True
            )
        )

    except Exception as e:
        logger.error(f"创建失败: {e}")
        return JsonResponse(
            json_response(code=500, msg="创建失败", success=False), status=500
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
    project_managers = body.get("projectManagers")
    org_id = request.user.get("orgId")

    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    try:
        with transaction.atomic():
            Project.objects.using("default").select_for_update().get(id=id)

            # 检查项目名称是否已存在（如果提供了新名称）
            if app_name:
                if (
                    Project.objects.using("default")
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
                Project.objects.using("default").filter(id=id).update(**update_data)
            )
            if updated_rows == 0:
                return JsonResponse(
                    json_response(code=400, msg="项目不存在或未修改", success=False),
                    status=400,
                )

            # 再次获取项目以获取更新后的数据（如果需要完整的数据）
            project = Project.objects.using("default").get(id=id)
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
        record = Project.objects.using("default").filter(id=id).first()
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
    query_data, sorter, limit, page = getBaseParams(
        request,
        ["app_name", "app_id", "project_managers", "description"],
    )

    try:
        # 查询用户 进行分页查询
        record = Project.objects.using("default").filter(query_data).order_by(*sorter)
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
                db="default",
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

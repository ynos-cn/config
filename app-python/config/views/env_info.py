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
from ..models.env_info import EnvInfo, EnvInfoSerializer
from rest_framework.parsers import JSONParser
from utils.decorators import GET, POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 创建环境 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    env_type = body.get("envType")
    env_name = body.get("envName")
    app_id = body.get("appId")

    if not env_type:
        return JsonResponse(
            json_response(code=400, msg="环境类型不能为空", success=False), status=400
        )
    if not env_name:
        return JsonResponse(
            json_response(code=400, msg="环境名称不能为空", success=False), status=400
        )
    if not app_id:
        return JsonResponse(
            json_response(code=400, msg="项目ID不能为空", success=False), status=400
        )

    try:
        query_data = Q()
        query_data &= Q(app_id=app_id)
        query_data &= Q(env_name=env_name)
        record = EnvInfo.objects.using("default").filter(query_data).first()

        if record:
            return JsonResponse(
                json_response(
                    code=400,
                    msg=f"{env_name} 环境名称已存在",
                    data=record.id,
                    success=False,
                ),
                status=400,
            )

        data = {
            "env_type": env_type,
            "app_id": app_id,
            "env_name": env_name,
            "env_desc": body.get("envDesc", ""),
        }

        serializer = EnvInfoSerializer(
            EnvInfo.objects.using("default").create(**data), many=False
        )

        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('envName')} 环境创建成功",
                data=serializer.data,
                success=True,
            ),
            safe=False,
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

    if not app_name:
        return JsonResponse(
            json_response(code=400, msg="项目名称不能为空", success=False), status=400
        )
    if not project_managers:
        return JsonResponse(
            json_response(code=400, msg="负责人不能为空", success=False), status=400
        )

    try:
        query_data = Q()
        query_data &= Q(id=id)
        record = Project.objects.using("default").filter(query_data).first()
        if not record:
            return JsonResponse(
                json_response(code=400, msg="项目不存在", success=False), status=400
            )

        query_data = Q()
        query_data &= Q(app_name=app_name)
        query_data &= Q(org_id=org_id)
        query_data &= ~Q(id=id)
        query_data &= ~Q(is_delete=1)
        record = Project.objects.using("default").filter(query_data).first()

        if record:
            return JsonResponse(
                json_response(
                    code=400,
                    msg=f"{app_name} 项目名称已存在",
                    data=record.id,
                    success=False,
                ),
                status=400,
            )

        user_name = request.user.get("username")
        data = {
            "update_time": format_datetime(),
            "app_name": app_name,
            "project_managers": project_managers,
            "description": body.get("description", ""),
            "pull_switch": body.get("pullSwitch", 0),
            "env_switch": body.get("envSwitch", 0),
            "updater": user_name,
        }

        Project.objects.using("default").filter(id=id).update(**data)
        org = Project.objects.using("default").filter(id=id).first()
        serializer = ProjectSerializer(org, many=False)

        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('app_name')} 项目修改成功",
                data=serializer.data,
                success=True,
            ),
            safe=False,
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
                msg=f"{serializer.data.get('name')} 项目详情",
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
    logger.info("============= 进入 项目环境 =============")
    logger.info(f"操作人: {request.user}")

    # 获取查询参数
    query_data, sorter, limit, page = getBaseParams(
        request,
        ["env_type", "env_name", "app_id", "env_desc"],
        allowed_org_ids=False,
        no_is_delete=True,
    )

    try:
        # 查询用户 进行分页查询
        record = EnvInfo.objects.using("default").filter(query_data).order_by(*sorter)
        total = record.count()

        if limit != -1:
            paginator = Paginator(record, limit)
            record = paginator.get_page(page)

        list_data = EnvInfoSerializer(record, many=True)
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
                EnvInfo,
                ids,
                db="default",
                org_id=request.user.get("orgId"),
                soft_delete=False,
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

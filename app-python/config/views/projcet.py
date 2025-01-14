from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from utlis.base_delete import delete_model_instances
from utlis.base_query import (
    delete_user_organizations,
    get_filter,
    get_user_organizations,
    getBaseParams,
)
from utlis.utils import (
    format_datetime,
    json_response,
    new_call_id,
)
from ..models.projcet import Project, ProjectSerializer
from rest_framework.parsers import JSONParser
from utlis.decorators import GET, POST, auth_user, DELETE
from utlis.log import logger
from django.db.models import Q


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
        query_data &= Q(app_name=app_name)
        query_data &= ~Q(is_delete=1)
        org = Project.objects.using("system_db").filter(query_data).first()

        if org:
            return JsonResponse(
                json_response(
                    code=400,
                    msg=f"{app_name} 项目名称已存在",
                    data=org.id,
                    success=False,
                ),
                status=400,
            )

        user_name = request.user.get("username")

        data = {
            "app_name": app_name,
            "app_id": new_call_id(),
            "project_managers": project_managers,
            "description": body.get("description"),
            "pull_switch": body.get("pullSwitch"),
            "env_switch": body.get("envSwitch"),
            "creator": user_name,
            "updater": user_name,
            "org_id": request.user.get("orgId"),
            "org_name": request.user.get("orgName"),
        }

        serializer = ProjectSerializer(
            Project.objects.using("default").create(**data), many=False
        )

        delete_user_organizations()

        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('name')} 项目创建成功",
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
    logger.info("============= 进入 修改机构 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    id = body.get("id")
    name = body.get("name")
    controllerName = body.get("controllerName")
    controllerTel = body.get("controllerTel")
    org_id = body.get("orgId")
    org_name = body.get("orgName")

    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    if id == body.get("orgId"):
        return JsonResponse(
            json_response(code=400, msg="所属机构绑定失败", success=False),
            status=400,
        )

    if id == request.user.get("orgId"):
        return JsonResponse(
            json_response(code=400, msg="不能修改自己所属机构", success=False),
            status=400,
        )

    if not name:
        return JsonResponse(
            json_response(code=400, msg="机构名称不能为空", success=False), status=400
        )

    try:
        query_data = Q()
        query_data &= ~Q(id=id)
        query_data &= Q(name=name)
        query_data &= ~Q(is_delete=1)
        org = Project.objects.using("system_db").filter(query_data).first()
        if org:
            return JsonResponse(
                json_response(
                    code=400, msg=f"{name} 机构已存在", data=org.id, success=False
                ),
                status=400,
            )

        data = {
            "name": name,
            "code": body.get("code"),
            "controller_name": controllerName,
            "controller_tel": controllerTel,
            "update_time": format_datetime(),
            "update_by_id": request.user.get("id"),
            "org_id": org_id,
            "org_name": org_name,
        }
        if not org_id:
            data["org_id"] = request.user.get("orgId")
            data["org_name"] = request.user.get("orgName")

        Project.objects.using("system_db").filter(id=id).update(**data)
        org = Project.objects.using("system_db").filter(id=id).first()
        serializer = ProjectSerializer(org, many=False)

        delete_user_organizations()

        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('name')} 机构修改成功",
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


@POST("updateOrg")
@auth_user()
def update_org(request: HttpRequest):
    """
    更新机构所属组织
    """
    print(f"\n")
    logger.info("============= 进入 更新机构所属组织 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    id = body.get("id")
    org_id = body.get("orgId")
    org_name = body.get("orgName")

    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    if id == body.get("orgId"):
        return JsonResponse(
            json_response(code=400, msg="所属机构绑定失败", success=False),
            status=400,
        )

    try:
        query_data = Q()
        query_data &= ~Q(id=id)
        query_data &= ~Q(is_delete=1)
        org = Project.objects.using("system_db").filter(query_data).first()
        if not org:
            return JsonResponse(
                json_response(code=400, msg=f"机构不存在", success=False),
                status=400,
            )

        data = {
            "update_time": format_datetime(),
            "update_by_id": request.user.get("id"),
            "org_id": org_id,
            "org_name": org_name,
        }
        Project.objects.using("system_db").filter(id=id).update(**data)
        org = Project.objects.using("system_db").filter(id=id).first()
        serializer = ProjectSerializer(org, many=False)

        delete_user_organizations()

        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('name')} 机构修改成功",
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
    logger.info("============= 进入 机构详情 =============")
    logger.info(f"操作人: {request.user}")

    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    try:
        org = Project.objects.using("system_db").filter(id=id).first()
        if not org:
            return JsonResponse(
                json_response(code=400, msg="机构不存在", success=False), status=400
            )

        serializer = ProjectSerializer(org, many=False)
        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('name')} 机构详情",
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
    logger.info("============= 进入 机构查询 =============")
    logger.info(f"操作人: {request.user}")

    # 获取查询参数
    query_data, sorter, limit, page = getBaseParams(
        request,
        ["name", "code", "controller_name", "controller_tel", "org_ame"],
    )

    try:
        # 查询用户 进行分页查询
        orgs = Project.objects.using("system_db").filter(query_data).order_by(*sorter)
        total = Project.objects.using("system_db").filter(query_data).count()

        if limit != -1:
            paginator = Paginator(orgs, limit)
            orgs = paginator.get_page(page)

        user_list = ProjectSerializer(orgs, many=True)
        # 返回数据
        return JsonResponse(
            json_response(msg="查询成功", data=user_list.data, total=total), safe=False
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
    logger.info("============= 进入 机构删除 =============")
    logger.info(f"操作人: {request.user}")

    ids = JSONParser().parse(request)
    logger.info(f"获取到的参数: {ids}")

    if ids:
        try:
            delete_model_instances(
                Project,
                ids,
                db="system_db",
            )
            return JsonResponse(
                json_response(code=200, msg="删除成功", data=len(ids), success=True),
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

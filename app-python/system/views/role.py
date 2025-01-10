from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from utlis.base_query import getBaseParams
from utlis.utils import json_response, new_call_id
from ..models import Role, RoleSerializer
from rest_framework.parsers import JSONParser
from utlis.decorators import POST, auth_user
from utlis.log import logger


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 角色创建 =============")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    name = body.get("name")
    user_id = request.user.get("id")
    org_id = request.user.get("orgId")
    if not name:
        return JsonResponse(
            json_response(code=400, msg="角色名称不能为空", success=False), status=400
        )

    try:
        role = Role.objects.filter(name=name, org_id=org_id).first()
        if role:
            return JsonResponse(
                json_response(
                    code=400, msg=f"{name} 角色已存在", data=role.id, success=False
                ),
                status=400,
            )

        data = {
            "id": new_call_id(),
            "name": name,
            "code": body.get("code"),
            "describe": body.get("describe"),
            "create_by_id": user_id,
            "update_by_id": user_id,
            "org_id": org_id,
        }

        serializer = RoleSerializer(Role.objects.create(**data), many=False)
        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('name')} 角色创建成功",
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


@POST("find")
@auth_user()
def find(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 角色查询 =============")
    # 获取查询参数
    query_data, sorter, limit, page = getBaseParams(
        request, ["name", "code", "describe"]
    )

    try:
        # 查询用户 进行分页查询
        list_data = Role.objects.filter(query_data).order_by(*sorter)
        total = Role.objects.filter(query_data).count()

        if limit != -1:
            paginator = Paginator(list_data, limit)
            list_data = paginator.get_page(page)

        user_list = RoleSerializer(list_data, many=True)
        # 返回数据
        return JsonResponse(
            json_response(msg="查询成功", data=user_list.data, total=total), safe=False
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=400, msg="查询失败", success=False), status=400
        )

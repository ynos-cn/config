from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from utlis.base_delete import delete_model_instances
from utlis.base_query import getBaseParams
from utlis.utils import get_redis_cli, json_response, new_call_id
from ..models import User, UserSerializer, Org
from rest_framework.parsers import JSONParser
from utlis.decorators import DELETE, POST, auth_user
from utlis.log import logger
import bcrypt


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 用户创建 =============")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    password = "123456"
    phone = body.get("phone")
    org_id = body.get("orgId")
    org_name = body.get("orgName")
    joinTime = body.get("joinTime")

    if not phone:
        return JsonResponse(
            json_response(code=400, msg="手机号码不能为空", success=False), status=400
        )

    try:
        if not org_id:
            org_id = request.user.get("orgId")
            org_name = request.user.get("orgName")

        user = (
            User.objects.using("system_db")
            .using("users_db")
            .filter(phone=phone, org_id=org_id)
            .first()
        )
        if user:
            return JsonResponse(
                json_response(
                    code=400, msg=f"该机构 {phone} 手机号码已存在", success=False
                ),
                status=200,
            )

        data = {
            "id": new_call_id(),
            "phone": phone,
            "name": body.get("name"),
            "position": body.get("position"),
            "sex": body.get("sex"),
            "email": body.get("email"),
            "create_by_id": request.user.get("id"),
            "org_id": org_id,
            "org_name": org_name,
            "join_time": joinTime,
            "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode(),
        }

        serializer = UserSerializer(
            User.objects.using("system_db").create(**data), many=False
        )

        return JsonResponse(
            json_response(code=200, msg="创建成功", data=serializer.data, success=True),
        )
    except Exception as e:
        logger.error(f"创建失败: {e}")
        return JsonResponse(
            json_response(code=400, msg="创建失败", success=False), status=400
        )


@POST("update")
@auth_user()
def update(request: HttpRequest):
    from django.db.models import Q

    print(f"\n")
    logger.info("============= 进入 用户更新 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    id = body.get("id")
    phone = body.get("phone")
    name = body.get("name")
    org_id = body.get("orgId")
    org_name = body.get("orgName")
    joinTime = body.get("joinTime")

    if not name:
        return JsonResponse(
            json_response(code=400, msg="姓名不能为空", success=False), status=400
        )
    if not phone:
        return JsonResponse(
            json_response(code=400, msg="手机号码不能为空", success=False), status=400
        )
    if not id:
        return JsonResponse(
            json_response(code=400, msg="id不能为空", success=False), status=400
        )

    try:
        query_data = Q()
        query_data &= ~Q(id=id)
        query_data &= Q(phone=phone)
        query_data &= Q(org_id=org_id)
        user = User.objects.using("system_db").filter(query_data).first()
        if user:
            return JsonResponse(
                json_response(
                    code=400, msg=f"{phone} 手机号码已存在", data=user.id, success=False
                ),
                status=400,
            )

        data = {
            "phone": phone,
            "name": name,
            "position": body.get("position"),
            "sex": body.get("sex"),
            "email": body.get("email"),
            "org_id": org_id,
            "org_name": org_name,
            "join_time": joinTime,
        }

        if not org_id:
            del data["org_id"]
            del data["org_name"]

        User.objects.using("system_db").filter(id=id).update(**data)
        user = User.objects.using("system_db").filter(id=id).first()
        serializer = UserSerializer(user, many=False)

        get_redis_cli().delete(f"user:{user.org_id}_{user.id}")

        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('name')} 用户修改成功",
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


@POST("find")
@auth_user()
def find(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 用户查询 =============")
    # 获取查询参数
    query_data, sorter, limit, page = getBaseParams(
        request, ["name", "phone", "position", "email", "org_name"]
    )

    try:
        # 查询用户 进行分页查询
        list_data = User.objects.using("system_db").filter(query_data).order_by(*sorter)
        total = User.objects.using("system_db").filter(query_data).count()

        if limit != -1:
            paginator = Paginator(list_data, limit)
            list_data = paginator.get_page(page)

        user_list = UserSerializer(list_data, many=True)
        # 返回数据
        return JsonResponse(
            json_response(msg="查询成功", data=user_list.data, total=total), safe=False
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=400, msg="查询失败", success=False), status=400
        )


@DELETE("delete")
@auth_user()
def delete(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 用户删除 =============")
    logger.info(f"操作人: {request.user}")

    ids = JSONParser().parse(request)
    logger.info(f"获取到的参数: {ids}")

    if ids:
        try:
            delete_model_instances(
                User,
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

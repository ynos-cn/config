from django.http import HttpRequest, JsonResponse

from system.models.org import Org
from utlis.base_query import getBaseParams
from .models import User, UserSerializer

# from .serializers import UserSerializer
from utlis.decorators import POST, auth_user
from utlis.utils import json_response, new_call_id
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator
from utlis.log import logger
import bcrypt


# 用户查询接口
@POST("find")
@auth_user()
def find(request: HttpRequest):
    logger.info("============= 进入 用户查询 =============")
    # 获取查询参数
    query_data, sorter, limit, page = getBaseParams(
        request, ["username", "email", "phone"]
    )

    try:
        # 查询用户 进行分页查询
        users = User.objects.using("system_db").filter(query_data).order_by(*sorter)
        total = User.objects.using("system_db").filter(query_data).count()

        if limit != -1:
            paginator = Paginator(users, limit)
            users = paginator.get_page(page)

        user_list = UserSerializer(users, many=True)
        # 返回数据
        return JsonResponse(
            json_response(msg="查询成功", data=user_list.data, total=total), safe=False
        )
    except Exception as e:
        logger.error(f"查询失败: {e}")
        return JsonResponse(
            json_response(code=400, msg="查询失败", success=False), status=400
        )


# 用户注册
@POST("reg")
def reg(request: HttpRequest):
    logger.info("============= 进入 用户注册 =============")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    username = body.get("username")
    password = body.get("password")

    if not username:
        return JsonResponse(
            json_response(code=400, msg="用户名不能为空", success=False), status=400
        )
    if not password:
        return JsonResponse(
            json_response(code=400, msg="密码不能为空", success=False), status=400
        )

    # 查询用户名是否存在，如果存在，则返回错误
    if User.objects.using("system_db").filter(username=username).exists():
        return JsonResponse(
            json_response(code=400, msg=f"{username} 用户名已存在", success=False),
            status=200,
        )
    body["id"] = new_call_id()
    body["password"] = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()
    try:
        serializer = UserSerializer(User.objects.using("system_db").create(**body))
        return JsonResponse(
            json_response(
                msg=f"{serializer.data.get('username')} 用户注册成功",
                data=serializer.data,
            ),
            status=200,
        )
    except Exception as e:
        print(e)
        return JsonResponse(
            json_response(code=400, msg=f"用户注册失败", success=False),
            status=400,
        )


# 验证手机号码是否已存在
@POST("verifyPhone")
def verifyPhone(request: HttpRequest):
    """
    验证手机号码是否已存在
    """
    logger.info("============= 进入 验证手机号码是否已存在 =============")
    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    phone = body.get("phone")
    country_code = body.get("countryCode")
    if not phone:
        return JsonResponse(
            json_response(code=400, msg="手机号码不能为空", success=False), status=400
        )
    if User.objects.using("system_db").filter(phone=phone, code=country_code).exists():
        return JsonResponse(
            json_response(code=400, msg=f"{phone} 手机号码已存在", success=False),
            status=200,
        )
    return JsonResponse(
        json_response(msg=f"{phone} 手机号码不存在", data=phone, success=True),
        status=200,
    )


# 验证邮箱是否已存在
@POST("verifyEmail")
def verifyEmail(request: HttpRequest):
    """
    验证邮箱是否已存在
    """
    logger.info("============= 进入 验证邮箱是否已存在 =============")
    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    email = body.get("email")
    if not email:
        return JsonResponse(
            json_response(code=400, msg="邮箱不能为空", success=False), status=400
        )
    if User.objects.using("system_db").filter(email=email).exists():
        return JsonResponse(
            json_response(code=400, msg=f"{email} 邮箱已存在", success=False),
            status=200,
        )
    return JsonResponse(
        json_response(msg=f"{email} 邮箱不存在", data=email, success=True), status=200
    )


# 验证用户名是否已存在
@POST("verifyUsername")
def verifyUsername(request: HttpRequest):
    """
    验证用户名是否已存在
    """
    logger.info("============= 进入 验证用户名是否已存在 =============")
    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    username = body.get("username")
    if not username:
        return JsonResponse(
            json_response(code=400, msg="用户名不能为空", success=False), status=400
        )
    if User.objects.using("system_db").filter(username=username).exists():
        return JsonResponse(
            json_response(code=400, msg=f"{username} 用户名已存在", success=False),
            status=200,
        )
    return


# 用户创建
@POST("create")
def create(request: HttpRequest):
    logger.info("============= 进入 用户创建 =============")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    password = "123456"
    phone = body.get("phone")
    org_id = body.get("orgId")
    joinTime = body.get("joinTime")

    if not phone:
        return JsonResponse(
            json_response(code=400, msg="手机号码不能为空", success=False), status=400
        )

    if not org_id:
        return JsonResponse(
            json_response(code=400, msg="机构id不能为空", success=False), status=400
        )

    org = Org.objects.using("system_db").filter(id=org_id).first()
    if not org:
        return JsonResponse(
            json_response(code=400, msg="机构不存在", data=org_id, success=False),
            status=400,
        )

    body["id"] = new_call_id()
    body["org_id"] = org.id
    body["org_name"] = org.name
    body["join_time"] = joinTime
    body["password"] = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()

    if "joinTime" in body:
        del body["joinTime"]
    if "orgId" in body:
        del body["orgId"]

    user = User.objects.using("system_db").filter(phone=phone, org_id=org_id).first()
    if user:
        return JsonResponse(
            json_response(
                code=400, msg=f"该机构 {phone} 手机号码已存在", success=False
            ),
            status=200,
        )

    serializer = UserSerializer(User.objects.using("system_db").create(**body), many=False)

    return JsonResponse(
        json_response(code=200, msg="创建成功", data=serializer.data, success=False),
    )

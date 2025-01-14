from datetime import datetime
import json
import random
from django.http import HttpRequest, JsonResponse
from rest_framework.parsers import JSONParser, FormParser
from system.models.user import User, UserSerializer
from utlis.decorators import GET, POST, auth_user
from utlis.log import logger
from utlis.utils import generate_token, get_redis_cli, json_response, new_call_id
import bcrypt
from django.conf import settings
from datetime import datetime
import random
import string
from django.db.models import Q


# 用户名密码登录
@POST("login")
def login(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 用户登录 =============")

    try:
        body = FormParser().parse(request)
        logger.info(f"body: {body}")

        phone = body.get("phone")
        password = body.get("password")

        if not phone:
            return JsonResponse(
                json_response(
                    code=400, msg="用户名/邮箱/手机号码不能为空", success=False
                ),
                status=400,
            )
        if not password:
            return JsonResponse(
                json_response(code=400, msg="密码不能为空", success=False),
                status=400,
            )

        user = (
            User.objects.using("system_db")
            .filter(Q(phone=phone) | Q(email=phone) | Q(username=phone))
            .first()
        )
        logger.info(f"查询到用户: {user}")

        if user is None:
            return JsonResponse(
                json_response(code=400, msg=f"{phone} 用户不存在", success=False),
                status=400,
            )
        else:
            if bcrypt.checkpw(password.encode(), user.password.encode()):

                # 如果登录成功 修改登录时间
                user.last_login_time = datetime.now()
                user.save()

                user = UserSerializer(user).data
                logger.info(f"用户: {user.keys()}")

                keys = user.keys()
                user_dict = {}
                for key in keys:
                    user_dict[key] = "" if user.get(key) is None else user.get(key)

                # 将用户存储在redis
                key = f"user:{user.get('orgId')}_{user.get('id')}"
                get_redis_cli().hmset(
                    key,
                    user_dict,
                )
                get_redis_cli().expire(key, settings.JWT_AUTH["JWT_EXP_DELTA_SECONDS"])

                token = generate_token(user)
                return JsonResponse(
                    json_response(msg="登录成功", data=user, success=True, token=token),
                    status=200,
                )
            else:
                return JsonResponse(
                    json_response(code=400, msg=f"{phone} 密码错误", success=False),
                    status=400,
                )

    except Exception as e:
        logger.error(f"登录失败: {e}")
        return JsonResponse(
            json_response(code=400, msg=f"登录失败", success=False),
            status=400,
        )


# 验证token
@POST("isAuth")
@GET("isAuth")
@auth_user()
def is_auth(request: HttpRequest):
    if request.user:
        return JsonResponse(
            json_response(
                msg="已登录", data=request.user, success=True, token=request.token
            ),
            status=200,
        )

    return JsonResponse({"code": 401, "msg": "未登录"}, status=401)


# 退出登录
@POST("logout")
@GET("logout")
@auth_user()
def logout(request: HttpRequest):
    logger.info("============= 进入 用户退出登录 =============")
    logger.info(f"用户={request.user}")
    id = request.user.get("id")
    org_id = request.user.get("orgId")
    try:
        get_redis_cli().delete(f"user:{org_id}_{id}")
    except Exception as e:
        logger.error(f"退出登录失败: {e}")

    return JsonResponse({"code": 200, "msg": "账号已退出"}, status=200)


# 获取验证码
@POST("code")
def code(request: HttpRequest):
    """
    获取验证码
    """
    logger.info("============= 进入 获取验证码 =============")
    # 获取查询参数
    body = JSONParser().parse(request)
    logger.info(f"获取到的参数: {body}")

    phone = body.get("phone")
    country_code = body.get("countryCode")  # 国家/地区编码
    salt = body.get("salt")

    logger.info(f"phone = {phone}")
    if phone == "" or phone is None:
        return JsonResponse(
            json_response(code=400, msg="手机号不能为空", success=False),
            status=400,
        )

    if salt == "" or salt is None:
        return JsonResponse(
            json_response(code=400, msg="salt 不能为空", success=False),
            status=400,
        )

    # 判断redis是否已存在过验证码
    if get_redis_cli().get(f"code:{phone}-{salt}") is not None:
        return JsonResponse(
            json_response(code=400, msg="验证码已发送", success=False),
            status=400,
        )

    # 生成6位数字的验证码
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    logger.info(f"code = {code}")

    # 将验证码存储在redis
    get_redis_cli().set(f"code:{body.get('phone')}-{salt}", code, ex=60 * 5)

    return JsonResponse(
        json_response(code=200, msg="获取验证码成功", success=True),
        status=200,
    )


# 手机验证码登录
@POST("codeLogin")
def code_login(request: HttpRequest):
    """
    手机验证码登录
    """
    logger.info("============= 进入 手机验证码登录 =============")

    # 获取查询参数
    body = FormParser().parse(request)
    logger.info(f"获取到的参数: {body}")

    phone = body.get("phone")
    salt = body.get("salt")
    _code = body.get("code")  # 手机验证码
    country_code = body.get("countryCode")  # 国家/地区编码

    if phone is None:
        return JsonResponse(
            json_response(code=400, msg="手机号不能为空", success=False),
            status=400,
        )

    if salt is None:
        return JsonResponse(
            json_response(code=400, msg="salt 不能为空", success=False),
            status=400,
        )

    if _code is None:
        return JsonResponse(
            json_response(code=400, msg="验证码不能为空", success=False),
            status=400,
        )

    if len(_code) != 6:
        return JsonResponse(
            json_response(code=400, msg="验证码格式错误", success=False),
            status=400,
        )

    # 查询数据库是否存在该手机号
    user = (
        User.objects.using("system_db").filter(phone=phone, code=country_code).first()
    )
    if user is None:
        return JsonResponse(
            json_response(code=400, msg="手机号不存在", success=False),
            status=400,
        )

    code = get_redis_cli().get(f"code:{phone}-{salt}")
    if code is None:
        return JsonResponse(
            json_response(code=400, msg="验证码已过期", success=False),
            status=400,
        )

    if code.decode("utf-8") != _code:
        return JsonResponse(
            json_response(code=400, msg="验证码错误", success=False),
            status=400,
        )

    user.last_login = datetime.now()
    user.save()
    user = UserSerializer(user).data
    keys = user.keys()
    user_dict = {}
    for key in keys:
        user_dict[key] = "" if user.get(key) is None else user.get(key)

    # 将用户存储在redis
    get_redis_cli().hmset(
        f"user:{user.get('orgId')}_{user.get('id')}",
        user_dict,
    )

    token = generate_token(user)

    # 登录成功删除redis中的验证码
    get_redis_cli().delete(f"code:{phone}-{salt}")

    return JsonResponse(
        json_response(msg="登录成功", data=user, success=True, token=token),
        status=200,
    )


# 验证码注册
@POST("codeRegisterLogin")
def code_register(request: HttpRequest):
    logger.info("============= 进入 手机验证码注册 =============")
    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    phone = body.get("phone")
    country_code = body.get("countryCode")  # 国家/地区编码
    salt = body.get("salt")
    _code = body.get("code")  # 手机验证码

    if phone is None:
        return JsonResponse(
            json_response(code=400, msg="手机号不能为空", success=False),
            status=400,
        )
    if _code is None:
        return JsonResponse(
            json_response(code=400, msg="验证码不能为空", success=False),
            status=400,
        )
    if salt is None:
        return JsonResponse(
            json_response(code=400, msg="salt 不能为空", success=False),
            status=400,
        )

    if len(str(_code)) != 6:
        return JsonResponse(
            json_response(code=400, msg="验证码格式错误", success=False),
            status=400,
        )

    code = get_redis_cli().get(f"code:{phone}-{salt}")
    if code is None:
        return JsonResponse(
            json_response(code=400, msg="验证码已过期", success=False),
            status=400,
        )

    if str(_code) != code.decode("utf-8"):
        return JsonResponse(
            json_response(code=400, msg="验证码错误", success=False),
            status=400,
        )

    # 查询数据库是否存在该手机号
    user = (
        User.objects.using("system_db").filter(phone=phone, code=country_code).first()
    )
    msg = "注册"
    if user is None:
        # 创建用户
        characters = string.ascii_letters + string.digits
        random_code = "".join(random.choice(characters) for _ in range(6))
        password = "".join(random.choice(characters) for _ in range(16))

        _user = {
            "id": new_call_id(),
            "phone": phone,
            "username": f"{phone}_{random_code}",
            "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode(),
            "code": country_code,
            "last_login": datetime.now(),
        }

        serializer = UserSerializer(User.objects.using("system_db").create(**_user))
    else:
        msg = "登录"
        user.last_login = datetime.now()
        user.save()
        serializer = UserSerializer(user)

    # 删除验证码
    get_redis_cli().delete(f"code:{phone}-{salt}")

    # 将用户存储在redis
    keys = serializer.data.keys()
    user_dict = {}
    for key in keys:
        user_dict[key] = (
            "" if serializer.data.get(key) is None else serializer.data.get(key)
        )

    # 将用户存储在redis
    key = f"user:{serializer.data.get('orgId')}_{serializer.data.get('id')}"
    get_redis_cli().hmset(
        key,
        user_dict,
    )
    get_redis_cli().expire(key, settings.JWT_AUTH["JWT_EXP_DELTA_SECONDS"])

    token = generate_token(serializer.data)

    return JsonResponse(
        json_response(
            msg=f"{serializer.data.get('username')} 用户{msg}成功",
            data=serializer.data,
            success=True,
            token=token,
        ),
        status=200,
    )

from django.http import HttpRequest, JsonResponse
from utils.utils import json_response


def custom_400_view(request, exception):
    return JsonResponse(
        json_response(code=400, msg="请求参数错误", success=False), status=400
    )


def custom_403_view(request, exception):
    return JsonResponse(
        json_response(code=403, msg="没有权限", success=False), status=403
    )


def custom_404_view(request, exception):
    path = request.path
    return JsonResponse(
        json_response(code=404, msg=f"找不到相关地址: {path}", success=False),
        status=404,
    )


def custom_500_view(request):
    return JsonResponse(
        json_response(code=500, msg="系统出错了", success=False), status=500
    )

# 验证token
def is_start(request: HttpRequest):
    return JsonResponse({"code": 200, "msg": "服务运行中"}, status=200)

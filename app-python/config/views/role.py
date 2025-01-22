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
from ..models import (
    RoleInfo,
    RoleInfoSerializer,
    RoleRelation,
    Project,
    RoleRelationSerializer,
)
from rest_framework.parsers import JSONParser
from utils.decorators import GET, POST, auth_user, DELETE
from utils.log import logger
from django.db.models import Q
from django.db import transaction


@POST("create")
@auth_user()
def create(request: HttpRequest):
    print(f"\n")
    logger.info("============= 进入 创建角色 =============")
    logger.info(f"操作人: {request.user}")

    body = JSONParser().parse(request)
    logger.info(f"body: {body}")
    app_id = body.get("appId")  # 项目ID
    object = body.get("object", "*")  # 分组
    name = body.get("name")  # 角色名称
    permission_types = body.get("permissionTypes")  # 权限类型
    persons = body.get("persons")  # 人员
    env_names = body.get("envNames")  # 环境
    if permission_types is None:
        return JsonResponse(
            json_response(code=400, msg="请分配权限类型", success=False), status=400
        )
    if persons is None:
        return JsonResponse(
            json_response(code=400, msg="请提供人员列表", success=False), status=400
        )
    if app_id is None:
        return JsonResponse(
            json_response(code=400, msg="项目ID不能为空", success=False), status=400
        )
    if env_names is None:
        return JsonResponse(
            json_response(code=400, msg="请提供环境类型", success=False), status=400
        )
    if name is None:
        return JsonResponse(
            json_response(code=400, msg="请提供角色名", success=False), status=400
        )

    try:
        with transaction.atomic():
            # 根据appid判断项目是否存在
            current_user = request.user.get("username")
            query_data = Q()
            query_data &= Q(app_id=app_id)
            query_data &= Q(creator=current_user)
            # 处理 project_managers 条件
            # 使用正则表达式确保匹配整个单词
            query_data |= Q(project_managers__iregex=r"\b" + current_user + r"\b")

            if (
                not Project.objects.using("config_db")
                .filter(query_data)
                .exclude(is_delete=1)
                .exists()
            ):
                return JsonResponse(
                    json_response(
                        code=400, msg=f"{app_id} 项目ID不存在", success=False
                    ),
                    status=400,
                )

            # 开始创建角色
            # 判断 permission_types 是否为列表 如果是列表则合并分号分隔
            if isinstance(permission_types, list):
                permission_types = ",".join(map(str, permission_types))

            role_data = {
                "app_id": app_id,
                "name": name,
                "object": object,
                "permission_types": permission_types,
                "env_names": env_names,
            }

            role = RoleInfo.objects.using("config_db").create(**role_data)

            # 遍历person处理数据添加到一个list中并且将这个list插入到数据库RoleRelation表中
            role_relation_data = [
                {
                    "app_id": app_id,
                    # "user_type": person["type"],
                    "role_id": role.id,
                    # "username_list": person.get("names"),
                    # "org_id": person.get("orgId") if person["type"] == 2 else None,
                }
                for person in persons
            ]
            res = RoleRelation.objects.using("config_db").bulk_create(
                role_relation_data, ignore_conflicts=False
            )
            print("\n\n\n")
            print(res.app_id)
            print("\n\n\n")

            # # 创建成功后，返回角色信息并且连表查询 RoleRelation 将 RoleRelation 的数据也返回
            # role_data_list = RoleInfoSerializer(role).data
            # role_relation_data_list = RoleRelation.objects.using("config_db").filter(
            #     role_id=role.id
            # )

            # role_relation_data_list = RoleRelationSerializer(
            #     role_relation_data_list, many=True
            # ).data
            # role_data_list["persons"] = role_relation_data_list

            return JsonResponse(
                json_response(
                    msg=f"创建成功",
                    # data=role_data_list,
                    success=True,
                ),
                safe=False,
            )
    except Exception as e:
        logger.error(f"创建失败: {e}")
        transaction.rollback()
        return JsonResponse(
            json_response(code=500, msg="创建失败", success=False), status=500
        )

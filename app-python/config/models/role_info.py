from utils.utils import format_datetime
from django.db import models
from rest_framework import serializers
from ..utils import PermissionType
from datetime import datetime, timezone


# 角色
class RoleInfo(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    app_id = models.CharField(verbose_name="AppID", max_length=256, db_index=True)
    name = models.CharField(verbose_name="角色名", max_length=32)
    object = models.TextField(verbose_name="分组")
    permission_types = models.CharField(
        verbose_name="权限类型；1、只读；2、添加配置；3、修改配置；4、删除配置；6、管理分组；8、提交发布；10、执行发布；11、审批发布",
        max_length=255,
    )
    env_names = models.CharField(verbose_name="环境列表", max_length=1024)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "tb_role"  # 数据库表名
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按照创建时间倒序排列
        managed = False  # 告诉Django不要管理这个表


class RoleInfoSerializer(serializers.ModelSerializer):
    appId = serializers.CharField(source="app_id", read_only=True)
    permissionTypes = serializers.CharField(source="permission_types", read_only=True)
    envNames = serializers.CharField(source="env_names", read_only=True)
    create_time = serializers.SerializerMethodField(default=timezone.utc)

    def get_create_time(self, obj):
        return format_datetime(obj.create_time)

    class Meta:
        model = RoleInfo
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["createTime"] = representation.pop("create_time")
        representation["appId"] = representation.pop("app_id")
        representation["permissionTypes"] = representation.pop("permission_types")
        representation["envNames"] = representation.pop("env_names")

        return representation


# 角色关联表
class RoleRelation(models.Model):
    app_id = models.CharField(verbose_name="AppID", max_length=256, db_index=True)
    user_type = models.SmallIntegerField(verbose_name="角色类型，1、OA帐号；2、机构")
    role_id = models.IntegerField(verbose_name="角色ID")
    username_list = models.TextField(verbose_name="用户list")
    org_list = models.TextField(verbose_name="用户list")

    class Meta:
        db_table = "tb_role_relation"  # 数据库表名
        verbose_name = "角色关系"
        verbose_name_plural = verbose_name
        managed = False  # 告诉Django不要管理这个表


class RoleRelationSerializer(serializers.ModelSerializer):
    appId = serializers.CharField(source="app_id", read_only=True)
    userType = serializers.CharField(source="user_type", read_only=True)
    roleId = serializers.CharField(source="role_id", read_only=True)
    names = serializers.CharField(source="username_list", read_only=True)

    class Meta:
        model = RoleRelation
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["appId"] = representation.pop("app_id")
        representation["userType"] = representation.pop("user_type")
        representation["roleId"] = representation.pop("role_id")
        representation["names"] = representation.pop("username_list")

        return representation

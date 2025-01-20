from django.db.models.manager import BaseManager
from django.db import models

from rest_framework import serializers

from utlis.base_models import BaseModel, BaseModelSerializer
from utlis.utils import format_datetime

# 用户表
class User(BaseModel):
    phone = models.CharField(verbose_name="手机号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    name = models.CharField(verbose_name="姓名", max_length=32)
    username = models.CharField(verbose_name="用户名", max_length=32)

    position = models.CharField(
        verbose_name="职位",
        max_length=32,
        blank=True,
        null=True,
    )
    join_time = models.DateTimeField(
        verbose_name="入职时间",
        max_length=32,
        blank=True,
        null=True,
    )

    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "可用"),
    )
    status = models.IntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=1)

    SEX_CHOICES = (
        (0, "女"),
        (1, "男"),
    )
    sex = models.IntegerField(
        verbose_name="性别",
        choices=SEX_CHOICES,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="邮箱",
        max_length=64,
        blank=True,
        null=True,
    )

    org_name = models.CharField(verbose_name="机构名称", max_length=255)

    last_login_time = models.DateTimeField(
        blank=True, null=True, verbose_name="最近登录时间"
    )

    class Meta:
        db_table = "users"  # 数据库表名
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按照创建时间倒序排列


class UserSerializer(BaseModelSerializer):
    join_time = serializers.SerializerMethodField(source="join_time", read_only=True)
    orgName = serializers.CharField(source="org_name", read_only=True)

    last_login_time = serializers.SerializerMethodField(source="last_login_time")

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
            },  # 密码字段仅在创建或更新时使用，不在响应中返回
            "username": {"required": True, "allow_blank": False},
        }

    def get_last_login_time(self, obj):
        return format_datetime(obj.last_login_time)

    def get_join_time(self, obj):
        return format_datetime(obj.join_time, "%Y-%m-%d")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["joinTime"] = representation.pop("join_time")
        representation["orgName"] = representation.pop("org_name")
        representation["lastLoginTime"] = representation.pop("last_login_time")
        return representation

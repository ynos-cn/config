from utils.utils import format_datetime
from django.db import models
from rest_framework import serializers
from ..utils import EnvironmentType
from datetime import datetime, timezone


# 自定义用户
class CustomUser(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    app_id = models.CharField(verbose_name="AppID", max_length=256)
    user_name = models.CharField(verbose_name="用户名", max_length=32)
    user_id = models.CharField(verbose_name="用户id", max_length=64)
    secret_key = models.CharField(verbose_name="用户密钥", max_length=64)
    enable_status = models.SmallIntegerField(
        verbose_name="用户开关状态：0关闭 1：打开", default=1
    )
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "tb_custom_user"  # 数据库表名
        verbose_name = "自定义用户"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按照创建时间倒序排列


class CustomUserSerializer(serializers.ModelSerializer):
    appId = serializers.CharField(source="app_id", read_only=True)
    userName = serializers.CharField(source="user_name", read_only=True)
    userId = serializers.CharField(source="user_id", read_only=True)
    secret_key = serializers.CharField(source="secretKey", read_only=True)
    enable_status = serializers.CharField(source="enableStatus", read_only=True)
    create_time = serializers.SerializerMethodField(default=timezone.utc)

    def get_create_time(self, obj):
        return format_datetime(obj.create_time)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["createTime"] = representation.pop("create_time")
        representation["userName"] = representation.pop("user_name")
        representation["appId"] = representation.pop("app_id")
        representation["userId"] = representation.pop("user_id")
        representation["secret_key"] = representation.pop("secretKey")
        representation["enable_status"] = representation.pop("enableStatus")

        return representation

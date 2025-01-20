from utils.utils import format_datetime
from django.db import models
from rest_framework import serializers
from ..utils import EnvironmentType
from datetime import datetime, timezone


# 环境表
class EnvInfo(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    env_type = models.CharField(
        max_length=20,
        choices=[(env.value, env.name) for env in EnvironmentType],
        verbose_name="环境类型",
    )
    env_name = models.CharField(verbose_name="自定义环境名称", max_length=32)
    app_id = models.CharField(verbose_name="AppID", max_length=64)

    env_desc = models.CharField(verbose_name="描述", max_length=256)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "tb_env_info"  # 数据库表名
        verbose_name = "环境表"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按照创建时间倒序排列


class EnvInfoSerializer(serializers.ModelSerializer):
    envName = serializers.CharField(source="env_name", read_only=True)
    appId = serializers.CharField(source="app_id", read_only=True)
    envDesc = serializers.CharField(source="env_desc", read_only=True)
    envType = serializers.CharField(source="env_type", read_only=True)
    create_time = serializers.SerializerMethodField(default=timezone.utc)

    def get_create_time(self, obj):
        return format_datetime(obj.create_time)

    class Meta:
        model = EnvInfo
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["createTime"] = representation.pop("create_time")
        representation["envName"] = representation.pop("env_name")
        representation["appId"] = representation.pop("app_id")
        representation["envDesc"] = representation.pop("env_desc")
        representation["envType"] = representation.pop("env_type")

        return representation

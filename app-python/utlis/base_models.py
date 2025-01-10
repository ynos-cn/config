from datetime import datetime, timezone
from django.db import models
from rest_framework import serializers


def format_datetime(dt, fmt="%Y-%m-%d %H:%M:%S"):
    """
    格式化时间
    """
    if isinstance(dt, datetime):
        return dt.strftime(fmt)
    return dt


# 基础字段
class BaseModel(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=32)

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)
    create_by_id = models.CharField(verbose_name="创建人id", max_length=32)
    update_by_id = models.CharField(verbose_name="更新人id", max_length=32)
    org_id = models.CharField(verbose_name="所属机构", max_length=32)
    is_delete = models.IntegerField(
        verbose_name="是否删除 1.删除 0.未删除",
        blank=True,
        null=True,
    )

    class Meta:
        # 抽象类， 用于继承，迁移的时候不创建
        abstract = True


class BaseModelSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField(default=timezone.utc)
    update_time = serializers.SerializerMethodField(default=timezone.utc)
    createById = serializers.CharField(
        source="create_by_id", read_only=True, max_length=32, default=None
    )
    updateById = serializers.CharField(
        source="update_by_id", read_only=True, max_length=32, default=None
    )
    orgId = serializers.CharField(source="org_id", read_only=True)
    isDelete = serializers.IntegerField(source="is_delete", read_only=True)

    class Meta:
        # 抽象类， 用于继承，迁移的时候不创建
        abstract = True

    def get_create_time(self, obj):
        return format_datetime(obj.create_time)

    def get_update_time(self, obj):
        return format_datetime(obj.update_time)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["createTime"] = representation.pop("create_time")
        representation["updateTime"] = representation.pop("update_time")
        representation["createById"] = representation.pop("create_by_id")
        representation["updateById"] = representation.pop("update_by_id")
        representation["orgId"] = representation.pop("org_id")
        representation["isDelete"] = representation.pop("is_delete")
        return representation

from django.db import models
from rest_framework import serializers

from utlis.base_models import BaseModel, BaseModelSerializer


# 角色
class Role(BaseModel):
    id = models.CharField(primary_key=True, editable=False, max_length=32)
    name = models.CharField(verbose_name="名称", max_length=255)
    code = models.CharField(verbose_name="角色代码", unique=True, max_length=255)
    describe = models.CharField(verbose_name="描述", max_length=255)

    class Meta:
        db_table = "sys_role"  # 数据库表名
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按照创建时间倒序排列


class RoleSerializer(BaseModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

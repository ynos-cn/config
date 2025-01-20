from django.db import models
from rest_framework import serializers

from utils.base_models import BaseModel, BaseModelSerializer


# 项目表
class Project(BaseModel):
    id = models.AutoField(primary_key=True, editable=False)
    app_name = models.CharField(verbose_name="项目名称", max_length=255)
    app_id = models.CharField(verbose_name="AppID", unique=True, max_length=255)
    project_managers = models.CharField(verbose_name="项目管理员", max_length=500)
    org_name = models.CharField(verbose_name="所属机构名称", max_length=255)
    description = models.CharField(verbose_name="描述", max_length=500)
    pull_switch = models.SmallIntegerField(
        verbose_name="配置拉取认证开关：0关闭 1：打开", default=0
    )
    env_switch = models.SmallIntegerField(verbose_name="多环境开关", default=0)

    class Meta:
        db_table = "tb_app_info"  # 数据库表名
        verbose_name = "项目表"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按照创建时间倒序排列


class ProjectSerializer(BaseModelSerializer):
    projectManagers = serializers.CharField(source="project_managers", read_only=True)
    orgName = serializers.CharField(source="org_name", read_only=True)
    appName = serializers.CharField(source="app_name", read_only=True)
    appId = serializers.CharField(source="app_id", read_only=True)
    pullSwitch = serializers.CharField(source="pull_switch", read_only=True)
    envSwitch = serializers.CharField(source="env_switch", read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["projectManagers"] = representation.pop("project_managers")
        representation["orgName"] = representation.pop("org_name")
        representation["appName"] = representation.pop("app_name")
        representation["appId"] = representation.pop("app_id")
        representation["pullSwitch"] = representation.pop("pull_switch")
        representation["envSwitch"] = representation.pop("env_switch")
        return representation

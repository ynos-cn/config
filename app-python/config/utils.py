from enum import Enum


class EnvironmentType(Enum):
    """
    环境类型
    """

    # 开发环境
    DEVELOPMENT = "development"
    # 测试环境
    TESTING = "testing"
    # 预发布环境
    STAGING = "staging"
    # 生产环境
    PRODUCTION = "production"

    # 自定义方法来获取大写的字符串表示
    def __str__(self):
        return self.name

    # 自定义方法来获取小写的字符串表示，用于存储到数据库
    def to_db(self):
        return self.value


class PermissionType(Enum):
    """
    权限类型
    """

    # 只读
    PERMISSION_LOOK = 1
    # 添加配置
    PERMISSION_ADD = 2
    # 修改配置
    PERMISSION_UPDATE = 3
    # 删除配置
    PERMISSION_DELETE = 4
    # 提交发布
    PERMISSION_CREATE_TASK = 8
    # 审批发布(固定审批人)
    PERMISSION_APPROVE_TASK = 11
    # 执行发布
    PERMISSION_RELEASE_TASK = 10
    # 管理分组
    PERMISSION_RELEASE = 6

    # 自定义方法来获取大写的字符串表示
    def __str__(self):
        return self.name

    # 自定义方法来获取小写的字符串表示，用于存储到数据库
    def to_db(self):
        return self.value

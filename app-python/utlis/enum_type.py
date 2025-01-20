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

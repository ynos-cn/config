CREATE TABLE `tb_app_info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `app_id` varchar(256) NOT NULL DEFAULT '' COMMENT 'AppID',
  `project_managers` varchar(500) NOT NULL DEFAULT '' COMMENT '项目管理员',
  `org_name` varchar(255) NOT NULL COMMENT '所属机构名称',
  `description` varchar(500) DEFAULT NULL COMMENT '描述',
  `creator` varchar(128) NOT NULL COMMENT '创建人',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_delete` tinyint DEFAULT NULL COMMENT '是否删除 1.删除',
  `app_name` varchar(256) NOT NULL COMMENT '项目名称',
  `pull_switch` tinyint DEFAULT '0' COMMENT '配置拉取认证开关：0关闭 1：打开',
  `env_switch` tinyint DEFAULT '0' COMMENT '多环境开关',
  `org_id` char(32) NOT NULL COMMENT '所属机构',
  `updater` varchar(128) NOT NULL COMMENT '更新人',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_id` (`app_id`,`app_name`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3 COMMENT='项目表'

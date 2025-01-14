-- Active: 1720062235405@@sk.yn59.cn@13306@config_db
--
-- Table structure for table `tb_app_acl_info`
--

DROP TABLE IF EXISTS `tb_app_acl_info`;

CREATE TABLE `tb_app_acl_info` (
                                   `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                   `app_id` varchar(64) NOT NULL DEFAULT '' COMMENT 'appid',
                                   `list_type` int(10) NOT NULL COMMENT '1、黑名单；2、白名单',
                                   `status` int(10) NOT NULL COMMENT '1、开启；2、关闭',
                                   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='api访问控制表';


--
-- Table structure for table `tb_app_gray_rule`
--

DROP TABLE IF EXISTS `tb_app_gray_rule`;

CREATE TABLE `tb_app_gray_rule` (
                                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                    `gray_rule_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '灰度类型id',
                                    `app_id` varchar(128) NOT NULL,
                                    PRIMARY KEY (`id`),
                                    UNIQUE KEY `app_id` (`app_id`,`gray_rule_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='灰度类型表';


INSERT INTO `tb_app_gray_rule` VALUES (1,1,''),(2,2,''),(3,3,'');

--
-- Table structure for table `tb_app_info`
--

DROP TABLE IF EXISTS `tb_app_info`;

CREATE TABLE `tb_app_info` (
                               `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                               `app_id` varchar(256) NOT NULL DEFAULT '' COMMENT 'AppID',
                               `project_managers` varchar(500) NOT NULL DEFAULT '' COMMENT '项目管理员',
                               `dept` varchar(64) NOT NULL DEFAULT '' COMMENT '部门信息',
                               `description` varchar(500) NOT NULL DEFAULT '' COMMENT '描述',
                               `creator` varchar(128) NOT NULL DEFAULT '' COMMENT '创建人',
                               `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                               `is_delete` tinyint(4) NOT NULL DEFAULT '0' COMMENT '1: delete, 2: not delete',
                               `app_name` varchar(256) NOT NULL,
                               `pull_switch` tinyint(4) NOT NULL DEFAULT '0' COMMENT '配置拉取认证开关：0关闭 1：打开',
                               `app_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '项目类型：0：默认 1：错误码',
                               `snapshot_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0：全量快照 1：增量',
                               `snapshot_version_num` int(11) NOT NULL DEFAULT '0' COMMENT '快照版本保存数',
                               `env_switch` tinyint(4) NOT NULL DEFAULT '0' COMMENT '多环境开关',
                               `version_type` tinyint(4) NOT NULL DEFAULT '0',
                               PRIMARY KEY (`id`),
                               UNIQUE KEY `app_id` (`app_id`,`app_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目表';


--
-- Table structure for table `tb_app_white_list`
--

DROP TABLE IF EXISTS `tb_app_white_list`;

CREATE TABLE `tb_app_white_list` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                     `white_list_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '白名单类型id',
                                     `app_id` varchar(128) NOT NULL,
                                     PRIMARY KEY (`id`),
                                     UNIQUE KEY `app_id` (`app_id`,`white_list_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='白名单应用类型表';


INSERT INTO `tb_app_white_list` VALUES (1,1,'');
--
-- Table structure for table `tb_apply_log`
--

DROP TABLE IF EXISTS `tb_apply_log`;

CREATE TABLE `tb_apply_log` (
                                `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                `app_id` varchar(256) NOT NULL DEFAULT '' COMMENT 'AppID',
                                `domain_name` varchar(64) NOT NULL DEFAULT '' COMMENT '领域名',
                                `module_name` varchar(64) NOT NULL DEFAULT '' COMMENT '模块名',
                                `enum_name` varchar(500) NOT NULL DEFAULT '' COMMENT '枚举名',
                                `apply_type` tinyint(4) NOT NULL COMMENT '申请类型：1:添加领域;2:领域负责人;3:转义配置人;4:转义审批人;5:添加模块;6:模块负责人;',
                                `apply_user` varchar(32) NOT NULL DEFAULT '' COMMENT '申请用户',
                                `apply_reason` varchar(256) NOT NULL DEFAULT '0' COMMENT '申请原因',
                                `approve_user` varchar(256) NOT NULL COMMENT '可审批人',
                                `approve_exe_user` varchar(32) NOT NULL DEFAULT '' COMMENT '审批执行人',
                                `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '审批状态0:待审批;1:同意;2:驳回',
                                `apply_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
                                `approve_time` datetime DEFAULT NULL COMMENT '审批通过时间',
                                `approve_reason` varchar(256) NOT NULL DEFAULT '' COMMENT '审批通过原因',
                                `before_fix_record` text COMMENT '修改前记录',
                                `after_fix_record` text COMMENT '修改后记录',
                                `ref_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '关联记录id',
                                PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_auto_group_map`
--

DROP TABLE IF EXISTS `tb_auto_group_map`;

CREATE TABLE `tb_auto_group_map` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                     `group_rule_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组规则id',
                                     `ret_value` int(11) NOT NULL DEFAULT '0' COMMENT '返回值',
                                     `group_name` varchar(256) NOT NULL,
                                     `app_id` varchar(128) NOT NULL,
                                     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分组规则检查映射表';


--
-- Table structure for table `tb_auto_group_ret_value`
--

DROP TABLE IF EXISTS `tb_auto_group_ret_value`;

CREATE TABLE `tb_auto_group_ret_value` (
                                           `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                           `ret_value` int(11) NOT NULL DEFAULT '0' COMMENT '返回值',
                                           `app_id` varchar(128) NOT NULL,
                                           PRIMARY KEY (`id`),
                                           KEY `RET_VALUE_APP_IDX` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分组规则返回指表';


--
-- Table structure for table `tb_auto_group_rule`
--

DROP TABLE IF EXISTS `tb_auto_group_rule`;

CREATE TABLE `tb_auto_group_rule` (
                                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                      `app_id` varchar(128) NOT NULL,
                                      `group_prefix` varchar(2048) NOT NULL COMMENT '分组前缀',
                                      `name` varchar(2048) NOT NULL DEFAULT '' COMMENT '分组名',
                                      `auto_rule_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '自动分组的ruleid',
                                      `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态',
                                      `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                      `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                      PRIMARY KEY (`id`),
                                      KEY `GROUP_APP_IDX` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='自动分组表';


--
-- Table structure for table `tb_auto_group_rule_type`
--

DROP TABLE IF EXISTS `tb_auto_group_rule_type`;

CREATE TABLE `tb_auto_group_rule_type` (
                                           `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                           `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识',
                                           `name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则名',
                                           `en_name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则英文名',
                                           `app_id` varchar(128) NOT NULL,
                                           PRIMARY KEY (`id`),
                                           UNIQUE KEY `app_id` (`app_id`,`en_name`,`client_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='自动分组规则表';


--
-- Table structure for table `tb_cdn_release`
--

DROP TABLE IF EXISTS `tb_cdn_release`;

CREATE TABLE `tb_cdn_release` (
                                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                  `group_id` int(11) NOT NULL DEFAULT '0',
                                  `app_id` varchar(128) NOT NULL COMMENT '项目appid',
                                  `row_file` varchar(256) NOT NULL,
                                  `release_url` text COMMENT '发布链接',
                                  `task_id` int(11) NOT NULL DEFAULT '0',
                                  `envs` varchar(128) NOT NULL COMMENT '已发布的环境列表',
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `uniq_row` (`app_id`,`group_id`,`row_file`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_client_log`
--

DROP TABLE IF EXISTS `tb_client_log`;

CREATE TABLE `tb_client_log` (
                                 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                 `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识名',
                                 `client_value` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识值',
                                 `version_name` varchar(128) NOT NULL DEFAULT '' COMMENT '版本名称',
                                 `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                 `group_name` varchar(256) NOT NULL DEFAULT '' COMMENT '分组名',
                                 `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                 PRIMARY KEY (`id`),
                                 UNIQUE KEY `app_id` (`app_id`,`group_name`,`client_name`,`client_value`,`version_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户端列表';


--
-- Table structure for table `tb_client_log_cicd`
--

DROP TABLE IF EXISTS `tb_client_log_cicd`;

CREATE TABLE `tb_client_log_cicd` (
                                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                      `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识名',
                                      `client_value` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识指',
                                      `cur_version_name` varchar(128) NOT NULL DEFAULT '' COMMENT '当前版本名',
                                      `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                      `group_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名',
                                      `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                      `cur_module_version` varchar(128) NOT NULL DEFAULT '',
                                      `prev_module_version` varchar(128) NOT NULL DEFAULT '',
                                      `prev_version_uuid` varchar(128) NOT NULL DEFAULT '',
                                      `status` tinyint(4) NOT NULL COMMENT '1.发起变更 2.拉取配置成功 3.渲染文件成功 4.新建或覆盖配置文件成功',
                                      `cur_exe_version` varchar(128) NOT NULL DEFAULT '',
                                      `prev_exe_version` varchar(128) NOT NULL DEFAULT '',
                                      `release_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:默认初始态 1：发布成功 2：发布失败',
                                      `task_id` bigint(20) NOT NULL COMMENT '发布任务id',
                                      `cur_version_uuid` varchar(128) NOT NULL DEFAULT '',
                                      `env_name` varchar(32) NOT NULL DEFAULT 'default' COMMENT '环境名',
                                      PRIMARY KEY (`id`),
                                      UNIQUE KEY `uniq_task_index` (`task_id`,`client_name`,`client_value`),
                                      KEY `key_group_cli` (`group_name`,`client_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_client_log_history`
--

DROP TABLE IF EXISTS `tb_client_log_history`;

CREATE TABLE `tb_client_log_history` (
                                         `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                         `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识名',
                                         `client_value` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识值',
                                         `version_name` varchar(128) NOT NULL DEFAULT '' COMMENT '版本名称',
                                         `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                         `group_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名',
                                         `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                         PRIMARY KEY (`id`),
                                         UNIQUE KEY `app_id` (`app_id`,`group_name`,`client_name`,`client_value`,`version_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户端列表';


--
-- Table structure for table `tb_client_log_lastest`
--

DROP TABLE IF EXISTS `tb_client_log_lastest`;

CREATE TABLE `tb_client_log_lastest` (
                                         `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                         `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                         `group_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名',
                                         `client_id` text NOT NULL COMMENT '客户端标识值',
                                         `client_md5` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识值',
                                         `version_uuid` varchar(128) NOT NULL DEFAULT '' COMMENT '版本uuid',
                                         `status` int(11) NOT NULL DEFAULT '0' COMMENT '客户端状态',
                                         `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                         `effect_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生效时间',
                                         PRIMARY KEY (`id`),
                                         UNIQUE KEY `uniq_client` (`client_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户端列表最新版';


--
-- Table structure for table `tb_client_log_old`
--

DROP TABLE IF EXISTS `tb_client_log_old`;

CREATE TABLE `tb_client_log_old` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                     `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识名',
                                     `client_value` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识值',
                                     `version_name` varchar(128) NOT NULL DEFAULT '' COMMENT '版本名称',
                                     `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                     `group_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名',
                                     `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                     PRIMARY KEY (`id`),
                                     UNIQUE KEY `app_id` (`app_id`,`group_name`,`client_name`,`client_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户端列表最新版';


--
-- Table structure for table `tb_cmdb_info`
--

DROP TABLE IF EXISTS `tb_cmdb_info`;

CREATE TABLE `tb_cmdb_info` (
                                `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                `dept_id` int(64) NOT NULL COMMENT '部门id',
                                `content` text NOT NULL,
                                `iplist_md5` varchar(64) NOT NULL COMMENT 'ip集合md5',
                                `app_id` varchar(64) NOT NULL COMMENT '项目id',
                                `group_id` int(11) NOT NULL COMMENT '分组id',
                                `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                `mod_ids` text COMMENT '三级模块id组合',
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `app_id` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_cmdb_instance`
--

DROP TABLE IF EXISTS `tb_cmdb_instance`;

CREATE TABLE `tb_cmdb_instance` (
                                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                    `app_id` varchar(64) NOT NULL COMMENT '项目名',
                                    `group_id` int(11) NOT NULL COMMENT '分组id',
                                    `mod_id` varchar(64) NOT NULL COMMENT '三级模块id',
                                    `mod_name` text NOT NULL COMMENT '三级模块名',
                                    `city` varchar(32) NOT NULL COMMENT '城市',
                                    `machine_room` varchar(256) NOT NULL COMMENT '机房名',
                                    `ip` text NOT NULL COMMENT '三级模块对应ip列表',
                                    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                    PRIMARY KEY (`id`),
                                    KEY `group_index` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_code_id`
--

DROP TABLE IF EXISTS `tb_code_id`;

CREATE TABLE `tb_code_id` (
                              `id` int(11) NOT NULL AUTO_INCREMENT,
                              `seq` int(11) NOT NULL,
                              PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_column_info`
--

DROP TABLE IF EXISTS `tb_column_info`;

CREATE TABLE `tb_column_info` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                  `column_type` int(11) NOT NULL COMMENT '字段类型枚举',
                                  `en_name` varchar(256) NOT NULL COMMENT '字段英文名',
                                  `ch_name` varchar(256) NOT NULL COMMENT '字段展示名',
                                  `default_value` varchar(256) NOT NULL COMMENT '默认值',
                                  `max_length` tinyint(4) NOT NULL COMMENT '限制长度(仅类型对应varchar有效)',
                                  `value_list` text COMMENT '设置默认值列表,用|分隔(如下拉框)',
                                  `primary_key` tinyint(4) NOT NULL COMMENT '是否主键,1:是;2:否',
                                  `is_unique` tinyint(4) NOT NULL COMMENT '是否唯一，类似mysql中unique',
                                  `is_read_only` tinyint(4) NOT NULL COMMENT '是否只读',
                                  `display_seq` tinyint(4) NOT NULL COMMENT '字段展示顺序',
                                  `table_id` int(11) NOT NULL COMMENT '表ID',
                                  `app_id` varchar(64) NOT NULL COMMENT '项目id',
                                  `group_id` int(11) NOT NULL COMMENT '分组ID',
                                  `create_time` datetime NOT NULL COMMENT '创建时间',
                                  `plugin_id` varchar(128) NOT NULL DEFAULT '',
                                  `is_display` tinyint(4) NOT NULL DEFAULT '0' COMMENT '字段是否展示 0：默认展示 other：其他不展示',
                                  `table_verid` int(11) NOT NULL DEFAULT '0' COMMENT '表结构版本id',
                                  `required` tinyint(11) NOT NULL DEFAULT '1' COMMENT '0:表示非必填,1:表示必填',
                                  `old_en_name` varchar(256) NOT NULL DEFAULT '' COMMENT '旧的字段英文名',
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `app_id` (`app_id`,`group_id`,`table_id`,`en_name`,`table_verid`),
                                  UNIQUE KEY `app_id_2` (`app_id`,`group_id`,`table_id`,`ch_name`,`table_verid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_column_type`
--

DROP TABLE IF EXISTS `tb_column_type`;

CREATE TABLE `tb_column_type` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                  `user_typename` varchar(256) NOT NULL COMMENT '展示类型：如文件、图片url、颜色、自增ID、日期等类型',
                                  `user_typeid` int(11) NOT NULL,
                                  `sql_type` varchar(256) NOT NULL COMMENT '如颜色 -> varchar',
                                  `has_default_value` tinyint(4) NOT NULL COMMENT '是否有默认值,1:有,2:无',
                                  `default_value` varchar(256) NOT NULL COMMENT '初始默认值，如false、null',
                                  `is_read_only` tinyint(4) NOT NULL COMMENT '是否只读,1:是，2:否',
                                  `is_system_reserved` tinyint(4) NOT NULL COMMENT '是否系统保留,1:是，2:否',
                                  `is_unique` tinyint(4) NOT NULL COMMENT '是否唯一,1:是，2:否',
                                  `is_null` tinyint(4) NOT NULL COMMENT '是否为空，1:不为空;2:为空',
                                  `has_max_length` tinyint(4) NOT NULL COMMENT '是否有最大长度限制，1:有，2:无',
                                  `default_max_length` int(11) NOT NULL COMMENT '默认最大长度限制',
                                  `is_primary_key` tinyint(4) NOT NULL COMMENT '是否主键,1:是,2:否',
                                  `can_set_value_list` tinyint(4) NOT NULL COMMENT '是否需设置value_list：1：是 2：否',
                                  `app_id` varchar(256) DEFAULT '',
                                  `default_en_name` varchar(256) DEFAULT NULL,
                                  `default_ch_name` varchar(256) DEFAULT NULL,
                                  `unique_able` int(11) NOT NULL COMMENT '是否可设置唯一：1：可设置唯一',
                                  `required` tinyint(4) NOT NULL DEFAULT '1' COMMENT '默认是否必填',
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `app_id` (`app_id`,`user_typeid`,`user_typename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `tb_column_type` VALUES (13,'数字',1,'varchar(256)',1,'',2,2,2,1,2,0,2,2,'','','',1,1),(14,'字符串',2,'varchar(1024)',1,'',2,2,2,1,2,0,2,2,'','','',1,1),(15,'文本',3,'text',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(16,'JSON',4,'text',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(17,'XML',5,'text',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(20,'颜色',8,'varchar(256)',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(22,'下拉框',10,'text',1,'',2,2,2,1,2,0,2,1,'','','',0,1),(23,'BOOL',11,'int',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(24,'自增ID',12,'int',2,'',2,1,1,1,2,0,2,2,'','_auto_id','自增ID',1,1),(33,'负责人',15,'text',2,'',2,1,2,1,2,0,2,2,'','_owner','负责人',0,1),(28,'链接',16,'varchar(1024)',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(29,'时间',17,'datetime',1,'',2,2,2,1,2,0,2,2,'','','',0,1),(37,'用户特征组合',19,'text',2,'',2,1,1,1,2,0,2,2,'','rules','用户特征组合',0,1),(62,'多选下拉框',21,'text',1,'',2,2,2,1,2,0,2,1,'','','',0,1);
--
-- Table structure for table `tb_config`
--

DROP TABLE IF EXISTS `tb_config`;

CREATE TABLE `tb_config` (
                             `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                             `ckey` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '配置key名称',
                             `cvalue` mediumtext NOT NULL COMMENT '配置内容',
                             `value_type` int(11) NOT NULL COMMENT 'Value: (1-NUMBER;2-STRING;3-TEXT;4-JSON;5-XML;6-FILE)',
                             `check_rule_id` int(11) NOT NULL DEFAULT '0' COMMENT '规则id',
                             `description` varchar(2048) NOT NULL DEFAULT '' COMMENT '描述',
                             `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '版本id',
                             `value_md5` varchar(256) NOT NULL COMMENT 'md5',
                             `from_group_id` int(11) NOT NULL DEFAULT '0' COMMENT '来源分组id',
                             `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                             `app_id` varchar(256) NOT NULL DEFAULT '' COMMENT 'AppID',
                             `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                             `status` int(11) NOT NULL DEFAULT '0',
                             `plugin_id` varchar(128) NOT NULL DEFAULT '',
                             `encrypt` varchar(16) NOT NULL DEFAULT '' COMMENT '加密方式，为空表示不加密',
                             `operator` varchar(64) NOT NULL DEFAULT '',
                             PRIMARY KEY (`id`),
                             UNIQUE KEY `app_id` (`app_id`,`group_id`,`version_id`,`ckey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='配置表';


--
-- Table structure for table `tb_config_mid`
--

DROP TABLE IF EXISTS `tb_config_mid`;

CREATE TABLE `tb_config_mid` (
                                 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                 `ckey` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '配置key名称',
                                 `cvalue` mediumtext NOT NULL,
                                 `value_type` int(11) NOT NULL COMMENT 'Value类型(1-NUMBER;2-STRING;3-TEXT;4-JSON;5-XML;6-FILE)',
                                 `check_rule_id` int(11) NOT NULL DEFAULT '0' COMMENT '数据校验规则id',
                                 `description` varchar(2048) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '备注',
                                 `value_md5` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'md5',
                                 `source_value_md5` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'md5',
                                 `from_group_id` int(11) NOT NULL DEFAULT '0' COMMENT '来源分组id',
                                 `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组ID',
                                 `app_id` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'AppID',
                                 `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态(0-已发布;1-修改;2-删除;3-增加)',
                                 `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
                                 `operator` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
                                 `plugin_id` varchar(128) CHARACTER SET utf8 NOT NULL DEFAULT '',
                                 `encrypt` varchar(16) NOT NULL DEFAULT '' COMMENT '加密方式，为空表示不加密',
                                 PRIMARY KEY (`id`),
                                 UNIQUE KEY `app_id` (`app_id`,`group_id`,`ckey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配置中间表';


--
-- Table structure for table `tb_cos_info`
--

DROP TABLE IF EXISTS `tb_cos_info`;

CREATE TABLE `tb_cos_info` (
                               `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                               `bucket` varchar(256) NOT NULL COMMENT 'cos的桶',
                               `cos_url` varchar(1024) NOT NULL COMMENT 'cos存储地址',
                               `secret_id` varchar(256) DEFAULT NULL COMMENT 'cos身份 id',
                               `secret_key` varchar(256) NOT NULL COMMENT 'cos密️钥',
                               `auth_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:公开;1:私有，需要鉴权',
                               `app_ids` varchar(128) NOT NULL DEFAULT '' COMMENT '项目ID(为’’表示所有项目共享)',
                               PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='同步实例表';


--
-- Table structure for table `tb_ctrl_code`
--

DROP TABLE IF EXISTS `tb_ctrl_code`;

CREATE TABLE `tb_ctrl_code` (
                                `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                `app_id` varchar(256) NOT NULL,
                                `code_name` varchar(256) NOT NULL,
                                `code_desc` varchar(256) DEFAULT NULL,
                                `operate` text,
                                `is_use_url` int(11) NOT NULL DEFAULT '0',
                                `url` text,
                                `is_custom` int(11) NOT NULL DEFAULT '0',
                                `pic_url` text,
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `app_ctrl_code` (`app_id`,`code_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_custom_user`
--

DROP TABLE IF EXISTS `tb_custom_user`;

CREATE TABLE `tb_custom_user` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT,
                                  `app_id` varchar(64) NOT NULL,
                                  `user_name` varchar(32) NOT NULL,
                                  `user_id` varchar(64) NOT NULL,
                                  `secret_key` varchar(64) NOT NULL COMMENT '用户密钥',
                                  `enable_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '用户开关状态 0:关闭 1:打开',
                                  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `app_id` (`app_id`,`user_name`),
                                  KEY `user_id_index` (`user_id`(16))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_custom_user_role`
--

DROP TABLE IF EXISTS `tb_custom_user_role`;

CREATE TABLE `tb_custom_user_role` (
                                       `id` int(11) NOT NULL AUTO_INCREMENT,
                                       `app_id` varchar(64) NOT NULL,
                                       `custom_user` varchar(32) NOT NULL,
                                       `ref_role_id` int(11) NOT NULL,
                                       `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                       PRIMARY KEY (`id`),
                                       UNIQUE KEY `uniq_appid_user_role` (`app_id`,`custom_user`,`ref_role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_department_info`
--

DROP TABLE IF EXISTS `tb_department_info`;

CREATE TABLE `tb_department_info` (
                                      `department_id` int(11) NOT NULL,
                                      `department_name` varchar(256) NOT NULL,
                                      `department_full_name` text NOT NULL,
                                      `location_string` varchar(512) NOT NULL,
                                      `parent_department_id` int(11) NOT NULL,
                                      UNIQUE KEY `department_id` (`department_id`,`department_name`),
                                      KEY `TB_DEPARTMENT_INFO_INDEX` (`department_name`),
                                      KEY `TB_DEPARTMENT_INFO_LOCATION_INDEX` (`location_string`),
                                      KEY `TB_DEPARTMENT_INFO_PARENT_INDEX` (`parent_department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_dept_info`
--

DROP TABLE IF EXISTS `tb_dept_info`;

CREATE TABLE `tb_dept_info` (
                                `id` int(10) NOT NULL AUTO_INCREMENT,
                                `dept_id` int(11) NOT NULL COMMENT '部门id',
                                `dept_name` varchar(256) NOT NULL COMMENT '部门名称',
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `dept_id` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_dimen_ctrlflow`
--

DROP TABLE IF EXISTS `tb_dimen_ctrlflow`;

CREATE TABLE `tb_dimen_ctrlflow` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                     `dimen` varchar(256) NOT NULL COMMENT '场景维度',
                                     `ctrl_flow` varchar(256) NOT NULL COMMENT '控制流',
                                     `app_id` varchar(64) NOT NULL,
                                     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_domain_id`
--

DROP TABLE IF EXISTS `tb_domain_id`;

CREATE TABLE `tb_domain_id` (
                                `id` int(11) NOT NULL AUTO_INCREMENT,
                                `seq` int(11) NOT NULL,
                                PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_domain_source`
--

DROP TABLE IF EXISTS `tb_domain_source`;

CREATE TABLE `tb_domain_source` (
                                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
                                    `domain_name` varchar(256) NOT NULL COMMENT '领域名',
                                    `app_id` varchar(64) NOT NULL,
                                    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_ecode_type`
--

DROP TABLE IF EXISTS `tb_ecode_type`;

CREATE TABLE `tb_ecode_type` (
                                 `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键id',
                                 `type_id` int(11) NOT NULL COMMENT '类型id',
                                 `type_name` varchar(64) NOT NULL COMMENT '类型名',
                                 `comment` varchar(256) NOT NULL COMMENT '描述',
                                 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_enum_assign_log`
--

DROP TABLE IF EXISTS `tb_enum_assign_log`;

CREATE TABLE `tb_enum_assign_log` (
                                      `id` int(11) NOT NULL AUTO_INCREMENT,
                                      `src_type` tinyint(4) NOT NULL COMMENT '领域来源类型',
                                      `enum_val` bigint(20) NOT NULL,
                                      `app_id` varchar(64) NOT NULL,
                                      PRIMARY KEY (`id`),
                                      UNIQUE KEY `uniq_type` (`app_id`,`src_type`,`enum_val`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_env_info`
--

DROP TABLE IF EXISTS `tb_env_info`;

CREATE TABLE `tb_env_info` (
                               `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '环境ID',
                               `env_type` varchar(32) NOT NULL COMMENT 'development,testing,staging,production',
                               `env_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '自定义环境名称',
                               `module_name` varchar(128) NOT NULL DEFAULT '' COMMENT '模块名',
                               `app_id` varchar(64) NOT NULL COMMENT '项目appid',
                               `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                               `env_desc` varchar(256) NOT NULL DEFAULT '' COMMENT '环境描述',
                               PRIMARY KEY (`id`),
                               UNIQUE KEY `uniq_type` (`app_id`,`env_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_env_relation`
--

DROP TABLE IF EXISTS `tb_env_relation`;

CREATE TABLE `tb_env_relation` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                   `env_id` varchar(8) NOT NULL COMMENT '环境id',
                                   `env_name` varchar(128) NOT NULL COMMENT '环境名',
                                   `namespace` varchar(64) NOT NULL COMMENT '命名空间',
                                   `plat_flag` varchar(16) NOT NULL COMMENT '来源平台名：123/sumeru',
                                   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_ex_link`
--

DROP TABLE IF EXISTS `tb_ex_link`;

CREATE TABLE `tb_ex_link` (
                              `id` int(11) NOT NULL AUTO_INCREMENT,
                              `app_id` varchar(64) NOT NULL,
                              `user` varchar(64) NOT NULL DEFAULT '',
                              `name` varchar(64) NOT NULL COMMENT '标题',
                              `url` varchar(512) NOT NULL COMMENT '链接',
                              `open_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '打开方式 0:iframe内嵌 1:跳转链接',
                              `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                              PRIMARY KEY (`id`),
                              UNIQUE KEY `app_ex_link` (`app_id`,`name`),
                              KEY `app_id` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_exe_module`
--

DROP TABLE IF EXISTS `tb_exe_module`;

CREATE TABLE `tb_exe_module` (
                                 `id` int(11) NOT NULL AUTO_INCREMENT,
                                 `shell_switch` text COMMENT 'agent初始化脚本开关：0：关闭 1：打开',
                                 `init_shell` text COMMENT 'agent初始化脚本内容',
                                 `before_exe_file` text COMMENT 'agent替换文件前执行',
                                 `after_exe_file` text COMMENT 'agent替换文件后执行',
                                 `app_id` varchar(64) NOT NULL COMMENT '项目appid',
                                 `group_id` int(11) NOT NULL COMMENT '分组id',
                                 `path` varchar(256) NOT NULL DEFAULT '' COMMENT '脚本下发路径',
                                 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_favorite_app`
--

DROP TABLE IF EXISTS `tb_favorite_app`;

CREATE TABLE `tb_favorite_app` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                   `app_id` varchar(128) NOT NULL,
                                   `person` varchar(64) NOT NULL,
                                   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   PRIMARY KEY (`id`),
                                   KEY `FAVOR_PERSON_IDX` (`person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='收藏的app';


--
-- Table structure for table `tb_gray_rule`
--

DROP TABLE IF EXISTS `tb_gray_rule`;

CREATE TABLE `tb_gray_rule` (
                                `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                `app_id` varchar(128) NOT NULL,
                                `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                `task_id` int(11) NOT NULL DEFAULT '0' COMMENT '任务id',
                                `gray_rule_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '灰度类型id',
                                `content` text NOT NULL COMMENT '内容',
                                `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态',
                                `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `app_id` (`app_id`,`group_id`,`task_id`),
                                UNIQUE KEY `app_id_2` (`app_id`,`group_id`,`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='灰度规则表';


--
-- Table structure for table `tb_gray_rule_mid`
--

DROP TABLE IF EXISTS `tb_gray_rule_mid`;

CREATE TABLE `tb_gray_rule_mid` (
                                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                    `app_id` varchar(128) NOT NULL,
                                    `group_id` int(11) NOT NULL,
                                    `task_id` int(11) NOT NULL DEFAULT '0' COMMENT '任务id',
                                    `gray_rule_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '灰度类型id',
                                    `content` text NOT NULL COMMENT '内容',
                                    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                    `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                    PRIMARY KEY (`id`),
                                    UNIQUE KEY `app_id` (`app_id`,`group_id`,`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='灰度规则中间表';


--
-- Table structure for table `tb_gray_rule_status`
--

DROP TABLE IF EXISTS `tb_gray_rule_status`;

CREATE TABLE `tb_gray_rule_status` (
                                       `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                       `app_id` varchar(128) NOT NULL,
                                       `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                       `task_id` int(11) NOT NULL DEFAULT '0' COMMENT '任务id',
                                       `gray_rule_id` int(11) NOT NULL DEFAULT '0' COMMENT '灰度规则id',
                                       `op_type` tinyint(4) NOT NULL COMMENT '操作类型',
                                       `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                       PRIMARY KEY (`id`),
                                       UNIQUE KEY `app_id` (`app_id`,`group_id`,`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='灰度状态表';


--
-- Table structure for table `tb_gray_rule_type`
--

DROP TABLE IF EXISTS `tb_gray_rule_type`;

CREATE TABLE `tb_gray_rule_type` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                     `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识',
                                     `name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则名',
                                     `en_name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则英文名',
                                     `src_page_type` tinyint(4) DEFAULT '0' COMMENT '0:默认 1:灰度页面来源',
                                     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='灰度规则类型表';


INSERT INTO `tb_gray_rule_type` VALUES (1,'ip','ip类型','ip_list',1),(2,'dockerid','dockerid类型','in_list',0),(3,'uin','uin类型','in_list',0);
--
-- Table structure for table `tb_gray_service`
--

DROP TABLE IF EXISTS `tb_gray_service`;

CREATE TABLE `tb_gray_service` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                   `app_id` varchar(64) NOT NULL COMMENT '项目ID',
                                   `app_name` varchar(64) NOT NULL COMMENT '项目名',
                                   `service_name` varchar(128) NOT NULL COMMENT '服务名',
                                   `namespace` varchar(64) NOT NULL COMMENT '命名空间',
                                   `env_name` varchar(64) NOT NULL COMMENT '环境名',
                                   `plat_name` varchar(64) NOT NULL COMMENT '平台名',
                                   `ip_list` text COMMENT 'ip灰度列表(为空则按服务粒度灰度)',
                                   `status` tinyint(4) NOT NULL COMMENT '0:待启动 1：开始灰度 2：关闭灰度',
                                   `creator` varchar(64) NOT NULL COMMENT '灰度提交人',
                                   `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '变更时间',
                                   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_group`
--

DROP TABLE IF EXISTS `tb_group`;

CREATE TABLE `tb_group` (
                            `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                            `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
                            `description` varchar(500) NOT NULL DEFAULT '' COMMENT '描述',
                            `type` int(11) NOT NULL DEFAULT '0' COMMENT '分组类型',
                            `app_id` varchar(128) NOT NULL,
                            `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态ˆ',
                            `white_list_status` int(11) NOT NULL DEFAULT '2',
                            `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                            `config_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:kv类型; 1:table类型',
                            `table_id` int(11) NOT NULL DEFAULT '0' COMMENT '主table的id',
                            `publish_type` tinyint(4) NOT NULL DEFAULT '0',
                            `open_config_module` tinyint(4) NOT NULL DEFAULT '0',
                            `omit_approval` tinyint(4) NOT NULL DEFAULT '0' COMMENT '免审批开关：0：需要审批 1：免审批',
                            `env_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT 'Default' COMMENT '关联环境名',
                            `model_type` tinyint(4) DEFAULT '0',
                            `table_verid` int(11) NOT NULL DEFAULT '0' COMMENT '表结构版本id',
                            PRIMARY KEY (`id`),
                            UNIQUE KEY `app_id` (`app_id`,`name`,`env_name`,`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分组信息';


--
-- Table structure for table `tb_group_lastest_version`
--

DROP TABLE IF EXISTS `tb_group_lastest_version`;

CREATE TABLE `tb_group_lastest_version` (
                                            `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                            `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组ID',
                                            `group_name` varchar(512) NOT NULL DEFAULT '' COMMENT '分组名称',
                                            `main_version` varchar(128) NOT NULL DEFAULT '' COMMENT '主versionID',
                                            `prev_main_version` varchar(128) NOT NULL DEFAULT '' COMMENT '上一主versionID',
                                            `gray_version` varchar(128) NOT NULL DEFAULT '' COMMENT '灰度versionID',
                                            `lastest_event_id` bigint(20) NOT NULL DEFAULT '0',
                                            `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                            `main_version_name` varchar(128) NOT NULL,
                                            `gray_version_name` varchar(128) NOT NULL,
                                            `config_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '分组类型 0:kv 1:table',
                                            `main_max_auto_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '当前最大自增id',
                                            `gray_max_auto_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '当前灰度版本最大自增id',
                                            `is_incr` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否增量发布0：默认 1：增量',
                                            `env_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT 'Default' COMMENT '关联环境名',
                                            UNIQUE KEY `app_id` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='最新配置版本表';


--
-- Table structure for table `tb_group_relation`
--

DROP TABLE IF EXISTS `tb_group_relation`;

CREATE TABLE `tb_group_relation` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                     `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                     `from_group_id` int(11) NOT NULL DEFAULT '0' COMMENT '来源分组id',
                                     `app_id` varchar(128) NOT NULL,
                                     `from_version_id` int(11) NOT NULL DEFAULT '0' COMMENT '来源版本id',
                                     PRIMARY KEY (`id`),
                                     KEY `RELATION_GROUP_IDX` (`app_id`,`group_id`),
                                     KEY `RELATION_FROM_GROUP_IDX` (`app_id`,`from_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分组关联表';


--
-- Table structure for table `tb_group_table_relation`
--

DROP TABLE IF EXISTS `tb_group_table_relation`;

CREATE TABLE `tb_group_table_relation` (
                                           `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                           `from_group_id` int(11) NOT NULL COMMENT '关联分组id',
                                           `from_table_name` varchar(32) NOT NULL COMMENT '关联表名',
                                           `from_column_name` varchar(32) NOT NULL COMMENT '关联的列名',
                                           `to_group_id` int(11) NOT NULL COMMENT '被关联分组id',
                                           `to_table_name` varchar(32) NOT NULL COMMENT '被关联表名',
                                           `to_column_name` varchar(32) NOT NULL COMMENT '被关联的列名',
                                           PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_group_table_version_relation`
--

DROP TABLE IF EXISTS `tb_group_table_version_relation`;

CREATE TABLE `tb_group_table_version_relation` (
                                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                                   `app_id` varchar(128) NOT NULL COMMENT '项目appid',
                                                   `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                                   `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '版本id',
                                                   `version_uuid` varchar(64) NOT NULL DEFAULT '' COMMENT '版本uuid',
                                                   `table_verid` int(11) NOT NULL DEFAULT '0' COMMENT '表结构版本id',
                                                   `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                                   PRIMARY KEY (`id`),
                                                   UNIQUE KEY `group_ver_key` (`app_id`,`group_id`,`version_id`),
                                                   UNIQUE KEY `table_ver_key` (`app_id`,`group_id`,`version_id`,`table_verid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_group_version_status`
--

DROP TABLE IF EXISTS `tb_group_version_status`;

CREATE TABLE `tb_group_version_status` (
                                           `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                           `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                           `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '版本id',
                                           `prev_version_id` int(11) NOT NULL DEFAULT '0' COMMENT '上个版本id',
                                           `status` int(11) NOT NULL DEFAULT '1' COMMENT '状态',
                                           `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                           `module_version_id` int(11) NOT NULL DEFAULT '0',
                                           `prev_module_version_id` int(11) NOT NULL DEFAULT '0',
                                           UNIQUE KEY `app_id` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='版本状态表';


--
-- Table structure for table `tb_limit_info`
--

DROP TABLE IF EXISTS `tb_limit_info`;

CREATE TABLE `tb_limit_info` (
                                 `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                 `type_id` int(10) NOT NULL COMMENT 'type_id',
                                 `rate` int(10) NOT NULL COMMENT '速率',
                                 `uint` varchar(256) NOT NULL DEFAULT '' COMMENT '速率的单位，秒:s,分:m,时:h',
                                 `attribute` varchar(500) NOT NULL DEFAULT '' COMMENT '限流类型对应的属性，比如appid、接口名、客户端标识等',
                                 `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                 `limit_on` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0 关闭，1 开启',
                                 `downgrade` tinyint(4) NOT NULL DEFAULT '0' COMMENT '降级开关：1、开启(亦直接拒绝下游请求)；0、关闭',
                                 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='限流信息表';


--
-- Table structure for table `tb_limit_type`
--

DROP TABLE IF EXISTS `tb_limit_type`;

CREATE TABLE `tb_limit_type` (
                                 `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                 `limit_type` int(10) NOT NULL COMMENT '不同的限制粒度，1:整个单机，2:app，3:接口，4:客户端标识等',
                                 `description` varchar(128) NOT NULL DEFAULT '' COMMENT '限流粒度描述，比如单机粒度，应用粒度、接口粒度、客户端粒度等',
                                 `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                 `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT '关联的appid',
                                 `moudle_type` int(10) NOT NULL DEFAULT '0' COMMENT '七彩石模块类型，如: api:0, config:1, admin:2',
                                 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='限流类型表';


--
-- Table structure for table `tb_module_config`
--

DROP TABLE IF EXISTS `tb_module_config`;

CREATE TABLE `tb_module_config` (
                                    `id` int(11) NOT NULL AUTO_INCREMENT,
                                    `path` varchar(1024) NOT NULL,
                                    `auth` varchar(32) NOT NULL,
                                    `user` varchar(32) NOT NULL,
                                    `ugroup` varchar(32) NOT NULL,
                                    `group_id` int(11) NOT NULL,
                                    `app_id` varchar(128) NOT NULL,
                                    `content_md5` varchar(128) NOT NULL DEFAULT '',
                                    PRIMARY KEY (`id`),
                                    UNIQUE KEY `uniq_app_group` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_module_id`
--

DROP TABLE IF EXISTS `tb_module_id`;

CREATE TABLE `tb_module_id` (
                                `id` int(11) NOT NULL AUTO_INCREMENT,
                                `seq` int(11) NOT NULL,
                                PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_module_info`
--

DROP TABLE IF EXISTS `tb_module_info`;

CREATE TABLE `tb_module_info` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT,
                                  `version_id` int(11) NOT NULL,
                                  `module_name` varchar(256) NOT NULL,
                                  `module_content` mediumblob NOT NULL,
                                  `content_md5` varchar(128) NOT NULL,
                                  `group_id` int(11) NOT NULL,
                                  `app_id` varchar(128) NOT NULL,
                                  `operator` varchar(128) NOT NULL DEFAULT '',
                                  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                  `module_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0：普通文件内容 1：文件元数据',
                                  PRIMARY KEY (`id`),
                                  KEY `key_app_group` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_module_info_mid`
--

DROP TABLE IF EXISTS `tb_module_info_mid`;

CREATE TABLE `tb_module_info_mid` (
                                      `id` int(11) NOT NULL AUTO_INCREMENT,
                                      `module_name` varchar(256) NOT NULL,
                                      `module_content` mediumblob NOT NULL,
                                      `content_md5` varchar(128) NOT NULL,
                                      `group_id` int(11) NOT NULL,
                                      `app_id` varchar(128) NOT NULL,
                                      `source_content_md5` varchar(128) NOT NULL DEFAULT '',
                                      `status` tinyint(4) NOT NULL DEFAULT '0',
                                      `operator` varchar(128) NOT NULL DEFAULT '',
                                      `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                      `module_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0：普通文件内容 1：文件元数据',
                                      PRIMARY KEY (`id`),
                                      UNIQUE KEY `group_id` (`group_id`,`module_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_msg_module`
--

DROP TABLE IF EXISTS `tb_msg_module`;

CREATE TABLE `tb_msg_module` (
                                 `msg_type` tinyint(4) NOT NULL,
                                 `content` text NOT NULL,
                                 UNIQUE KEY `msg_type` (`msg_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_plugin_bind`
--

DROP TABLE IF EXISTS `tb_plugin_bind`;

CREATE TABLE `tb_plugin_bind` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT,
                                  `app_id` varchar(64) NOT NULL COMMENT '项目id',
                                  `group_id` int(11) NOT NULL COMMENT '分组id',
                                  `category` tinyint(4) NOT NULL COMMENT '插件种类 1:数据过滤',
                                  `plugin_type_id` varchar(64) NOT NULL COMMENT '分组绑定插件类型id',
                                  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '绑定时间',
                                  PRIMARY KEY (`id`),
                                  KEY `group_index` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_plugin_type`
--

DROP TABLE IF EXISTS `tb_plugin_type`;

CREATE TABLE `tb_plugin_type` (
                                  `id` int(11) NOT NULL AUTO_INCREMENT,
                                  `category` tinyint(4) NOT NULL COMMENT '1：数据过滤 2：Table数据录入插件 3：Table数据编辑插件 4：数据录入插件 5：KV数据编辑插件',
                                  `en_name` varchar(32) NOT NULL COMMENT '插件英文名',
                                  `ch_name` varchar(32) NOT NULL COMMENT '插件中文名',
                                  `app_id` varchar(64) NOT NULL DEFAULT '',
                                  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                  `type_id` varchar(64) NOT NULL COMMENT '插件id',
                                  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_product_info`
--

DROP TABLE IF EXISTS `tb_product_info`;

CREATE TABLE `tb_product_info` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                   `name` varchar(256) NOT NULL COMMENT '制品名称',
                                   `app_id` varchar(128) NOT NULL COMMENT '项目id',
                                   `version_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '版本id',
                                   `version_name` varchar(256) NOT NULL DEFAULT '' COMMENT '版本名',
                                   `source` varchar(128) NOT NULL DEFAULT '' COMMENT '版本名',
                                   `content` mediumtext NOT NULL COMMENT '制品内容',
                                   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                                   PRIMARY KEY (`id`),
                                   KEY `version_key` (`app_id`,`name`,`version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='制品信息表';


--
-- Table structure for table `tb_release_task`
--

DROP TABLE IF EXISTS `tb_release_task`;

CREATE TABLE `tb_release_task` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                   `app_id` varchar(128) NOT NULL,
                                   `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                   `group_name` varchar(512) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名称',
                                   `version_name` varchar(128) NOT NULL DEFAULT '' COMMENT '版本名',
                                   `apply_user` varchar(128) NOT NULL DEFAULT '' COMMENT '申请人',
                                   `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态',
                                   `reject_reason` text NOT NULL COMMENT '拒绝的原因',
                                   `approval_user` varchar(128) NOT NULL DEFAULT '' COMMENT '审批人',
                                   `description` varchar(2048) NOT NULL DEFAULT '' COMMENT '描述',
                                   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '当前版本号',
                                   `prev_version_id` int(11) NOT NULL DEFAULT '0' COMMENT '上一版本号',
                                   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                   `approve_pending_user` varchar(2048) DEFAULT '',
                                   `approve_type` tinyint(4) NOT NULL DEFAULT '0',
                                   PRIMARY KEY (`id`),
                                   KEY `TASK_APP_GROUP_NAME_IDX` (`app_id`,`group_id`,`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务表';


--
-- Table structure for table `tb_release_task_config`
--

DROP TABLE IF EXISTS `tb_release_task_config`;

CREATE TABLE `tb_release_task_config` (
                                          `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                          `ckey` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '配置key名称',
                                          `cvalue` mediumtext NOT NULL,
                                          `value_type` int(11) NOT NULL DEFAULT '0' COMMENT '(1-NUMBER;2-STRING;3-TEXT;4-JSON;5-XML;6-FILE)',
                                          `description` varchar(2048) NOT NULL DEFAULT '' COMMENT '描述',
                                          `task_id` int(11) NOT NULL DEFAULT '0' COMMENT '任务id',
                                          `app_id` varchar(128) NOT NULL,
                                          `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态',
                                          `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                          PRIMARY KEY (`id`),
                                          UNIQUE KEY `app_id` (`app_id`,`task_id`,`ckey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务配置';


--
-- Table structure for table `tb_role`
--

DROP TABLE IF EXISTS `tb_role`;

CREATE TABLE `tb_role` (
                           `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                           `name` varchar(128) NOT NULL COMMENT 'AppID',
                           `app_id` varchar(128) NOT NULL,
                           `persons` varchar(500) NOT NULL DEFAULT '' COMMENT '人员列表',
                           `object` text NOT NULL,
                           `permission_type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '权限类型',
                           `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                           `permission_new_type` varchar(128) NOT NULL DEFAULT '',
                           `env_names` varchar(1024) DEFAULT 'Default' COMMENT '环境列表',
                           PRIMARY KEY (`id`),
                           KEY `ROLE_APP_PERSONS_IDX` (`app_id`,`persons`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色表';


--
-- Table structure for table `tb_role_relation`
--

DROP TABLE IF EXISTS `tb_role_relation`;

CREATE TABLE `tb_role_relation` (
                                    `user_type` tinyint(4) NOT NULL,
                                    `role_id` int(11) NOT NULL,
                                    `userid_list` text NOT NULL,
                                    `username_list` text NOT NULL,
                                    `app_id` varchar(128) NOT NULL,
                                    `persons` mediumtext NOT NULL,
                                    UNIQUE KEY `role_id` (`role_id`,`user_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_auth`
--

DROP TABLE IF EXISTS `tb_row_auth`;

CREATE TABLE `tb_row_auth` (
                               `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                               `auth_type` tinyint(4) NOT NULL COMMENT '1:全表可见;2:仅自己可见;3:修改;4:删除',
                               `table_id` int(11) NOT NULL COMMENT '表ID',
                               `app_id` varchar(64) NOT NULL COMMENT '项目id',
                               `group_id` int(11) NOT NULL COMMENT '分组ID',
                               `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                               `enable_status` tinyint(4) NOT NULL COMMENT '权限勾选状态：1：选中 2未选中',
                               PRIMARY KEY (`id`),
                               UNIQUE KEY `table_id` (`table_id`,`auth_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_latest_version`
--

DROP TABLE IF EXISTS `tb_row_latest_version`;

CREATE TABLE `tb_row_latest_version` (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                         `app_id` varchar(128) NOT NULL COMMENT '项目id',
                                         `group_id` int(11) NOT NULL COMMENT '分组ID',
                                         `group_name` varchar(256) NOT NULL COMMENT '分组名称',
                                         `row_key` varchar(256) NOT NULL COMMENT '行级key',
                                         `col_key` varchar(256) NOT NULL COMMENT '列关键字',
                                         `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '主versionID',
                                         `prev_version_id` int(11) NOT NULL DEFAULT '0' COMMENT '上一主versionID',
                                         `gray_version_id` int(11) NOT NULL DEFAULT '0' COMMENT '灰度versionID',
                                         `latest_event_id` bigint(20) NOT NULL DEFAULT '0',
                                         `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                         `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                                         `config_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '分组类型 0:kv 1:table',
                                         `env_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT 'Default' COMMENT '关联环境名',
                                         `app_type` tinyint(4) NOT NULL,
                                         PRIMARY KEY (`id`),
                                         KEY `row_idx` (`app_id`,`group_id`,`row_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_release_task`
--

DROP TABLE IF EXISTS `tb_row_release_task`;

CREATE TABLE `tb_row_release_task` (
                                       `id` int(11) NOT NULL AUTO_INCREMENT,
                                       `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT '项目id',
                                       `group_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名称',
                                       `group_id` int(11) NOT NULL COMMENT '分组id',
                                       `col_key` varchar(256) NOT NULL COMMENT '唯一key',
                                       `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '当前版本id',
                                       `apply_user` varchar(128) NOT NULL DEFAULT '' COMMENT '发布申请人',
                                       `status` int(11) NOT NULL DEFAULT '0' COMMENT '发布任务状态,(1:等待审批,2:审批拒绝,3:待发布,4:已全量发布,5:已灰度发布,6:回滚,7:任务已完成)',
                                       `description` varchar(256) NOT NULL DEFAULT '0发布描述',
                                       `row_key` varchar(256) NOT NULL COMMENT '行级key',
                                       `reason` text NOT NULL COMMENT '审批原因',
                                       `approval_user` varchar(32) NOT NULL DEFAULT '' COMMENT '审批人',
                                       `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                       `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                       `release_type` varchar(16) NOT NULL COMMENT '发布类型',
                                       `release_env` varchar(64) NOT NULL COMMENT 'CDN环境',
                                       PRIMARY KEY (`id`),
                                       KEY `app_idx` (`app_id`,`group_id`,`row_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_task_event`
--

DROP TABLE IF EXISTS `tb_row_task_event`;

CREATE TABLE `tb_row_task_event` (
                                     `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                     `event_type` varchar(64) NOT NULL DEFAULT '' COMMENT '任务类型',
                                     `task_id` int(11) NOT NULL DEFAULT '0' COMMENT '任务ID',
                                     `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                     `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                     `row_key` varchar(256) NOT NULL COMMENT '行级版本key',
                                     `src_ver_id` int(11) NOT NULL DEFAULT '0' COMMENT '源版本名称',
                                     `dst_ver_id` int(11) NOT NULL DEFAULT '0' COMMENT '目标版本',
                                     `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                     PRIMARY KEY (`id`),
                                     KEY `EVENT_APP_GROUP_IDX` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_version_create`
--

DROP TABLE IF EXISTS `tb_row_version_create`;

CREATE TABLE `tb_row_version_create` (
                                         `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                         `group_id` int(11) NOT NULL DEFAULT '0',
                                         `auto_incr_id` int(11) NOT NULL DEFAULT '0' COMMENT '自增版本id',
                                         `app_id` varchar(128) NOT NULL COMMENT '项目appid',
                                         `row_key` varchar(256) NOT NULL COMMENT '行级key',
                                         PRIMARY KEY (`id`),
                                         UNIQUE KEY `uniq_row` (`app_id`,`group_id`,`row_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_version_info`
--

DROP TABLE IF EXISTS `tb_row_version_info`;

CREATE TABLE `tb_row_version_info` (
                                       `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                       `row_ver_id` int(11) NOT NULL,
                                       `description` varchar(2048) NOT NULL DEFAULT '',
                                       `creator` varchar(64) NOT NULL DEFAULT '' COMMENT '分组创建人',
                                       `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组ID',
                                       `app_id` varchar(128) NOT NULL,
                                       `row_key` varchar(256) NOT NULL COMMENT '行级key',
                                       `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                       `status` int(11) NOT NULL DEFAULT '1',
                                       PRIMARY KEY (`id`),
                                       KEY `VERSION_APP_GROUP_IDX` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_row_version_status`
--

DROP TABLE IF EXISTS `tb_row_version_status`;

CREATE TABLE `tb_row_version_status` (
                                         `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '环境ID',
                                         `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT '项目id',
                                         `group_id` int(11) NOT NULL,
                                         `version_id` int(11) NOT NULL DEFAULT '0' COMMENT '当前版本id',
                                         `prev_version_id` int(11) NOT NULL DEFAULT '0' COMMENT '前一版本id',
                                         `row_key` varchar(256) NOT NULL COMMENT '行级key',
                                         `status` int(11) NOT NULL DEFAULT '1' COMMENT '1:版本可修改 2：版本发布中不可修改',
                                         `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                         `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                         PRIMARY KEY (`id`),
                                         UNIQUE KEY `app_id` (`app_id`,`group_id`,`row_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_schema_config`
--

DROP TABLE IF EXISTS `tb_schema_config`;

CREATE TABLE `tb_schema_config` (
                                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                    `group_id` int(11) NOT NULL DEFAULT '0',
                                    `app_id` varchar(128) NOT NULL COMMENT '项目appid',
                                    `release_type` varchar(16) NOT NULL COMMENT '发布方式：CDN,RAINBOW',
                                    `data_format` varchar(16) NOT NULL COMMENT '数据格式：JSON,JSONP,CUSTOM',
                                    PRIMARY KEY (`id`),
                                    UNIQUE KEY `uniq_idx` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_secret_key_info`
--

DROP TABLE IF EXISTS `tb_secret_key_info`;

CREATE TABLE `tb_secret_key_info` (
                                      `id` int(11) NOT NULL AUTO_INCREMENT,
                                      `app_id` varchar(64) NOT NULL,
                                      `group_id` int(11) NOT NULL,
                                      `type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '类型 1:cos自定义密钥',
                                      `secret` varchar(128) NOT NULL COMMENT '密钥',
                                      `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态,0 不加密;1 正在加密;2 已加密;3 加密失败',
                                      `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                      PRIMARY KEY (`id`),
                                      UNIQUE KEY `group_key` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_staff_info`
--

DROP TABLE IF EXISTS `tb_staff_info`;

CREATE TABLE `tb_staff_info` (
                                 `staff_id` int(11) NOT NULL,
                                 `staff_name` varchar(128) NOT NULL,
                                 `department_id` int(11) NOT NULL,
                                 UNIQUE KEY `staff_name` (`staff_name`),
                                 KEY `TB_STAFF_INFO_DEPART_INDEX` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_sync_info`
--

DROP TABLE IF EXISTS `tb_sync_info`;

CREATE TABLE `tb_sync_info` (
                                `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                `sync_type` tinyint(4) NOT NULL COMMENT '同步类型枚举(1:cmdb,2:url)',
                                `sync_input` text NOT NULL COMMENT '同步输入内容',
                                `output_md5` varchar(64) NOT NULL COMMENT '结果md5',
                                `sync_interval` int(11) NOT NULL COMMENT '同步间隔(s),前端可定1分、1小时、1天等',
                                `timeout` int(11) NOT NULL DEFAULT '0' COMMENT '超时时间',
                                `last_result` tinyint(4) NOT NULL COMMENT '上次同步结果(1:成功;2:失败)',
                                `last_result_msg` varchar(128) NOT NULL DEFAULT '',
                                `is_open` tinyint(4) NOT NULL COMMENT '同步开关0:关闭 1：开启',
                                `is_syncing` tinyint(4) NOT NULL COMMENT '是否正在同步 0:否 1：是',
                                `updator` varchar(128) NOT NULL COMMENT '更新人',
                                `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '同步更新时间',
                                `group_id` int(11) NOT NULL COMMENT '分组 ID',
                                `app_id` varchar(128) NOT NULL COMMENT '项目 ID',
                                `mod_ids` text COMMENT '三级模块id组合',
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `app_group_id` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='同步信息表';


--
-- Table structure for table `tb_sync_list`
--

DROP TABLE IF EXISTS `tb_sync_list`;

CREATE TABLE `tb_sync_list` (
                                `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                `app_id` varchar(128) NOT NULL COMMENT '项目ID',
                                `group_id` int(11) NOT NULL COMMENT '分组 ID',
                                `content` text NOT NULL COMMENT '内容',
                                `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `app_group_id` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='同步实例表';


--
-- Table structure for table `tb_table_info`
--

DROP TABLE IF EXISTS `tb_table_info`;

CREATE TABLE `tb_table_info` (
                                 `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                 `en_name` varchar(32) NOT NULL COMMENT '表英文名',
                                 `description` varchar(256) NOT NULL DEFAULT '' COMMENT '描述',
                                 `row_auth_enable` tinyint(4) NOT NULL COMMENT '是否开启行权限,1:是,2:否',
                                 `creator` varchar(32) DEFAULT NULL COMMENT '创建者',
                                 `app_id` varchar(64) DEFAULT NULL COMMENT '项目id',
                                 `group_id` int(11) NOT NULL COMMENT '分组id',
                                 `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '表创建时间',
                                 PRIMARY KEY (`id`),
                                 UNIQUE KEY `app_id` (`app_id`,`group_id`,`en_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_table_relation`
--

DROP TABLE IF EXISTS `tb_table_relation`;

CREATE TABLE `tb_table_relation` (
                                     `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                     `app_id` varchar(64) NOT NULL,
                                     `from_table_id` int(11) NOT NULL,
                                     `from_group_id` int(11) NOT NULL,
                                     `from_group_name` varchar(32) NOT NULL,
                                     `from_table_name` varchar(32) NOT NULL,
                                     `from_column_name` varchar(32) NOT NULL,
                                     `to_group_id` int(11) NOT NULL,
                                     `to_group_name` varchar(32) NOT NULL,
                                     `to_table_name` varchar(32) NOT NULL,
                                     `to_table_id` int(11) NOT NULL,
                                     `to_column_name` varchar(32) NOT NULL,
                                     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_table_version_info`
--

DROP TABLE IF EXISTS `tb_table_version_info`;

CREATE TABLE `tb_table_version_info` (
                                         `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                         `app_id` varchar(128) NOT NULL COMMENT '项目appid',
                                         `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                         `table_id` int(11) NOT NULL DEFAULT '0' COMMENT '表id',
                                         `creator` varchar(64) NOT NULL DEFAULT '' COMMENT '创建人',
                                         `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                         PRIMARY KEY (`id`),
                                         KEY `table_key` (`app_id`,`group_id`,`table_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_task_event`
--

DROP TABLE IF EXISTS `tb_task_event`;

CREATE TABLE `tb_task_event` (
                                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                 `event_type` varchar(64) NOT NULL DEFAULT '' COMMENT '任务类型',
                                 `task_id` int(11) NOT NULL DEFAULT '0' COMMENT '任务ID',
                                 `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                 `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                 `src_version_name` varchar(128) NOT NULL DEFAULT '0' COMMENT '源版本名称',
                                 `dst_version_name` varchar(128) NOT NULL DEFAULT '0' COMMENT '目标版本名称',
                                 `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                 PRIMARY KEY (`id`),
                                 KEY `EVENT_APP_GROUP_IDX` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_task_notice`
--

DROP TABLE IF EXISTS `tb_task_notice`;

CREATE TABLE `tb_task_notice` (
                                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
                                  `app_id` varchar(64) NOT NULL COMMENT '项目appid',
                                  `group_id` int(11) NOT NULL COMMENT '分组id',
                                  `notice_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0：无 1：服务号 2：群机器人',
                                  `chat_id` varchar(64) NOT NULL DEFAULT '' COMMENT '群机器人chat_id',
                                  `notice_status` varchar(64) DEFAULT '' COMMENT '通知状态：1：待审批 2：审批拒绝 3：待发布 4：已全量 5：已灰度 6：回滚 7：已完成',
                                  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_template_config`
--

DROP TABLE IF EXISTS `tb_template_config`;

CREATE TABLE `tb_template_config` (
                                      `id` int(11) NOT NULL AUTO_INCREMENT,
                                      `app_id` varchar(64) NOT NULL DEFAULT '',
                                      `type` tinyint(4) NOT NULL COMMENT '1:用户分类模板',
                                      `content` text NOT NULL COMMENT '模板表结构配置',
                                      `name` varchar(32) NOT NULL COMMENT '模板名称',
                                      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_token_info`
--

DROP TABLE IF EXISTS `tb_token_info`;

CREATE TABLE `tb_token_info` (
                                 `id` int(11) NOT NULL AUTO_INCREMENT,
                                 `username` varchar(64) NOT NULL COMMENT '用户名',
                                 `token` varchar(256) NOT NULL COMMENT '用户票据',
                                 `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                 `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                 PRIMARY KEY (`id`),
                                 UNIQUE KEY `user_key` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_upload_file_info`
--

DROP TABLE IF EXISTS `tb_upload_file_info`;

CREATE TABLE `tb_upload_file_info` (
                                       `id` int(11) NOT NULL AUTO_INCREMENT,
                                       `app_id` varchar(64) NOT NULL,
                                       `user` varchar(64) NOT NULL DEFAULT '用户',
                                       `name` varchar(64) NOT NULL COMMENT '文件名',
                                       `url` varchar(512) NOT NULL COMMENT '链接',
                                       `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                       `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                       PRIMARY KEY (`id`),
                                       UNIQUE KEY `url_key` (`url`),
                                       KEY `app_id` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_user_info`
--

DROP TABLE IF EXISTS `tb_user_info`;

CREATE TABLE `tb_user_info` (
                                `id` int(11) NOT NULL AUTO_INCREMENT,
                                `username` varchar(64) NOT NULL COMMENT '用户名',
                                `password_md5` varchar(64) NOT NULL COMMENT '用户密码',
                                `email` varchar(1204) NOT NULL COMMENT '用户邮箱',
                                `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `user_key` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `tb_user_op_log`
--

DROP TABLE IF EXISTS `tb_user_op_log`;

CREATE TABLE `tb_user_op_log` (
                                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                                  `app_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'AppID',
                                  `group` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '分组名',
                                  `user` varchar(64) NOT NULL COMMENT '用户名',
                                  `env_name` varchar(64) NOT NULL COMMENT 'env name',
                                  `record_type` varchar(64) NOT NULL COMMENT '操作类型，如更改数据、发布操作',
                                  `data_log` text NOT NULL COMMENT '更改数据的内容',
                                  `release_log` text NOT NULL COMMENT '发布版本记录',
                                  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                  PRIMARY KEY (`id`),
                                  KEY `time_key` (`time`),
                                  KEY `group_key` (`app_id`,`env_name`,`group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户端列表最新版';


--
-- Table structure for table `tb_value_check_rule`
--

DROP TABLE IF EXISTS `tb_value_check_rule`;

CREATE TABLE `tb_value_check_rule` (
                                       `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                       `value_type` int(11) NOT NULL COMMENT '(1-NUMBER;2-STRING;3-TEXT;4-JSON;5-XML;6-FILE)',
                                       `name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则名',
                                       `content` varchar(64) NOT NULL DEFAULT '' COMMENT '内容',
                                       `check_type` int(11) NOT NULL DEFAULT '0' COMMENT '规则类型',
                                       `app_id` varchar(128) NOT NULL,
                                       PRIMARY KEY (`id`),
                                       UNIQUE KEY `app_id` (`app_id`,`value_type`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='类型检查表';


--
-- Table structure for table `tb_version_info`
--

DROP TABLE IF EXISTS `tb_version_info`;

CREATE TABLE `tb_version_info` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                   `name` varchar(128) NOT NULL,
                                   `description` varchar(2048) NOT NULL DEFAULT '',
                                   `creator` varchar(64) NOT NULL DEFAULT '' COMMENT '创建人',
                                   `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                   `app_id` varchar(128) NOT NULL,
                                   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   `version_uuid` varchar(128) NOT NULL DEFAULT '',
                                   `status` int(11) NOT NULL DEFAULT '1',
                                   `version_type` tinyint(4) NOT NULL DEFAULT '0',
                                   `dimens` varchar(4096) DEFAULT NULL COMMENT '维度',
                                   PRIMARY KEY (`id`),
                                   KEY `VERSION_APP_GROUP_IDX` (`app_id`,`group_id`),
                                   KEY `VERSION_INFO_UUID` (`version_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='版本信息';


--
-- Table structure for table `tb_version_info_mid`
--

DROP TABLE IF EXISTS `tb_version_info_mid`;

CREATE TABLE `tb_version_info_mid` (
                                       `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                       `name` varchar(128) NOT NULL,
                                       `description` varchar(2048) NOT NULL DEFAULT '',
                                       `creator` varchar(64) NOT NULL DEFAULT '' COMMENT '创建人',
                                       `group_id` int(11) NOT NULL DEFAULT '0' COMMENT '分组id',
                                       `app_id` varchar(128) NOT NULL,
                                       `version_uuid` varchar(128) NOT NULL DEFAULT '',
                                       PRIMARY KEY (`id`),
                                       UNIQUE KEY `app_id` (`app_id`,`group_id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='版本信息中间表';


--
-- Table structure for table `tb_version_log`
--

DROP TABLE IF EXISTS `tb_version_log`;

CREATE TABLE `tb_version_log` (
                                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                  `version_name` varchar(128) NOT NULL,
                                  `app_id` varchar(128) NOT NULL,
                                  `group_name` varchar(2048) NOT NULL DEFAULT '' COMMENT '分组名',
                                  `ckey` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
                                  `cvalue` mediumtext,
                                  `op_type` int(11) NOT NULL DEFAULT '0' COMMENT '操作类型',
                                  `operator` varchar(2048) NOT NULL DEFAULT '' COMMENT '操作人',
                                  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                  `version_uuid` varchar(128) NOT NULL DEFAULT '',
                                  `group_id` int(11) NOT NULL DEFAULT '0',
                                  PRIMARY KEY (`id`),
                                  KEY `VERSION_LOG_APP_IDX` (`app_id`,`version_name`,`ckey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='配置更改表´';


--
-- Table structure for table `tb_white_list`
--

DROP TABLE IF EXISTS `tb_white_list`;

CREATE TABLE `tb_white_list` (
                                 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                 `app_id` varchar(128) NOT NULL,
                                 `group_id` int(11) NOT NULL COMMENT '分组id',
                                 `white_list_type_id` int(11) NOT NULL COMMENT '白名单类型id',
                                 `content` text NOT NULL COMMENT '内容¹',
                                 `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                 PRIMARY KEY (`id`),
                                 UNIQUE KEY `app_id` (`app_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='白名单';


--
-- Table structure for table `tb_white_list_type`
--

DROP TABLE IF EXISTS `tb_white_list_type`;

CREATE TABLE `tb_white_list_type` (
                                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
                                      `client_name` varchar(64) NOT NULL DEFAULT '' COMMENT '客户端标识名',
                                      `name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则名',
                                      `en_name` varchar(64) NOT NULL DEFAULT '' COMMENT '规则英文',
                                      `type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '白名单类型：0：ip类型 1：cmdb类型',
                                      PRIMARY KEY (`id`),
                                      UNIQUE KEY `en_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='白名单规则类型';


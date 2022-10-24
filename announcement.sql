/*
 Navicat MySQL Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : announcement

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 24/10/2022 15:29:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for agency_unit
-- ----------------------------
DROP TABLE IF EXISTS `agency_unit`;
CREATE TABLE `agency_unit`  (
  `Id` bigint NOT NULL COMMENT '标识',
  `OrgName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织名称',
  `OrgCode` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构代码',
  `UpId` bigint NULL DEFAULT NULL COMMENT '上级组织',
  `UpName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上级组织名称',
  `IdentityState` tinyint NOT NULL COMMENT '身份状态0：无效，1：有效',
  `ImportTime` date NOT NULL COMMENT '录入时间',
  `MainProperty` tinyint NULL DEFAULT NULL COMMENT '主体性质1、政府   2、企业  3、个体户  4、其它组织',
  `BusTerm` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '营业期限',
  `FoundTime` date NULL DEFAULT NULL COMMENT '成立日期',
  `RegMoney` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '注册资金',
  `Linkman` bigint NULL DEFAULT NULL COMMENT '单位联系人',
  `LinkmanName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '单位联系人名称',
  `LinkmanPhone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '单位联系人电话',
  `Remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '描述',
  `LocalProv` bigint NULL DEFAULT NULL COMMENT '所在省',
  `LocalProvName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所在省名',
  `LocalCity` bigint NULL DEFAULT NULL COMMENT '所在市',
  `LocalCityName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所在市名',
  `LocalCounty` bigint NULL DEFAULT NULL COMMENT '所在区/县',
  `LocalCountyName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所在区县名',
  `LocalAddr` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所在详细地址',
  `PostCode` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮编',
  `MainScope` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '主营范围',
  `ConcurrentlyScope` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '兼营范围',
  `TradeType` tinyint NULL DEFAULT NULL COMMENT '行业类型标识',
  `TradeTypeName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '行业名称：工商 公安 质监 教委 地税 财政 卫生 农委 民政 国土 环保 计生 监狱  体育 检察 林业 社保 市政 水利 文广 药监 法院',
  `CompanyType` tinyint NULL DEFAULT NULL COMMENT '公司类型1-总公司 2-分支机构',
  `LegalPerson` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '法人代表',
  `LegalPersonIdentity` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '法人身份证号',
  `LegalPersonEmail` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '法人邮箱',
  `LegalPersonPhone` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '法人电话',
  `RegAddress` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '注册地址',
  `EffectAreaId` bigint NULL DEFAULT NULL COMMENT '有效区域标识',
  `EffectAreaName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '有效区域名称',
  `IsConfirm` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0' COMMENT '是否已人工确认',
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '代理机构信息库' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for agent_unit
-- ----------------------------
DROP TABLE IF EXISTS `agent_unit`;
CREATE TABLE `agent_unit`  (
  `id` bigint NOT NULL,
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '代理机构识别编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构名称',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构地址',
  PRIMARY KEY (`id`, `code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for an_agent_rel
-- ----------------------------
DROP TABLE IF EXISTS `an_agent_rel`;
CREATE TABLE `an_agent_rel`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `an_table` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告所属表\\r\\nCB_G: call_bid_government\\r\\nWB_G: win_bid_government\\r\\nFB_G: failure_bid_government\\r\\nMB_G: modify_bid_government\\r\\nCB_E: call_bid_engineering',
  `an_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告ID',
  `ag_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for an_at_rel
-- ----------------------------
DROP TABLE IF EXISTS `an_at_rel`;
CREATE TABLE `an_at_rel`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `an_table` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告所属表\\r\\nCB_G: call_bid_government\\r\\nWB_G: win_bid_government\\r\\nFB_G: failure_bid_government\\r\\nMB_G: modify_bid_government\\r\\nCB_E: call_bid_engineering',
  `an_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告ID',
  `at_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件ID',
  `at_table` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件对应表\\r\\nFL: file_list\\r\\nACT: attachment',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99757601499120043 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for an_callunit_rel
-- ----------------------------
DROP TABLE IF EXISTS `an_callunit_rel`;
CREATE TABLE `an_callunit_rel`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `an_table` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告所属表\\r\\nCB_G: call_bid_government\\r\\nWB_G: win_bid_government\\r\\nFB_G: failure_bid_government\\r\\nMB_G: modify_bid_government\\r\\nCB_E: call_bid_engineering',
  `an_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告ID',
  `callunit_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 308773531428430279 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for an_prov_rel
-- ----------------------------
DROP TABLE IF EXISTS `an_prov_rel`;
CREATE TABLE `an_prov_rel`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `an_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告ID',
  `prov_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '供货商ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for an_relation_analysis_version
-- ----------------------------
DROP TABLE IF EXISTS `an_relation_analysis_version`;
CREATE TABLE `an_relation_analysis_version`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `an_id` bigint NULL DEFAULT NULL,
  `an_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `relation_analysis_version` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `real_version` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `an_id_and_type`(`an_id`, `an_type`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for an_supp_rel
-- ----------------------------
DROP TABLE IF EXISTS `an_supp_rel`;
CREATE TABLE `an_supp_rel`  (
  `id` bigint NOT NULL,
  `an_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `supp_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for attachment
-- ----------------------------
DROP TABLE IF EXISTS `attachment`;
CREATE TABLE `attachment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '附件名',
  `file_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '附件类型',
  `file_size` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '附件大小',
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件URL地址',
  `local_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件存储本地路径',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99757601499120040 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for call_bid_engineering
-- ----------------------------
DROP TABLE IF EXISTS `call_bid_engineering`;
CREATE TABLE `call_bid_engineering`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proj_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `proj_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目编号',
  `resource_from` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '资金来源',
  `ET` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '计划工期',
  `region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '行政区域',
  `proj_unit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购单位名称',
  `proj_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位地址',
  `proj_rel_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标人联系人',
  `proj_rel_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标人联系方式',
  `agent_unit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构名称',
  `agent_unit_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标代理机构联系人',
  `agent_unit_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标代理机构联系方式',
  `agent_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `tender_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '投标地点',
  `bid_sale_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标书发售方式',
  `bid_sale_op_time` datetime NULL DEFAULT NULL COMMENT '标书发售起止时间',
  `bid_sale_en_time` datetime NULL DEFAULT NULL COMMENT '标书发售起止时间',
  `bid_price` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标书售价',
  `bid_sale_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标书发售地点',
  `bid_end_time` datetime NULL DEFAULT NULL COMMENT '投标结束时间',
  `other_ex` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '其它说明',
  `sourse_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `proj_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目地点',
  `web_site` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应目标网站',
  `source_web_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源网站名网站',
  `ancm_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `resolution_rate` float NULL DEFAULT 0.5 COMMENT '数据解析率，默认0.5',
  `insert_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99757601499119959 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for call_bid_government
-- ----------------------------
DROP TABLE IF EXISTS `call_bid_government`;
CREATE TABLE `call_bid_government`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proj_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '采购项目名称',
  `proj_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目编号',
  `proj_item` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '品目',
  `call_unit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购单位',
  `region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '行政区域',
  `ancm_time` datetime NULL DEFAULT NULL COMMENT '公告发布时间',
  `budget` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '预算金额',
  `call_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位地址',
  `proj_rel_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目联系人',
  `proj_rel_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目联系方式',
  `agent_unit_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构名称',
  `agent_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `agent_unit_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构联系人',
  `agent_unit_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构联系方式',
  `tender_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '投标地点',
  `bid_sale_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标书发售方式',
  `bid_sale_op_time` datetime NULL DEFAULT NULL COMMENT '标书发售时间',
  `bid_sale_en_time` datetime NULL DEFAULT NULL COMMENT '标书发售截止时间',
  `bid_sale_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标书发售地点',
  `bid_price` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标书售价',
  `bid_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '开标地点',
  `other_ex` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '其他说明',
  `purchase_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购方式',
  `sourse_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公告网页URL',
  `bid_time` datetime NULL DEFAULT NULL COMMENT '开标时间',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公告标题',
  `web_site` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应目标网站',
  `source_web_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源网站名网站',
  `bid_end_time` datetime NULL DEFAULT NULL COMMENT '投标结束时间',
  `resolution_rate` float NULL DEFAULT 0.5 COMMENT '数据解析率，默认0.5',
  `insert_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `proj_name`(`proj_name`(100)) USING BTREE,
  INDEX `proj_code`(`proj_code`(100)) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 408768510880315898 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for call_bid_unit
-- ----------------------------
DROP TABLE IF EXISTS `call_bid_unit`;
CREATE TABLE `call_bid_unit`  (
  `id` bigint NOT NULL,
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '采购机构唯一识别码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购机构名',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购机构地址',
  PRIMARY KEY (`id`, `code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for contract
-- ----------------------------
DROP TABLE IF EXISTS `contract`;
CREATE TABLE `contract`  (
  `id` bigint NOT NULL,
  `contract_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '合同编号',
  `contract_name` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '合同名称',
  `project_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '项目编号',
  `project_name` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '项目名称',
  `region` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '区域',
  `purchase_directory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购目录（可能有多个物品）',
  `specification_and_model` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '规格型号（可能有多个物品）',
  `purchase_time` date NULL DEFAULT NULL COMMENT '采购时间',
  `purchase_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购方式',
  `purchase_number` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购数量（可能有多个物品）',
  `win_bid_brand` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中标品牌',
  `win_bid_model` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中标型号',
  `unit_price` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '中标单价（可能有多个物品）',
  `total_amount` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中标总金额',
  `import_and_export` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '进出口',
  `brief_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '简要信息',
  `contract_sign_date` date NULL DEFAULT NULL COMMENT '合同签订日期',
  `contract_announcement_date` date NULL DEFAULT NULL COMMENT '合同公告日期',
  `enclosure_link` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '附件链接',
  `supplier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '供应商',
  `supplier_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '供应商联系电话',
  `supplier_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '供应商地址',
  `agency` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构',
  `agency_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构联系电话',
  `agency_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `purchaser` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购人',
  `purchaser_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购人联系电话',
  `purchaser_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购人地址',
  `tender_an_link` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '招标公告链接',
  `result_an_link` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '结果公告链接',
  `contract_an_link` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '合同公告链接',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for dishonest_list
-- ----------------------------
DROP TABLE IF EXISTS `dishonest_list`;
CREATE TABLE `dishonest_list`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '企业名称',
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '统一社会信用代码（或组织机构代码）',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '企业地址',
  `behavior` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '严重违法失信行为的具体情形',
  `punishment_result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '处罚结果',
  `punishment_basis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '处罚依据',
  `open_date` datetime NULL DEFAULT NULL COMMENT '公布日期',
  `punishment_date` date NULL DEFAULT NULL COMMENT '处罚日期',
  `deadline` date NULL DEFAULT NULL COMMENT '公布截止日期',
  `law_enforcement_unit` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '执法单位',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99786518775726774 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for expert
-- ----------------------------
DROP TABLE IF EXISTS `expert`;
CREATE TABLE `expert`  (
  `id` bigint NOT NULL,
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专家唯一识别编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '专家名',
  PRIMARY KEY (`id`, `code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for failure_bid_government
-- ----------------------------
DROP TABLE IF EXISTS `failure_bid_government`;
CREATE TABLE `failure_bid_government`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proj_name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '项目名称',
  `proj_code` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '项目编号',
  `region` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '行政区域',
  `ancm_time` datetime NULL DEFAULT NULL COMMENT '公告发布时间',
  `purchasing_unit_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '采购单位名称',
  `call_unit_address` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '采购单位地址',
  `proj_rel_p` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '项目联系人',
  `proj_rel_m` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '项目联系方式',
  `agent_unit_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '代理机构名称',
  `agent_unit_address` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `agent_unit_p` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '代理机构联系人',
  `agent_unit_m` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '代理机构联系方式',
  `other_ex` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '其他说明',
  `purchase_m` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '采购方式',
  `sourse_url` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '公告URL',
  `bid_time` datetime NULL DEFAULT NULL COMMENT '开标时间',
  `title` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '公告标题',
  `failure_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '流标内容',
  `web_site` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '对应目标网站',
  `source_web_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '来源网站名网站',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for farm_market
-- ----------------------------
DROP TABLE IF EXISTS `farm_market`;
CREATE TABLE `farm_market`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '标识',
  `market` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '市场',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品类别',
  `variety` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '品种',
  `time` datetime NULL DEFAULT NULL COMMENT '日期',
  `method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '售卖方式',
  `price` float NULL DEFAULT NULL COMMENT '价格',
  `unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '单价',
  `yesterdaynum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昨日量',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99968013960216708 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for intention_detail
-- ----------------------------
DROP TABLE IF EXISTS `intention_detail`;
CREATE TABLE `intention_detail`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proj_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '名称',
  `survey` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '概况',
  `budget` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预算',
  `purchase_time` datetime NULL DEFAULT NULL COMMENT '采购时间',
  `other` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `insert_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99854610834916744 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for intention_main
-- ----------------------------
DROP TABLE IF EXISTS `intention_main`;
CREATE TABLE `intention_main`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '直辖市的省、市相同',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '非直辖市：省本级，市、区字段为null；',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '市本级，区字段为null',
  `level` int NULL DEFAULT NULL COMMENT '1.省本级；2：市本级；3.区级\r\n1.省本级；2：市本级；3.区级\r\n1.省本级；2：市本级；3.区级',
  `call_unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发布单位',
  `purchase_unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `acnm_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `total_budget` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '明细表中预算金额之和',
  `source_website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '网站名',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '源地址url',
  `insert_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间（自动填充）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99854610834916737 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for intention_rel
-- ----------------------------
DROP TABLE IF EXISTS `intention_rel`;
CREATE TABLE `intention_rel`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `main_id` bigint NOT NULL,
  `detail_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99854610834916747 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for modify_bid_government
-- ----------------------------
DROP TABLE IF EXISTS `modify_bid_government`;
CREATE TABLE `modify_bid_government`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proj_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '采购项目名',
  `proj_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目编号',
  `region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '行政区域',
  `ancm_time` datetime NULL DEFAULT NULL COMMENT '公告发布时间',
  `purchasing_unit_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位名称',
  `call_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位地址',
  `proj_rel_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目联系人',
  `proj_rel_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目联系方式',
  `agent_unit_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构名称',
  `agent_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `agent_unit_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构联系人',
  `agent_unit_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构联系方式',
  `other_ex` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '其他说明',
  `purchase_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购方式',
  `sourse_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公告URL',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公告标题',
  `modify_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '更正内容',
  `origin_announce_time` datetime NULL DEFAULT NULL COMMENT '起始发布时间',
  `web_site` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应目标网站',
  `source_web_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源网站名网站',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for provide_unit
-- ----------------------------
DROP TABLE IF EXISTS `provide_unit`;
CREATE TABLE `provide_unit`  (
  `id` bigint NOT NULL,
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '供应商唯一识别标识',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '供应商名',
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '供应商地址',
  PRIMARY KEY (`id`, `code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for results_an_engineering
-- ----------------------------
DROP TABLE IF EXISTS `results_an_engineering`;
CREATE TABLE `results_an_engineering`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proj_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `proj_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目编号',
  `opening_time` datetime NULL DEFAULT NULL COMMENT '开标时间',
  `notice_period` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公示期',
  `price_ceiling` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '最高限价',
  `proj_unit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购单位名称',
  `proj_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位地址',
  `proj_rel_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标人联系人',
  `proj_rel_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标人联系方式',
  `agent_unit_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标代理机构联系人',
  `agent_unit_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '招标代理机构联系方式',
  `agent_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `other_ex` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '其它说明',
  `sourse_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `web_site` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应目标网站',
  `source_web_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源网站名网站',
  `ancm_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `resolution_rate` float NULL DEFAULT 0.5 COMMENT '数据解析率，默认0.5',
  `insert_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for undefined_exp
-- ----------------------------
DROP TABLE IF EXISTS `undefined_exp`;
CREATE TABLE `undefined_exp`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `sub_an_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属公告ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for wb_supplier
-- ----------------------------
DROP TABLE IF EXISTS `wb_supplier`;
CREATE TABLE `wb_supplier`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `supp_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '中标供应商',
  `supp_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中标供应商编号',
  `supp_ranking` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中标供应商名次',
  `supp_amount` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '中标金额',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for win_bid_government
-- ----------------------------
DROP TABLE IF EXISTS `win_bid_government`;
CREATE TABLE `win_bid_government`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proj_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '采购项目名称',
  `proj_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目编号',
  `proj_item` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '品目',
  `call_unit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购单位',
  `region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '行政区域',
  `ancm_time` datetime NULL DEFAULT NULL COMMENT '公告发布时间',
  `actual_price` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '中标金额',
  `call_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购单位地址',
  `proj_rel_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目联系人',
  `proj_rel_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '项目联系方式',
  `agent_unit_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构名称',
  `agent_unit_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理机构地址',
  `agent_unit_p` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构联系人',
  `agent_unit_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构联系方式',
  `other_ex` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '其他说明',
  `purchase_m` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '采购方式',
  `sourse_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公告网页URL',
  `bid_time` datetime NULL DEFAULT NULL COMMENT '开标时间',
  `provide_unit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '供应商',
  `provide_address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '供应商地址',
  `review_time` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '评审时间',
  `review_place` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '评审地点',
  `pxy_fee_standard` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构收费标准',
  `pxy_fee` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '代理机构收费金额',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '公告标题',
  `web_site` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应目标网站',
  `source_web_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源网站名网站',
  `resolution_rate` float NULL DEFAULT 0.5 COMMENT '数据解析率，默认0.5',
  `insert_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `proj_name`(`proj_name`(100)) USING BTREE,
  INDEX `proj_code`(`proj_code`(100)) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 508746082913539322 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Procedure structure for update_a
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_a`;
delimiter ;;
CREATE PROCEDURE `update_a`()
BEGIN
set @cnt1 =(SELECT ancm_time FROM announcement.call_bid_government ORDER BY ancm_time DESC LIMIT 1);
SELECT @cnt1;
DELETE FROM announcement.call_bid_government WHERE ancm_time >= @cnt1;
INSERT into  announcement.call_bid_government SELECT * FROM an.`call_bid_government` WHERE ancm_time >= @cnt1 ORDER BY ancm_time;

set @cnt2 =(SELECT ancm_time FROM announcement.win_bid_government ORDER BY ancm_time DESC LIMIT 1);
SELECT @cnt2;
DELETE FROM announcement.win_bid_government WHERE ancm_time >= @cnt2;
INSERT into  announcement.win_bid_government SELECT * FROM an.`win_bid_government` WHERE ancm_time >= @cnt2 ORDER BY ancm_time;
END
;;
delimiter ;

-- ----------------------------
-- Event structure for second_event
-- ----------------------------
DROP EVENT IF EXISTS `second_event`;
delimiter ;;
CREATE EVENT `second_event`
ON SCHEDULE
EVERY '60' SECOND STARTS '2021-06-25 10:25:56'
ON COMPLETION PRESERVE
DISABLE
DO call update_a()
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

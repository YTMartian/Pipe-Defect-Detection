/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 8.0.17 : Database - pipe_defect_detection_system
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`pipe_defect_detection_system` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `pipe_defect_detection_system`;

/*Table structure for table `defect` */

DROP TABLE IF EXISTS `defect`;

CREATE TABLE `defect` (
  `defect_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '缺陷id',
  `video_id` int(11) DEFAULT NULL COMMENT '视频id',
  `time_in_video` int(11) DEFAULT '0' COMMENT '视频内时间',
  `defect_type_id` int(11) DEFAULT '1' COMMENT '缺陷类别',
  `defect_distance` float DEFAULT '0' COMMENT '缺陷距离(纵向距离)',
  `defect_length` float DEFAULT '0' COMMENT '缺陷长度',
  `clock_start` int(11) DEFAULT '1' COMMENT '环向起点(钟点方向，1至12)',
  `clock_end` int(11) DEFAULT '1' COMMENT '环向终点',
  `defect_grade_id` int(11) DEFAULT '1' COMMENT '缺陷级别id',
  `defect_remark` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '备注信息',
  `defect_date` datetime DEFAULT NULL COMMENT '判读日期',
  `defect_attribute` varchar(100) DEFAULT '结构性缺陷' COMMENT '缺陷性质',
  PRIMARY KEY (`defect_id`),
  KEY `defect_type_id_fk` (`defect_type_id`),
  KEY `defect_grade_id_fk` (`defect_grade_id`),
  KEY `video_id_fk` (`video_id`),
  CONSTRAINT `defect_grade_id_fk` FOREIGN KEY (`defect_grade_id`) REFERENCES `defect_grade` (`defect_grade_id`),
  CONSTRAINT `defect_type_id_fk` FOREIGN KEY (`defect_type_id`) REFERENCES `defect_type` (`defect_type_id`),
  CONSTRAINT `video_id_fk` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8;

/*Data for the table `defect` */

insert  into `defect`(`defect_id`,`video_id`,`time_in_video`,`defect_type_id`,`defect_distance`,`defect_length`,`clock_start`,`clock_end`,`defect_grade_id`,`defect_remark`,`defect_date`,`defect_attribute`) values 
(97,53,5,6,10,0,1,1,20,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(98,53,83,16,0,0,1,1,55,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(99,53,501,13,0,0,1,1,45,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(100,53,557,6,0,0,1,1,20,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(102,53,983,1,0,0,1,1,1,NULL,'2020-01-13 10:21:34','结构性缺陷'),
(103,53,1021,7,0,0,1,1,23,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(104,53,1314,6,0,0,1,1,21,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(105,53,1336,1,0,0,1,1,1,NULL,'2020-01-13 10:21:34','结构性缺陷'),
(106,53,1656,2,0,0,1,1,4,'支管未通过检查井直接侧向接入主管。','2020-01-13 10:21:34','结构性缺陷'),
(142,35,1990,1,0,0,1,1,1,NULL,'2020-02-21 15:49:12','结构性缺陷'),
(143,53,101,1,1.2,0,1,1,1,'支管未通过检查井直接侧向接入主管。','2020-02-21 15:59:16','结构性缺陷'),
(145,53,294,1,0,0,1,1,1,NULL,'2020-02-21 18:41:36','结构性缺陷'),
(147,53,1870,4,0,0,1,1,12,'支管未通过检查井直接侧向接入主管。','2020-02-21 18:41:46','结构性缺陷'),
(148,53,2258,2,0,0,1,1,7,'支管未通过检查井直接侧向接入主管。','2020-02-21 18:41:49','结构性缺陷'),
(150,53,1178,1,0,0,1,1,1,NULL,'2020-02-21 18:43:47','结构性缺陷'),
(151,53,1505,1,0,0,1,1,1,NULL,'2020-02-21 18:43:50','结构性缺陷'),
(153,53,201,1,0,0,1,1,1,NULL,'2020-02-21 18:43:57','结构性缺陷'),
(154,53,399,1,0,0,1,1,1,NULL,'2020-02-21 18:44:00','结构性缺陷'),
(155,53,684,1,0,0,1,1,1,NULL,'2020-02-21 18:44:06','结构性缺陷');

/*Table structure for table `defect_grade` */

DROP TABLE IF EXISTS `defect_grade`;

CREATE TABLE `defect_grade` (
  `defect_grade_id` int(11) NOT NULL COMMENT '缺陷级别id',
  `defect_grade_name` varchar(100) DEFAULT NULL COMMENT '名称',
  `defeact_type_id` int(11) DEFAULT NULL COMMENT '缺陷类别',
  `score` float DEFAULT '0' COMMENT '分值',
  PRIMARY KEY (`defect_grade_id`),
  KEY `defeact_type_id_fk` (`defeact_type_id`),
  CONSTRAINT `defeact_type_id_fk` FOREIGN KEY (`defeact_type_id`) REFERENCES `defect_type` (`defect_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `defect_grade` */

insert  into `defect_grade`(`defect_grade_id`,`defect_grade_name`,`defeact_type_id`,`score`) values 
(1,'1级：支管进入主管内的长度不大于主管内径的10%',1,0.5),
(2,'2级：支管进入主管内的长度在主管直径的10%~20%之间',1,2),
(3,'3级：支管进入主管内的长度大于主管直径的20%',1,5),
(4,'1级：变形不大于管道直径的5%',2,1),
(5,'2级：变形为管道直径的5%~15%',2,2),
(6,'3级：变形为管道直径的15%~25%',2,5),
(7,'4级：变形大于管道直径的25%',2,10),
(8,'1级：沉积物厚度为管道直径的20%~30%',3,0.5),
(9,'2级：沉积物厚度为管道直径的30%~40%',3,2),
(10,'3级：沉积物厚度为管道直径的40%~50%',3,5),
(11,'4级：沉积物厚度大于管道直径的50%',3,10),
(12,'1级：轻度错口，相接的两个管口偏差不大于管壁厚度的1/2',4,0.5),
(13,'2级：中度错口，相接的两个管口偏差为管壁厚度的1/2~1倍',4,2),
(14,'3级：重度错口，相接的两个管口偏差为管壁厚度的1~2倍',4,5),
(15,'4级：严重错口，相接的两个管口偏差为管壁厚度的2倍以上',4,10),
(16,'1级：过水断面损失不大于15%',5,1),
(17,'2级：过水断面损失在15%~25%之间',5,3),
(18,'3级：过水断面损失在25%~50%之间',5,5),
(19,'4级：过水断面损失大于50%',5,10),
(20,'1级：异物在管道内且占用过水断面面积不大于10%',6,0.5),
(21,'2级：异物在管道内占用过水断面面积为10%~30%',6,2),
(22,'3级：异物在管道内且占用过水断面面积大于30%',6,5),
(23,'1级：轻度腐蚀，表面轻微剥落，管壁出现凹凸面',7,0.5),
(24,'2级：中度腐蚀，表面剥落显露出粗骨料或钢筋',7,2),
(25,'3级：重度腐蚀，粗骨料或钢筋完全显露',7,5),
(26,'1级：零星的漂浮物，漂浮物占水面面积不大于30%',8,0),
(27,'2级：较多的漂浮物，漂浮物占水面面积为30%~60%',8,0),
(28,'3级：大量的漂浮物，漂浮物占水面面积大于60%',8,0),
(29,'1级：硬质结构造成的过水断面损失不大于15%；软质结构造成的过水断面损失在15%~25%之间',9,0.5),
(30,'2级：硬质结构造成的过水断面损失在15%~25%之间；软质结构造成的过水断面损失在25%~50%之间',9,2),
(31,'3级：硬质结构造成的过水断面损失在25%~50%之间；软质结构造成的过水断面损失在50%~80%之间',9,5),
(32,'4级：硬质结构造成的过水断面损失大于50%；软质结构造成的过水断面损失大于80%',9,10),
(33,'1级：裂痕，当下列一个或多个情况存在时：1、在管壁上可见细裂痕。2、在管壁上由细裂痕处冒出少量沉积物。3、轻度剥落。',10,0.5),
(34,'2级：裂口，破裂处已形成明显间隙，但管道的形状未受影响且破裂无脱落',10,2),
(35,'3级：破碎，管壁破裂或脱落处所剩碎片的环向覆盖范围不不大于弧长60°',10,5),
(36,'4级：坍塌，当下列一个或多个情况存在时：1、管道材料裂痕、裂口或破碎处边缘环向覆盖范围大于弧长60°。2、管壁材料发生脱落的环向范围大于弧长60°',10,10),
(37,'1级：起伏高/管径≤20%',11,0.5),
(38,'2级：20%＜起伏高/管径≤35%',11,2),
(39,'3级：35%＜起伏高/管径≤50%',11,5),
(40,'4级：50%＜起伏高/管径',11,10),
(41,'1级：过水断面损失不大于15%',12,0.5),
(42,'2级：过水断面损失在15%~25%之间',12,2),
(43,'3级：过水断面损失在25%~50%之间',12,5),
(44,'4级：过水断面损失大于50%',12,10),
(45,'1级：滴漏，水持续从缺陷点滴出，沿管壁流动',13,0.5),
(46,'2级：线漏，水持续从缺陷点流出，并脱离管壁流动',13,2),
(47,'3级：涌漏，水从缺陷点涌出，涌漏水面的面积不大于管道断面的1/3',13,5),
(48,'4级：喷漏，水从缺陷点大量涌出或喷出，涌漏水面的面积大于管道断面的1/3',13,10),
(49,'1级：轻度脱节，管道端部有少量泥土挤入',14,1),
(50,'2级：中度脱节，脱节距离不大于20mm',14,3),
(51,'3级：重度脱节，脱节距离为20mm~50mm',14,5),
(52,'4级：严重脱节，脱节距离为50mm以上',14,10),
(53,'1级：接口材料在管道内水平方向中心线上部可见',15,1),
(54,'2级：接口材料在管道内水平方向中心线下部可见',15,3),
(55,'1级：过水断面损失不大于15%',16,0.1),
(56,'2级：过水断面损失在15%~25%之间',16,2),
(57,'3级：过水断面损失在25%~50%之间',16,5),
(58,'4级：过水断面损失大于50%',16,10);

/*Table structure for table `defect_type` */

DROP TABLE IF EXISTS `defect_type`;

CREATE TABLE `defect_type` (
  `defect_type_id` int(11) NOT NULL COMMENT '缺陷类别id',
  `defect_type_name` varchar(100) DEFAULT NULL COMMENT '名称',
  `defect_default_info` varchar(100) DEFAULT NULL COMMENT '备注信息',
  PRIMARY KEY (`defect_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `defect_type` */

insert  into `defect_type`(`defect_type_id`,`defect_type_name`,`defect_default_info`) values 
(1,'AJ（支管暗接）','支管未通过检查井直接侧向接入主管。'),
(2,'BX（变形）','管道受外力挤压造成形状变异。'),
(3,'CJ（沉积）','杂质在管道底部沉淀淤积。'),
(4,'CK（错口）','同一接口的两个管口产生横向偏差，未处于管道的正确位置。'),
(5,'CQ（残墙、坝根）','管道闭水试验时砌筑的临时砖墙封堵，试验后未拆除或拆除不彻底的遗留物。'),
(6,'CR（异物穿入）','非管道系统附属设施的物体穿透管壁进入管内。'),
(7,'FS（腐蚀）','管道内壁受侵蚀而流失或剥落，出现麻面或露出钢筋。'),
(8,'FZ（浮渣）','管道内水面上的漂浮物（该缺陷需记入检测记录表，不参与计算）。'),
(9,'JG（结垢）','管道内壁上的附着物。'),
(10,'PL（破裂）','管道的外部压力超过自身的承受力致使管子发生破裂。其形式有纵向、环向和复合3种。'),
(11,'QF（起伏）','接口位置偏移，管道竖向位置发生变化，在低处形成洼水。'),
(12,'SG（树根）','单根树根或是树根群自然生长进入管道。'),
(13,'SL（渗漏）','管外的水流入管道。'),
(14,'TJ（脱节）','两根管道的端部未充分接合或接口脱离。'),
(15,'TL（接口材料脱落）','橡胶圈、沥青、水泥等类似的接口材料进入管道。'),
(16,'ZW（障碍物）','管道内影响过流的阻挡物。');

/*Table structure for table `detection` */

DROP TABLE IF EXISTS `detection`;

CREATE TABLE `detection` (
  `detection_id` int(11) NOT NULL COMMENT '检测类型编号',
  `detection_method` varchar(100) DEFAULT NULL COMMENT '检测类型名称',
  PRIMARY KEY (`detection_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `detection` */

insert  into `detection`(`detection_id`,`detection_method`) values 
(1,'常规见证检验'),
(2,'常规检验'),
(3,'抽样检验'),
(4,'委托检验'),
(5,'其它');

/*Table structure for table `drainage` */

DROP TABLE IF EXISTS `drainage`;

CREATE TABLE `drainage` (
  `drainage_id` int(11) NOT NULL COMMENT '排水方式编号',
  `drainage_method` varchar(100) DEFAULT NULL COMMENT '排水方式名称',
  PRIMARY KEY (`drainage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `drainage` */

insert  into `drainage`(`drainage_id`,`drainage_method`) values 
(1,'无'),
(2,'临排管'),
(3,'水泵临时抽水'),
(4,'其它');

/*Table structure for table `dredging` */

DROP TABLE IF EXISTS `dredging`;

CREATE TABLE `dredging` (
  `dredging_id` int(11) NOT NULL COMMENT '清疏方式编号',
  `dredging_method` varchar(100) DEFAULT NULL COMMENT '清疏方式名称',
  PRIMARY KEY (`dredging_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `dredging` */

insert  into `dredging`(`dredging_id`,`dredging_method`) values 
(1,'无'),
(2,'高压水枪'),
(3,'高压疏通车'),
(4,'其它');

/*Table structure for table `joint_form` */

DROP TABLE IF EXISTS `joint_form`;

CREATE TABLE `joint_form` (
  `joint_form_id` int(11) NOT NULL COMMENT '接口形式id',
  `joint_form` varchar(100) DEFAULT NULL COMMENT '接口形式',
  PRIMARY KEY (`joint_form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `joint_form` */

insert  into `joint_form`(`joint_form_id`,`joint_form`) values 
(1,'橡胶圈接口'),
(2,'承插橡胶圈接口'),
(3,'套筒橡胶圈接口'),
(4,'电热熔带接口'),
(5,'热收缩带接口'),
(6,'现浇混凝土套环接口'),
(7,'现浇混凝土套环柔性接口'),
(8,'钢丝网水泥砂浆抹带接口');

/*Table structure for table `manhole` */

DROP TABLE IF EXISTS `manhole`;

CREATE TABLE `manhole` (
  `manhole_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '井id',
  `manhole_no` varchar(100) DEFAULT NULL COMMENT '井编号',
  `manhole_type_id` int(11) DEFAULT '1' COMMENT '井类型id',
  `manhole_material_id` int(11) DEFAULT '1' COMMENT '井材料id',
  `manhole_cover_id` int(11) DEFAULT '1' COMMENT '井盖id',
  `manhole_construction_year` date DEFAULT NULL COMMENT '井年代',
  `manhole_longitude` float DEFAULT NULL COMMENT '井经度坐标',
  `manhole_latitude` float DEFAULT NULL COMMENT '井纬度坐标',
  `internal_defect` varchar(100) DEFAULT NULL COMMENT '井内部缺陷',
  `external_defect` varchar(100) DEFAULT NULL COMMENT '井外部缺陷',
  `pipe_invert` float DEFAULT NULL,
  `pipe_elevation` float DEFAULT NULL COMMENT '管道高程',
  PRIMARY KEY (`manhole_id`),
  KEY `manhole_cover_id_fk` (`manhole_cover_id`),
  KEY `manhole_material _id_fk` (`manhole_material_id`),
  KEY `manhole_type_id_fk` (`manhole_type_id`),
  CONSTRAINT `manhole_cover_id_fk` FOREIGN KEY (`manhole_cover_id`) REFERENCES `manhole_cover` (`manhole_cover_id`) ON DELETE CASCADE,
  CONSTRAINT `manhole_material _id_fk` FOREIGN KEY (`manhole_material_id`) REFERENCES `manhole_material` (`manhole_material_id`) ON DELETE CASCADE,
  CONSTRAINT `manhole_type_id_fk` FOREIGN KEY (`manhole_type_id`) REFERENCES `manhole_type` (`manhole_type_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;

/*Data for the table `manhole` */

insert  into `manhole`(`manhole_id`,`manhole_no`,`manhole_type_id`,`manhole_material_id`,`manhole_cover_id`,`manhole_construction_year`,`manhole_longitude`,`manhole_latitude`,`internal_defect`,`external_defect`,`pipe_invert`,`pipe_elevation`) values 
(18,'w123',2,3,2,'2020-01-08',123,22.3,'内部缺陷','外部缺陷',11,21),
(19,'w125',1,1,1,'2020-01-09',11,12.4,'内部缺陷','外部缺陷',1,2),
(54,'w2',4,2,2,NULL,8,2,'没有','也没有',NULL,12),
(55,'w4',3,2,2,NULL,-3,9,'有吗','没有',NULL,1),
(60,'',1,1,1,NULL,0,0,'','',NULL,0),
(61,'',1,1,1,NULL,0,0,'','',NULL,0);

/*Table structure for table `manhole_cover` */

DROP TABLE IF EXISTS `manhole_cover`;

CREATE TABLE `manhole_cover` (
  `manhole_cover_id` int(11) NOT NULL COMMENT '井盖材料类型id',
  `manhole_cover_type` varchar(100) DEFAULT NULL COMMENT '井盖材料类型',
  PRIMARY KEY (`manhole_cover_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `manhole_cover` */

insert  into `manhole_cover`(`manhole_cover_id`,`manhole_cover_type`) values 
(1,'铸铁'),
(2,'钢筋混凝土'),
(3,'塑料');

/*Table structure for table `manhole_material` */

DROP TABLE IF EXISTS `manhole_material`;

CREATE TABLE `manhole_material` (
  `manhole_material_id` int(11) NOT NULL COMMENT '井材料类型id',
  `manhole_material_type` varchar(100) DEFAULT NULL COMMENT '井材料类型',
  PRIMARY KEY (`manhole_material_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `manhole_material` */

insert  into `manhole_material`(`manhole_material_id`,`manhole_material_type`) values 
(1,'砖砌'),
(2,'塑料'),
(3,'钢筋混凝土');

/*Table structure for table `manhole_type` */

DROP TABLE IF EXISTS `manhole_type`;

CREATE TABLE `manhole_type` (
  `manhole_type_id` int(11) NOT NULL COMMENT '井类型id',
  `manhole_type` varchar(100) DEFAULT NULL COMMENT '井类型',
  PRIMARY KEY (`manhole_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `manhole_type` */

insert  into `manhole_type`(`manhole_type_id`,`manhole_type`) values 
(1,'雨水口'),
(2,'检查井'),
(3,'连接暗井'),
(4,'溢流井'),
(5,'跌水井'),
(6,'水封井'),
(7,'冲洗井'),
(8,'沉泥井'),
(9,'闸门井'),
(10,'潮门井'),
(11,'倒虹管'),
(12,'其它');

/*Table structure for table `move` */

DROP TABLE IF EXISTS `move`;

CREATE TABLE `move` (
  `move_id` int(11) NOT NULL COMMENT '移动方式编号',
  `move_method` varchar(100) DEFAULT NULL COMMENT '移动方式名称',
  PRIMARY KEY (`move_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `move` */

insert  into `move`(`move_id`,`move_method`) values 
(1,'人工牵引'),
(2,'漂浮筏顺流'),
(3,'爬行器自走'),
(4,'其它');

/*Table structure for table `pipe_material` */

DROP TABLE IF EXISTS `pipe_material`;

CREATE TABLE `pipe_material` (
  `pipe_material_id` int(11) NOT NULL COMMENT '管段材质id',
  `pipe_material` varchar(100) DEFAULT NULL COMMENT '管段材质',
  PRIMARY KEY (`pipe_material_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `pipe_material` */

insert  into `pipe_material`(`pipe_material_id`,`pipe_material`) values 
(1,'砖砌'),
(2,'塑料'),
(3,'钢筋混凝土');

/*Table structure for table `pipe_type` */

DROP TABLE IF EXISTS `pipe_type`;

CREATE TABLE `pipe_type` (
  `pipe_type_id` int(11) NOT NULL COMMENT '管段类型id',
  `pipe_type` varchar(100) DEFAULT NULL COMMENT '管段类型',
  PRIMARY KEY (`pipe_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `pipe_type` */

insert  into `pipe_type`(`pipe_type_id`,`pipe_type`) values 
(1,'雨水管道'),
(2,'污水管道'),
(3,'雨污合流管道');

/*Table structure for table `plugging` */

DROP TABLE IF EXISTS `plugging`;

CREATE TABLE `plugging` (
  `plugging_id` int(11) NOT NULL COMMENT '封堵方式编号',
  `plugging_method` varchar(100) DEFAULT NULL COMMENT '封堵方式名称',
  PRIMARY KEY (`plugging_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `plugging` */

insert  into `plugging`(`plugging_id`,`plugging_method`) values 
(1,'无'),
(2,'气囊封堵'),
(3,'砖砌堵头'),
(4,'气囊加砖砌堵头'),
(5,'其它');

/*Table structure for table `project` */

DROP TABLE IF EXISTS `project`;

CREATE TABLE `project` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '工程id',
  `project_no` varchar(100) DEFAULT NULL COMMENT '工程编号',
  `project_name` varchar(100) DEFAULT NULL COMMENT '工程名称',
  `project_address` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '工程地址',
  `staff_id` int(11) DEFAULT NULL COMMENT '负责人id',
  `start_date` date DEFAULT NULL COMMENT '开工日期',
  `report_no` varchar(100) DEFAULT NULL COMMENT '报告编号',
  `requester_unit` varchar(100) DEFAULT NULL COMMENT '委托单位',
  `construction_unit` varchar(100) DEFAULT NULL COMMENT '建设单位',
  `design_unit` varchar(100) DEFAULT NULL COMMENT '设计单位',
  `build_unit` varchar(100) DEFAULT NULL COMMENT '施工单位',
  `supervisory_unit` varchar(100) DEFAULT NULL COMMENT '监理单位',
  `detection_id` int(11) DEFAULT NULL COMMENT '检测类型',
  `move_id` int(11) DEFAULT NULL COMMENT '移动方式',
  `plugging_id` int(11) DEFAULT NULL COMMENT '封堵方式',
  `drainage_id` int(11) DEFAULT NULL COMMENT '排水方式',
  `dredging_id` int(11) DEFAULT NULL COMMENT '清疏方式',
  `detecetion_equipment` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '检测设备',
  PRIMARY KEY (`project_id`),
  KEY `detection_id_fk` (`detection_id`),
  KEY `move_id_fk` (`move_id`),
  KEY `plugging_id_fk` (`plugging_id`),
  KEY `drainage_id_fk` (`drainage_id`),
  KEY `dredging_id_fk` (`dredging_id`),
  KEY `staff_id_fk` (`staff_id`),
  CONSTRAINT `detection_id_fk` FOREIGN KEY (`detection_id`) REFERENCES `detection` (`detection_id`),
  CONSTRAINT `drainage_id_fk` FOREIGN KEY (`drainage_id`) REFERENCES `drainage` (`drainage_id`),
  CONSTRAINT `dredging_id_fk` FOREIGN KEY (`dredging_id`) REFERENCES `dredging` (`dredging_id`),
  CONSTRAINT `move_id_fk` FOREIGN KEY (`move_id`) REFERENCES `move` (`move_id`),
  CONSTRAINT `plugging_id_fk` FOREIGN KEY (`plugging_id`) REFERENCES `plugging` (`plugging_id`),
  CONSTRAINT `staff_id_fk` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

/*Data for the table `project` */

insert  into `project`(`project_id`,`project_no`,`project_name`,`project_address`,`staff_id`,`start_date`,`report_no`,`requester_unit`,`construction_unit`,`design_unit`,`build_unit`,`supervisory_unit`,`detection_id`,`move_id`,`plugging_id`,`drainage_id`,`dredging_id`,`detecetion_equipment`) values 
(13,'工程编号','工程名臣','工程地址',102,'2020-01-07','报告编号','这是委托单位','这是建设单位','这是设计单位','这是施工单位','这是监理单位',1,2,2,2,2,NULL),
(14,'1','1','1',101,'2020-01-13','','','','','','',1,1,1,1,1,NULL);

/*Table structure for table `project_video` */

DROP TABLE IF EXISTS `project_video`;

CREATE TABLE `project_video` (
  `project_id` int(11) NOT NULL COMMENT '工程Id',
  `video_id` int(11) NOT NULL COMMENT '视频id',
  PRIMARY KEY (`project_id`,`video_id`),
  KEY `video_id_fk1` (`video_id`),
  CONSTRAINT `project_id_fk1` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE,
  CONSTRAINT `video_id_fk1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `project_video` */

insert  into `project_video`(`project_id`,`video_id`) values 
(13,35),
(13,53),
(13,56);

/*Table structure for table `regional` */

DROP TABLE IF EXISTS `regional`;

CREATE TABLE `regional` (
  `regional_id` int(11) NOT NULL COMMENT '地区重要性id',
  `regional_info` varchar(100) DEFAULT NULL COMMENT '地区重要性内容',
  `regional_value` int(11) DEFAULT NULL COMMENT '地区重要性数值',
  PRIMARY KEY (`regional_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `regional` */

insert  into `regional`(`regional_id`,`regional_info`,`regional_value`) values 
(1,'中心商业、附近具有甲类民用建筑工程的区域',10),
(2,'交通干道、附近具有乙类民用建筑工程的区域',6),
(3,'其他行车道路、附近具有丙类民用建筑工程的区域',3),
(4,'所有其他区域或 F<4 时',0);

/*Table structure for table `section_shape` */

DROP TABLE IF EXISTS `section_shape`;

CREATE TABLE `section_shape` (
  `section_shape_id` int(11) NOT NULL COMMENT '截面形状id',
  `section_shape` varchar(100) DEFAULT NULL COMMENT '截面形状',
  PRIMARY KEY (`section_shape_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `section_shape` */

insert  into `section_shape`(`section_shape_id`,`section_shape`) values 
(1,'圆形'),
(2,'矩形'),
(3,'椭圆形');

/*Table structure for table `soil` */

DROP TABLE IF EXISTS `soil`;

CREATE TABLE `soil` (
  `soil_id` int(11) NOT NULL COMMENT '土质影响id',
  `soil_info` varchar(100) DEFAULT NULL COMMENT '土质影响信息',
  `soil_value` int(11) DEFAULT NULL COMMENT '土质影响数值',
  PRIMARY KEY (`soil_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `soil` */

insert  into `soil`(`soil_id`,`soil_info`,`soil_value`) values 
(1,'一般土层或 F=0',0),
(2,'Ⅰ级湿陷性黄土、Ⅱ级湿陷性黄土、弱膨胀土',6),
(3,'Ⅲ级湿陷性黄土、中膨胀土、淤泥质土、红黏土',8),
(4,'粉砂层、Ⅳ级湿陷性黄土、强膨胀土、淤泥',10);

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '人员id',
  `staff_name` varchar(100) DEFAULT NULL COMMENT '人员姓名',
  `staff_category` int(11) DEFAULT NULL COMMENT '人员类别',
  PRIMARY KEY (`staff_id`),
  CONSTRAINT `staff_category_value` CHECK ((`staff_category` in (0,1,2)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `staff` */

insert  into `staff`(`staff_id`,`staff_name`,`staff_category`) values 
(101,'林彪',0),
(102,'罗荣桓',0);

/*Table structure for table `video` */

DROP TABLE IF EXISTS `video`;

CREATE TABLE `video` (
  `video_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '视频id',
  `staff_id` int(11) DEFAULT NULL COMMENT '检测人员',
  `record_date` datetime DEFAULT NULL COMMENT '检测日期/录制日期',
  `road_name` varchar(100) DEFAULT NULL COMMENT '道路名称',
  `start_manhole_id` int(11) DEFAULT '1' COMMENT '起始井id',
  `end_manhole_id` int(11) DEFAULT NULL COMMENT '结束井id',
  `pipe_type_id` int(11) DEFAULT '1' COMMENT '管道类型',
  `section_shape_id` int(11) DEFAULT '1' COMMENT '截面形状',
  `joint_form_id` int(11) DEFAULT '1' COMMENT '接口形式',
  `pipe_material_id` int(11) DEFAULT '1' COMMENT '管道材质',
  `pipe_diameter` float DEFAULT '0' COMMENT '管道直径（mm）',
  `start_pipe_depth` float DEFAULT '0' COMMENT '起点埋深（m）',
  `end_pipe_depth` float DEFAULT '0' COMMENT '终点埋深（m）',
  `pipe_length` float DEFAULT '0' COMMENT '管道长度（m）',
  `detection_length` float DEFAULT '0' COMMENT '检测长度（m）',
  `detection_direction` int(11) DEFAULT '1' COMMENT '检测方向，0-顺流，1-逆流',
  `construction_year` date DEFAULT NULL COMMENT '敷设年代',
  `regional_importance_id` int(11) DEFAULT '1' COMMENT '地区重要性',
  `soil_id` int(11) DEFAULT '1' COMMENT '土质影响',
  `video_remark` varchar(100) DEFAULT NULL COMMENT '备注信息',
  `video_name` varchar(100) DEFAULT NULL COMMENT '视频文件名',
  `import_date` datetime DEFAULT NULL COMMENT '导入日期',
  PRIMARY KEY (`video_id`),
  KEY `pipe_type_id_fk` (`pipe_type_id`),
  KEY `section_shape_id_fk` (`section_shape_id`),
  KEY `joint_form_id_fk` (`joint_form_id`),
  KEY `pipe_material_id_fk` (`pipe_material_id`),
  KEY `regional importance_id_fk` (`regional_importance_id`),
  KEY `soil_id_fk` (`soil_id`),
  KEY `video_staff_id_fk` (`staff_id`),
  KEY `end_manhole_id_fk` (`end_manhole_id`),
  KEY `start_manhole_id_fk` (`start_manhole_id`),
  CONSTRAINT `end_manhole_id_fk` FOREIGN KEY (`end_manhole_id`) REFERENCES `manhole` (`manhole_id`) ON DELETE CASCADE,
  CONSTRAINT `joint_form_id_fk` FOREIGN KEY (`joint_form_id`) REFERENCES `joint_form` (`joint_form_id`),
  CONSTRAINT `pipe_material_id_fk` FOREIGN KEY (`pipe_material_id`) REFERENCES `pipe_material` (`pipe_material_id`),
  CONSTRAINT `pipe_type_id_fk` FOREIGN KEY (`pipe_type_id`) REFERENCES `pipe_type` (`pipe_type_id`),
  CONSTRAINT `regional importance_id_fk` FOREIGN KEY (`regional_importance_id`) REFERENCES `regional` (`regional_id`),
  CONSTRAINT `section_shape_id_fk` FOREIGN KEY (`section_shape_id`) REFERENCES `section_shape` (`section_shape_id`),
  CONSTRAINT `soil_id_fk` FOREIGN KEY (`soil_id`) REFERENCES `soil` (`soil_id`),
  CONSTRAINT `start_manhole_id_fk` FOREIGN KEY (`start_manhole_id`) REFERENCES `manhole` (`manhole_id`) ON DELETE CASCADE,
  CONSTRAINT `video_staff_id_fk` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`),
  CONSTRAINT `detection_direction_check` CHECK ((`detection_direction` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

/*Data for the table `video` */

insert  into `video`(`video_id`,`staff_id`,`record_date`,`road_name`,`start_manhole_id`,`end_manhole_id`,`pipe_type_id`,`section_shape_id`,`joint_form_id`,`pipe_material_id`,`pipe_diameter`,`start_pipe_depth`,`end_pipe_depth`,`pipe_length`,`detection_length`,`detection_direction`,`construction_year`,`regional_importance_id`,`soil_id`,`video_remark`,`video_name`,`import_date`) values 
(35,102,'2019-05-24 17:20:20','长安街',18,19,1,3,2,1,15,23,32,99.99,99,1,'2020-01-09',1,2,'备注信息','F:/Graduation-Project/排水管道系统/PipeSight/Videos/czz3isohmpn.mp4','2020-01-07 14:05:06'),
(53,102,'2019-05-26 18:45:56','一号路',54,55,2,1,5,1,7,2,3,20,10,1,'2019-12-31',2,1,'没有啊','F:/Graduation-Project/排水管道系统/PipeSight/Videos/a4gptz2rl45.mp4','2020-01-13 10:19:28'),
(56,102,'2020-02-24 13:56:27','abnormal',60,61,1,1,1,1,0,0,0,0,0,1,'2020-02-24',1,1,'','F:/Graduation-Project/排水管道系统/PipeSight/Videos/abnormal.mp4','2020-02-24 13:57:28');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

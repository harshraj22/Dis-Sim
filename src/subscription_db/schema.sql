DROP DATABASE IF EXISTS `DB`;
CREATE DATABASE `DB`;
USE `DB`;

DROP TABLE IF EXISTS `subscription`;
CREATE TABLE `subscription` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `subscription_tier` varchar(10) NOT NULL,
  `request_limit` int NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
alter table `subscription` add constraint ck_subscription_tier 
   check (subscription_tier in ('Free', 'Basic', 'Advanced'));
INSERT INTO `subscription` VALUES 
(1, 'test', 'Free', 2), (2, 'premium', 'Advanced', 200);
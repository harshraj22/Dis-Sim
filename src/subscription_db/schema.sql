DROP DATABASE IF EXISTS `DB`;
CREATE DATABASE `DB`;
USE `DB`;

DROP TABLE IF EXISTS `subscription`;
CREATE TABLE `subscription` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `subscription_tier` varchar(10) NOT NULL UNIQUE,
  `request_limit` int NOT NULL, -- Number of allowed requests per minute
  `retention_period` int NOT NULL, -- Number of days the result should be stored in the backend
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `auth`;
CREATE TABLE auth (
  `username` VARCHAR(20) PRIMARY KEY,
  `password` VARCHAR(80) NOT NULL,
  `subscription_tier` varchar(10) NOT NULL,
  FOREIGN KEY (`subscription_tier`) REFERENCES `subscription`(`subscription_tier`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- alter table `subscription` add constraint ck_subscription_tier 
--    check (subscription_tier in ('Free', 'Basic', 'Advanced'));
-- INSERT INTO `subscription` VALUES 
-- (1, 'test', 'Free', 2), (2, 'premium', 'Advanced', 200);
INSERT INTO `subscription` (`subscription_tier`, `request_limit`, `retention_period`) 
VALUES 
    ('Free', 10, 1),
    ('Basic', 100, 15),
    ('Advanced', 1000, 60);

INSERT INTO `auth` (`username`, `password`, `subscription_tier`) 
VALUES 
('free_user', '$2b$12$Zyc0kpMpoqAefW9GHzotku4zxqru.2ihF.xdfuzAc6LmiRTURzcbm', 'Free'), -- password: 'free'
('basic_user', '$2b$12$GdyyqYJ0PumKjP3RmEJJceD78xbAvoAXLS5i70kHFmelbei8x9ddG', 'Basic'), -- password: 'basic'
('advanced_user', '$2b$12$bjNu058XT2R0dEgUi0Usn.hw4xbeahN/lmM1w3t3W8pLV9r70MXxu', 'Advanced'), -- password: 'advanced'
('test', '$2b$12$1w6qLVssMOpw4vFoVerFQunrZnlQT1YZUW7.sErHVXSSGJPtvEvte', 'Advanced'); -- password: 'test'


CREATE VIEW `subscription_details` AS SELECT a.username, s.subscription_tier, s.request_limit, s.retention_period FROM auth a INNER JOIN subscription s ON a.subscription_tier = s.subscription_tier;
-- phpMyAdmin SQL Dump
-- version 4.0.10.20
-- https://www.phpmyadmin.net
--
-- ホスト: mysql594.phy.lolipop.lan
-- 生成日時: 2026 年 2 月 14 日 23:27
-- サーバのバージョン: 5.1.73-community-log
-- PHP のバージョン: 5.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- データベース: `LAA0291032-snakefish`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `t_access_log`
--

CREATE TABLE IF NOT EXISTS `t_access_log` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `AS_OF_DATE` date NOT NULL COMMENT '基準日',
  `PATH` varchar(100) NOT NULL COMMENT 'アクセスパス',
  `IP` varchar(20) NOT NULL COMMENT 'IPアドレス',
  `USER_AGENT` varchar(500) NOT NULL COMMENT 'ユーザーエージェント',
  `CREATED_AT` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '作成日',
  PRIMARY KEY (`ID`),
  KEY `PATH` (`PATH`),
  KEY `AS_OF_DATE` (`AS_OF_DATE`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='アクセスログ' AUTO_INCREMENT=2 ;


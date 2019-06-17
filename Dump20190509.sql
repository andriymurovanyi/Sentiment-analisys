-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: sentimentmodel
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chat`
--

DROP TABLE IF EXISTS `chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `chat` (
  `idChat` int(10) NOT NULL AUTO_INCREMENT,
  `chat_name` varchar(45) NOT NULL,
  `chat_type` varchar(45) NOT NULL,
  `chat_id` bigint(20) NOT NULL,
  PRIMARY KEY (`idChat`),
  UNIQUE KEY `chat_id_UNIQUE` (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feature`
--

DROP TABLE IF EXISTS `feature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `feature` (
  `idFeature` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8_bin NOT NULL,
  `description` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`idFeature`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feature_and_message`
--

DROP TABLE IF EXISTS `feature_and_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `feature_and_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idMessage` int(11) NOT NULL,
  `idFeature` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_message_idx` (`idMessage`),
  KEY `fk_feature_idx` (`idFeature`),
  CONSTRAINT `fk_feature` FOREIGN KEY (`idFeature`) REFERENCES `feature` (`idfeature`) ON UPDATE CASCADE,
  CONSTRAINT `fk_message` FOREIGN KEY (`idMessage`) REFERENCES `message` (`idmessage`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `message` (
  `idMessage` int(10) NOT NULL AUTO_INCREMENT,
  `sender` varchar(45) NOT NULL,
  `sender_id` bigint(20) NOT NULL,
  `m_date` date NOT NULL,
  `m_time` time NOT NULL,
  `text` text,
  `idChat` int(10) NOT NULL,
  PRIMARY KEY (`idMessage`),
  KEY `fk_message_chat_idx` (`idChat`),
  CONSTRAINT `fk_message_chat` FOREIGN KEY (`idChat`) REFERENCES `chat` (`idchat`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36723 DEFAULT CHARSET=utf8 MAX_ROWS=2000;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `message_and_word`
--

DROP TABLE IF EXISTS `message_and_word`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `message_and_word` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idMessage` int(11) NOT NULL,
  `idWord` int(11) NOT NULL,
  `pos_tag` varchar(45) COLLATE utf8_bin NOT NULL,
  `position` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_message_idx` (`idMessage`),
  KEY `fk_word_idx` (`idWord`),
  CONSTRAINT `fk_message_w` FOREIGN KEY (`idMessage`) REFERENCES `message` (`idmessage`) ON UPDATE CASCADE,
  CONSTRAINT `fk_word_w` FOREIGN KEY (`idWord`) REFERENCES `word` (`idword`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `result` (
  `idResult` int(11) NOT NULL AUTO_INCREMENT,
  `polarity` double NOT NULL,
  `subjectivity` double NOT NULL,
  `idMessage` int(11) NOT NULL,
  PRIMARY KEY (`idResult`),
  UNIQUE KEY `idMessage_UNIQUE` (`idMessage`),
  KEY `fk_result_message_idx` (`idMessage`),
  CONSTRAINT `fk_result_message` FOREIGN KEY (`idMessage`) REFERENCES `message` (`idmessage`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `word`
--

DROP TABLE IF EXISTS `word`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `word` (
  `idWord` int(11) NOT NULL AUTO_INCREMENT,
  `word_text` varchar(45) COLLATE utf8_bin NOT NULL,
  `lemma` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`idWord`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-09 20:14:43

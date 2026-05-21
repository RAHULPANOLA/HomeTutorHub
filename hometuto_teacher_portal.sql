/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: hometuto_teacher_portal
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-cll-lve

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`id`, `full_name`, `email`, `password`, `created_at`) VALUES (1,'Admin','admin@gmail.com','scrypt:32768:8:1$tjmt5JnaVRkG4TIr$ab19d9bf9758624993f35dc55b83ecb60ba34e06100e660499d07a8c8ad415b373acc48c07278a44c1736c0bf42bd5d2e05640cda413b68545835c6e6969b21c','2026-03-08 12:59:10');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `category` enum('email','class_update','promotional','general') DEFAULT 'general',
  `target_audience` enum('all','teachers','students') DEFAULT 'all',
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `admin` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` (`id`, `title`, `content`, `category`, `target_audience`, `created_by`, `created_at`) VALUES (1,'Welcome note','Welcome to home tutor hub','general','students',1,'2026-05-08 18:51:18');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demo_sessions`
--

DROP TABLE IF EXISTS `demo_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `request_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `demo_date` datetime NOT NULL,
  `demo_mode` enum('home','online','center') DEFAULT 'home',
  `status` enum('scheduled','completed','cancelled','rescheduled') DEFAULT 'scheduled',
  `feedback` text DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_sessions`
--

LOCK TABLES `demo_sessions` WRITE;
/*!40000 ALTER TABLE `demo_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `demo_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faqs`
--

DROP TABLE IF EXISTS `faqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `faqs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `category` varchar(50) DEFAULT 'general',
  `display_order` int(11) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faqs`
--

LOCK TABLES `faqs` WRITE;
/*!40000 ALTER TABLE `faqs` DISABLE KEYS */;
/*!40000 ALTER TABLE `faqs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `featured_tutors`
--

DROP TABLE IF EXISTS `featured_tutors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `featured_tutors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `display_order` int(11) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_featured` (`teacher_id`),
  CONSTRAINT `featured_tutors_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `featured_tutors`
--

LOCK TABLES `featured_tutors` WRITE;
/*!40000 ALTER TABLE `featured_tutors` DISABLE KEYS */;
/*!40000 ALTER TABLE `featured_tutors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_type` enum('student','teacher') NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 and `rating` <= 5),
  `title` varchar(200) DEFAULT NULL,
  `description` text NOT NULL,
  `is_featured` tinyint(1) DEFAULT 0,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `admin_note` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_featured` (`is_featured`),
  KEY `idx_user` (`user_id`,`user_type`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` (`id`, `user_id`, `user_type`, `user_name`, `rating`, `title`, `description`, `is_featured`, `status`, `admin_note`, `created_at`, `updated_at`) VALUES (1,9,'student','Rahul Panola',5,'Great experience with my python teacher','it is very use full for student and teachers',0,'approved','','2026-05-10 09:06:23','2026-05-10 17:39:50');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_articles`
--

DROP TABLE IF EXISTS `help_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `help_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `category` enum('student','teacher','general') DEFAULT 'general',
  `step_order` int(11) DEFAULT 0,
  `icon` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_articles`
--

LOCK TABLES `help_articles` WRITE;
/*!40000 ALTER TABLE `help_articles` DISABLE KEYS */;
INSERT INTO `help_articles` (`id`, `title`, `content`, `category`, `step_order`, `icon`, `is_active`, `created_at`) VALUES (1,'How to Register as a Student','<div class=\"step-item\"><strong>Step 1:</strong> Click on \"Sign In\" button in the top right corner.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Click on \"Join as Student\" button.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Fill in your personal details (Name, Email, Password, Phone).</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Enter your academic details (City, Qualification, Specialization).</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Set up a security question for password recovery.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Click \"Register & Claim 50 Points\" to complete registration.</div>\r\n<div class=\"step-item highlight\">[BONUS] You get 49 bonus points on registration!</div>','student',1,'fa-user-plus',1,'2026-05-10 15:01:46'),
(2,'How to Find and Unlock a Tutor','<div class=\"step-item\"><strong>Step 1:</strong> Login to your student account.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Go to \"Find a Tutor\" page from the navigation menu.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Use the search filters (Subject, City, Mode) to find tutors.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Browse through the tutor cards showing experience, fees, and subjects.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Click \"Unlock Contact (49 pts)\" button on your preferred tutor.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Confirm the transaction in the popup.</div>\r\n<div class=\"step-item\"><strong>Step 7:</strong> Once unlocked, you will see the tutor\'s email and phone number.</div>\r\n<div class=\"step-item\"><strong>Step 8:</strong> Contact the tutor directly to schedule sessions.</div>','student',2,'fa-chalkboard-user',1,'2026-05-10 15:01:46'),
(3,'How to Buy Points','<div class=\"step-item\"><strong>Step 1:</strong> Click on the \"Add Points\" button next to your wallet balance.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Select a package (100 pts for Rs.99, 500 pts for Rs.449, or 1000 pts for Rs.799).</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Or enter a custom amount (minimum Rs.10).</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Click \"Proceed to Payment\".</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Complete payment using Razorpay (Cards, UPI, Netbanking).</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Points will be added instantly to your wallet.</div>','student',3,'fa-indian-rupee-sign',1,'2026-05-10 15:01:46'),
(4,'How to Post a Tuition Request','<div class=\"step-item\"><strong>Step 1:</strong> Click on your profile avatar in the top right.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Select \"Post Tuition Request\" from the dropdown menu.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Fill in the subject you need help with.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Select preferred mode (Online/Offline/Both).</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Add location, class/grade, and preferred timing.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Add any additional description (optional).</div>\r\n<div class=\"step-item\"><strong>Step 7:</strong> Click \"Post Request\" to submit.</div>\r\n<div class=\"step-item highlight\">[NOTE] Teachers will see your request and can contact you!</div>','student',4,'fa-pen-alt',1,'2026-05-10 15:01:46'),
(5,'How to Request an Offline Home Tutor','<div class=\"step-item\"><strong>Step 1:</strong> Login to your student account.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Click on the \"Offline Request\" button in the top bar.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Your profile information will be auto-filled.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Enter your complete address.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Fill in subject, class, preferred timing, and budget.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Submit the request.</div>\r\n<div class=\"step-item\"><strong>Step 7:</strong> Admin will review and assign a suitable teacher.</div>\r\n<div class=\"step-item\"><strong>Step 8:</strong> You will be contacted for a free demo session.</div>','student',5,'fa-home',1,'2026-05-10 15:01:46'),
(6,'How to Give Feedback','<div class=\"step-item\"><strong>Step 1:</strong> Click on your profile avatar.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Select \"Give Feedback\" from the dropdown.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Rate your experience (1-5 stars).</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Write your feedback or suggestion.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Click \"Submit Feedback\".</div>\r\n<div class=\"step-item highlight\">Your feedback helps us improve our services!</div>','student',6,'fa-star',1,'2026-05-10 15:01:46'),
(7,'How to Change Password','<div class=\"step-item\"><strong>Step 1:</strong> Click on your profile avatar in the top right.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Select \"Change Password\" from the dropdown.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Enter your current password.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Enter your new password.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Confirm the new password.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Click \"Update Password\".</div>','student',7,'fa-key',1,'2026-05-10 15:01:46'),
(8,'How to Register as a Teacher','<div class=\"step-item\"><strong>Step 1:</strong> Click on \"Sign In\" button.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Click on \"Join as Tutor\" button.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Fill in your personal details (Name, Email, Password, Phone).</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Upload your profile photo and resume.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Fill in your qualification and experience.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Add subjects you teach, classes, and boards.</div>\r\n<div class=\"step-item\"><strong>Step 7:</strong> Set your preferred teaching mode and fees (monthly/hourly).</div>\r\n<div class=\"step-item\"><strong>Step 8:</strong> Submit registration for admin verification.</div>\r\n<div class=\"step-item highlight\">[NOTE] Admin will verify your profile within 24 hours.</div>','teacher',1,'fa-user-graduate',1,'2026-05-10 15:01:46'),
(9,'How to Find Students and Tuition Requests','<div class=\"step-item\"><strong>Step 1:</strong> Login to your teacher dashboard.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Go to the \"Tuition Requests\" tab.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Use filters (Subject, Location, Class) to find relevant requests.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Review student requirements and preferences.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Click \"Unlock Contact (49 pts)\" on requests you want to respond to.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Contact the student via phone or email.</div>','teacher',2,'fa-users',1,'2026-05-10 15:01:46'),
(10,'How to Update Your Profile','<div class=\"step-item\"><strong>Step 1:</strong> Go to your teacher dashboard.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Click on \"Edit Profile\" button near your name.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Update your phone number, city, qualification, or experience.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Update subjects you teach.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Change your profile photo or resume.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Click \"Save Changes\" to update.</div>','teacher',3,'fa-edit',1,'2026-05-10 15:01:46'),
(11,'How to Set Offline Teaching Availability','<div class=\"step-item\"><strong>Step 1:</strong> Scroll down to \"Offline Teaching Availability\" section on dashboard.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Enter your preferred teaching area.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Set maximum distance you can travel (km).</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Check \"Available for Offline Classes\".</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Click \"Update Availability\".</div>\r\n<div class=\"step-item highlight\">Admin will assign offline requests based on your availability.</div>','teacher',4,'fa-location-dot',1,'2026-05-10 15:01:46'),
(12,'How to Earn and Use Points','<div class=\"step-item\"><strong>Step 1:</strong> Points are earned when students unlock your contact (49 points).</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Teachers receive 49 points on registration.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> View your point balance in the \"My Points\" section.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Use points to unlock student tuition requests (49 pts per unlock).</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Buy more points if needed using \"Add Points\" button.</div>','teacher',5,'fa-coins',1,'2026-05-10 15:01:46'),
(13,'How to Close Completed Requests','<div class=\"step-item\"><strong>Step 1:</strong> Go to \"Offline Requests\" section in admin panel (for admin).</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Select the completed request.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Click \"Mark as Completed\".</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Student will be notified.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> The request will move to completed section.</div>','teacher',6,'fa-check-circle',1,'2026-05-10 15:01:46'),
(14,'How to Give Feedback as Teacher','<div class=\"step-item\"><strong>Step 1:</strong> Click on your profile avatar.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Select \"Give Feedback\".</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Rate your experience.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Share your suggestions.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Submit feedback.</div>','teacher',7,'fa-star',1,'2026-05-10 15:01:46'),
(24,'How to Update Your Profile','<div class=\"step-item\"><strong>Step 1:</strong> Go to your teacher dashboard.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Click on \"Edit Profile\" button near your name.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Update your phone number, city, qualification, or experience.</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Update subjects you teach.</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Change your profile photo or resume.</div>\r\n<div class=\"step-item\"><strong>Step 6:</strong> Click \"Save Changes\" to update.</div>','teacher',3,'fa-edit',1,'2026-05-10 15:05:41'),
(25,'How to Set Offline Teaching Availability','<div class=\"step-item\"><strong>Step 1:</strong> Scroll down to \"Offline Teaching Availability\" section on dashboard.</div>\r\n<div class=\"step-item\"><strong>Step 2:</strong> Enter your preferred teaching area.</div>\r\n<div class=\"step-item\"><strong>Step 3:</strong> Set maximum distance you can travel (km).</div>\r\n<div class=\"step-item\"><strong>Step 4:</strong> Check \"Available for Offline Classes\".</div>\r\n<div class=\"step-item\"><strong>Step 5:</strong> Click \"Update Availability\".</div>\r\n<div class=\"step-item highlight\">Admin will assign offline requests based on your availability.</div>','teacher',4,'fa-location-dot',1,'2026-05-10 15:05:41');
/*!40000 ALTER TABLE `help_articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offline_requests`
--

DROP TABLE IF EXISTS `offline_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `offline_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `student_name` varchar(100) NOT NULL,
  `student_email` varchar(100) NOT NULL,
  `student_phone` varchar(20) NOT NULL,
  `student_address` text NOT NULL,
  `student_city` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `class_grade` varchar(50) NOT NULL,
  `preferred_timing` varchar(100) DEFAULT NULL,
  `additional_info` text DEFAULT NULL,
  `budget` varchar(50) DEFAULT NULL,
  `preferred_tutor_gender` enum('male','female','any') DEFAULT 'any',
  `status` enum('pending','assigned','demo_scheduled','completed','cancelled') DEFAULT 'pending',
  `assigned_teacher_id` int(11) DEFAULT NULL,
  `demo_date` datetime DEFAULT NULL,
  `admin_notes` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_city` (`student_city`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offline_requests`
--

LOCK TABLES `offline_requests` WRITE;
/*!40000 ALTER TABLE `offline_requests` DISABLE KEYS */;
INSERT INTO `offline_requests` (`id`, `student_id`, `student_name`, `student_email`, `student_phone`, `student_address`, `student_city`, `subject`, `class_grade`, `preferred_timing`, `additional_info`, `budget`, `preferred_tutor_gender`, `status`, `assigned_teacher_id`, `demo_date`, `admin_notes`, `created_at`, `updated_at`) VALUES (1,9,'Rahul Panola','rcoolest92@gmail.com','9691164692','14/2, mahalaxmi nagar','indore','science','Graduation','Evening: 6-8 pm','','3000','female','pending',NULL,NULL,NULL,'2026-05-10 11:22:40','2026-05-10 11:22:40'),
(2,10,'Rohan','rahul54singh@gmail.com','9009033877','Sudama nagar','INDORE','Pcm','Class 11','3 pm','With competative iit jee','5000','any','pending',NULL,NULL,NULL,'2026-05-10 12:52:30','2026-05-10 12:52:30');
/*!40000 ALTER TABLE `offline_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `plan` varchar(100) DEFAULT NULL,
  `screenshot` varchar(255) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `rejection_reason` text DEFAULT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `payments_ibfk_1` (`student_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` (`id`, `student_id`, `teacher_id`, `amount`, `plan`, `screenshot`, `payment_method`, `status`, `rejection_reason`, `payment_date`) VALUES (7,9,NULL,99.00,'razorpay','pay_SnaR7tCTpBvMXx','razorpay','approved',NULL,'2026-05-10 07:57:13'),
(8,9,NULL,10.00,'razorpay','pay_SnaVwM3UVVsUtu','razorpay','approved',NULL,'2026-05-10 08:01:36');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_settings`
--

DROP TABLE IF EXISTS `site_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `site_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) NOT NULL,
  `setting_value` text DEFAULT NULL,
  `setting_type` enum('text','textarea','image','json') DEFAULT 'text',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_settings`
--

LOCK TABLES `site_settings` WRITE;
/*!40000 ALTER TABLE `site_settings` DISABLE KEYS */;
INSERT INTO `site_settings` (`id`, `setting_key`, `setting_value`, `setting_type`, `updated_at`) VALUES (1,'home_hero_title','Find Your Perfect Tutor','text','2026-05-11 17:08:53'),
(2,'home_hero_subtitle','Connect with experienced tutors for personalized learning','text','2026-05-10 17:27:41'),
(3,'home_hero_button_text','Get Started','text','2026-05-10 17:27:41'),
(4,'contact_email','support@hometutorhub.in','text','2026-05-10 17:27:41'),
(5,'contact_phone','+91 98765 43210','text','2026-05-10 17:27:41'),
(6,'footer_copyright','© 2026 HomeTutorHub. All rights reserved. Developed by Rahul P.','text','2026-05-11 18:02:25'),
(7,'social_facebook','','text','2026-05-10 17:35:27'),
(8,'social_twitter','','text','2026-05-10 17:35:27'),
(9,'social_instagram','','text','2026-05-10 17:35:27'),
(10,'social_linkedin','','text','2026-05-10 17:35:27'),
(11,'social_youtube','https://www.youtube.com/','text','2026-05-10 17:36:40'),
(20,'about_content','HomeTutorHub is India\'s leading platform connecting students with qualified tutors...','text','2026-05-11 17:00:44'),
(23,'contact_address','123, Education District, New Delhi, India - 110001','text','2026-05-11 17:00:44'),
(25,'meta_description','Find the best tutors in India. HomeTutorHub connects students with qualified teachers for online and offline learning.','text','2026-05-11 17:00:44'),
(26,'meta_keywords','tutor, home tutor, online tutoring, education','text','2026-05-11 17:00:44');
/*!40000 ALTER TABLE `site_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_unlocked_teachers`
--

DROP TABLE IF EXISTS `student_unlocked_teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_unlocked_teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `unlocked_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`,`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_unlocked_teachers`
--

LOCK TABLES `student_unlocked_teachers` WRITE;
/*!40000 ALTER TABLE `student_unlocked_teachers` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_unlocked_teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `father_name` varchar(100) DEFAULT NULL,
  `father_phone` varchar(20) DEFAULT NULL,
  `mother_name` varchar(100) DEFAULT NULL,
  `mother_phone` varchar(20) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  `points` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` (`id`, `full_name`, `email`, `password`, `phone`, `father_name`, `father_phone`, `mother_name`, `mother_phone`, `city`, `state`, `pincode`, `qualification`, `specialization`, `address`, `security_question`, `security_answer`, `points`, `created_at`) VALUES (9,'Rahul Panola','rcoolest95@gmail.com','pbkdf2:sha256:600000$dlUFA6Bo7u2uuiah$5776b8ab4dfd94497fba18081af2bb7b2df3ca1a63a5ab8612597a24f443b6be','9691164692',NULL,NULL,NULL,NULL,'indore',NULL,NULL,'12th','science','14/2, mahalaxmi nagar','What is your pet\'s name?','pbkdf2:sha256:600000$lT7hUo0BkUHA56V7$4bb98931e8b8794fc314bb0b1769b1f9a4923fb349d1bd9785d22805e5e6efbd',111,'2026-05-06 23:48:53'),
(10,'Rohan','rahul54singh@gmail.com','pbkdf2:sha256:600000$fpR7cplYN64k1g3i$ca531d7fb7af07710580aa18868429d9d7ed35f3bbefee71c3541e88dcf50131','9009033877',NULL,NULL,NULL,NULL,'INDORE',NULL,NULL,'12th','Pcm',NULL,'What is your pet\'s name?','pbkdf2:sha256:600000$9do9adSy8UgXkQTv$586da6b434373e19c048ed4ea2394d5a1bae79631274c864eab4fc43b0a9e857',49,'2026-05-10 08:07:45'),
(12,'Raju Parmar','rcoolest92@gmail.com','pbkdf2:sha256:600000$910yNDSTZMqG5A5A$e6156583ca974471b79a41d62408d3e0eec2d6eaadc46459e9142261d2ec0d7f','9691164692','kailash parmar','9691164692','komal parmar','969164692','Kapurthala','Punjab','144411','12th','science','1, law gate LPU','What is your pet\'s name?','pbkdf2:sha256:600000$F1D7AjFFBqQx0axg$eced05e44594b908e97f0dc0554bd973aab668231e7078862416109b50723df3',49,'2026-05-10 12:08:52');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject_name` (`subject_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` (`id`, `subject_name`) VALUES (4,'Biology'),
(3,'Chemistry'),
(6,'Computer Science'),
(5,'English'),
(1,'Mathematics'),
(2,'Physics');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_availability`
--

DROP TABLE IF EXISTS `teacher_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_availability` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `preferred_area` varchar(200) DEFAULT NULL,
  `max_distance_km` int(11) DEFAULT 10,
  `is_available_for_offline` tinyint(1) DEFAULT 1,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_teacher` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_availability`
--

LOCK TABLES `teacher_availability` WRITE;
/*!40000 ALTER TABLE `teacher_availability` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_subjects`
--

DROP TABLE IF EXISTS `teacher_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `teacher_subjects_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_subjects`
--

LOCK TABLES `teacher_subjects` WRITE;
/*!40000 ALTER TABLE `teacher_subjects` DISABLE KEYS */;
INSERT INTO `teacher_subjects` (`id`, `teacher_id`, `subject_name`) VALUES (14,9,'python'),
(16,10,'Biology'),
(17,15,'English'),
(18,15,'Hindi'),
(19,15,'Sanskrit');
/*!40000 ALTER TABLE `teacher_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `qualification` varchar(150) DEFAULT NULL,
  `experience` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `aadhaar` varchar(20) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `resume` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `is_verified` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `my_points` int(11) DEFAULT 0,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  `mode` varchar(50) DEFAULT 'Offline',
  `gender` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `whatsapp` varchar(20) DEFAULT NULL,
  `alt_phone` varchar(20) DEFAULT NULL,
  `locality` varchar(255) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `university` varchar(255) DEFAULT NULL,
  `passing_year` int(11) DEFAULT NULL,
  `subjects` text DEFAULT NULL,
  `classes` text DEFAULT NULL,
  `boards` text DEFAULT NULL,
  `exp_type` text DEFAULT NULL,
  `timing` varchar(255) DEFAULT NULL,
  `pref_area` varchar(255) DEFAULT NULL,
  `monthly_fee` decimal(10,2) DEFAULT NULL,
  `hourly_fee` decimal(10,2) DEFAULT NULL,
  `languages` text DEFAULT NULL,
  `special_skills` text DEFAULT NULL,
  `plan` varchar(50) DEFAULT 'free_trial',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` (`id`, `full_name`, `email`, `password`, `phone`, `qualification`, `experience`, `city`, `address`, `aadhaar`, `photo`, `resume`, `status`, `is_verified`, `created_at`, `my_points`, `security_question`, `security_answer`, `mode`, `gender`, `dob`, `whatsapp`, `alt_phone`, `locality`, `state`, `pincode`, `specialization`, `university`, `passing_year`, `subjects`, `classes`, `boards`, `exp_type`, `timing`, `pref_area`, `monthly_fee`, `hourly_fee`, `languages`, `special_skills`, `plan`) VALUES (9,'Rahul Panola','rcoolest92@gmail.com','pbkdf2:sha256:600000$UqSgCZ2Se2rDXx0u$3862975a734beaea6969a896acd5c0a6926d1ce104d2e1fe864632887e4f1b13','9691164692','MCA',3,'Ratlam','14/2','3986 3675 9367','image.png','OS_Mastry_Quest02_Deadlock_Dominator.docx','active',1,'2026-05-06 13:38:54',51,'What is your pet\'s name?','pbkdf2:sha256:600000$7At7hJCflSSMj1Iz$a600f24e17d2675ee1289935c93de6fa34a1c6936535a624fad0c071fb22bc68','Online','Male','1992-01-15','9691164692','9691164692','Mahalaxmi Nagar','Madhya Pradesh','457001','Computer Application','RGPV',2022,'Computer','','CBSE,ICSE,State Board,Other','School,Online','6PM-8PM','Ratlam',3000.00,500.00,'Hindi, English','PYthon, sql','free_trial'),
(10,'Sai Srinivas','puthurusaisrinivas12@gmail.com','pbkdf2:sha256:600000$pdOySxvdgJrGZwsq$86a82b774342b84fdcc787ea46d959f6b78e58429f4aa293cdc62818c3af3cda','8919666322','B.Sc B.ed CBZ',1,'Nellore','Gudur','7750 5616 5166','1000271021.jpg','Sai_Srinivas_Resume_.pdf','active',1,'2026-05-06 13:54:28',49,'What city were you born in?','pbkdf2:sha256:600000$5SM6sPzJMrjKSY8t$a05f28a783369db714751e92b48b5eb6402c7e610bf281e78ff617d4072ecd74','Online','Male','2003-08-13','8919666322','','Dhurjeti nagar ','Andhra Pradesh','524101','Biology ','RIE MYSORE',2025,'Science','Class 6–8,Class 9–10','CBSE,State Board','School','7-8 / 7-9','',20000.00,700.00,'Telugu , English , Kannada ','NEET','free_trial'),
(12,'Swati Singh','swatikatheriya88@gmail.com','pbkdf2:sha256:600000$YiZvNDcI85OjJoZ8$d3772b5ace1c1e80d8578d05b322b3bf0b52548a1cc01596de0df7e3499c7783','9528958340','12',0,'Sirsaganj','Village kairawali Sirsaganj Firozabad Uttar Pradesh ','5472 1870 5234','1000045807.jpg','DOC-20260323-WA0003.pdf','active',1,'2026-05-08 06:57:31',49,'What city were you born in?','pbkdf2:sha256:600000$UFpANGzNosMMUOpZ$eb79d2ec7db3ebb6d34ff72543277eba081b30274209e681163e1a995406d813','Online','Female','2026-07-07','9528958340','9410481378','Kairawali ','Uttar Pradesh','283151','Social science ,   Hindi ','Regional institute of Education NCERT Ajmer ',2026,'SST','Class 1–5,Class 6–8,Class 9–10','CBSE,State Board','School,Home Tuition',' 8-11 pm','',5000.00,500.00,'Hindi ','Teaching ','free_trial'),
(13,'Rahul Singh Sisodiya ','rahulabhaysinghsisodiya@gmail.com','pbkdf2:sha256:600000$OUyvrhk1Dab652OI$f7f7495b43058714d4ea3aa98ab84501c6dcc081aab2a740d9a5d7bf11f762d3','9009033877','M.Sc. Chemistry ',10,'INDORE','34 Pushpratan park','9574 1816 6585','1000882120.jpg','resume_1.pdf','active',1,'2026-05-09 09:30:01',49,'What is your pet\'s name?','pbkdf2:sha256:600000$bD3H3KX17ZuL6Snr$41a6cd810e7b86e53afff8a51143d9d7da754b0c30a279a271b4add77d7bb670','Both','Male','1987-08-30','9009033877','','Indore','Madhya Pradesh','452016','Chemistry ','DAVV',2014,'Chemistry','Class 11–12','CBSE,ICSE','School,Coaching,Home Tuition','Evening ','Indore',8000.00,350.00,'Hindi, English ','IIT-JEE LEVEL, neet level ','free_trial'),
(14,'sONALI','sonaligaur0079@gmail.com','pbkdf2:sha256:600000$biLLMAVK5N5WIWpw$93a70967f6ba2c3b5c7ccf18acd779746d4478aa8d89fc81b95b719be24e3cb8','9870332191','M. A',5,'South West Delhi','RZH-115/1-A, Gali No. 3, Near Solanki Chowk, Rajanagar-II, palm colony','4301 6759 1180','download.jpeg','Sonali_CV.pdf','active',1,'2026-05-12 19:16:58',49,'What city were you born in?','pbkdf2:sha256:600000$a8qrUcTDxsbF4xgu$c6d0bfdb02d1ad7ff9329e3a7647cfc6011f021350ad7f71e210d742d84d877d','Online','Female','2001-05-26','9870332191','','Palam colony','Delhi','110077','Sociology','IGNOU',2024,'Maths,Science,Computer,Other,Chemistry','Class 6–8,Class 9–10','CBSE,ICSE','Coaching,Home Tuition','7pm-9pm','',3000.00,600.00,'Hindi, english','','free_trial'),
(15,'Ranjana kushwaha ','ranjanakushwaha307@gmail.com','pbkdf2:sha256:600000$ExtpodHmlAy9Ibzy$4d3837af9eb78d5dc69ea3510c654c0586d615246977e4b4d748318f747fc334','8109125363','MA ',3,'Indore','204 siddhipuram colony near gopur square indore ','7709 6890 1963','IMG_20260428_094252_1778641169.jpg','CV_Ranjana_kushwaha_.pdf','active',1,'2026-05-13 02:56:31',49,'What is your pet\'s name?','pbkdf2:sha256:600000$bhw7oW1nOwM2l31h$50aea4266ca59f8289be7931b370c876c7fed40d1a35fad340295e5bb74036e1','Both','Female','1999-01-01','8109125363','','Gopur square ','Madhya Pradesh','452009','English ','Jiwaji university gwalior ',2023,'','Class 1–5,Class 6–8','CBSE,State Board','Home Tuition','4pm to 9pm','',25000.00,500.00,'Hindi, English and Sanskrit ','','free_trial');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testimonials`
--

DROP TABLE IF EXISTS `testimonials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `testimonials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  `content` text NOT NULL,
  `rating` int(11) DEFAULT 5,
  `display_order` int(11) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `feedback_id` (`feedback_id`),
  CONSTRAINT `testimonials_ibfk_1` FOREIGN KEY (`feedback_id`) REFERENCES `feedback` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testimonials`
--

LOCK TABLES `testimonials` WRITE;
/*!40000 ALTER TABLE `testimonials` DISABLE KEYS */;
/*!40000 ALTER TABLE `testimonials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tuition_requests`
--

DROP TABLE IF EXISTS `tuition_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tuition_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `mode` varchar(50) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `class_grade` varchar(50) DEFAULT NULL,
  `preferred_timing` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Open',
  `assigned_teacher_id` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `tuition_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tuition_requests`
--

LOCK TABLES `tuition_requests` WRITE;
/*!40000 ALTER TABLE `tuition_requests` DISABLE KEYS */;
INSERT INTO `tuition_requests` (`id`, `student_id`, `subject`, `mode`, `location`, `class_grade`, `preferred_timing`, `description`, `status`, `assigned_teacher_id`, `created_at`, `updated_at`) VALUES (2,9,'chemistry','Online','Ratlam','Class 12','6:30 AM to 7:30 PM','','Open',NULL,'2026-05-10 04:56:27','2026-05-10 04:56:27');
/*!40000 ALTER TABLE `tuition_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unlocked_leads`
--

DROP TABLE IF EXISTS `unlocked_leads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `unlocked_leads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `request_id` int(11) DEFAULT NULL,
  `unlocked_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_unlock` (`teacher_id`,`student_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `unlocked_leads_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `unlocked_leads_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unlocked_leads`
--

LOCK TABLES `unlocked_leads` WRITE;
/*!40000 ALTER TABLE `unlocked_leads` DISABLE KEYS */;
INSERT INTO `unlocked_leads` (`id`, `teacher_id`, `student_id`, `request_id`, `unlocked_at`) VALUES (3,9,9,NULL,'2026-05-10 04:57:30');
/*!40000 ALTER TABLE `unlocked_leads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'hometuto_teacher_portal'
--

--
-- Dumping routines for database 'hometuto_teacher_portal'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-14 22:33:03

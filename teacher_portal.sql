-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 19, 2026 at 08:00 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `teacher_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `full_name`, `email`, `password`, `created_at`) VALUES
(1, 'Admin', 'admin@gmail.com', 'scrypt:32768:8:1$tjmt5JnaVRkG4TIr$ab19d9bf9758624993f35dc55b83ecb60ba34e06100e660499d07a8c8ad415b373acc48c07278a44c1736c0bf42bd5d2e05640cda413b68545835c6e6969b21c', '2026-03-08 12:59:10');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `screenshot` varchar(255) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `rejection_reason` text DEFAULT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `student_id`, `teacher_id`, `amount`, `screenshot`, `payment_method`, `status`, `rejection_reason`, `payment_date`) VALUES
(3, 3, NULL, 20.00, '3.jpeg', NULL, 'failed', '111', '2026-03-10 08:00:51');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  `points` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `my_points` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `full_name`, `email`, `password`, `phone`, `city`, `qualification`, `specialization`, `security_question`, `security_answer`, `points`, `created_at`, `my_points`) VALUES
(3, 'Vinay Dangi', 'vinay@gmail.com', 'scrypt:32768:8:1$OjBiLZ0isqL6S5rj$bd5db89cf6a691e0ebbbdbc5d16a522bf3e18d75f2c87882eb87a4e98859485bec3e8096c6bfed68b0c3df62fb654e5b4a56c52f7d107566fd7b1544ca64937f', '98278712121', 'Indore', '10th Pursuing', 'General', 'What city were you born in?', 'scrypt:32768:8:1$cpqFrqvX5BgZr9RY$4e4b6737e00ba0c10a6001aa6f4c877a9f4de9ff416d67b23a55cf6d96c0a92c5a600e2894edc5ef918392bd47183d59febd41929aecc24ef364a51b167d1d78', 50, '2026-03-10 08:00:28', 5),
(4, 'Saksham Choudhary', 'akkisaksham431@gmail.com', 'scrypt:32768:8:1$krFq9orItjT9tPpe$77da8ca757133b971db2c3bf42dc00bb8dbce82a63f4234e04b5ca0cabe00e832c6db963dfabb0c3c20be7bb7a75ba986c92376efa4e6a1f92028c7416ed4007', '9622299614', 'Indore', '12th `', 'Biology', 'What is your pet\'s name?', 'scrypt:32768:8:1$VGf7YfSqcDBmIxUr$8c4a440a330d1778d28829e6dda4d1ef301fe0906718928534939dba33522e2522e0276bea76b451ce60312fe14c8f9a97c7ed0e7a39848ccbd31f15efd98d04', 50, '2026-03-11 08:50:08', 30),
(5, 'mehak knanaparthy', 'kanaparthymehak8@gmail.com', 'scrypt:32768:8:1$i6NRNYgZiY9bIYOa$3dae28065e3c1fb74280612cee5deda6f1edf9451e63ddd4b150d2955b4ac879b335dcdbbc3173d3e74dd3fef72b808fc5ea6bbe70ee6d0da1afc9cb75b88129', '7573854031', 'indore', '12th', 'mathematics', 'What city were you born in?', 'scrypt:32768:8:1$0piwAh7DEOqvr8Ee$717addd458cbade858a093c465feb3526a7f5d316938a10be27bc5d1f4111b2439b80db5d4c11b2726618643383da7001141218eccc0220baeafacf30bfc4930', 50, '2026-03-11 08:52:20', 30),
(6, 'Kartik Arya', 'kartikarya789@gmail.com', 'scrypt:32768:8:1$muANyjadW0akHTN7$8d51c93899c2a623755903333a22bed1446a3ecfd996a1306b15c37b90545340d9032f24d246e111dd25cee7f7c7e4b5b4f609c3bb6c92053eea4b467a88f265', '9867523420', 'jhansi', '12th', 'mathematics', 'What is your pet\'s name?', 'scrypt:32768:8:1$CorlhlIMNk9rNdZP$134dfa20472b1429fafabc35c1666296105c9ba6319ad58efdcf53b8e024fffc66d70451f348e5d10eb24f6d7c67ce9d26fdab5363187fc79b8d782beb5eb7a3', 50, '2026-03-11 08:55:00', 30),
(7, 'Ayush Dongare', 'manojdongare48@gmail.com', 'scrypt:32768:8:1$IjLdDSrI8V5FBQtR$fe3af87ebb9bcf405eba9628ba85a1a8c471534df7238689346b2b395f575dd33602030bc2d1c9320603eac10b195883f875e72b5d2341b63a24a072b091ccba', '9589130070', 'indore', '12th', 'biology', 'What is your pet\'s name?', 'scrypt:32768:8:1$O5LLY2kaBcJkoWaT$06daf57cd34d8a17992d3f690fe008cdf71033fd74ada0a88d1f704dcea992c22989f27c8f2f9217b1a4d42eb6a3d0aa295fa973ee8a837a9c39feb9eae500e3', 50, '2026-03-11 08:56:33', 30),
(8, 'Kunal Suman', 'kunalsuman084@gmail.com', 'scrypt:32768:8:1$2pbfdq4GnkchnsHF$e67cdf6bc274ee27922810a3503503ab8ab4d994e2dcdf10aa8552a65a5840b1492be020e2b2ef7831008a9dbebb3d04d6bf78388b9fadd549298cab4fef9d2c', '9111374948', 'Indore', '12th', 'Science', 'What city were you born in?', 'scrypt:32768:8:1$apVbEZNsC04Ef3nf$9bce1eda6fac84ad3d40a2985544e2fa6e3dfb4d3e7593bba50c4434eef82b661e2361f49e21776820b31753aae8c4c7af513986fd3988c35944b7d9f38f2732', 50, '2026-03-11 08:57:47', 30);

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `subject_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`id`, `subject_name`) VALUES
(4, 'Biology'),
(3, 'Chemistry'),
(6, 'Computer Science'),
(5, 'English'),
(1, 'Mathematics'),
(2, 'Physics');

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
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
  `points` int(11) DEFAULT 0,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  `my_points` int(11) NOT NULL DEFAULT 0,
  `mode` enum('Online','Offline') DEFAULT 'Offline'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`id`, `full_name`, `email`, `password`, `phone`, `qualification`, `experience`, `city`, `address`, `aadhaar`, `photo`, `resume`, `status`, `is_verified`, `created_at`, `points`, `security_question`, `security_answer`, `my_points`, `mode`) VALUES
(3, 'rahul singh sisodiya', 'rahul54singh@gmail.com', 'scrypt:32768:8:1$6Ot1ighX8nAmbUYq$47ed0e8a19129d303f2f3d3bcbf6103b7b4526103b6f6277a124b680e24a3de7e836d95d1cbb252238f09ff003bdbd656b55de37cdb062b9f501f21247080f71', '9009033877', 'M.Sc. Chemistry', 5, 'Indore', 'pushp ratan park', '3986367868', '1.jpeg', 'SCAN_20260303_085909991.pdf', 'active', 1, '2026-03-09 08:27:10', 20, 'What city were you born in?', 'scrypt:32768:8:1$l7tVDwy3OH7RWcsi$858d13b8a27688f00ef8f08a994f6b81f2791018aa3921a8b439d408f48af6bb1bc180c157324852d4506c76ee4b80bb6ba89f388cc53fd2831290cf03eda5b3', 20, 'Online'),
(4, 'Ashiwin Rajput', 'arjun@gmail.com', 'scrypt:32768:8:1$UQhVe2dJRyW4FaMT$f75ed09bb57d21e77ae8f3e8bcdce2126c6490b4ca696f77627436a39ee2794eb04e35d1c318af2d2cbf34d081d62d864d56d23c1e38de63754935b5a87946aa', '9009033877', 'M. Tech', 8, 'Indore', 'Teen Imli Chouhraha', '3986 3675 9367', '2.jpeg', '402_Information_Tech_SQP.pdf', 'active', 1, '2026-03-11 04:41:32', 30, 'What is your pet\'s name?', 'scrypt:32768:8:1$mPMXqQ0DuYwNRF28$e8c373ff0385a73b1f87c5e31646d75373b645d8d6bb05886834025570d71e0cf878fef5896d6ba8d6ebe06c75249ec22f137484acea64113e99a823563974e8', 0, 'Offline');

-- --------------------------------------------------------

--
-- Table structure for table `teacher_requests`
--

CREATE TABLE `teacher_requests` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `status` enum('pending','accepted','rejected') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `Mode` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teacher_requests`
--

INSERT INTO `teacher_requests` (`id`, `student_id`, `teacher_id`, `status`, `created_at`, `Mode`) VALUES
(1, 3, 3, 'accepted', '2026-03-10 18:37:55', 'Online'),
(2, 3, 4, 'accepted', '2026-03-11 05:02:53', 'Offline');

-- --------------------------------------------------------

--
-- Table structure for table `teacher_subjects`
--

CREATE TABLE `teacher_subjects` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teacher_subjects`
--

INSERT INTO `teacher_subjects` (`id`, `teacher_id`, `subject_name`) VALUES
(6, 3, 'Chemistry'),
(7, 4, 'Physics'),
(8, 4, 'Maths'),
(9, 4, 'Robotics'),
(10, 4, 'AI');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teacher_id` (`teacher_id`),
  ADD KEY `payments_ibfk_1` (`student_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `subject_name` (`subject_name`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `teacher_requests`
--
ALTER TABLE `teacher_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indexes for table `teacher_subjects`
--
ALTER TABLE `teacher_subjects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `teacher_requests`
--
ALTER TABLE `teacher_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `teacher_subjects`
--
ALTER TABLE `teacher_subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`);

--
-- Constraints for table `teacher_requests`
--
ALTER TABLE `teacher_requests`
  ADD CONSTRAINT `teacher_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `teacher_requests_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`);

--
-- Constraints for table `teacher_subjects`
--
ALTER TABLE `teacher_subjects`
  ADD CONSTRAINT `teacher_subjects_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

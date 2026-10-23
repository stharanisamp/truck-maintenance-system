-- ==============================================================================
-- TRUCK MAINTENANCE SYSTEM - COMPLETE DATABASE SCHEMA & DATA
-- File: database.sql
-- Database Name: truck_maintenance_system
-- Compatible with: MySQL 5.7+, MySQL 8.0+, MariaDB, XAMPP, phpMyAdmin
-- ==============================================================================

SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET NAMES utf8mb4;

-- ----------------------------------------------------------------------
-- Database Creation
-- ----------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `truck_maintenance_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `truck_maintenance_system`;

-- ----------------------------------------------------------------------
-- Table structure and data for `admins`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE IF NOT EXISTS `admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(150) NOT NULL,
    `phone` VARCHAR(20),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `admins` (2 records)
INSERT INTO `admins` (`id`, `username`, `email`, `password_hash`, `full_name`, `phone`, `created_at`, `updated_at`) VALUES (1, 'admin', 'stharanisamp@gmail.com', 'scrypt:32768:8:1$FKir3nt85ARUOSPM$eca3f79f44f7041cea3437ebe3ca9bdb863558a60870d8eccb2754b75ac86f89a80105f73403d058b60b84894d29c3dff87fb678b49b0dbccca7ac2090ec6938', 'Tharani (Fleet Owner)', '+91 98765 43210', '2026-09-04 05:15:38.984559', '2026-09-08 16:33:30.565381');
INSERT INTO `admins` (`id`, `username`, `email`, `password_hash`, `full_name`, `phone`, `created_at`, `updated_at`) VALUES (2, 'ambiga', 'ambigaa075@gmail.com', 'scrypt:32768:8:1$ax8OfvCef1wlze50$49d3a33f6bfd86a85b07320c124d9a5305361fcfddc1aeefc51e44084e911d774213f3b540671aa51eb8f28c27f654468d9e38fa988d8d59d1995c7d2a3540df', 'Ambiga (Fleet Owner)', '+91 98765 43210', '2026-09-08 17:02:02.395990', '2026-09-08 17:02:02.395995');

-- ----------------------------------------------------------------------
-- Table structure and data for `drivers`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `drivers`;
CREATE TABLE IF NOT EXISTS `drivers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `driver_code` VARCHAR(50) NOT NULL UNIQUE,
    `full_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(20) NOT NULL,
    `address` TEXT,
    `license_number` VARCHAR(100) NOT NULL UNIQUE,
    `license_expiry_date` DATE,
    `date_of_birth` DATE,
    `joining_date` DATE,
    `password_hash` VARCHAR(255) NOT NULL,
    `profile_photo` VARCHAR(255) DEFAULT 'default_avatar.png',
    `status` VARCHAR(20) DEFAULT 'Active',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `drivers` (4 records)
INSERT INTO `drivers` (`id`, `driver_code`, `full_name`, `email`, `phone`, `address`, `license_number`, `license_expiry_date`, `date_of_birth`, `joining_date`, `password_hash`, `profile_photo`, `status`, `created_at`, `updated_at`) VALUES (1, 'DRV-001', 'Murugan Selvam', 'murugan@truck.com', '+91 94431 11223', '42 Anna Nagar, Namakkal, Tamil Nadu', 'TN-28-2015-001122', '2028-01-17', '1986-05-14', '2021-01-10', 'scrypt:32768:8:1$f6IJBYOOfnQ0uowX$995e9b8d48ad56e60d7ffe7cb6a132d055205d3c0fa90341a4e92e07587b8242b0a3f168e8a199937ac24fcd470102ae24a74a3a6d6e0fafe142c7c9899f0102', 'default_avatar.png', 'Active', '2026-09-04 05:15:39.551222', '2026-09-06 15:53:46.613321');
INSERT INTO `drivers` (`id`, `driver_code`, `full_name`, `email`, `phone`, `address`, `license_number`, `license_expiry_date`, `date_of_birth`, `joining_date`, `password_hash`, `profile_photo`, `status`, `created_at`, `updated_at`) VALUES (2, 'DRV-002', 'Karthik Pandian', 'karthik@truck.com', '+91 98840 22334', '18 Bypass Road, Sankari, Salem, Tamil Nadu', 'TN-30-2018-004455', '2026-09-24', '1991-10-22', '2022-03-15', 'scrypt:32768:8:1$HeJObafqNjh8V8Mj$624fe3180b6ce76fe8231d11cf3e56938979ef4f80efdc926c646fe49e6b2204a2a5922e999f1fddb71131a978c3a76881c2c59437079d0fb18cf772aea9491e', 'default_avatar.png', 'Active', '2026-09-04 05:15:39.551230', '2026-09-04 05:15:39.551231');
INSERT INTO `drivers` (`id`, `driver_code`, `full_name`, `email`, `phone`, `address`, `license_number`, `license_expiry_date`, `date_of_birth`, `joining_date`, `password_hash`, `profile_photo`, `status`, `created_at`, `updated_at`) VALUES (3, 'DRV-003', 'Ramesh Kumar', 'ramesh@truck.com', '+91 97722 33445', '89 NH-44 Tiruchengode, Tamil Nadu', 'TN-52-2016-009988', '2027-08-30', '1989-02-18', '2023-06-01', 'scrypt:32768:8:1$LO1I0hdYC8qqnHmR$6b89f015106c1dca9f6d3072b32c69692e627248ba5308b00d43c562f97c8ae7674f89557067cf9a2a697a6dc4ae5e09e69dca2c28d0998ec739529919de8a79', 'default_avatar.png', 'Active', '2026-09-04 05:15:39.551232', '2026-09-04 05:15:39.551233');
INSERT INTO `drivers` (`id`, `driver_code`, `full_name`, `email`, `phone`, `address`, `license_number`, `license_expiry_date`, `date_of_birth`, `joining_date`, `password_hash`, `profile_photo`, `status`, `created_at`, `updated_at`) VALUES (4, 'DRV-004', 'tharani', 'stharanisamp@gmail.com', '7904279427', '', 'TN-LIC-882407', NULL, NULL, '2026-09-08', 'scrypt:32768:8:1$tDncF5sK2PSFoUGy$e4f936ff12960371fe3876549847fdfc8ae6c144489109895420b8b71490cb348c235c6843413657c90e8ea712e74a34ea31457db18d73bf14665fb416c1b0f8', 'default_avatar.png', 'Active', '2026-09-08 15:54:53.018039', '2026-09-08 15:54:53.018042');

-- ----------------------------------------------------------------------
-- Table structure and data for `vehicles`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `vehicles`;
CREATE TABLE IF NOT EXISTS `vehicles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `vehicle_number` VARCHAR(50) NOT NULL UNIQUE,
    `vehicle_type` VARCHAR(50) NOT NULL,
    `brand` VARCHAR(100),
    `model` VARCHAR(100),
    `rc_number` VARCHAR(100) NOT NULL UNIQUE,
    `rc_expiry_date` DATE,
    `insurance_number` VARCHAR(100),
    `insurance_expiry_date` DATE,
    `capacity` VARCHAR(50),
    `chassis_number` VARCHAR(100),
    `engine_number` VARCHAR(100),
    `registration_date` DATE,
    `assigned_driver_id` INT NULL,
    `status` VARCHAR(30) DEFAULT 'Active',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_db_vehicles_driver` FOREIGN KEY (`assigned_driver_id`) REFERENCES `drivers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `vehicles` (4 records)
INSERT INTO `vehicles` (`id`, `vehicle_number`, `vehicle_type`, `brand`, `model`, `rc_number`, `rc_expiry_date`, `insurance_number`, `insurance_expiry_date`, `capacity`, `chassis_number`, `engine_number`, `registration_date`, `assigned_driver_id`, `status`, `created_at`, `updated_at`) VALUES (1, 'TN 28 AB 1234', '10 Wheeler', 'Tata Motors', 'Signa 2823.K', 'RC-TN28-2021-9988', '2036-03-12', 'INS-HDFC-88990', '2027-05-02', '28 Tons', 'MAT624001E0A12345', '6TC98765432', '2021-03-12', 1, 'Active', '2026-09-04 05:15:39.026817', '2026-09-04 05:15:39.026822');
INSERT INTO `vehicles` (`id`, `vehicle_number`, `vehicle_type`, `brand`, `model`, `rc_number`, `rc_expiry_date`, `insurance_number`, `insurance_expiry_date`, `capacity`, `chassis_number`, `engine_number`, `registration_date`, `assigned_driver_id`, `status`, `created_at`, `updated_at`) VALUES (2, 'TN 30 CD 5678', '14 Wheeler', 'Ashok Leyland', '3520 Multi-Axle', 'RC-TN30-2022-7711', '2037-05-18', 'INS-ICICI-44332', '2026-09-19', '35 Tons', 'MB1A12345F0B56789', 'H6ETIC4RU22', '2022-05-18', 2, 'In Trip', '2026-09-04 05:15:39.026824', '2026-09-04 05:15:39.026825');
INSERT INTO `vehicles` (`id`, `vehicle_number`, `vehicle_type`, `brand`, `model`, `rc_number`, `rc_expiry_date`, `insurance_number`, `insurance_expiry_date`, `capacity`, `chassis_number`, `engine_number`, `registration_date`, `assigned_driver_id`, `status`, `created_at`, `updated_at`) VALUES (3, 'TN 52 EF 9012', 'Container', 'BharatBenz', '2823R Heavy Truck', 'RC-TN52-2023-3344', '2038-09-10', 'INS-BAJAJ-11223', '2027-07-21', '30 Tons', 'ME1B98765G0C90123', 'OM926LA110', '2023-09-10', 3, 'Active', '2026-09-04 05:15:39.026826', '2026-09-04 05:15:39.026826');
INSERT INTO `vehicles` (`id`, `vehicle_number`, `vehicle_type`, `brand`, `model`, `rc_number`, `rc_expiry_date`, `insurance_number`, `insurance_expiry_date`, `capacity`, `chassis_number`, `engine_number`, `registration_date`, `assigned_driver_id`, `status`, `created_at`, `updated_at`) VALUES (4, 'TN 88 GH 3456', 'Trailer', 'Eicher Motors', 'Pro 6040 Trailer', 'RC-TN88-2020-5566', '2035-11-25', 'INS-TATA-66778', '2026-08-30', '40 Tons', 'MC2C54321H0D34567', 'VEDX8CRDI04', '2020-11-25', 4, 'In Maintenance', '2026-09-04 05:15:39.026827', '2026-09-04 05:15:39.026827');

-- ----------------------------------------------------------------------
-- Table structure and data for `customers`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE IF NOT EXISTS `customers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `driver_id` INT NOT NULL,
    `company_name` VARCHAR(150) NOT NULL,
    `contact_person` VARCHAR(150),
    `mobile_number` VARCHAR(20) NOT NULL,
    `email` VARCHAR(150),
    `address` TEXT,
    `gst_number` VARCHAR(50),
    `loading_location` VARCHAR(200),
    `unloading_location` VARCHAR(200),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY `idx_driver_id` (`driver_id`),
    CONSTRAINT `fk_customers_driver` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `customers` (8 records)
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (1, 1, 'Annamalai Cement Logistics', 'V. Senthil Nathan', '+91 98427 12345', 'dispatch@annamalai.in', 'Industrial Estate, Ariyalur', '33AAACA1234A1Z5', 'Ariyalur Cement Plant', 'Chennai Harbour Yard', '2026-09-04 05:15:39.572288', '2026-09-04 05:15:39.572292');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (2, 1, 'Kongu Steel Traders', 'P. Arumugam', '+91 94422 67890', 'kongusteels@yahoo.com', 'Steel Market, Salem', '33AABCK5678B1Z2', 'Salem Steel Plant', 'Coimbatore SIDCO', '2026-09-04 05:15:39.572294', '2026-09-04 05:15:39.572294');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (3, 2, 'Cauvery Granites Ltd', 'K. Balan', '+91 97890 54321', 'orders@cauverygranites.com', 'SIPCOT Phase II, Hosur', '33AAACG9012C1Z8', 'Hosur Quarry', 'Tuticorin Port', '2026-09-04 05:15:39.572295', '2026-09-04 05:15:39.572296');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (4, 1, 'Antigravity Freight Hub', 'Vignesh Kumar', '+91 91234 56789', 'logistics@antigravity.in', 'Coimbatore, Tamil Nadu', '33AABCT9988D1Z4', 'Coimbatore Airport Road', 'Bangalore Electronic City', '2026-09-04 05:56:12.618877', '2026-09-04 05:56:12.618886');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (5, 1, 'Antigravity Freight Hub', 'Vignesh Kumar', '+91 91234 56789', 'logistics@antigravity.in', 'Coimbatore, Tamil Nadu', '33AABCT9988D1Z4', 'Coimbatore Airport Road', 'Bangalore Electronic City', '2026-09-04 07:39:49.630601', '2026-09-04 07:39:49.630605');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (6, 1, 'Antigravity Freight Hub', 'Vignesh Kumar', '+91 91234 56789', 'logistics@antigravity.in', 'Coimbatore, Tamil Nadu', '33AABCT9988D1Z4', 'Coimbatore Airport Road', 'Bangalore Electronic City', '2026-09-04 08:39:12.917747', '2026-09-04 08:39:12.917775');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (7, 1, 'Antigravity Freight Hub', 'Vignesh Kumar', '+91 91234 56789', 'logistics@antigravity.in', 'Coimbatore, Tamil Nadu', '33AABCT9988D1Z4', 'Coimbatore Airport Road', 'Bangalore Electronic City', '2026-09-04 08:39:59.002132', '2026-09-04 08:39:59.002136');
INSERT INTO `customers` (`id`, `driver_id`, `company_name`, `contact_person`, `mobile_number`, `email`, `address`, `gst_number`, `loading_location`, `unloading_location`, `created_at`, `updated_at`) VALUES (8, 1, 'Antigravity Freight Hub', 'Vignesh Kumar', '+91 91234 56789', 'logistics@antigravity.in', 'Coimbatore, Tamil Nadu', '33AABCT9988D1Z4', 'Coimbatore Airport Road', 'Bangalore Electronic City', '2026-09-06 15:53:46.650217', '2026-09-06 15:53:46.650222');

-- ----------------------------------------------------------------------
-- Table structure and data for `memos`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `memos`;
CREATE TABLE IF NOT EXISTS `memos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `memo_number` VARCHAR(100) NOT NULL UNIQUE,
    `driver_id` INT NOT NULL,
    `vehicle_id` INT DEFAULT NULL,
    `vehicle_number_text` VARCHAR(50) DEFAULT NULL,
    `customer_id` INT DEFAULT NULL,
    `memo_date` DATE NOT NULL,
    `source` VARCHAR(150) NOT NULL,
    `destination` VARCHAR(150) NOT NULL,
    `freight_amount` DOUBLE DEFAULT 0.0,
    `advance_amount` DOUBLE DEFAULT 0.0,
    `total_expense` DOUBLE DEFAULT 0.0,
    `profit` DOUBLE DEFAULT 0.0,
    `net_amount` DOUBLE DEFAULT 0.0,
    `status` VARCHAR(20) DEFAULT 'Profit',
    `memo_file_path` VARCHAR(255) DEFAULT NULL,
    `enhanced_image_path` VARCHAR(255) DEFAULT NULL,
    `ocr_raw_text` LONGTEXT,
    `extracted_json` LONGTEXT,
    `verification_status` VARCHAR(50) DEFAULT 'SAVED',
    `confidence_score` FLOAT DEFAULT 1.0,
    `material` VARCHAR(150) DEFAULT NULL,
    `load_quantity` VARCHAR(50) DEFAULT NULL,
    `start_km` FLOAT DEFAULT NULL,
    `end_km` FLOAT DEFAULT NULL,
    `driver_phone` VARCHAR(50) DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY `idx_memo_driver` (`driver_id`),
    KEY `idx_memo_vehicle` (`vehicle_id`),
    KEY `idx_memo_customer` (`customer_id`),
    CONSTRAINT `fk_memos_driver` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_memos_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_memos_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `memos` (8 records)
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (1, 'MEMO-2026-001', 1, 1, 'TN 28 AB 1234', NULL, '2026-08-23', 'Ariyalur', 'Chennai Harbour', 48000.0, 15000.0, 32400.0, 15600.0, 600.0, 'Profit', 'sample_memos/sample_memo_1.png', NULL, '2026-09-04 05:15:39.597297', '2026-09-04 05:15:39.597303', NULL, NULL, 'SAVED', 1.0, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (2, 'MEMO-2026-002', 1, 1, 'TN 28 AB 1234', NULL, '2026-08-30', 'Salem', 'Coimbatore', 26000.0, 8000.0, 18500.0, 7500.0, -500.0, 'Profit', 'sample_memos/sample_memo_2.png', NULL, '2026-09-04 05:15:39.603355', '2026-09-04 05:15:39.603362', NULL, NULL, 'SAVED', 1.0, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (3, 'MEMO-2026-003', 2, 2, 'TN 30 CD 5678', NULL, '2026-09-02', 'Hosur', 'Tuticorin', 42000.0, 10000.0, 45200.0, -3200.0, -13200.0, 'Loss', 'sample_memos/sample_memo_3.png', NULL, '2026-09-04 05:15:39.608773', '2026-09-04 05:15:39.608777', NULL, NULL, 'SAVED', 1.0, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (4, 'MEMO-2026-001-116', 1, NULL, 'TN 28 AB 1234', NULL, '2026-08-12', 'Ariyalur', 'Chennai Harbour', 48000.0, 15000.0, 32400.0, 15600.0, 600.0, 'Profit', 'uploads/memos/sample_memo_1.png', 'test text', '2026-09-04 08:38:36.617626', '2026-09-04 08:38:36.617633', NULL, NULL, 'SAVED', 1.0, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (5, 'MEMO-202609071219', 1, NULL, 'TN 21 AJ 1234', NULL, '2026-09-07', 'Coimbalore', 'Salem', 2026.0, 500.0, 17600.0, -15574.0, -16074.0, 'Loss', 'uploads/memos/memo_DRV-001_1788763723.png', 'Date   24/08 _   2026   Vehicle No.   TN   21   AJ   1234   Driver Name   R. Karthik 

 From   Coimbalore   To   Chennai   Via   Salem   Ve llore 

 Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k 

 Consignee Name   Sri   Balaji   Textiles   Consignor Name   Kovai   Texliles 

 SI. No:   Particulars   Amount (?) 

 Freight Charges   18,000 

 2   Loading Charges   1   500 

 Unloading Charges   200 

 4   Toll Charges   850 

 5   Fuel   Diesel   6,350 

 Driver Allowance   0o0 

 Other Expenses   Parking ]   Tea   etc   600 

 Total Expenses (A)   12,500 

 Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026 

 Advance Taken   5,000   Trip   Status   Completed 

 Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik 

 Remarks   Goods   delivered   in   Jood   Condition 

 Owner / Transport Signature   3   Muwae', '2026-09-07 06:49:37.893177', '2026-09-07 06:49:37.893186', 'uploads/memos/memo_DRV-001_1788763723_enhanced.png', '{"memo_number": "MEMO-202609071219", "date": "2026-09-07", "vehicle_number": "TN 21 AJ 1234", "driver_name": null, "driver_phone": null, "owner_name": null, "from_place": "Coimbalore", "to_place": "Salem", "starting_location": "Coimbalore", "destination": "Salem", "material": "Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K", "load_quantity": null, "quantity_unit": null, "starting_km": null, "ending_km": null, "total_km": null, "fuel_quantity": null, "fuel_expense": 5.0, "toll_expense": 4.0, "loading_charge": 2.0, "unloading_charge": 200.0, "driver_advance": 5000.0, "food_expense": 600.0, "parking_expense": 600.0, "repair_expense": null, "other_expense": 9100.0, "total_expense": 12500.0, "trip_amount": 18000.0, "freight_amount": 18000.0, "balance_amount": 500.0, "remarks": null, "confidence": {"vehicle_number": 0.98, "date": 0.5, "from_place": 0.94, "to_place": 0.94, "memo_number": 0.65, "material": 0.88, "trip_amount": 0.96, "loading_charge": 0.91, "unloading_charge": 0.91, "toll_expense": 0.94, "fuel_expense": 0.95, "food_expense": 0.92, "parking_expense": 0.9, "total_expense": 0.95, "driver_advance": 0.94, "other_expense": 0.85}, "table_rows": [{"s_no": 1, "category_key": "other", "category_name": "Other Expenses (\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Other Expenses", "category_name_ta": "\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k", "amount": 8500, "is_expense": true}, {"s_no": 2, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Charges   18,000", "amount": 18000, "is_expense": false}, {"s_no": 3, "category_key": "loading", "category_name": "Loading Charges (\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Loading Charges", "category_name_ta": "\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "2   Loading Charges   1   500", "amount": 500, "is_expense": true}, {"s_no": 4, "category_key": "unloading", "category_name": "Unloading Charges (\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Unloading Charges", "category_name_ta": "\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "Unloading Charges   200", "amount": 200, "is_expense": true}, {"s_no": 5, "category_key": "toll", "category_name": "Toll / Fastag (\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd)", "category_name_en": "Toll / Fastag", "category_name_ta": "\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd", "detected_text": "4   Toll Charges   850", "amount": 850, "is_expense": true}, {"s_no": 6, "category_key": "diesel", "category_name": "Diesel / Fuel (\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Diesel / Fuel", "category_name_ta": "\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "5   Fuel   Diesel   6,350", "amount": 6350, "is_expense": true}, {"s_no": 7, "category_key": "parking", "category_name": "Parking (\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd)", "category_name_en": "Parking", "category_name_ta": "\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd", "detected_text": "Other Expenses   Parking ]   Tea   etc   600", "amount": 600, "is_expense": true}, {"s_no": 8, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026", "amount": 2026, "is_expense": false}, {"s_no": 9, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Advance Taken   5,000   Trip   Status   Completed", "amount": 5000, "is_expense": false}, {"s_no": 10, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik", "amount": 500, "is_expense": false}], "table_columns": [{"key": "s_no", "label_en": "S.No", "label_ta": "\\u0bb5.\\u0b8e\\u0ba3\\u0bcd", "width": 8}, {"key": "category_name_ta", "label_en": "Category (Tamil)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0ba4\\u0bae\\u0bbf\\u0bb4\\u0bcd)", "width": 25}, {"key": "category_name_en", "label_en": "Category (English)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0b86\\u0b99\\u0bcd\\u0b95\\u0bbf\\u0bb2\\u0bae\\u0bcd)", "width": 25}, {"key": "detected_text", "label_en": "Original Text from Memo", "label_ta": "\\u0bae\\u0bc6\\u0bae\\u0bcb\\u0bb5\\u0bbf\\u0bb2\\u0bcd \\u0b89\\u0bb3\\u0bcd\\u0bb3 \\u0b9a\\u0bca\\u0bb2\\u0bcd", "width": 35}, {"key": "amount", "label_en": "Amount (INR)", "label_ta": "\\u0ba4\\u0bca\\u0b95\\u0bc8 (\\u0bb0\\u0bc2)", "width": 18}, {"key": "is_expense", "label_en": "Classification", "label_ta": "\\u0baa\\u0bbf\\u0bb0\\u0bbf\\u0bb5\\u0bc1", "width": 15}], "memo_model": "TRIP_MEMO", "financial_summary": {"freight_amount": 20026.0, "advance_amount": 5500.0, "diesel_expense": 6350.0, "toll_expense": 850.0, "food_expense": 0.0, "loading_charges": 500.0, "unloading_charges": 200.0, "other_expenses": 9100.0, "total_expense": 17000.0, "handwritten_total": 12500.0, "net_profit": 3026.0, "driver_balance": -2474.0, "math_consistent": false, "math_variance": 4500.0}}', 'VERIFIED', 1.0, 'Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K', '', 0.0, 0.0, '');
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (6, 'MEMO-202609071443', 1, NULL, 'TN 21 AJ 1234', NULL, '2026-09-07', 'Coimbalore', 'Salem', 2026.0, 500.0, 17600.0, -15574.0, -16074.0, 'Loss', 'uploads/memos/memo_DRV-001_1788772356.png', 'Date   24/08 _   2026   Vehicle No.   TN   21   AJ   1234   Driver Name   R. Karthik 

 From   Coimbalore   To   Chennai   Via   Salem   Ve llore 

 Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k 

 Consignee Name   Sri   Balaji   Textiles   Consignor Name   Kovai   Texliles 

 SI. No:   Particulars   Amount (?) 

 Freight Charges   18,000 

 2   Loading Charges   1   500 

 Unloading Charges   200 

 4   Toll Charges   850 

 5   Fuel   Diesel   6,350 

 Driver Allowance   0o0 

 Other Expenses   Parking ]   Tea   etc   600 

 Total Expenses (A)   12,500 

 Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026 

 Advance Taken   5,000   Trip   Status   Completed 

 Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik 

 Remarks   Goods   delivered   in   Jood   Condition 

 Owner / Transport Signature   3   Muwae', '2026-09-07 09:16:12.670936', '2026-09-07 09:16:12.670943', 'uploads/memos/memo_DRV-001_1788772356_enhanced.png', '{"memo_number": "MEMO-202609071443", "date": "2026-09-07", "vehicle_number": "TN 21 AJ 1234", "driver_name": null, "driver_phone": null, "owner_name": null, "from_place": "Coimbalore", "to_place": "Salem", "starting_location": "Coimbalore", "destination": "Salem", "material": "Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K", "load_quantity": null, "quantity_unit": null, "starting_km": null, "ending_km": null, "total_km": null, "fuel_quantity": null, "fuel_expense": 5.0, "toll_expense": 4.0, "loading_charge": 2.0, "unloading_charge": 200.0, "driver_advance": 5000.0, "food_expense": 600.0, "parking_expense": 600.0, "repair_expense": null, "other_expense": 9100.0, "total_expense": 12500.0, "trip_amount": 18000.0, "freight_amount": 18000.0, "balance_amount": 500.0, "remarks": null, "confidence": {"vehicle_number": 0.98, "date": 0.5, "from_place": 0.94, "to_place": 0.94, "memo_number": 0.65, "material": 0.88, "trip_amount": 0.96, "loading_charge": 0.91, "unloading_charge": 0.91, "toll_expense": 0.94, "fuel_expense": 0.95, "food_expense": 0.92, "parking_expense": 0.9, "total_expense": 0.95, "driver_advance": 0.94, "other_expense": 0.85}, "table_rows": [{"s_no": 1, "category_key": "other", "category_name": "Other Expenses (\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Other Expenses", "category_name_ta": "\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k", "amount": 8500, "is_expense": true}, {"s_no": 2, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Charges   18,000", "amount": 18000, "is_expense": false}, {"s_no": 3, "category_key": "loading", "category_name": "Loading Charges (\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Loading Charges", "category_name_ta": "\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "2   Loading Charges   1   500", "amount": 500, "is_expense": true}, {"s_no": 4, "category_key": "unloading", "category_name": "Unloading Charges (\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Unloading Charges", "category_name_ta": "\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "Unloading Charges   200", "amount": 200, "is_expense": true}, {"s_no": 5, "category_key": "toll", "category_name": "Toll / Fastag (\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd)", "category_name_en": "Toll / Fastag", "category_name_ta": "\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd", "detected_text": "4   Toll Charges   850", "amount": 850, "is_expense": true}, {"s_no": 6, "category_key": "diesel", "category_name": "Diesel / Fuel (\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Diesel / Fuel", "category_name_ta": "\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "5   Fuel   Diesel   6,350", "amount": 6350, "is_expense": true}, {"s_no": 7, "category_key": "parking", "category_name": "Parking (\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd)", "category_name_en": "Parking", "category_name_ta": "\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd", "detected_text": "Other Expenses   Parking ]   Tea   etc   600", "amount": 600, "is_expense": true}, {"s_no": 8, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026", "amount": 2026, "is_expense": false}, {"s_no": 9, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Advance Taken   5,000   Trip   Status   Completed", "amount": 5000, "is_expense": false}, {"s_no": 10, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik", "amount": 500, "is_expense": false}], "table_columns": [{"key": "s_no", "label_en": "S.No", "label_ta": "\\u0bb5.\\u0b8e\\u0ba3\\u0bcd", "width": 8}, {"key": "category_name_ta", "label_en": "Category (Tamil)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0ba4\\u0bae\\u0bbf\\u0bb4\\u0bcd)", "width": 25}, {"key": "category_name_en", "label_en": "Category (English)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0b86\\u0b99\\u0bcd\\u0b95\\u0bbf\\u0bb2\\u0bae\\u0bcd)", "width": 25}, {"key": "detected_text", "label_en": "Original Text from Memo", "label_ta": "\\u0bae\\u0bc6\\u0bae\\u0bcb\\u0bb5\\u0bbf\\u0bb2\\u0bcd \\u0b89\\u0bb3\\u0bcd\\u0bb3 \\u0b9a\\u0bca\\u0bb2\\u0bcd", "width": 35}, {"key": "amount", "label_en": "Amount (INR)", "label_ta": "\\u0ba4\\u0bca\\u0b95\\u0bc8 (\\u0bb0\\u0bc2)", "width": 18}, {"key": "is_expense", "label_en": "Classification", "label_ta": "\\u0baa\\u0bbf\\u0bb0\\u0bbf\\u0bb5\\u0bc1", "width": 15}], "memo_model": "TRIP_MEMO", "financial_summary": {"freight_amount": 20026.0, "advance_amount": 5500.0, "diesel_expense": 6350.0, "toll_expense": 850.0, "food_expense": 0.0, "loading_charges": 500.0, "unloading_charges": 200.0, "other_expenses": 9100.0, "total_expense": 17000.0, "handwritten_total": 12500.0, "net_profit": 3026.0, "driver_balance": -2474.0, "math_consistent": false, "math_variance": 4500.0}}', 'VERIFIED', 1.0, 'Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K', '', 0.0, 0.0, '');
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (7, 'MEMO-202609081021', 1, NULL, 'TN 21 AJ 1234', NULL, '2026-09-08', 'Coimbalore', 'Salem', 2026.0, 500.0, 17600.0, -15574.0, -16074.0, 'Loss', 'uploads/memos/memo_DRV-001_1788843027.png', 'Date   24/08 _   2026   Vehicle No.   TN   21   AJ   1234   Driver Name   R. Karthik 

 From   Coimbalore   To   Chennai   Via   Salem   Ve llore 

 Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k 

 Consignee Name   Sri   Balaji   Textiles   Consignor Name   Kovai   Texliles 

 SI. No:   Particulars   Amount (?) 

 Freight Charges   18,000 

 2   Loading Charges   1   500 

 Unloading Charges   200 

 4   Toll Charges   850 

 5   Fuel   Diesel   6,350 

 Driver Allowance   0o0 

 Other Expenses   Parking ]   Tea   etc   600 

 Total Expenses (A)   12,500 

 Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026 

 Advance Taken   5,000   Trip   Status   Completed 

 Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik 

 Remarks   Goods   delivered   in   Jood   Condition 

 Owner / Transport Signature   3   Muwae', '2026-09-08 04:51:32.982568', '2026-09-08 04:51:32.982574', 'uploads/memos/memo_DRV-001_1788843027_enhanced.png', '{"memo_number": "MEMO-202609081021", "date": "2026-09-08", "vehicle_number": "TN 21 AJ 1234", "driver_name": null, "driver_phone": null, "owner_name": null, "from_place": "Coimbalore", "to_place": "Salem", "starting_location": "Coimbalore", "destination": "Salem", "material": "Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K", "load_quantity": null, "quantity_unit": null, "starting_km": null, "ending_km": null, "total_km": null, "fuel_quantity": null, "fuel_expense": 5.0, "toll_expense": 4.0, "loading_charge": 2.0, "unloading_charge": 200.0, "driver_advance": 5000.0, "food_expense": 600.0, "parking_expense": 600.0, "repair_expense": null, "other_expense": 9100.0, "total_expense": 12500.0, "trip_amount": 18000.0, "freight_amount": 18000.0, "balance_amount": 500.0, "remarks": null, "confidence": {"vehicle_number": 0.98, "date": 0.5, "from_place": 0.94, "to_place": 0.94, "memo_number": 0.65, "material": 0.88, "trip_amount": 0.96, "loading_charge": 0.91, "unloading_charge": 0.91, "toll_expense": 0.94, "fuel_expense": 0.95, "food_expense": 0.92, "parking_expense": 0.9, "total_expense": 0.95, "driver_advance": 0.94, "other_expense": 0.85}, "table_rows": [{"s_no": 1, "category_key": "other", "category_name": "Other Expenses (\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Other Expenses", "category_name_ta": "\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k", "amount": 8500, "is_expense": true}, {"s_no": 2, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Charges   18,000", "amount": 18000, "is_expense": false}, {"s_no": 3, "category_key": "loading", "category_name": "Loading Charges (\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Loading Charges", "category_name_ta": "\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "2   Loading Charges   1   500", "amount": 500, "is_expense": true}, {"s_no": 4, "category_key": "unloading", "category_name": "Unloading Charges (\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Unloading Charges", "category_name_ta": "\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "Unloading Charges   200", "amount": 200, "is_expense": true}, {"s_no": 5, "category_key": "toll", "category_name": "Toll / Fastag (\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd)", "category_name_en": "Toll / Fastag", "category_name_ta": "\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd", "detected_text": "4   Toll Charges   850", "amount": 850, "is_expense": true}, {"s_no": 6, "category_key": "diesel", "category_name": "Diesel / Fuel (\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Diesel / Fuel", "category_name_ta": "\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "5   Fuel   Diesel   6,350", "amount": 6350, "is_expense": true}, {"s_no": 7, "category_key": "parking", "category_name": "Parking (\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd)", "category_name_en": "Parking", "category_name_ta": "\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd", "detected_text": "Other Expenses   Parking ]   Tea   etc   600", "amount": 600, "is_expense": true}, {"s_no": 8, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026", "amount": 2026, "is_expense": false}, {"s_no": 9, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Advance Taken   5,000   Trip   Status   Completed", "amount": 5000, "is_expense": false}, {"s_no": 10, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik", "amount": 500, "is_expense": false}, {"s_no": 11, "category_key": "other", "category_name": "Other Expenses (\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Other Expenses", "category_name_ta": "\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "Extra Expense", "amount": 0, "is_expense": true}], "table_columns": [{"key": "s_no", "label_en": "S.No", "label_ta": "\\u0bb5.\\u0b8e\\u0ba3\\u0bcd", "width": 8}, {"key": "category_name_ta", "label_en": "Category (Tamil)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0ba4\\u0bae\\u0bbf\\u0bb4\\u0bcd)", "width": 25}, {"key": "category_name_en", "label_en": "Category (English)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0b86\\u0b99\\u0bcd\\u0b95\\u0bbf\\u0bb2\\u0bae\\u0bcd)", "width": 25}, {"key": "detected_text", "label_en": "Original Text from Memo", "label_ta": "\\u0bae\\u0bc6\\u0bae\\u0bcb\\u0bb5\\u0bbf\\u0bb2\\u0bcd \\u0b89\\u0bb3\\u0bcd\\u0bb3 \\u0b9a\\u0bca\\u0bb2\\u0bcd", "width": 35}, {"key": "amount", "label_en": "Amount (INR)", "label_ta": "\\u0ba4\\u0bca\\u0b95\\u0bc8 (\\u0bb0\\u0bc2)", "width": 18}, {"key": "is_expense", "label_en": "Classification", "label_ta": "\\u0baa\\u0bbf\\u0bb0\\u0bbf\\u0bb5\\u0bc1", "width": 15}], "memo_model": "TRIP_MEMO", "financial_summary": {"freight_amount": 20026.0, "advance_amount": 5500.0, "diesel_expense": 6350.0, "toll_expense": 850.0, "food_expense": 0.0, "loading_charges": 500.0, "unloading_charges": 200.0, "other_expenses": 9100.0, "total_expense": 17000.0, "handwritten_total": 12500.0, "net_profit": 3026.0, "driver_balance": -2474.0, "math_consistent": false, "math_variance": 4500.0}}', 'VERIFIED', 1.0, 'Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K', '', 0.0, 0.0, '');
INSERT INTO `memos` (`id`, `memo_number`, `driver_id`, `vehicle_id`, `vehicle_number_text`, `customer_id`, `memo_date`, `source`, `destination`, `freight_amount`, `advance_amount`, `total_expense`, `profit`, `net_amount`, `status`, `memo_file_path`, `ocr_raw_text`, `created_at`, `updated_at`, `enhanced_image_path`, `extracted_json`, `verification_status`, `confidence_score`, `material`, `load_quantity`, `start_km`, `end_km`, `driver_phone`) VALUES (8, 'MEMO-202609081216', 1, NULL, 'TN 21 AJ 1234', NULL, '2026-09-08', 'Coimbalore', 'Salem', 2026.0, 500.0, 17600.0, -15574.0, -16074.0, 'Loss', 'uploads/memos/memo_DRV-001_1788849964.png', 'Date   24/08 _   2026   Vehicle No.   TN   21   AJ   1234   Driver Name   R. Karthik 

 From   Coimbalore   To   Chennai   Via   Salem   Ve llore 

 Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k 

 Consignee Name   Sri   Balaji   Textiles   Consignor Name   Kovai   Texliles 

 SI. No:   Particulars   Amount (?) 

 Freight Charges   18,000 

 2   Loading Charges   1   500 

 Unloading Charges   200 

 4   Toll Charges   850 

 5   Fuel   Diesel   6,350 

 Driver Allowance   0o0 

 Other Expenses   Parking ]   Tea   etc   600 

 Total Expenses (A)   12,500 

 Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026 

 Advance Taken   5,000   Trip   Status   Completed 

 Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik 

 Remarks   Goods   delivered   in   Jood   Condition 

 Owner / Transport Signature   3   Muwae', '2026-09-08 06:46:41.119935', '2026-09-08 06:46:41.119967', 'uploads/memos/memo_DRV-001_1788849964_enhanced.png', '{"memo_number": "MEMO-202609081216", "date": "2026-09-08", "vehicle_number": "TN 21 AJ 1234", "driver_name": null, "driver_phone": null, "owner_name": null, "from_place": "Coimbalore", "to_place": "Salem", "starting_location": "Coimbalore", "destination": "Salem", "material": "Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K", "load_quantity": null, "quantity_unit": null, "starting_km": null, "ending_km": null, "total_km": null, "fuel_quantity": null, "fuel_expense": 5.0, "toll_expense": 4.0, "loading_charge": 2.0, "unloading_charge": 200.0, "driver_advance": 5000.0, "food_expense": 600.0, "parking_expense": 600.0, "repair_expense": null, "other_expense": 9100.0, "total_expense": 12500.0, "trip_amount": 18000.0, "freight_amount": 18000.0, "balance_amount": 500.0, "remarks": null, "confidence": {"vehicle_number": 0.98, "date": 0.5, "from_place": 0.94, "to_place": 0.94, "memo_number": 0.65, "material": 0.88, "trip_amount": 0.96, "loading_charge": 0.91, "unloading_charge": 0.91, "toll_expense": 0.94, "fuel_expense": 0.95, "food_expense": 0.92, "parking_expense": 0.9, "total_expense": 0.95, "driver_advance": 0.94, "other_expense": 0.85}, "table_rows": [{"s_no": 1, "category_key": "other", "category_name": "Other Expenses (\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Other Expenses", "category_name_ta": "\\u0b87\\u0ba4\\u0bb0 \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "Particulars of Goods   Textile   Rolls   No. of Packages   32   Weight   8500 k", "amount": 8500, "is_expense": true}, {"s_no": 2, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Charges   18,000", "amount": 18000, "is_expense": false}, {"s_no": 3, "category_key": "loading", "category_name": "Loading Charges (\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Loading Charges", "category_name_ta": "\\u0b8f\\u0bb1\\u0bcd\\u0bb1\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "2   Loading Charges   1   500", "amount": 500, "is_expense": true}, {"s_no": 4, "category_key": "unloading", "category_name": "Unloading Charges (\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf)", "category_name_en": "Unloading Charges", "category_name_ta": "\\u0b87\\u0bb1\\u0b95\\u0bcd\\u0b95\\u0bc1 \\u0b95\\u0bc2\\u0bb2\\u0bbf", "detected_text": "Unloading Charges   200", "amount": 200, "is_expense": true}, {"s_no": 5, "category_key": "toll", "category_name": "Toll / Fastag (\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd)", "category_name_en": "Toll / Fastag", "category_name_ta": "\\u0b9a\\u0bc1\\u0b99\\u0bcd\\u0b95\\u0bae\\u0bcd / \\u0b9f\\u0bcb\\u0bb2\\u0bcd\\u0b95\\u0bc7\\u0b9f\\u0bcd", "detected_text": "4   Toll Charges   850", "amount": 850, "is_expense": true}, {"s_no": 6, "category_key": "diesel", "category_name": "Diesel / Fuel (\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1)", "category_name_en": "Diesel / Fuel", "category_name_ta": "\\u0b9f\\u0bc0\\u0b9a\\u0bb2\\u0bcd \\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1", "detected_text": "5   Fuel   Diesel   6,350", "amount": 6350, "is_expense": true}, {"s_no": 7, "category_key": "parking", "category_name": "Parking (\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd)", "category_name_en": "Parking", "category_name_ta": "\\u0baa\\u0bbe\\u0bb0\\u0bcd\\u0b95\\u0bcd\\u0b95\\u0bbf\\u0b99\\u0bcd", "detected_text": "Other Expenses   Parking ]   Tea   etc   600", "amount": 600, "is_expense": true}, {"s_no": 8, "category_key": "freight", "category_name": "Agreed Freight (\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8)", "category_name_en": "Agreed Freight", "category_name_ta": "\\u0bb2\\u0bbe\\u0bb0\\u0bbf \\u0bb5\\u0bbe\\u0b9f\\u0b95\\u0bc8", "detected_text": "Freight Collected (B)   18   0do | -   Trip   Completed on   24/o8   2026", "amount": 2026, "is_expense": false}, {"s_no": 9, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Advance Taken   5,000   Trip   Status   Completed", "amount": 5000, "is_expense": false}, {"s_no": 10, "category_key": "advance", "category_name": "Advance Paid (\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd)", "category_name_en": "Advance Paid", "category_name_ta": "\\u0bae\\u0bc1\\u0ba9\\u0bcd\\u0baa\\u0ba3\\u0bae\\u0bcd", "detected_text": "Balance Receivable (C) [B   (A   Advance)]   500   Signature of Driver   RRKarthik", "amount": 500, "is_expense": false}], "table_columns": [{"key": "s_no", "label_en": "S.No", "label_ta": "\\u0bb5.\\u0b8e\\u0ba3\\u0bcd", "width": 8}, {"key": "category_name_ta", "label_en": "Category (Tamil)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0ba4\\u0bae\\u0bbf\\u0bb4\\u0bcd)", "width": 25}, {"key": "category_name_en", "label_en": "Category (English)", "label_ta": "\\u0b9a\\u0bc6\\u0bb2\\u0bb5\\u0bc1 \\u0bb5\\u0b95\\u0bc8 (\\u0b86\\u0b99\\u0bcd\\u0b95\\u0bbf\\u0bb2\\u0bae\\u0bcd)", "width": 25}, {"key": "detected_text", "label_en": "Original Text from Memo", "label_ta": "\\u0bae\\u0bc6\\u0bae\\u0bcb\\u0bb5\\u0bbf\\u0bb2\\u0bcd \\u0b89\\u0bb3\\u0bcd\\u0bb3 \\u0b9a\\u0bca\\u0bb2\\u0bcd", "width": 35}, {"key": "amount", "label_en": "Amount (INR)", "label_ta": "\\u0ba4\\u0bca\\u0b95\\u0bc8 (\\u0bb0\\u0bc2)", "width": 18}, {"key": "is_expense", "label_en": "Classification", "label_ta": "\\u0baa\\u0bbf\\u0bb0\\u0bbf\\u0bb5\\u0bc1", "width": 15}], "memo_model": "TRIP_MEMO", "financial_summary": {"freight_amount": 20026.0, "advance_amount": 5500.0, "diesel_expense": 6350.0, "toll_expense": 850.0, "food_expense": 0.0, "loading_charges": 500.0, "unloading_charges": 200.0, "other_expenses": 9100.0, "total_expense": 17000.0, "handwritten_total": 12500.0, "net_profit": 3026.0, "driver_balance": -2474.0, "math_consistent": false, "math_variance": 4500.0}}', 'VERIFIED', 1.0, 'Particulars Of Goods   Textile   Rolls   No. Of Packages   32   Weight   8500 K', '', 0.0, 0.0, '');

-- ----------------------------------------------------------------------
-- Table structure and data for `memo_expenses`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `memo_expenses`;
CREATE TABLE IF NOT EXISTS `memo_expenses` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `memo_id` INT NOT NULL UNIQUE,
    `diesel_expense` DOUBLE DEFAULT 0.0,
    `toll_expense` DOUBLE DEFAULT 0.0,
    `food_expense` DOUBLE DEFAULT 0.0,
    `loading_charges` DOUBLE DEFAULT 0.0,
    `unloading_charges` DOUBLE DEFAULT 0.0,
    `other_expenses` DOUBLE DEFAULT 0.0,
    `other_notes` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_memo_expenses_memo` FOREIGN KEY (`memo_id`) REFERENCES `memos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `memo_expenses` (8 records)
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (1, 1, 21500.0, 3200.0, 2200.0, 3000.0, 2000.0, 500.0, 'Puncture repair at Tindivanam', '2026-09-04 05:15:39.605608');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (2, 2, 12500.0, 1600.0, 1400.0, 1500.0, 1200.0, 300.0, 'Weighbridge slip', '2026-09-04 05:15:39.607240');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (3, 3, 31000.0, 4800.0, 2800.0, 3200.0, 2600.0, 800.0, 'Emergency radiator hose fix', '2026-09-04 05:15:39.609151');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (4, 4, 21500.0, 3200.0, 2200.0, 3000.0, 2000.0, 500.0, '', '2026-09-04 08:38:36.624952');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (5, 5, 6350.0, 850.0, 600.0, 500.0, 200.0, 9100.0, 'Parking: ₹600.0', '2026-09-07 06:49:37.907144');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (6, 6, 6350.0, 850.0, 600.0, 500.0, 200.0, 9100.0, 'Parking: ₹600.0', '2026-09-07 09:16:12.679345');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (7, 7, 6350.0, 850.0, 600.0, 500.0, 200.0, 9100.0, 'Parking: ₹600.0', '2026-09-08 04:51:32.996779');
INSERT INTO `memo_expenses` (`id`, `memo_id`, `diesel_expense`, `toll_expense`, `food_expense`, `loading_charges`, `unloading_charges`, `other_expenses`, `other_notes`, `created_at`) VALUES (8, 8, 6350.0, 850.0, 600.0, 500.0, 200.0, 9100.0, 'Parking: ₹600.0', '2026-09-08 06:46:41.126352');

-- ----------------------------------------------------------------------
-- Table structure and data for `fuel_bills`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `fuel_bills`;
CREATE TABLE IF NOT EXISTS `fuel_bills` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `driver_id` INT NOT NULL,
    `vehicle_id` INT DEFAULT NULL,
    `memo_id` INT DEFAULT NULL,
    `fuel_station_name` VARCHAR(200) NOT NULL,
    `bill_number` VARCHAR(100) DEFAULT NULL,
    `bill_date` DATE NOT NULL,
    `bill_time` TIME DEFAULT NULL,
    `fuel_quantity` DOUBLE NOT NULL,
    `rate_per_liter` DOUBLE DEFAULT 0.0,
    `total_amount` DOUBLE NOT NULL,
    `bill_file_path` VARCHAR(255) DEFAULT NULL,
    `ocr_raw_text` LONGTEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    KEY `idx_fuel_driver` (`driver_id`),
    KEY `idx_fuel_vehicle` (`vehicle_id`),
    KEY `idx_fuel_memo` (`memo_id`),
    CONSTRAINT `fk_fuel_driver` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_fuel_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_fuel_memo` FOREIGN KEY (`memo_id`) REFERENCES `memos` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `fuel_bills` (9 records)
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (1, 1, 1, 1, 'Indian Oil Corporation - Tindivanam Bypass', 'IOCL-B7721', '2026-08-23', NULL, 180.0, 95.5, 17190.0, 'sample_memos/sample_fuel_bill_1.png', NULL, '2026-09-04 05:15:39.625691');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (2, 1, 1, 1, 'Bharat Petroleum - Chengalpattu', 'BPCL-99014', '2026-08-24', NULL, 45.0, 95.8, 4311.0, 'sample_memos/sample_fuel_bill_2.png', NULL, '2026-09-04 05:15:39.625696');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (3, 2, 2, 3, 'HPCL Oasis Express - Madurai Ring Road', 'HPCL-6652', '2026-09-02', NULL, 320.0, 96.0, 30720.0, 'sample_memos/sample_fuel_bill_3.png', NULL, '2026-09-04 05:15:39.625697');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (4, 1, NULL, NULL, 'Volume (L)', 'FB-202609041341', '2026-09-04', '12:00:00.000000', 150.0, 96.0, 14400.0, 'uploads/fuel_bills/fuel_DRV-001_1788509474.jpeg', 'Volume (L) 

 Rate (? /L) 

 Rate (? /L) 

 Tonei 

 Petrol Diesel 

 ''iRe 

 M0 

 9 

 8 

 Amount 

 ensity{ 

 FthS SALE 

 ~FiLLiNG +', '2026-09-04 08:12:03.895301');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (5, 1, NULL, NULL, 'Volume (L)', 'FB-202609041343', '2026-09-04', '12:00:00.000000', 150.0, 96.0, 14400.0, 'uploads/fuel_bills/fuel_DRV-001_1788509590.jpeg', 'Volume (L) 

 Rate (? /L) 

 Rate (? /L) 

 Tonei 

 Petrol Diesel 

 ''iRe 

 M0 

 9 

 8 

 Amount 

 ensity{ 

 FthS SALE 

 ~FiLLiNG +', '2026-09-04 08:13:43.077311');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (6, 1, NULL, NULL, 'Hant', 'FB-202609071257', '2026-09-07', '12:57:00.000000', 1.0, 81.0, 81.0, 'uploads/fuel_bills/fuel_DRV-001_1788766013.jpeg', 'Hant 

 SSO1g 

 @8 

 8 

 6 

 E 

 Txe 

 E 

 2 

 1 

 2 

 81 

 ! 

 1 

 ! 

 1', '2026-09-07 07:27:58.245657');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (7, 1, NULL, NULL, 'Hant', 'FB-202609071258', '2026-09-07', '12:58:00.000000', 1.0, 81.0, 81.0, 'uploads/fuel_bills/fuel_DRV-001_1788766097.jpeg', 'Hant 

 SSO1g 

 @8 

 8 

 6 

 E 

 Txe 

 E 

 2 

 1 

 2 

 81 

 ! 

 1 

 ! 

 1', '2026-09-07 07:28:43.901269');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (8, 1, NULL, NULL, 'Hant', 'FB-202609071449', '2026-09-07', '14:49:00.000000', 1.0, 81.0, 81.0, 'uploads/fuel_bills/fuel_DRV-001_1788772751.jpeg', 'Hant 

 SSO1g 

 @8 

 8 

 6 

 E 

 Txe 

 E 

 2 

 1 

 2 

 81 

 ! 

 1 

 ! 

 1', '2026-09-07 09:21:20.676977');
INSERT INTO `fuel_bills` (`id`, `driver_id`, `vehicle_id`, `memo_id`, `fuel_station_name`, `bill_number`, `bill_date`, `bill_time`, `fuel_quantity`, `rate_per_liter`, `total_amount`, `bill_file_path`, `ocr_raw_text`, `created_at`) VALUES (9, 1, NULL, NULL, 'Hant', 'FB-202609071528', '2026-09-07', '15:28:00.000000', 1.0, 81.0, 81.0, 'uploads/fuel_bills/fuel_DRV-001_1788775066.jpeg', 'Hant 

 SSO1g 

 @8 

 8 

 6 

 E 

 Txe 

 E 

 2 

 1 

 2 

 81 

 ! 

 1 

 ! 

 1', '2026-09-07 09:58:06.800513');

-- ----------------------------------------------------------------------
-- Table structure and data for `otp_codes`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `otp_codes`;
CREATE TABLE IF NOT EXISTS `otp_codes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(150) NOT NULL,
    `otp_code` VARCHAR(10) NOT NULL,
    `purpose` VARCHAR(50) DEFAULT 'LOGIN',
    `expires_at` DATETIME NOT NULL,
    `is_used` TINYINT(1) DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `otp_codes` (14 records)
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (1, 'murugan@truck.com', '452593', 'LOGIN', '2026-09-04 06:06:11.066437', 1, '2026-09-04 05:56:11.086924');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (2, 'murugan@truck.com', '660332', 'LOGIN', '2026-09-04 06:31:40.010549', 0, '2026-09-04 06:21:40.012898');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (3, 'admin@truck.com', '706333', 'ADMIN_LOGIN', '2026-09-08 14:16:23.042269', 1, '2026-09-08 14:06:23.050384');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (4, 'stharanisamp@gmail.com', '513128', 'REGISTRATION', '2026-09-08 14:19:38.540841', 1, '2026-09-08 14:09:38.555573');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (5, 'stharanisamp@gmail.com', '423943', 'REGISTRATION', '2026-09-08 15:41:46.273625', 1, '2026-09-08 15:31:46.317852');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (6, 'stharanisamp@gmail.com', '348799', 'REGISTRATION', '2026-09-08 15:56:41.337888', 1, '2026-09-08 15:46:41.367962');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (7, 'stharanisamp@gmail.com', '677780', 'REGISTRATION', '2026-09-08 15:56:43.174099', 1, '2026-09-08 15:46:43.182095');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (8, 'stharanisamp@gmail.com', '762391', 'REGISTRATION', '2026-09-08 15:56:47.981371', 1, '2026-09-08 15:46:47.991883');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (9, 'stharanisamp@gmail.com', '294622', 'REGISTRATION', '2026-09-08 16:04:18.772811', 1, '2026-09-08 15:54:18.800503');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (10, 'stharanisamp@gmail.com', '987971', 'ADMIN_LOGIN', '2026-09-08 17:07:23.969064', 1, '2026-09-08 16:57:23.981321');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (11, 'ambigaa075@gmail.com', '741698', 'ADMIN_LOGIN', '2026-09-08 17:12:19.733849', 1, '2026-09-08 17:02:19.743405');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (12, 'ambigaa075@gmail.com', '420871', 'ADMIN_LOGIN', '2026-09-08 17:13:39.363561', 1, '2026-09-08 17:03:39.375862');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (13, 'ambigaa075@gmail.com', '700113', 'ADMIN_LOGIN', '2026-09-08 17:15:28.599663', 1, '2026-09-08 17:05:28.628293');
INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `purpose`, `expires_at`, `is_used`, `created_at`) VALUES (14, 'stharanisamp@gmail.com', '397012', 'ADMIN_LOGIN', '2026-09-09 07:16:59.486242', 0, '2026-09-09 07:06:59.500854');

-- ----------------------------------------------------------------------
-- Table structure and data for `notifications`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `message` TEXT NOT NULL,
    `alert_type` VARCHAR(50) NOT NULL,
    `severity` VARCHAR(20) DEFAULT 'Normal',
    `is_read` TINYINT(1) DEFAULT 0,
    `link` VARCHAR(255) DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `notifications` (21 records)
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (1, 'Suspicious Fuel Consumption Warning', 'Vehicle TN 30 CD 5678 logged 320 Liters on Hosur to Tuticorin trip (Expected: 240 Liters). Discrepancy: +33.3% [High Risk].', 'FUEL_THEFT', 'High Risk', 0, '/admin/fuel-monitoring', '2026-09-04 05:15:39.638617');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (2, 'Vehicle Insurance Expiry Warning', 'Vehicle TN 30 CD 5678 insurance expires in 15 days (Policy # INS-ICICI-44332).', 'INSURANCE_EXPIRY', 'Warning', 0, '/admin/vehicles', '2026-09-04 05:15:39.638623');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (3, 'Vehicle Insurance Expired Alert', 'Vehicle TN 88 GH 3456 insurance expired 5 days ago! Immediate renewal required.', 'INSURANCE_EXPIRY', 'High Risk', 0, '/admin/vehicles', '2026-09-04 05:15:39.638625');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (4, 'Driver License Renewal Alert', 'Driver Karthik Pandian''s driving license expires in 20 days.', 'LICENSE_EXPIRY', 'Warning', 0, '/admin/drivers', '2026-09-04 05:15:39.638626');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (5, 'New Memo Uploaded', 'Driver Murugan Selvam uploaded trip memo MEMO-2026-002 (Salem -> Coimbatore).', 'NEW_MEMO', 'Normal', 1, '/admin/memos', '2026-09-04 05:15:39.638627');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (6, 'Fuel Bill Uploaded', 'Driver Murugan Selvam logged fuel bill FB-202609041341 (150.0 L, Rs. 14400.0) at Volume (L).', 'SYSTEM', 'Normal', 0, '/admin/fuel-monitoring', '2026-09-04 08:12:03.934346');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (7, 'Fuel Bill Uploaded', 'Driver Murugan Selvam logged fuel bill FB-202609041343 (150.0 L, Rs. 14400.0) at Volume (L).', 'SYSTEM', 'Normal', 0, '/admin/fuel-monitoring', '2026-09-04 08:13:43.085523');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (8, 'Fuel Anomaly Detected: High Risk', 'Trip MEMO-2026-001-116 (Ariyalur -> Chennai Harbour) by Murugan Selvam on vehicle TN 28 AB 1234: Actual Fuel 226.32 L vs Expected 100.0 L (+126.3%). Potential fuel pilferage!', 'FUEL_THEFT', 'High Risk', 0, '/admin/fuel-monitoring', '2026-09-04 08:38:36.629901');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (9, 'New Trip Memo Uploaded', 'Driver Murugan Selvam submitted memo MEMO-2026-001-116 for route Ariyalur -> Chennai Harbour. Status: Profit.', 'NEW_MEMO', 'Normal', 0, '/admin/memos/4', '2026-09-04 08:38:36.650619');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (10, 'New Verified Trip Memo Uploaded', 'Driver Murugan Selvam verified and submitted memo MEMO-202609071219 (Coimbalore -> Salem). Status: Loss.', 'NEW_MEMO', 'Normal', 0, '/admin/memos/5', '2026-09-07 06:49:37.916550');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (11, 'Fuel Bill Uploaded', 'Driver Murugan Selvam logged fuel bill FB-202609071257 (1.0 L, Rs. 81.0) at Hant.', 'SYSTEM', 'Normal', 0, '/admin/fuel-monitoring', '2026-09-07 07:27:58.253634');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (12, 'Fuel Bill Uploaded', 'Driver Murugan Selvam logged fuel bill FB-202609071258 (1.0 L, Rs. 81.0) at Hant.', 'SYSTEM', 'Normal', 0, '/admin/fuel-monitoring', '2026-09-07 07:28:43.904756');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (13, 'New Verified Trip Memo Uploaded', 'Driver Murugan Selvam verified and submitted memo MEMO-202609071443 (Coimbalore -> Salem). Status: Loss.', 'NEW_MEMO', 'Normal', 0, '/admin/memos/6', '2026-09-07 09:16:12.688997');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (14, 'Fuel Bill Uploaded', 'Driver Murugan Selvam logged fuel bill FB-202609071449 (1.0 L, Rs. 81.0) at Hant.', 'SYSTEM', 'Normal', 0, '/admin/fuel-monitoring', '2026-09-07 09:21:20.684915');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (15, 'Fuel Bill Uploaded', 'Driver Murugan Selvam logged fuel bill FB-202609071528 (1.0 L, Rs. 81.0) at Hant.', 'SYSTEM', 'Normal', 0, '/admin/fuel-monitoring', '2026-09-07 09:58:06.803981');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (16, 'New Verified Trip Memo Uploaded', 'Driver Murugan Selvam verified and submitted memo MEMO-202609081021 (Coimbalore -> Salem). Status: Loss.', 'NEW_MEMO', 'Normal', 0, '/admin/memos/7', '2026-09-08 04:51:33.004437');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (17, 'New Verified Trip Memo Uploaded', 'Driver Murugan Selvam verified and submitted memo MEMO-202609081216 (Coimbalore -> Salem). Status: Loss.', 'NEW_MEMO', 'Normal', 0, '/admin/memos/8', '2026-09-08 06:46:41.135527');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (18, 'New Driver Registered', 'Driver Raja Test (DRV-004) has completed email verification and registered.', 'NEW_DRIVER', 'Normal', 0, '/admin/drivers', '2026-09-08 11:05:44.023533');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (19, 'New Driver Registered', 'Driver Tharani (DRV-004) has completed email verification and registered.', 'NEW_DRIVER', 'Normal', 0, '/admin/drivers', '2026-09-08 14:46:48.937195');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (20, 'New Driver Registered', 'Driver Tharani (DRV-004) has completed email verification and registered.', 'NEW_DRIVER', 'Normal', 0, '/admin/drivers', '2026-09-08 14:47:13.781648');
INSERT INTO `notifications` (`id`, `title`, `message`, `alert_type`, `severity`, `is_read`, `link`, `created_at`) VALUES (21, 'New Driver Registered', 'Driver tharani (DRV-004) has completed email verification and registered.', 'NEW_DRIVER', 'Normal', 0, '/admin/drivers', '2026-09-08 15:54:53.021133');

-- ----------------------------------------------------------------------
-- Table structure and data for `activity_logs`
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS `activity_logs`;
CREATE TABLE IF NOT EXISTS `activity_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_type` VARCHAR(20) NOT NULL,
    `user_id` INT NOT NULL,
    `user_name` VARCHAR(150) DEFAULT NULL,
    `action` VARCHAR(100) NOT NULL,
    `details` TEXT,
    `ip_address` VARCHAR(50) DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `activity_logs` (56 records)
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (1, 'Admin', 1, 'Rajesh Transport Owner', 'System Init', 'Initialized Truck Maintenance System with seed records', NULL, '2026-09-04 05:15:39.657548');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (2, 'Driver', 1, 'Murugan Selvam', 'Upload Memo', 'Uploaded MEMO-2026-001', NULL, '2026-09-04 05:15:39.657555');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (3, 'Driver', 1, 'Murugan Selvam', 'Upload Fuel Bill', 'Uploaded IOCL-B7721 (180 L)', NULL, '2026-09-04 05:15:39.657556');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (4, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 05:27:52.775665');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (5, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 05:55:37.134243');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (6, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 05:55:48.534489');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (7, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 05:56:10.624964');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (8, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver verified OTP from 127.0.0.1', NULL, '2026-09-04 05:56:12.548305');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (9, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 06:08:53.131246');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (10, 'Admin', 1, 'Rajesh Transport Owner', 'Logout', 'User logged out successfully', NULL, '2026-09-04 06:20:10.616173');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (11, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 07:39:04.309542');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (12, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 07:39:04.737775');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (13, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 07:39:48.879502');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (14, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 07:39:49.381557');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (15, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 07:49:21.061789');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (16, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 08:38:17.434611');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (17, 'Driver', 1, 'Murugan Selvam', 'Upload Memo', 'Saved Memo MEMO-2026-001-116: Freight Rs.48000.0, Expenses Rs.32400.0, Profit Rs.15600.0 (Profit)', NULL, '2026-09-04 08:38:36.638173');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (18, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 08:39:12.288740');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (19, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 08:39:12.703329');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (20, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 08:39:58.281186');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (21, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-04 08:39:58.762151');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (22, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 09:29:20.242773');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (23, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 09:44:31.851573');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (24, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-04 09:56:22.607613');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (25, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-06 15:37:58.309517');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (26, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-06 15:53:45.971016');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (27, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 15:53:46.427932');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (28, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 15:57:07.692063');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (29, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 16:37:10.363790');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (30, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 16:38:10.162436');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (31, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 16:39:41.859359');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (32, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 16:40:13.331185');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (33, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-06 16:41:02.986849');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (34, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-07 06:48:23.288806');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (35, 'Driver', 1, 'Murugan Selvam', 'Upload & Verify Memo', 'Verified Memo MEMO-202609071219: Freight ₹2,026.00, Expenses ₹17,600.00, Net Profit ₹-15,574.00', NULL, '2026-09-07 06:49:37.914786');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (36, 'Driver', 1, 'Murugan Selvam', 'Upload & Verify Memo', 'Verified Memo MEMO-202609071443: Freight ₹2,026.00, Expenses ₹17,600.00, Net Profit ₹-15,574.00', NULL, '2026-09-07 09:16:12.687887');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (37, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-07 10:33:06.772165');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (38, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-08 04:49:54.942477');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (39, 'Driver', 1, 'Murugan Selvam', 'Upload & Verify Memo', 'Verified Memo MEMO-202609081021: Freight ₹2,026.00, Expenses ₹17,600.00, Net Profit ₹-15,574.00', NULL, '2026-09-08 04:51:33.003313');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (40, 'Driver', 1, 'Murugan Selvam', 'Upload & Verify Memo', 'Verified Memo MEMO-202609081216: Freight ₹2,026.00, Expenses ₹17,600.00, Net Profit ₹-15,574.00', NULL, '2026-09-08 06:46:41.133759');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (41, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-08 11:04:04.013159');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (42, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in from 127.0.0.1', NULL, '2026-09-08 11:04:04.213543');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (43, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-08 11:05:43.630735');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (44, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in from 127.0.0.1', NULL, '2026-09-08 11:05:43.798188');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (45, 'Driver', 4, 'Raja Test', 'Driver Login', 'Driver logged in from 127.0.0.1', NULL, '2026-09-08 11:05:44.354330');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (46, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in from 127.0.0.1', NULL, '2026-09-08 13:49:57.092922');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (47, 'Driver', 1, 'Murugan Selvam', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-08 14:06:23.027682');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (48, 'Admin', 1, 'Rajesh Transport Owner', 'Admin Login', 'Admin logged in with 2FA OTP from 127.0.0.1', NULL, '2026-09-08 14:06:23.217850');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (49, 'Driver', 0, 'Tharani', 'Driver Registered', 'Driver registered and verified via email OTP from 127.0.0.1', NULL, '2026-09-08 14:46:48.932914');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (50, 'Admin', 2, 'Tharani Admin Fleet Owner', 'Admin Registered', 'Admin account created and verified from 127.0.0.1', NULL, '2026-09-08 14:46:49.197018');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (51, 'Driver', 0, 'Tharani', 'Driver Registered', 'Driver registered and verified via email OTP from 127.0.0.1', NULL, '2026-09-08 14:47:13.777134');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (52, 'Admin', 2, 'Tharani Admin Fleet Owner', 'Admin Registered', 'Admin account created and verified from 127.0.0.1', NULL, '2026-09-08 14:47:14.039159');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (53, 'Driver', 0, 'tharani', 'Driver Registered', 'Driver registered and verified via email OTP from 127.0.0.1', NULL, '2026-09-08 15:54:53.012418');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (54, 'Admin', 2, 'Ambiga (Fleet Owner)', 'Admin Login', 'Admin logged in with 2FA OTP from 127.0.0.1', NULL, '2026-09-08 17:03:26.621830');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (55, 'Admin', 2, 'Ambiga (Fleet Owner)', 'Admin Login', 'Admin logged in with 2FA OTP from 127.0.0.1', NULL, '2026-09-08 17:05:50.387040');
INSERT INTO `activity_logs` (`id`, `user_type`, `user_id`, `user_name`, `action`, `details`, `ip_address`, `created_at`) VALUES (56, 'Driver', 4, 'tharani', 'Driver Login', 'Driver logged in directly from 127.0.0.1', NULL, '2026-09-09 07:12:00.866226');

SET FOREIGN_KEY_CHECKS = 1;
-- ========================== END OF FILE ================================
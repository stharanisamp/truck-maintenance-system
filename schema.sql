-- Truck Maintenance System MySQL Database Schema
-- Database: truck_maintenance_system

CREATE DATABASE IF NOT EXISTS `truck_maintenance_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `truck_maintenance_system`;

-- 1. Admins Table
CREATE TABLE IF NOT EXISTS `admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(150) NOT NULL,
    `phone` VARCHAR(20),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Drivers Table
CREATE TABLE IF NOT EXISTS `drivers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `driver_code` VARCHAR(50) NOT NULL UNIQUE,
    `full_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(20) NOT NULL,
    `address` TEXT,
    `license_number` VARCHAR(100) NOT NULL UNIQUE,
    `date_of_birth` DATE,
    `joining_date` DATE,
    `password_hash` VARCHAR(255) NOT NULL,
    `profile_photo` VARCHAR(255) DEFAULT 'default_avatar.png',
    `status` ENUM('Active', 'Inactive', 'Suspended') DEFAULT 'Active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Vehicles Table
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
    `status` ENUM('Active', 'In Maintenance', 'In Trip', 'Inactive') DEFAULT 'Active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_vehicles_driver` FOREIGN KEY (`assigned_driver_id`) REFERENCES `drivers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Customers Table (Managed by respective driver)
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
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`driver_id`) REFERENCES `drivers`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Memos Table (Trip Records)
CREATE TABLE IF NOT EXISTS `memos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `memo_number` VARCHAR(100) NOT NULL UNIQUE,
    `driver_id` INT NOT NULL,
    `vehicle_id` INT,
    `vehicle_number_text` VARCHAR(50),
    `customer_id` INT,
    `memo_date` DATE NOT NULL,
    `source` VARCHAR(150) NOT NULL,
    `destination` VARCHAR(150) NOT NULL,
    `freight_amount` DECIMAL(12, 2) DEFAULT 0.00,
    `advance_amount` DECIMAL(12, 2) DEFAULT 0.00,
    `total_expense` DECIMAL(12, 2) DEFAULT 0.00,
    `profit` DECIMAL(12, 2) DEFAULT 0.00,
    `net_amount` DECIMAL(12, 2) DEFAULT 0.00,
    `status` ENUM('Profit', 'Loss') DEFAULT 'Profit',
    `memo_file_path` VARCHAR(255),
    `ocr_raw_text` LONGTEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`driver_id`) REFERENCES `drivers`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`customer_id`) REFERENCES `customers`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Memo Expenses Table
CREATE TABLE IF NOT EXISTS `memo_expenses` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `memo_id` INT NOT NULL UNIQUE,
    `diesel_expense` DECIMAL(12, 2) DEFAULT 0.00,
    `toll_expense` DECIMAL(12, 2) DEFAULT 0.00,
    `food_expense` DECIMAL(12, 2) DEFAULT 0.00,
    `loading_charges` DECIMAL(12, 2) DEFAULT 0.00,
    `unloading_charges` DECIMAL(12, 2) DEFAULT 0.00,
    `other_expenses` DECIMAL(12, 2) DEFAULT 0.00,
    `other_notes` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`memo_id`) REFERENCES `memos`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Fuel Bills Table
CREATE TABLE IF NOT EXISTS `fuel_bills` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `driver_id` INT NOT NULL,
    `vehicle_id` INT,
    `memo_id` INT,
    `fuel_station_name` VARCHAR(200) NOT NULL,
    `bill_number` VARCHAR(100),
    `bill_date` DATE NOT NULL,
    `bill_time` TIME,
    `fuel_quantity` DECIMAL(10, 2) NOT NULL, -- Liters
    `rate_per_liter` DECIMAL(10, 2) DEFAULT 0.00,
    `total_amount` DECIMAL(12, 2) NOT NULL,
    `bill_file_path` VARCHAR(255),
    `ocr_raw_text` LONGTEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`driver_id`) REFERENCES `drivers`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`memo_id`) REFERENCES `memos`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. OTP Codes Table
CREATE TABLE IF NOT EXISTS `otp_codes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(150) NOT NULL,
    `otp_code` VARCHAR(10) NOT NULL,
    `purpose` VARCHAR(50) DEFAULT 'LOGIN',
    `expires_at` DATETIME NOT NULL,
    `is_used` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Notifications Table
CREATE TABLE IF NOT EXISTS `notifications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `message` TEXT NOT NULL,
    `alert_type` ENUM('FUEL_THEFT', 'MISSING_BILL', 'OCR_FAILURE', 'INSURANCE_EXPIRY', 'LICENSE_EXPIRY', 'NEW_DRIVER', 'NEW_MEMO', 'SYSTEM') NOT NULL,
    `severity` ENUM('Normal', 'Warning', 'High Risk') DEFAULT 'Normal',
    `is_read` BOOLEAN DEFAULT FALSE,
    `link` VARCHAR(255),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Activity Logs Table
CREATE TABLE IF NOT EXISTS `activity_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_type` ENUM('Admin', 'Driver') NOT NULL,
    `user_id` INT NOT NULL,
    `user_name` VARCHAR(150),
    `action` VARCHAR(100) NOT NULL,
    `details` TEXT,
    `ip_address` VARCHAR(50),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

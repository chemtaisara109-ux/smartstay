-- ============================================
-- SmartStay Booking System Schema
-- PHP/MySQL Backend
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS smartstay_bookings;
USE smartstay_bookings;

-- Users table (guests and hosts)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20),
    role ENUM('guest', 'host') DEFAULT 'guest',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Properties table
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    max_guests INT DEFAULT 1,
    description TEXT,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_host_id (host_id),
    INDEX idx_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT NOT NULL,
    property_id INT NOT NULL,
    guest_name VARCHAR(100) NOT NULL,
    guest_email VARCHAR(120) NOT NULL,
    guest_phone VARCHAR(20),
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    guests INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    notes TEXT,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP NULL,
    FOREIGN KEY (guest_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    INDEX idx_guest_id (guest_id),
    INDEX idx_property_id (property_id),
    INDEX idx_status (status),
    INDEX idx_dates (check_in, check_out)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Host notifications table (for dashboard)
CREATE TABLE IF NOT EXISTS host_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    booking_id INT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    INDEX idx_host_id (host_id),
    INDEX idx_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data for testing
INSERT INTO users (name, email, phone, role) VALUES
('John Doe', 'guest@smartstay.com', '+1234567890', 'guest'),
('Jane Smith', 'host@smartstay.com', '+0987654321', 'host');

INSERT INTO properties (host_id, title, location, price, max_guests, description) VALUES
(2, 'Cozy Beach Villa', 'Malibu, CA', 250.00, 4, 'Beautiful beachfront villa with ocean views'),
(2, 'Mountain Cabin', 'Aspen, CO', 180.00, 6, 'Rustic cabin in the mountains with fireplace'),
(2, 'City Loft', 'New York, NY', 150.00, 2, 'Modern loft in the heart of Manhattan');

-- Sample bookings
INSERT INTO bookings (guest_id, property_id, guest_name, guest_email, guest_phone, check_in, check_out, guests, total_price, notes, status) VALUES
(1, 1, 'John Doe', 'guest@smartstay.com', '+1234567890', '2024-02-15', '2024-02-18', 2, 750.00, 'Looking forward to the beach!', 'confirmed');
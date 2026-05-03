-- SmartStay Database Schema (MySQL)
-- Create database and tables for user authentication and host registration

CREATE DATABASE IF NOT EXISTS smartstay_db;
USE smartstay_db;

-- Users table for registration and login
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'guest',
    phone VARCHAR(20),
    property_name VARCHAR(200),
    location VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_email ON users(email);
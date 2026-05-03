<?php
/**
 * Database Connection for SmartStay Booking System
 * PHP/MySQL Backend
 */

// Database configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'smartstay_bookings');
define('DB_CHARSET', 'utf8mb4');

// Create database connection
function getDBConnection() {
    try {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
        $pdo = new PDO($dsn, DB_USER, DB_PASS, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]);

        return $pdo;
    } catch (PDOException $e) {
        die("Database connection failed: " . $e->getMessage());
    }
}

// Test database connection
function testConnection() {
    try {
        $pdo = getDBConnection();
        return ["success" => true, "message" => "Database connected successfully"];
    } catch (Exception $e) {
        return ["success" => false, "message" => "Connection failed: " . $e->getMessage()];
    }
}

// Sanitize input data
function sanitizeInput($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// Validate email format
function validateEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
}

// Validate phone number (basic validation)
function validatePhone($phone) {
    return preg_match('/^[\+]?[1-9][\d]{0,15}$/', $phone);
}

// Validate date format and logic
function validateDates($check_in, $check_out) {
    $checkInDate = DateTime::createFromFormat('Y-m-d', $check_in);
    $checkOutDate = DateTime::createFromFormat('Y-m-d', $check_out);
    $today = new DateTime();

    if (!$checkInDate || !$checkOutDate) {
        return ["valid" => false, "message" => "Invalid date format"];
    }

    if ($checkInDate < $today) {
        return ["valid" => false, "message" => "Check-in date cannot be in the past"];
    }

    if ($checkOutDate <= $checkInDate) {
        return ["valid" => false, "message" => "Check-out date must be after check-in date"];
    }

    return ["valid" => true, "nights" => $checkInDate->diff($checkOutDate)->days];
}

// Calculate total price
function calculateTotalPrice($price_per_night, $nights, $guests) {
    $base_price = $price_per_night * $nights;
    $service_fee = $base_price * 0.12; // 12% service fee
    return $base_price + $service_fee;
}
?>
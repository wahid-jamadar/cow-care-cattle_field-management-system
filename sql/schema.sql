CREATE DATABASE IF NOT EXISTS cattle_health_db;
USE cattle_health_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('Farmer','Veterinarian') NOT NULL DEFAULT 'Farmer'
);

CREATE TABLE IF NOT EXISTS cattle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_tag VARCHAR(50) NOT NULL UNIQUE,
    breed VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    weight DECIMAL(10,2) NOT NULL,
    photo VARCHAR(255) DEFAULT NULL,
    owner_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(100) NOT NULL UNIQUE,
    device_serial VARCHAR(100) NOT NULL,
    cattle_id INT NOT NULL,
    install_date DATE NOT NULL,
    status ENUM('Active','Inactive','Maintenance') DEFAULT 'Active',
    FOREIGN KEY (cattle_id) REFERENCES cattle(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS health_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    temp DECIMAL(4,1) NOT NULL,
    heart_rate INT NOT NULL,
    spo2 INT NOT NULL,
    motion VARCHAR(20) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES cattle(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    device_id INT DEFAULT NULL,
    message VARCHAR(255) NOT NULL,
    severity ENUM('Low','Medium','High') NOT NULL DEFAULT 'Medium',
    is_read TINYINT(1) DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES cattle(id) ON DELETE CASCADE,
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE SET NULL
);
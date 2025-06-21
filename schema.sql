-- Create database
CREATE DATABASE IF NOT EXISTS sport_room_booking;
USE sport_room_booking;

-- Drop tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS booking_room;
DROP TABLE IF EXISTS sports_room;
DROP TABLE IF EXISTS building;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create building table
CREATE TABLE building (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create sports_room table
CREATE TABLE sports_room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_building INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
    facility TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_building) REFERENCES building(id) ON DELETE CASCADE
);

-- Create booking_room table
CREATE TABLE booking_room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    id_sports_room INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_sports_room) REFERENCES sports_room(id) ON DELETE CASCADE,
    CHECK (status IN ('Pending', 'Approve', 'Reject'))
);

-- Create indexes for better performance
CREATE INDEX idx_booking_user ON booking_room(id_user);
CREATE INDEX idx_booking_room ON booking_room(id_sports_room);
CREATE INDEX idx_booking_status ON booking_room(status);
CREATE INDEX idx_sports_room_building ON sports_room(id_building);

-- Insert sample data
-- Admin user (password: admin123)
INSERT INTO users (username, password, email, role) VALUES 
('admin', 'admin123', 'admin@example.com', 'admin');

-- Regular user (password: user123)
INSERT INTO users (username, password, email, role) VALUES 
('user', 'user123', 'john@example.com', 'user');
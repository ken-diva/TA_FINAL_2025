-- Create database
CREATE DATABASE IF NOT EXISTS sport_room_booking;
USE sport_room_booking;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create building table
CREATE TABLE building (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    description TEXT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create sports_room table
CREATE TABLE sports_room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_building INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    facility TEXT,
    image_url VARCHAR(255),
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
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_sports_room) REFERENCES sports_room(id) ON DELETE CASCADE,
    CHECK (status IN ('Pending', 'Approve', 'Reject')),
    CHECK (end_time > start_time)
);

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_building_code ON building(code);
CREATE INDEX idx_sports_room_building ON sports_room(id_building);
CREATE INDEX idx_booking_user ON booking_room(id_user);
CREATE INDEX idx_booking_room ON booking_room(id_sports_room);
CREATE INDEX idx_booking_status ON booking_room(status);
CREATE INDEX idx_booking_time ON booking_room(start_time, end_time);

-- Insert sample data
INSERT INTO users (username, password, email, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2LN1B9tXvG', 'admin@campus.edu', 'admin'),
('john_doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2LN1B9tXvG', 'john@campus.edu', 'user'),
('jane_smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2LN1B9tXvG', 'jane@campus.edu', 'user');

INSERT INTO building (name, code, description, image_url) VALUES
('Sports Complex A', 'SCA', 'Main sports building with basketball and volleyball courts', '/static/images/building_sca.jpg'),
('Fitness Center B', 'FCB', 'Modern fitness center with gym and aerobic rooms', '/static/images/building_fcb.jpg');

INSERT INTO sports_room (id_building, name, capacity, facility, image_url) VALUES
(1, 'Basketball Court 1', 20, 'Full court, air conditioning, sound system', '/static/images/basketball1.jpg'),
(1, 'Volleyball Court 1', 16, 'Standard net, wooden floor, scoreboard', '/static/images/volleyball1.jpg'),
(2, 'Gym Room A', 30, 'Weight machines, free weights, mirrors', '/static/images/gym_a.jpg'),
(2, 'Aerobic Room B', 25, 'Sound system, mirrors, yoga mats available', '/static/images/aerobic_b.jpg');

INSERT INTO booking_room (id_user, id_sports_room, start_time, end_time, status) VALUES
(2, 1, '2025-06-20 14:00:00', '2025-06-20 16:00:00', 'Pending'),
(3, 2, '2025-06-21 10:00:00', '2025-06-21 12:00:00', 'Approve');
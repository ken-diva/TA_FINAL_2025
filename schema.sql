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
('john_doe', 'user123', 'john@example.com', 'user');

-- Sample buildings
INSERT INTO building (name, code, description, image_url) VALUES 
('Sports Complex A', 'SCA', 'Main sports complex with multiple indoor courts', '/static/images/complex_a.jpg'),
('Sports Complex B', 'SCB', 'Secondary sports complex with swimming pool', '/static/images/complex_b.jpg'),
('Fitness Center', 'FC', 'Modern fitness center with gym equipment', '/static/images/fitness_center.jpg');

-- Sample sports rooms
INSERT INTO sports_room (id_building, name, capacity, facility, image_url) VALUES 
(1, 'Basketball Court 1', 20, 'Full-size basketball court, scoreboard, bleachers', '/static/images/basketball1.jpg'),
(1, 'Basketball Court 2', 20, 'Full-size basketball court, scoreboard', '/static/images/basketball2.jpg'),
(1, 'Badminton Court A', 4, '2 badminton courts, equipment rental available', '/static/images/badminton_a.jpg'),
(2, 'Swimming Pool', 50, 'Olympic-size pool, 8 lanes, diving board', '/static/images/pool.jpg'),
(2, 'Tennis Court 1', 4, 'Indoor tennis court, lighting, equipment rental', '/static/images/tennis1.jpg'),
(3, 'Gym Floor 1', 30, 'Cardio machines, weight training equipment', '/static/images/gym1.jpg'),
(3, 'Yoga Studio', 15, 'Mirrors, mats, sound system', '/static/images/yoga.jpg');

-- Sample bookings
INSERT INTO booking_room (id_user, id_sports_room, start_time, end_time, status) VALUES 
(2, 1, '2025-06-20 09:00:00', '2025-06-20 11:00:00', 'Approve'),
(2, 3, '2025-06-21 14:00:00', '2025-06-21 15:00:00', 'Pending'),
(2, 5, '2025-06-22 16:00:00', '2025-06-22 18:00:00', 'Reject');
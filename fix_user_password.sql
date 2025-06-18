-- First, let's clear existing users and add them with correct password hashes
DELETE FROM users;

-- Reset auto increment
ALTER TABLE users AUTO_INCREMENT = 1;

-- Insert users with known working bcrypt hashes for "password"
INSERT INTO users (username, password, email, role) VALUES
('admin', '$2b$12$LH5xmv3ZBjm5kcV4fHX.W.tGjKgJkC7Y7z2Vt0vw.rYWgV2jN5gSu', 'admin@campus.edu', 'admin'),
('john_doe', '$2b$12$LH5xmv3ZBjm5kcV4fHX.W.tGjKgJkC7Y7z2Vt0vw.rYWgV2jN5gSu', 'john@campus.edu', 'user'),
('jane_smith', '$2b$12$LH5xmv3ZBjm5kcV4fHX.W.tGjKgJkC7Y7z2Vt0vw.rYWgV2jN5gSu', 'jane@campus.edu', 'user');
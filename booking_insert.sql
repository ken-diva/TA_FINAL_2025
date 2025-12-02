-- ======================================
-- USERS
-- ======================================
-- Clear existing users (optional, hati-hati jika sudah ada user lain)
DELETE FROM users;

INSERT INTO users (id, username, password, email, role, created_at, updated_at) VALUES
(1, 'admin', 'admin123', 'admin@telkomuniversity.ac.id', 'admin', NOW(), NOW()),
(2, 'rahman', 'rahman123', 'rahman@student.telkomuniversity.ac.id', 'admin', NOW(), NOW()),
(3, 'andi', 'andi123', 'andi@student.telkomuniversity.ac.id', 'user', NOW(), NOW()),
(4, 'reza', 'reza123', 'reza@student.telkomuniversity.ac.id', 'user', NOW(), NOW()),
(5, 'nanda', 'nanda123', 'nanda@student.telkomuniversity.ac.id', 'user', NOW(), NOW());

-- ======================================
-- BOOKING_ROOM
-- ======================================
-- Pastikan id_sports_room sesuai dengan urutan yang ada di database kamu
-- (urutannya mengikuti hasil insert sebelumnya)
-- Gunakan SELECT * FROM sports_room; untuk memastikan ID-nya

-- Misal ID hasil insert kamu adalah seperti ini:
-- 1. Lapangan Basket (Sport Center)
-- 2. Lapangan Volley (Sport Center)
-- 3. Lapangan Futsal (Sport Center)
-- 4. Lapangan Bulutangkis (Student Center)
-- 5. Lapangan Basket 3X3 selatan (Lap. Basket Selatan)
-- 6. Lapangan Basket 3X3 utara (Lap. Basket Utara)

INSERT INTO booking_room (id, id_user, id_sports_room, booking_date, start_time, end_time, status, created_at, updated_at) VALUES
(1, 2, 1, '2025-10-05 09:00:00', '2025-10-05 09:00:00', '2025-10-05 11:00:00', 'Approve', NOW(), NOW()),
(2, 3, 2, '2025-10-06 13:00:00', '2025-10-06 13:00:00', '2025-10-06 15:00:00', 'Pending', NOW(), NOW()),
(3, 4, 3, '2025-10-07 10:00:00', '2025-10-07 10:00:00', '2025-10-07 12:00:00', 'Approve', NOW(), NOW()),
(4, 5, 4, '2025-10-08 08:00:00', '2025-10-08 08:00:00', '2025-10-08 10:00:00', 'Reject', NOW(), NOW()),
(5, 2, 5, '2025-10-09 14:00:00', '2025-10-09 14:00:00', '2025-10-09 16:00:00', 'Approve', NOW(), NOW()),
(6, 3, 6, '2025-10-10 07:00:00', '2025-10-10 07:00:00', '2025-10-10 09:00:00', 'Pending', NOW(), NOW()),
(7, 4, 1, '2025-10-11 15:00:00', '2025-10-11 15:00:00', '2025-10-11 17:00:00', 'Approve', NOW(), NOW()),
(8, 5, 2, '2025-10-12 10:00:00', '2025-10-12 10:00:00', '2025-10-12 12:00:00', 'Pending', NOW(), NOW()),
(9, 2, 3, '2025-10-13 09:00:00', '2025-10-13 09:00:00', '2025-10-13 11:00:00', 'Approve', NOW(), NOW()),
(10, 3, 4, '2025-10-14 11:00:00', '2025-10-14 11:00:00', '2025-10-14 13:00:00', 'Approve', NOW(), NOW()),
(11, 4, 5, '2025-10-15 08:00:00', '2025-10-15 08:00:00', '2025-10-15 10:00:00', 'Pending', NOW(), NOW()),
(12, 5, 6, '2025-10-16 14:00:00', '2025-10-16 14:00:00', '2025-10-16 16:00:00', 'Approve', NOW(), NOW()),
(13, 2, 1, '2025-10-17 07:00:00', '2025-10-17 07:00:00', '2025-10-17 09:00:00', 'Reject', NOW(), NOW()),
(14, 3, 2, '2025-10-18 15:00:00', '2025-10-18 15:00:00', '2025-10-18 17:00:00', 'Approve', NOW(), NOW()),
(15, 4, 3, '2025-10-19 09:00:00', '2025-10-19 09:00:00', '2025-10-19 11:00:00', 'Pending', NOW(), NOW());

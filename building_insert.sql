-- Clear existing building data (optional, be careful in production)
-- DELETE FROM sports_room WHERE id_building IN (SELECT id FROM building);
-- DELETE FROM building;

-- Insert all buildings from the 3D model
INSERT INTO building (name, code, description, image_url) VALUES 
('Building A', 'GDG-A', 'Academic Building A - General classrooms and lecture halls', '/static/images/buildings/gdg-a.jpg'),
('Building B', 'GDG-B', 'Academic Building B - Laboratory and research facilities', '/static/images/buildings/gdg-b.jpg'),
('Basketball Court 1', 'GDG-BAS1', 'Indoor Basketball Court 1 - Professional court with spectator seating', '/static/images/buildings/gdg-bas1.jpg'),
('Basketball Court 2', 'GDG-BAS2', 'Indoor Basketball Court 2 - Training and practice facility', '/static/images/buildings/gdg-bas2.jpg'),
('Building E', 'GDG-E', 'Engineering Building - Engineering departments and workshops', '/static/images/buildings/gdg-e.jpg'),
('Building F', 'GDG-F', 'Faculty Building - Administrative offices and meeting rooms', '/static/images/buildings/gdg-f.jpg'),
('FIF Building', 'GDG-FIF', 'Faculty of Informatics - Computer labs and IT facilities', '/static/images/buildings/gdg-fif.jpg'),
('FIT Building', 'GDG-FIT', 'Faculty of Industrial Technology - Engineering labs and workshops', '/static/images/buildings/gdg-fit.jpg'),
('FKSF/FEB/PERP Building', 'GDG-FKSFEBPERP', 'Business, Communication, and Library complex', '/static/images/buildings/gdg-fksfebperp.jpg'),
('FRI Building', 'GDG-FRI', 'Faculty of Creative Industries - Art studios and design labs', '/static/images/buildings/gdg-fri.jpg'),
('FTE Building', 'GDG-FTE', 'Faculty of Electrical Engineering - Electronics and electrical labs', '/static/images/buildings/gdg-fte.jpg'),
('GKU Building', 'GDG-GKU', 'Main Auditorium - Large capacity auditorium for events', '/static/images/buildings/gdg-gku.jpg'),
('GSG Building', 'GDG-GSG', 'Multipurpose Hall - Sports and cultural activities', '/static/images/buildings/gdg-gsg.jpg'),
('Jogging Track', 'GDG-JOG', 'Outdoor Jogging Track - 400m athletic track', '/static/images/buildings/gdg-jog.jpg'),
('Language Center', 'GDG-LING', 'Language Learning Center - Language labs and classrooms', '/static/images/buildings/gdg-ling.jpg'),
('MSU Building', 'GDG-MSU', 'Student Center - Student organizations and activities', '/static/images/buildings/gdg-msu.jpg'),
('Graduate Building', 'GDG-PASCA', 'Postgraduate Building - Graduate programs and research', '/static/images/buildings/gdg-pasca.jpg'),
('Male Dormitory', 'GDG-PUTRA', 'Male Student Dormitory - Accommodation for male students', '/static/images/buildings/gdg-putra.jpg'),
('Female Dormitory', 'GDG-PUTRI', 'Female Student Dormitory - Accommodation for female students', '/static/images/buildings/gdg-putri.jpg'),
('Rectorate Building', 'GDG-REKT', 'University Administration - Main administrative offices', '/static/images/buildings/gdg-rekt.jpg'),
('Sports Complex', 'GDG-SPRT', 'Main Sports Complex - Various indoor sports facilities', '/static/images/buildings/gdg-sprt.jpg'),
('Stadium', 'GDG-STD', 'University Stadium - Football field and athletic facilities', '/static/images/buildings/gdg-std.jpg'),
('TUCH Building', 'GDG-TUCH', 'University Health Center - Medical and health services', '/static/images/buildings/gdg-tuch.jpg'),
('TULT Building', 'GDG-TULT', 'Advanced Technology Lab - Research and development center', '/static/images/buildings/gdg-tult.jpg');

-- Add some sports rooms to the sports-related buildings
INSERT INTO sports_room (id_building, name, capacity, facility, image_url) VALUES 
-- Basketball Courts
((SELECT id FROM building WHERE code = 'GDG-BAS1'), 'Main Basketball Court', 200, 'Professional court, electronic scoreboard, spectator seating, locker rooms', '/static/images/rooms/bas1-main.jpg'),
((SELECT id FROM building WHERE code = 'GDG-BAS2'), 'Practice Court A', 50, 'Full-size practice court, basic equipment', '/static/images/rooms/bas2-practice.jpg'),

-- Sports Complex
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Badminton Court 1', 20, '4 badminton courts, equipment rental', '/static/images/rooms/sprt-badminton1.jpg'),
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Badminton Court 2', 20, '4 badminton courts, professional lighting', '/static/images/rooms/sprt-badminton2.jpg'),
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Table Tennis Hall', 30, '8 table tennis tables, tournament setup available', '/static/images/rooms/sprt-tabletennis.jpg'),
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Fitness Center', 50, 'Modern gym equipment, cardio and weight training', '/static/images/rooms/sprt-fitness.jpg'),

-- GSG Building
((SELECT id FROM building WHERE code = 'GDG-GSG'), 'Multipurpose Hall', 500, 'Large hall for sports, events, and exhibitions', '/static/images/rooms/gsg-main.jpg'),
((SELECT id FROM building WHERE code = 'GDG-GSG'), 'Martial Arts Dojo', 40, 'Tatami mats, mirrors, training equipment', '/static/images/rooms/gsg-dojo.jpg'),

-- Stadium
((SELECT id FROM building WHERE code = 'GDG-STD'), 'Football Field', 1000, 'Standard football field, athletic track, grandstand', '/static/images/rooms/std-football.jpg'),
((SELECT id FROM building WHERE code = 'GDG-STD'), 'Athletic Track', 200, '400m running track, field event areas', '/static/images/rooms/std-track.jpg');
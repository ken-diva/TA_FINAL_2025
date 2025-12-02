-- Clear existing building data (optional, be careful in production)
DELETE FROM sports_room WHERE id_building IN (SELECT id FROM building);
DELETE FROM building;

-- Insert all buildings from the 3D model
INSERT INTO building (name, code, description, image_url) VALUES 
('Gedung A', 'GDG-A', 'Gedung A Telkom University adalah bagian dari Grha Wiyata Cacuk Sudarijanto yang merupakan Gedung Kuliah Umum (GKU). Gedung ini merupakan tempat yang digunakan untuk aktivitas perkuliahan dan termasuk salah satu gedung ikonik di kampus Telkom University.', '/static/uploads/1_gedung_a.jpg'),
('Gedung B', 'GDG-B', 'Gedung B (Gedung Kuliah Umum A) di Telkom University merupakan salah satu fasilitas penting untuk perkuliahan umum di kampus tersebut, yang berfungsi sebagai ruang kelas, fasilitas penelitian, dan lingkungan belajar yang kondusif. Gedung ini menyediakan berbagai ruangan untuk aktivitas akademik mahasiswa dan staf pengajar, mendukung peran Telkom University sebagai kampus penelitian dan kewirausahaan.', '/static/uploads/2_gedung_b.jpg'),
('Lapangan Basket Selatan', 'GDG-BAS1', 'Outdoor Lapangan Basket Selatan - Professional court with spectator seating', '/static/uploads/outdoor.jpeg'),
('Lapangan Basket Utara', 'GDG-BAS2', 'Outdoor Lapangan Basket Outdoor 2 - Training and practice facility', '/static/uploads/outdoor.jpeg'),
('Gedung E', 'GDG-E', 'Gedung Kultubai Utara', '/static/uploads/5_gd_e.jpg'),
('Gedung F', 'GDG-F', 'Gedung Kultubai Selatan', '/static/uploads/6_gd_f.jpg'),
('Gedung FIF ', 'GDG-FIF', 'Gedung Fakultas Informatika yang bernama Gedung Panambulai. Gedung ini juga berisi direktorat PUTI dan residensi mahasiswa S2 dan S3 Fakultas Informatika', '/static/uploads/7_fif.jpg'),
('Gedung FIT ', 'GDG-FIT', 'Gedung Fakultas Ilmu Terapan. Gedung ini memiliki banyak laboratorium praktikum untuk mesin berat dan elektronik.', '/static/uploads/8_fit.jpg'),
('Gedung FKSF/FEB/PERP ', 'GDG-FKSFEBPERP', 'Gedung gabungan antara Fakultas Komunikasi Sosial, Fakultas Ekonomi dan Bisnis serta Perpustakaan. Gedung fakultas berada pada sisi kanan dan kiri sedangkan perpustakaan berada pada lantai 5.', '/static/uploads/9_open_library.jpg'),
('Gedung FRI ', 'GDG-FRI', 'Gedung Fakultas Rekayasa Industri', '/static/uploads/10_fri.jpg'),
('Gedung FTE ', 'GDG-FTE', 'Gedung Fakultas Teknik Elektro', '/static/uploads/11_fte.jpg'),
('Gedung GKU ', 'GDG-GKU', 'Gedung Kuliah Umum. Gedung ini adalah pusat perkuliahan umum untuk seluruh mahasiswa Telkom University', '/static/uploads/12_gku.jpg'),
('Gedung GSG ', 'GDG-GSG', 'Gedung Serba Guna.', '/static/uploads/13_gsg.jpg'),
('Jogging Track', 'GDG-JOG', 'Tempat Jogging Outdoor yang dapat digunakan oleh staff, mahasiswa maupun penduduk sekitar', '/static/uploads/14_jogging.jpg'),
('Gedung Lingian', 'GDG-LING', 'Gedung ini memiliki kamar yang dapat disewa oleh orangtua mahasiswa terutama pada saat wisuda. Beberapa kamar juga menjadi tempat praktikum untuk mahasiswa jurusan D3 Perhotelan', '/static/uploads/15_lingian.jpg'),
('Masjid MSU', 'GDG-MSU', 'Masjid Syamsul Ulum.', '/static/uploads/16_msu.jpg'),
('Gedung Pascasarjana', 'GDG-PASCA', 'Gedung Pascasarjana digunakan sebagai pusat administrasi perkuliahan S2 ataupun S3. Disini juga terdapat ruang residensi cadangan jika dibutuhkan', '/static/uploads/17_pasca.jpg'),
('Asrama Putra', 'GDG-PUTRA', 'Asrama putra Telkom University adalah fasilitas wajib untuk mahasiswa baru selama tahun pertama kuliah, terdiri dari 10 gedung asrama yang menyediakan fasilitas kamar seperti tempat tidur, lemari, meja, kursi, dan kamar mandi dalam, serta fasilitas umum seperti WiFi gratis, lapangan olahraga, laundry, kantin, dan pusat pembinaan karakter melalui bidang adaptif, spiritual, akademis, dan sosial, dengan lokasi strategis di dalam kawasan kampus dekat dengan gedung perkuliahan.', '/static/uploads/18_asrama_putra.jpg'),
('Asrama Putri', 'GDG-PUTRI', 'Asrama Putri Telkom University adalah pusat hunian dan pembinaan karakter bagi mahasiswi baru yang wajib tinggal selama satu tahun pertama kuliah. Fasilitasnya lengkap, meliputi kamar pribadi dengan tempat tidur, meja, dan lemari, serta fasilitas umum seperti wifi, laundry, kantin, dan area olahraga. Asrama ini juga dilengkapi sistem keamanan yang baik dengan bantuan kakak asrama dan keamanan gedung, serta berbagai kegiatan pembinaan yang fokus pada adaptasi, spiritualitas, akademis, dan sosial.', '/static/uploads/19_asrama_putri.jpg'),
('Gedung Rektorat', 'GDG-REKT', 'Gedung Rektorat adalah pusat kegiatan staff dan tempat ruangan rektor serta jajarannya. Disini terdapat unit yang mengatur peran dosen, staff dan juga hubungan kerjasama baik luar maupun dalam negeri.', '/static/uploads/20_rektorat.jpg'),
('Sport Center', 'GDG-SPRT', 'Sport Center adalah pusat kegiatan untuk staff maupun mahasiswa. Disini terdapat lapangan basket indoor, lapangan futsal indoor dan lapangan volley indoor.', '/static/uploads/21_sport_center.jpg'),
('Student Center', 'GDG-STD', 'Student Center adalah pusat kegiatan UKM mahasiswa. Disini UKM diberikan ruangan untuk menyimpan peralatan dan berlatih jika dibutuhkan. Didalam gedung ini juga terdapat lapangan badminton yang bisa digunakan oleh staff ataupun mahasiswa', '/static/uploads/22_student_center.jpg'),
('Gedung TUCH', 'GDG-TUCH', 'Telkom University Convention Hall adalah gedung dengan kapasitas 4000 orang yang sering digunakan untuk acara seperti pengenalan mahasiswa baru, ulang tahun Tel-U dan lainnya.', '/static/uploads/23_tuch.jpg'),
('Gedung TULT', 'GDG-TULT', 'Telkom University Landmark Tower adalah gedung paling baru di Tel-U. Gedung ini menjadi tempat perkuliahan dan juga administrasi untuk tiga fakultas yaitu FIF, FTE dan FRI', '/static/uploads/24_tult.jpg');

-- Add some sports rooms to the sports-related buildings
INSERT INTO sports_room (id_building, name, capacity, facility, image_url) VALUES 
-- Sport Center
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Lapangan Basket', 50, 'Lapangan Basket indoor', '/static/uploads/lapangan_basket.png'),
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Lapangan Volley', 50, 'Lapangan Volley indoor', '/static/uploads/lapangan_voli.png'),
((SELECT id FROM building WHERE code = 'GDG-SPRT'), 'Lapangan Futsal', 50, 'Lapangan Futsal indoor', '/static/uploads/lapangan_futsal.png');
-- Student Center
INSERT INTO sports_room (id_building, name, capacity, facility, image_url) VALUES
((SELECT id FROM building WHERE code = 'GDG-STD'), 'Lapangan Bulutangkis A', 6, 'Lapangan Bulutangkis A indoor', '/static/uploads/bulutangkis_A.png'),
((SELECT id FROM building WHERE code = 'GDG-STD'), 'Lapangan Bulutangkis B', 6, 'Lapangan Bulutangkis B indoor', '/static/uploads/bulutangkis_B.png');
-- Lapangan Outdoor
INSERT INTO sports_room (id_building, name, capacity, facility, image_url) VALUES
((SELECT id FROM building WHERE code = 'GDG-BAS1'), 'Lapangan Basket 3X3 selatan', 6, 'Lapangan Basket 3X3 selatan', '/static/uploads/3_bas_selatan.png'),
((SELECT id FROM building WHERE code = 'GDG-BAS2'), 'Lapangan Basket 3X3 utara', 6, 'Lapangan Basket 3X3 utara', '/static/uploads/4_basket_utara.png');
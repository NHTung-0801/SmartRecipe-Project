SET NAMES utf8mb4;

-- Tạm thời gỡ liên kết
CREATE TABLE IF NOT EXISTS ingredients_old_aisles AS SELECT id, aisle_id FROM ingredients;
UPDATE ingredients SET aisle_id = NULL;

-- Xóa dữ liệu cũ và cập nhật dữ liệu mới
DELETE FROM aisles;
INSERT INTO aisles (id, name) VALUES 
(1, 'Thịt & Hải sản'), 
(2, 'Rau củ & Trái cây'), 
(3, 'Gia vị & Đồ khô'), 
(4, 'Sữa & Trứng');

-- Map lại
-- Cũ 2, 3 -> Mới 1 (Thịt & Hải sản)
UPDATE ingredients i JOIN ingredients_old_aisles o ON i.id = o.id SET i.aisle_id = 1 WHERE o.aisle_id IN (2, 3);
-- Cũ 1 -> Mới 2 (Rau củ & Trái cây)
UPDATE ingredients i JOIN ingredients_old_aisles o ON i.id = o.id SET i.aisle_id = 2 WHERE o.aisle_id = 1;
-- Cũ 4, 5 -> Mới 3 (Gia vị & Đồ khô)
UPDATE ingredients i JOIN ingredients_old_aisles o ON i.id = o.id SET i.aisle_id = 3 WHERE o.aisle_id IN (4, 5);
-- Cũ 6 -> Mới 4 (Sữa & Trứng)
UPDATE ingredients i JOIN ingredients_old_aisles o ON i.id = o.id SET i.aisle_id = 4 WHERE o.aisle_id = 6;

-- Xóa bảng tạm
DROP TABLE ingredients_old_aisles;

-- SINH TỰ ĐỘNG bởi tools/gen_seed_sql.py — ĐỪNG sửa tay.
-- Nguồn: dataset/ingredients_to_translate.csv
-- Dinh dưỡng: USDA FoodData Central, SR Legacy 2018-04 (trên 100 g).
--
-- 290 nguyên liệu, 15 dòng có quy đổi ml->g.
-- 24 dòng từng bị cờ review_needed trong pipeline và đã được
-- xác nhận hợp lệ: calo lệch Atwater là do gia vị khô nhiều xơ, do
-- axit hữu cơ trong nước cốt chanh/giấm, hoặc do tỷ lệ đạm đặc biệt
-- của rau lá. Không dòng nào là lỗi dữ liệu.
--
-- Nạp file (PowerShell 5.1 không có toán tử '<'):
--   docker cp sql/seed_ingredients.sql smartrecipe-mysql:/tmp/seed.sql
--   docker exec smartrecipe-mysql bash -c \
--     "mysql -uroot -proot --default-character-set=utf8mb4 < /tmp/seed.sql"

-- Thiếu dòng này thì client mysql dùng latin1 và mọi tên tiếng Việt
-- thành mojibake kiểu 'Cá h?i'.
SET NAMES utf8mb4;

USE `smart_recipe_db`;

-- Chạy lại được nhiều lần: khớp theo UNIQUE(name).
-- CỐ Ý không cập nhật `base_unit` — xem tools/gen_seed_sql.py.
INSERT INTO `ingredients`
    (`name`, `base_unit`, `calories_per_100g`, `protein`, `fat`, `carbs`, `aisle_id`)
VALUES
-- Kệ 1: Rau củ (74 dòng)
('Atisô', 'g', 47.00, 3.27, 0.15, 10.51, 1),
('Bí ngòi non', 'g', 21.00, 2.71, 0.40, 3.11, 1),
('Bí đao', 'g', 13.00, 0.40, 0.20, 3.00, 1),
('Bí đỏ', 'g', 26.00, 1.00, 0.10, 6.50, 1),
('Bông cải trắng', 'g', 25.00, 1.92, 0.28, 4.97, 1),
('Bông cải xanh', 'g', 34.00, 2.82, 0.37, 6.64, 1),
('Bắp cải', 'g', 25.00, 1.28, 0.10, 5.80, 1),
('Bắp cải tím', 'g', 31.00, 1.43, 0.16, 7.37, 1),
('Cà chua', 'g', 18.00, 0.88, 0.20, 3.89, 1),
('Cà chua xanh', 'g', 23.00, 1.20, 0.20, 5.10, 1),
('Cà rốt', 'g', 41.00, 0.93, 0.24, 9.58, 1),
('Cà tím', 'g', 25.00, 0.98, 0.18, 5.88, 1),
('Cải bó xôi', 'g', 23.00, 2.86, 0.39, 3.63, 1),
('Cải bẹ xanh', 'g', 27.00, 2.86, 0.42, 4.67, 1),
('Cải làn', 'g', 26.00, 1.20, 0.76, 4.67, 1),
('Cải thìa', 'g', 13.00, 1.50, 0.20, 2.18, 1),
('Cải thảo', 'g', 16.00, 1.20, 0.20, 3.23, 1),
('Cải xoong', 'g', 11.00, 2.30, 0.10, 1.29, 1),
('Cần tây', 'g', 14.00, 0.69, 0.17, 2.97, 1),
('Củ cải trắng', 'g', 18.00, 0.60, 0.10, 4.10, 1),
('Củ cải đỏ', 'g', 16.00, 0.68, 0.10, 3.40, 1),
('Củ năng', 'g', 97.00, 1.40, 0.10, 23.94, 1),
('Củ sen', 'g', 74.00, 2.60, 0.10, 17.23, 1),
('Củ từ', 'g', 118.00, 1.53, 0.17, 27.88, 1),
('Củ wasabi', 'g', 109.00, 4.80, 0.63, 23.54, 1),
('Củ đậu', 'g', 38.00, 0.72, 0.09, 8.82, 1),
('Dưa leo', 'g', 10.00, 0.59, 0.16, 2.16, 1),
('Dọc mùng', 'g', 11.00, 0.92, 0.09, 2.32, 1),
('Gừng', 'g', 80.00, 1.82, 0.75, 17.77, 1),
('Hoa bí', 'g', 15.00, 1.03, 0.07, 3.28, 1),
('Hành lá', 'g', 32.00, 1.83, 0.19, 7.34, 1),
('Hành ta', 'g', 34.00, 1.90, 0.40, 6.50, 1),
('Hành tây', 'g', 40.00, 1.10, 0.10, 9.34, 1),
('Hành tây ngọt', 'g', 32.00, 0.80, 0.08, 7.55, 1),
('Hành tím', 'g', 72.00, 2.50, 0.10, 16.80, 1),
('Khoai lang', 'g', 86.00, 1.57, 0.05, 20.12, 1),
('Khoai mì', 'g', 160.00, 1.36, 0.28, 38.06, 1),
('Khoai môn', 'g', 112.00, 1.50, 0.20, 26.46, 1),
('Khoai tây', 'g', 77.00, 2.05, 0.09, 17.49, 1),
('Khổ qua', 'g', 17.00, 1.00, 0.17, 3.70, 1),
('Lá hẹ', 'g', 30.00, 3.27, 0.73, 4.35, 1),
('Lá khoai môn', 'g', 42.00, 4.98, 0.74, 6.70, 1),
('Măng tây', 'g', 20.00, 2.20, 0.12, 3.88, 1),
('Măng tươi', 'g', 27.00, 2.60, 0.30, 5.20, 1),
('Mướp', 'g', 20.00, 1.20, 0.20, 4.35, 1),
('Ngò rí', 'g', 23.00, 2.13, 0.52, 3.67, 1),
('Ngò tây', 'g', 36.00, 2.97, 0.79, 6.33, 1),
('Ngô ngọt trắng', 'g', 86.00, 3.22, 1.18, 19.02, 1),
('Ngọn bí', 'g', 19.00, 3.15, 0.40, 2.33, 1),
('Ngọn hành lá', 'g', 27.00, 0.97, 0.47, 5.74, 1),
('Ngọn lá đậu đũa', 'g', 29.00, 4.10, 0.25, 4.82, 1),
('Nấm kim châm', 'g', 37.00, 2.66, 0.29, 7.81, 1),
('Nấm mỡ', 'g', 22.00, 3.09, 0.34, 3.26, 1),
('Nấm sò', 'g', 33.00, 3.31, 0.41, 6.09, 1),
('Nấm đông cô', 'g', 34.00, 2.24, 0.49, 6.79, 1),
('Rau dền', 'g', 23.00, 2.46, 0.33, 4.02, 1),
('Rau lang', 'g', 42.00, 2.49, 0.51, 8.82, 1),
('Rau muống', 'g', 19.00, 2.60, 0.20, 3.13, 1),
('Su su', 'g', 19.00, 0.82, 0.13, 4.51, 1),
('Sả', 'g', 99.00, 1.82, 0.49, 25.31, 1),
('Tỏi', 'g', 149.00, 6.36, 0.50, 33.06, 1),
('Tỏi tây', 'g', 61.00, 1.50, 0.30, 14.15, 1),
('Đậu Hà Lan', 'g', 81.00, 5.42, 0.40, 14.45, 1),
('Đậu bắp', 'g', 33.00, 1.93, 0.19, 7.45, 1),
('Đậu cô ve', 'g', 31.00, 1.83, 0.22, 6.97, 1),
('Đậu mắt đen non', 'g', 90.00, 2.95, 0.35, 18.83, 1),
('Đậu nành xanh', 'g', 147.00, 12.95, 6.80, 11.05, 1),
('Đậu đũa', 'g', 47.00, 2.80, 0.40, 8.35, 1),
('Ớt chuông vàng', 'g', 27.00, 1.00, 0.21, 6.32, 1),
('Ớt chuông xanh', 'g', 20.00, 0.86, 0.17, 4.64, 1),
('Ớt chuông đỏ', 'g', 26.00, 0.99, 0.30, 6.03, 1),
('Ớt jalapeño', 'g', 29.00, 0.91, 0.37, 6.50, 1),
('Ớt serrano', 'g', 32.00, 1.74, 0.44, 6.70, 1),
('Ớt đỏ', 'g', 40.00, 1.87, 0.44, 8.81, 1),
-- Kệ 2: Thịt & Gia cầm (47 dòng)
('Bao tử heo', 'g', 159.00, 16.85, 10.14, 0.00, 2),
('Bắp chân bò', 'g', 128.00, 21.75, 3.85, 0.00, 2),
('Chân heo', 'g', 212.00, 23.16, 12.59, 0.00, 2),
('Chân heo muối chua', 'g', 140.00, 11.63, 10.02, 0.01, 2),
('Cánh gà không da', 'g', 126.00, 21.97, 3.54, 0.00, 2),
('Cật bò', 'g', 99.00, 17.40, 3.09, 0.29, 2),
('Cật heo', 'g', 100.00, 16.46, 3.25, 0.00, 2),
('Gan bò', 'g', 135.00, 20.36, 3.63, 3.89, 2),
('Gan gà', 'g', 119.00, 16.92, 4.83, 0.73, 2),
('Gan heo', 'g', 134.00, 21.39, 3.65, 2.47, 2),
('Gan vịt', 'g', 136.00, 18.74, 4.64, 3.53, 2),
('Lưỡi bò', 'g', 224.00, 14.90, 16.09, 3.68, 2),
('Lưỡi heo', 'g', 225.00, 16.30, 17.20, 0.00, 2),
('Mề gà', 'g', 94.00, 17.66, 2.06, 0.00, 2),
('Sách bò', 'g', 85.00, 12.07, 3.69, 0.00, 2),
('Sườn bò', 'g', 175.00, 19.05, 10.19, 0.40, 2),
('Sườn lưng heo', 'g', 224.00, 19.07, 16.33, 0.00, 2),
('Sườn lưng heo nạc', 'g', 172.00, 20.85, 9.84, 0.00, 2),
('Sườn non heo', 'g', 277.00, 15.47, 23.40, 0.00, 2),
('Tai heo', 'g', 234.00, 22.45, 15.10, 0.60, 2),
('Thịt bò nạm', 'g', 149.00, 21.72, 6.29, 0.00, 2),
('Thịt bò thăn nội', 'g', 148.00, 22.06, 5.93, 0.00, 2),
('Thịt bò xay', 'g', 254.00, 17.17, 20.00, 0.00, 2),
('Thịt chim bồ câu', 'g', 142.00, 17.50, 7.50, 0.00, 2),
('Thịt gà có da', 'g', 215.00, 18.60, 15.06, 0.00, 2),
('Thịt gà không da', 'g', 119.00, 21.39, 3.08, 0.00, 2),
('Thịt gà tây xay', 'g', 150.00, 18.73, 8.34, 0.00, 2),
('Thịt gà xay', 'g', 143.00, 17.44, 8.10, 0.04, 2),
('Thịt heo ba rọi', 'g', 518.00, 9.34, 53.01, 0.00, 2),
('Thịt heo thăn nội', 'g', 109.00, 20.95, 2.17, 0.00, 2),
('Thịt heo xay', 'g', 263.00, 16.88, 21.19, 0.00, 2),
('Thịt heo xay nạc', 'g', 121.00, 21.10, 4.00, 0.21, 2),
('Thịt má heo', 'g', 655.00, 6.38, 69.61, 0.00, 2),
('Thịt vai bò hầm', 'g', 124.00, 21.90, 3.99, 0.21, 2),
('Thịt vai heo nạc', 'g', 148.00, 19.55, 7.14, 0.00, 2),
('Thịt đùi heo nạc', 'g', 136.00, 20.48, 5.41, 0.00, 2),
('Thịt ức bò nạc', 'g', 157.00, 20.72, 7.37, 0.60, 2),
('Tim bò', 'g', 112.00, 17.72, 3.94, 0.14, 2),
('Tim gà', 'g', 153.00, 15.55, 9.33, 0.71, 2),
('Tim heo', 'g', 118.00, 17.27, 4.36, 1.33, 2),
('Đuôi heo', 'g', 378.00, 17.75, 33.50, 0.00, 2),
('Đùi gà dưới có da', 'g', 161.00, 18.08, 9.20, 0.11, 2),
('Đùi gà không da', 'g', 120.00, 19.16, 4.22, 0.00, 2),
('Đùi gà trên có da', 'g', 221.00, 16.52, 16.61, 0.25, 2),
('Ức gà có da', 'g', 172.00, 20.85, 9.25, 0.00, 2),
('Ức gà không da không xương', 'g', 120.00, 22.50, 2.62, 0.00, 2),
('Ức gà tây', 'g', 114.00, 23.66, 1.48, 0.14, 2),
-- Kệ 3: Hải sản (28 dòng)
('Bạch tuộc', 'g', 82.00, 14.91, 1.04, 2.20, 3),
('Cua dungeness', 'g', 86.00, 17.41, 0.97, 0.74, 3),
('Cua xanh', 'g', 87.00, 18.06, 1.08, 0.04, 3),
('Cá chép', 'g', 127.00, 17.83, 5.60, 0.00, 3),
('Cá chình', 'g', 184.00, 18.44, 11.66, 0.00, 3),
('Cá cơm', 'g', 131.00, 20.35, 4.84, 0.00, 3),
('Cá hồi', 'g', 208.00, 20.42, 13.42, 0.00, 3),
('Cá hồng', 'g', 100.00, 20.51, 1.34, 0.00, 3),
('Cá mú', 'g', 92.00, 19.38, 1.02, 0.00, 3),
('Cá măng sữa', 'g', 148.00, 20.53, 6.73, 0.00, 3),
('Cá ngừ vây xanh', 'g', 144.00, 23.33, 4.90, 0.00, 3),
('Cá nục heo', 'g', 85.00, 18.50, 0.70, 0.00, 3),
('Cá rô phi', 'g', 96.00, 20.08, 1.70, 0.00, 3),
('Cá thu', 'g', 139.00, 19.29, 6.30, 0.00, 3),
('Cá thu Đại Tây Dương', 'g', 205.00, 18.60, 13.89, 0.00, 3),
('Cá trê', 'g', 95.00, 16.38, 2.82, 0.00, 3),
('Cá tuyết', 'g', 82.00, 17.81, 0.67, 0.00, 3),
('Cá vược vàng', 'g', 93.00, 19.14, 1.22, 0.00, 3),
('Cá đối', 'g', 117.00, 19.35, 3.79, 0.00, 3),
('Hàu', 'g', 81.00, 9.45, 2.30, 4.95, 3),
('Mực nang', 'g', 79.00, 16.24, 0.70, 0.82, 3),
('Mực ống', 'g', 92.00, 15.58, 1.38, 3.08, 3),
('Nghêu', 'g', 86.00, 14.67, 0.96, 3.57, 3),
('Sò điệp', 'g', 69.00, 12.06, 0.49, 3.18, 3),
('Tôm', 'g', 85.00, 20.10, 0.51, 0.00, 3),
('Vẹm xanh', 'g', 86.00, 11.90, 2.24, 3.69, 3),
('Đùi ếch', 'g', 73.00, 16.40, 0.30, 0.00, 3),
('Ốc', 'g', 90.00, 16.10, 1.40, 2.00, 3),
-- Kệ 4: Gia vị & Nước chấm (36 dòng)
('Bạc hà', 'g', 70.00, 3.75, 0.94, 14.89, 4),
('Bột cà ri', 'g', 325.00, 14.29, 14.01, 55.83, 4),
('Bột gừng', 'g', 335.00, 8.98, 4.24, 71.62, 4),
('Bột hành', 'g', 341.00, 10.41, 1.04, 79.12, 4),
('Bột hạt mù tạt', 'g', 508.00, 26.08, 36.24, 28.09, 4),
('Bột nghệ', 'g', 312.00, 9.68, 3.25, 67.14, 4),
('Bột nhục đậu khấu', 'g', 525.00, 5.84, 36.31, 49.29, 4),
('Bột quế', 'g', 247.00, 3.99, 1.24, 80.59, 4),
('Bột tỏi', 'g', 331.00, 16.55, 0.73, 72.73, 4),
('Bột đinh hương', 'g', 274.00, 5.97, 13.00, 65.53, 4),
('Dầu hào', 'g', 51.00, 1.35, 0.25, 10.92, 4),
('Giấm táo', 'g', 21.00, 0.00, 0.00, 0.93, 4),
('Húng lủi khô', 'g', 285.00, 19.93, 6.03, 52.04, 4),
('Húng quế', 'g', 23.00, 3.15, 0.64, 2.65, 4),
('Hạt ngò rí', 'g', 298.00, 12.37, 17.77, 54.99, 4),
('Hạt thì là', 'g', 345.00, 15.80, 14.87, 52.29, 4),
('Hạt thì là Ai Cập', 'g', 375.00, 17.81, 22.27, 44.24, 4),
('Lá nguyệt quế', 'g', 313.00, 7.61, 8.36, 74.97, 4),
('Muối', 'g', 0.00, 0.00, 0.00, 0.00, 4),
('Mật mía', 'g', 290.00, 0.00, 0.10, 74.73, 4),
('Mật ong', 'g', 304.00, 0.30, 0.00, 82.40, 4),
('Ngò rí khô', 'g', 279.00, 21.93, 4.78, 52.10, 4),
('Nước cốt dừa', 'g', 230.00, 2.29, 23.84, 5.54, 4),
('Nước cốt dừa đậm đặc', 'g', 330.00, 3.63, 34.68, 6.65, 4),
('Nước mắm', 'g', 35.00, 5.06, 0.01, 3.64, 4),
('Nước tương', 'g', 53.00, 8.14, 0.57, 4.93, 4),
('Nước tương tamari', 'g', 60.00, 10.51, 0.10, 5.57, 4),
('Tinh chất vani', 'g', 288.00, 0.06, 0.06, 12.65, 4),
('Tiêu đen', 'g', 251.00, 10.39, 3.26, 63.95, 4),
('Tương miso', 'g', 198.00, 12.79, 6.01, 25.37, 4),
('Tương đen hoisin', 'g', 220.00, 3.31, 3.39, 44.08, 4),
('Tương ớt sriracha', 'g', 93.00, 1.93, 0.93, 19.16, 4),
('Đường cát trắng', 'g', 387.00, 0.00, 0.00, 99.98, 4),
('Đường nâu', 'g', 380.00, 0.12, 0.00, 98.09, 4),
('Ớt bột', 'g', 282.00, 13.46, 14.28, 49.70, 4),
('Ớt bột paprika', 'g', 282.00, 14.14, 12.89, 53.99, 4),
-- Kệ 5: Đồ khô & Gạo (32 dòng)
('Bún gạo khô', 'g', 364.00, 5.95, 0.56, 80.18, 5),
('Bột báng', 'g', 358.00, 0.19, 0.02, 88.69, 5),
('Bột gạo lứt', 'g', 363.00, 7.23, 2.78, 76.48, 5),
('Bột mì làm bánh mì', 'g', 361.00, 11.98, 1.66, 72.53, 5),
('Bột mì nguyên cám', 'g', 340.00, 13.21, 2.50, 71.97, 5),
('Bột mì đa dụng', 'g', 364.00, 10.33, 0.98, 76.31, 5),
('Bột ngô thô trắng', 'g', 362.00, 8.12, 3.59, 76.89, 5),
('Bột ngô trắng', 'g', 361.00, 6.93, 3.86, 76.85, 5),
('Chao', 'g', 151.00, 12.50, 8.10, 6.90, 5),
('Gạo lứt', 'g', 367.00, 7.54, 3.20, 76.25, 5),
('Gạo trắng', 'g', 365.00, 7.13, 0.66, 79.95, 5),
('Hạt ngô trắng', 'g', 365.00, 9.42, 4.74, 74.26, 5),
('Hạt đậu đũa', 'g', 347.00, 24.33, 1.31, 61.91, 5),
('Miến đậu nành', 'g', 331.00, 0.10, 0.10, 82.32, 5),
('Mì xào chow mein', 'g', 471.00, 10.88, 21.24, 63.64, 5),
('Nấm mèo khô', 'g', 284.00, 9.25, 0.73, 73.01, 5),
('Rong biển kombu', 'g', 43.00, 1.68, 0.56, 9.57, 5),
('Rong biển wakame', 'g', 45.00, 3.03, 0.64, 9.14, 5),
('Tinh bột ngô', 'g', 381.00, 0.26, 0.05, 91.27, 5),
('Đậu gà', 'g', 378.00, 20.47, 6.04, 62.95, 5),
('Đậu hũ', 'g', 76.00, 8.08, 4.78, 1.87, 5),
('Đậu hũ cứng', 'g', 144.00, 17.27, 8.72, 2.78, 5),
('Đậu lăng', 'g', 352.00, 24.63, 1.06, 63.35, 5),
('Đậu rồng', 'g', 409.00, 29.65, 16.32, 41.71, 5),
('Đậu trắng', 'g', 333.00, 23.36, 0.85, 60.27, 5),
('Đậu tây', 'g', 333.00, 23.58, 0.83, 60.01, 5),
('Đậu tây đỏ', 'g', 337.00, 22.53, 1.06, 61.29, 5),
('Đậu urad', 'g', 341.00, 25.21, 1.64, 58.99, 5),
('Đậu xanh', 'g', 347.00, 23.86, 1.15, 62.62, 5),
('Đậu đen', 'g', 341.00, 21.60, 1.42, 62.36, 5),
('Đậu đen turtle', 'g', 339.00, 21.25, 0.90, 63.25, 5),
('Đậu đỏ', 'g', 329.00, 19.87, 0.53, 62.90, 5),
-- Kệ 6: Sữa & Trứng (19 dòng)
('Bơ mặn', 'g', 717.00, 0.85, 81.11, 0.06, 6),
('Kem chua', 'g', 198.00, 2.44, 19.35, 4.63, 6),
('Lòng trắng trứng', 'g', 52.00, 10.90, 0.17, 0.73, 6),
('Lòng đỏ trứng', 'g', 322.00, 15.86, 26.54, 3.59, 6),
('Phô mai cheddar', 'g', 403.00, 22.87, 33.31, 3.37, 6),
('Phô mai feta', 'g', 265.00, 14.21, 21.49, 3.88, 6),
('Phô mai kem', 'g', 350.00, 6.15, 34.44, 5.52, 6),
('Phô mai mozzarella', 'g', 299.00, 22.17, 22.14, 2.40, 6),
('Phô mai parmesan xay', 'g', 420.00, 28.42, 27.84, 13.91, 6),
('Phô mai ricotta', 'g', 150.00, 7.54, 10.18, 7.27, 6),
('Phô mai tươi queso fresco', 'g', 299.00, 18.09, 23.82, 2.98, 6),
('Sữa chua Hy Lạp không đường', 'g', 73.00, 9.95, 1.92, 3.94, 6),
('Sữa chua không đường', 'g', 63.00, 5.25, 1.55, 7.04, 6),
('Sữa tách béo', 'g', 34.00, 3.37, 0.08, 4.96, 6),
('Sữa tươi nguyên kem', 'g', 61.00, 3.15, 3.25, 4.80, 6),
('Sữa ít béo', 'g', 50.00, 3.30, 1.98, 4.80, 6),
('Trứng cút', 'g', 158.00, 13.05, 11.09, 0.41, 6),
('Trứng gà', 'g', 143.00, 12.56, 9.51, 0.72, 6),
('Trứng vịt', 'g', 185.00, 12.81, 13.77, 1.45, 6),
-- Kệ 7: Trái cây (34 dòng)
('Bưởi', 'g', 38.00, 0.76, 0.04, 9.62, 7),
('Bưởi chùm', 'g', 32.00, 0.63, 0.10, 8.08, 7),
('Cam', 'g', 47.00, 0.94, 0.12, 11.75, 7),
('Chanh', 'g', 30.00, 0.70, 0.20, 10.54, 7),
('Chanh dây', 'g', 97.00, 2.20, 0.70, 23.38, 7),
('Chuối', 'g', 89.00, 1.09, 0.33, 22.84, 7),
('Chuối sứ xanh', 'g', 152.00, 1.25, 0.07, 36.66, 7),
('Cùi dừa', 'g', 354.00, 3.33, 33.49, 15.23, 7),
('Dâu tây', 'g', 32.00, 0.67, 0.30, 7.68, 7),
('Dưa hấu', 'g', 30.00, 0.61, 0.15, 7.55, 7),
('Dứa', 'g', 50.00, 0.54, 0.12, 13.12, 7),
('Khế', 'g', 31.00, 1.04, 0.33, 6.73, 7),
('Kiwi', 'g', 61.00, 1.14, 0.52, 14.66, 7),
('Lựu', 'g', 83.00, 1.67, 1.17, 18.70, 7),
('Me', 'g', 239.00, 2.80, 0.60, 62.50, 7),
('Mãng cầu ta', 'g', 94.00, 2.06, 0.29, 23.64, 7),
('Mãng cầu xiêm', 'g', 66.00, 1.00, 0.30, 16.84, 7),
('Mít', 'g', 95.00, 1.72, 0.64, 23.25, 7),
('Nhãn', 'g', 60.00, 1.31, 0.10, 15.14, 7),
('Nước chanh dây', 'g', 51.00, 0.39, 0.05, 13.60, 7),
('Nước cốt chanh', 'g', 25.00, 0.42, 0.07, 8.42, 7),
('Nước cốt chanh vàng', 'g', 22.00, 0.35, 0.24, 6.90, 7),
('Nước dừa', 'g', 19.00, 0.72, 0.20, 3.71, 7),
('Quýt', 'g', 53.00, 0.81, 0.31, 13.34, 7),
('Quả bơ', 'g', 120.00, 2.23, 10.06, 7.82, 7),
('Quất', 'g', 71.00, 1.88, 0.86, 15.90, 7),
('Sầu riêng', 'g', 147.00, 1.47, 5.33, 27.09, 7),
('Táo', 'g', 52.00, 0.26, 0.17, 13.81, 7),
('Táo ta', 'g', 79.00, 1.20, 0.20, 20.23, 7),
('Vải', 'g', 66.00, 0.83, 0.44, 16.53, 7),
('Xoài', 'g', 60.00, 0.82, 0.38, 14.98, 7),
('Đu đủ', 'g', 43.00, 0.47, 0.26, 10.82, 7),
('Đào', 'g', 39.00, 0.91, 0.25, 9.54, 7),
('Ổi', 'g', 68.00, 2.55, 0.95, 14.32, 7),
-- Kệ 8: Dầu mỡ & Chất béo (9 dòng)
('Dầu bơ', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Dầu cọ', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Dầu dừa', 'g', 892.00, 0.00, 99.06, 0.00, 8),
('Dầu gạo', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Dầu hướng dương', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Dầu hạt cải', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Dầu mù tạt', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Dầu đậu nành', 'g', 884.00, 0.00, 100.00, 0.00, 8),
('Mỡ heo', 'g', 902.00, 0.00, 100.00, 0.00, 8),
-- Kệ 9: Các loại Hạt (11 dòng)
('Hạnh nhân', 'g', 579.00, 21.15, 49.93, 21.55, 9),
('Hạt bí', 'g', 559.00, 30.23, 49.05, 10.71, 9),
('Hạt dưa hấu', 'g', 557.00, 28.33, 47.37, 15.31, 9),
('Hạt dẻ', 'g', 224.00, 4.20, 1.11, 49.07, 9),
('Hạt hướng dương', 'g', 584.00, 20.78, 51.46, 20.00, 9),
('Hạt macadamia', 'g', 718.00, 7.91, 75.77, 13.82, 9),
('Hạt mè', 'g', 573.00, 17.73, 49.67, 23.45, 9),
('Hạt mè bóc vỏ', 'g', 631.00, 20.45, 61.21, 11.73, 9),
('Hạt sen', 'g', 89.00, 4.13, 0.53, 17.28, 9),
('Hạt điều', 'g', 553.00, 18.22, 43.85, 30.19, 9),
('Đậu phộng', 'g', 570.00, 26.15, 49.60, 15.83, 9)

ON DUPLICATE KEY UPDATE
    `calories_per_100g` = VALUES(`calories_per_100g`),
    `protein`           = VALUES(`protein`),
    `fat`               = VALUES(`fat`),
    `carbs`             = VALUES(`carbs`),
    `aisle_id`          = VALUES(`aisle_id`);

-- Quy đổi ml -> g riêng cho từng nguyên liệu, dùng khi công thức ghi
-- '100 ml nước mắm' mà tủ lạnh lưu theo gam. multiplier = khối lượng
-- riêng (g/ml). Chỉ những dòng có `density` trong CSV mới cần.
--
-- ingredient_id lấy bằng subquery theo tên, không hard-code số, vì id
-- do AUTO_INCREMENT sinh ra và khác nhau giữa các lần reset DB.
-- Dùng INSERT ... SELECT (thay cho VALUES) để subquery chạy được.
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu bơ'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu cọ'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu dừa'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu gạo'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.1000, `id` FROM `ingredients` WHERE `name` = 'Dầu hào'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu hướng dương'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu hạt cải'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu mù tạt'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 0.9200, `id` FROM `ingredients` WHERE `name` = 'Dầu đậu nành'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.1000, `id` FROM `ingredients` WHERE `name` = 'Nước mắm'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.0300, `id` FROM `ingredients` WHERE `name` = 'Sữa tách béo'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.0300, `id` FROM `ingredients` WHERE `name` = 'Sữa tươi nguyên kem'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.0300, `id` FROM `ingredients` WHERE `name` = 'Sữa ít béo'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.1000, `id` FROM `ingredients` WHERE `name` = 'Tương đen hoisin'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)
SELECT 'ml', 'g', 1.1000, `id` FROM `ingredients` WHERE `name` = 'Tương ớt sriracha'
ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);

-- Kiểm tra nhanh sau khi nạp.
SELECT COUNT(*) AS tong_nguyen_lieu FROM `ingredients`;  -- kỳ vọng 290
SELECT a.`id`, a.`name`, COUNT(i.`id`) AS so_nguyen_lieu
FROM `aisles` a LEFT JOIN `ingredients` i ON i.`aisle_id` = a.`id`
GROUP BY a.`id`, a.`name` ORDER BY a.`id`;
SELECT COUNT(*) AS so_quy_doi_rieng FROM `unit_conversions`
WHERE `ingredient_id` IS NOT NULL;  -- kỳ vọng 15


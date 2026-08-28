-- Script khởi tạo Cơ sở dữ liệu cho dự án Smart Recipe & Grocery Platform
-- Hỗ trợ MySQL / TiDB

-- BẮT BUỘC: client mysql mặc định dùng latin1, nên nếu thiếu dòng này thì mọi
-- chuỗi tiếng Việt trong phần seed bên dưới bị mã hóa hai lần (mojibake kiểu
-- 'Háº£i sáº£n'). Đây từng là nguyên nhân của các file sql/fix_*.sql và của
-- CommandLineRunner fixDbEncoding trong BackendApplication.java — cả hai đã
-- được xóa vì encoding giờ đúng ngay từ lúc khởi tạo.
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `smart_recipe_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
USE `smart_recipe_db`;

-- 1. Nhóm Dữ liệu nền tảng & Phân quyền
CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `role` ENUM('ADMIN', 'USER') NOT NULL DEFAULT 'USER',
    `display_name` VARCHAR(100) NULL,
    `avatar_url` VARCHAR(255) NULL,
    `bio` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `aisles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `ingredients` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    -- UNIQUE là bắt buộc cho seed_ingredients.sql: câu INSERT ... ON DUPLICATE
    -- KEY UPDATE chỉ nhận ra "đã tồn tại" thông qua một unique index. Không có
    -- nó thì chạy seed lần thứ hai sẽ nhân đôi toàn bộ 289 dòng.
    -- Cũng chặn luôn lỗi cũ: luồng AI từng tạo 10 dòng 'Thịt Gà' trùng nhau.
    -- COLLATE utf8mb4_0900_as_ci: phân biệt dấu (as), không phân biệt hoa/thường (ci).
    -- Cần thiết vì mặc định MySQL 8.0 dùng ai_ci (accent-insensitive), khiến
    -- 'Dầu dừa' = 'Đậu đũa' và UNIQUE index fail với 2 tên hoàn toàn khác nhau.
    `name` VARCHAR(100) NOT NULL UNIQUE COLLATE utf8mb4_0900_as_ci,
    `base_unit` VARCHAR(20) NOT NULL,
    `calories_per_100g` DECIMAL(10,2) NOT NULL,
    `protein` DECIMAL(10,2) NOT NULL,
    `fat` DECIMAL(10,2) NOT NULL,
    `carbs` DECIMAL(10,2) NOT NULL,
    `aisle_id` INT,
    FOREIGN KEY (`aisle_id`) REFERENCES `aisles`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 2. Nhóm Quản lý Công thức nấu ăn
CREATE TABLE IF NOT EXISTS `recipes` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `author_id` BIGINT NOT NULL,
    `cloned_from_id` BIGINT NULL,
    `title` VARCHAR(255) NOT NULL,
    `base_servings` INT NOT NULL,
    -- Phải khớp đủ 4 giá trị của enums/RecipeStatus.java. Thiếu DRAFT/DELETED sẽ
    -- gây "Data truncated for column 'status'" khi lưu bản nháp hoặc xóa công thức,
    -- vì ddl-auto:update không sửa type của cột đã tồn tại.
    `status` ENUM('DRAFT', 'PRIVATE', 'PUBLIC', 'DELETED') NOT NULL DEFAULT 'PRIVATE',
    `description` TEXT NULL,
    `image_url` VARCHAR(255) NULL,
    `prep_time` INT NULL, -- Đơn vị: phút
    `cook_time` INT NULL, -- Đơn vị: phút
    `difficulty` ENUM('EASY', 'MEDIUM', 'HARD') NULL,
    `like_count` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`author_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`cloned_from_id`) REFERENCES `recipes`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `recipe_steps` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `recipe_id` BIGINT NOT NULL,
    `step_number` INT NOT NULL,
    -- title/image_url: entity RecipeStep.java có, init cũ thiếu -> Hibernate tự thêm
    `title` VARCHAR(255) NULL,
    `instruction` TEXT NOT NULL,
    `image_url` VARCHAR(500) NULL,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `recipe_ingredients` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `recipe_id` BIGINT NOT NULL,
    `ingredient_id` BIGINT NOT NULL,
    `amount` DECIMAL(10,2) NOT NULL,
    `unit` VARCHAR(20) NOT NULL,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `tags` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `recipe_tags` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `recipe_id` BIGINT NOT NULL,
    `tag_id` INT NOT NULL,
    UNIQUE(`recipe_id`, `tag_id`),
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Nhóm Kho Tủ lạnh & Đi chợ
CREATE TABLE IF NOT EXISTS `user_pantry` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `ingredient_id` BIGINT NOT NULL,
    `quantity_available` DECIMAL(10,2) NOT NULL,
    `low_stock_threshold` DECIMAL(10,2) NULL,
    `expiry_date` DATE NULL,
    UNIQUE(`user_id`, `ingredient_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `grocery_lists` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `status` ENUM('ACTIVE', 'COMPLETED') NOT NULL DEFAULT 'ACTIVE',
    `name` VARCHAR(100) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `completed_at` TIMESTAMP NULL,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `grocery_items` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `grocery_list_id` BIGINT NOT NULL,
    `ingredient_id` BIGINT NOT NULL,
    `total_needed` DECIMAL(10,2) NOT NULL,
    `pantry_deducted` DECIMAL(10,2) NOT NULL DEFAULT 0,
    `final_to_buy` DECIMAL(10,2) NOT NULL,
    `is_bought` BOOLEAN DEFAULT FALSE,
    -- is_manual: item do user tự thêm, không sinh từ công thức (GroceryItem.java)
    `is_manual` BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (`grocery_list_id`) REFERENCES `grocery_lists`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `grocery_list_recipes` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `grocery_list_id` BIGINT NOT NULL,
    `recipe_id` BIGINT NOT NULL,
    `servings` INT NOT NULL,
    UNIQUE(`grocery_list_id`, `recipe_id`),
    FOREIGN KEY (`grocery_list_id`) REFERENCES `grocery_lists`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `unit_conversions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `from_unit` VARCHAR(20) NOT NULL,
    `to_unit` VARCHAR(20) NOT NULL,
    `multiplier` DECIMAL(10,4) NOT NULL,
    `ingredient_id` BIGINT NULL,
    UNIQUE(`from_unit`, `to_unit`, `ingredient_id`),
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Nhóm Nhật ký Bếp núc & Trợ lý AI
CREATE TABLE IF NOT EXISTS `cooking_journals` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `recipe_id` BIGINT NULL, -- Cho phép NULL khi công thức gốc bị xóa
    `cooked_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `iteration_notes` TEXT NULL,
    `image_url` VARCHAR(255) NULL,
    `actual_servings` INT NOT NULL,
    `rating` TINYINT NULL CHECK (`rating` >= 1 AND `rating` <= 5),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `ai_suggestion_logs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `type` ENUM('ZERO_WASTE', 'FEASIBLE_FINDER') NOT NULL,
    `input_ingredients` JSON NOT NULL,
    `output_response` JSON NOT NULL,
    `saved_recipe_id` BIGINT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`saved_recipe_id`) REFERENCES `recipes`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 5. Nhóm Cộng đồng & Tương tác xã hội
CREATE TABLE IF NOT EXISTS `recipe_likes` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `recipe_id` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(`user_id`, `recipe_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `recipe_comments` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL,
    `recipe_id` BIGINT NOT NULL,
    -- parent_id: comment trả lời comment khác (RecipeComment.java tự tham chiếu)
    `parent_id` BIGINT NULL,
    `content` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`parent_id`) REFERENCES `recipe_comments`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- follows: entity Follow.java đã có, init cũ thiếu bảng này
CREATE TABLE IF NOT EXISTS `follows` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `follower_id` BIGINT NOT NULL,
    `following_id` BIGINT NOT NULL,
    `created_at` DATETIME(6) NULL,
    UNIQUE(`follower_id`, `following_id`),
    FOREIGN KEY (`follower_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`following_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ==========================================
-- Chỉ mục (Indexes) cho hiệu suất truy vấn
-- ==========================================

-- Recipes: Tìm kiếm theo tác giả, lọc theo trạng thái, sắp xếp theo lượt thích
CREATE INDEX `idx_recipes_author_id` ON `recipes`(`author_id`);
CREATE INDEX `idx_recipes_status` ON `recipes`(`status`);
CREATE INDEX `idx_recipes_created_at` ON `recipes`(`created_at`);

-- Recipe Steps: Truy vấn theo công thức và sắp xếp theo thứ tự bước
CREATE INDEX `idx_recipe_steps_recipe_id` ON `recipe_steps`(`recipe_id`);

-- Recipe Ingredients: Truy vấn nguyên liệu của một công thức
CREATE INDEX `idx_recipe_ingredients_recipe_id` ON `recipe_ingredients`(`recipe_id`);

-- User Pantry: Truy vấn kho theo người dùng
CREATE INDEX `idx_user_pantry_user_id` ON `user_pantry`(`user_id`);

-- Grocery Lists: Lấy danh sách đi chợ theo người dùng
CREATE INDEX `idx_grocery_lists_user_id` ON `grocery_lists`(`user_id`);

-- Grocery Items: Lấy chi tiết theo danh sách đi chợ
CREATE INDEX `idx_grocery_items_grocery_list_id` ON `grocery_items`(`grocery_list_id`);

-- Cooking Journals: Lịch sử nấu ăn theo người dùng
CREATE INDEX `idx_cooking_journals_user_id` ON `cooking_journals`(`user_id`);

-- Recipe Likes: Đếm like theo công thức, kiểm tra user đã like chưa
CREATE INDEX `idx_recipe_likes_recipe_id` ON `recipe_likes`(`recipe_id`);

-- Recipe Comments: Lấy bình luận theo công thức
CREATE INDEX `idx_recipe_comments_recipe_id` ON `recipe_comments`(`recipe_id`);

-- AI Suggestion Logs: Lịch sử gợi ý theo người dùng
CREATE INDEX `idx_ai_suggestion_logs_user_id` ON `ai_suggestion_logs`(`user_id`);

-- ==========================================
-- Dữ liệu mẫu (Seeding Data) cho các bảng từ điển
-- ==========================================

-- 9 kệ hàng. Ghi thẳng ở đây thay cho sql/migrate_aisles_v2.sql (đã xóa):
-- vì quy trình reset là `docker-compose down -v` nên không có lý do gì để tạo
-- 6 kệ rồi migrate lên 9. id 1-9 phải khớp cột `aisle_id` trong
-- dataset/ingredients_to_translate.csv — đừng đổi thứ tự.
--
-- Vì sao 9 mà không phải 6: 6 kệ cũ không phủ hết 14 food_category của USDA.
-- 'Rau củ quả' gộp cà chua với chuối, còn dầu ăn và các loại hạt không có kệ.
INSERT INTO `aisles` (`id`, `name`) VALUES
(1, 'Rau củ'),
(2, 'Thịt & Gia cầm'),
(3, 'Hải sản'),
(4, 'Gia vị & Nước chấm'),
(5, 'Đồ khô & Gạo'),
(6, 'Sữa & Trứng'),
(7, 'Trái cây'),
(8, 'Dầu mỡ & Chất béo'),
(9, 'Các loại Hạt');

-- Đưa AUTO_INCREMENT về sau id lớn nhất, tránh va chạm khi thêm kệ qua API
ALTER TABLE `aisles` AUTO_INCREMENT = 10;

INSERT INTO `tags` (`name`) VALUES 
('Ăn chay'), 
('Giảm cân'), 
('Dưới 30 phút'), 
('Món kho'), 
('Món canh'), 
('Ăn sáng');

-- Quy đổi đơn vị dùng chung (ingredient_id = NULL nghĩa là áp dụng cho mọi
-- nguyên liệu). Lưu ý: UNIQUE(from_unit,to_unit,ingredient_id) KHÔNG chống
-- được trùng khi ingredient_id IS NULL vì MySQL coi mỗi NULL là một giá trị
-- khác nhau. Vì vậy file này chỉ được chạy trên database rỗng; muốn chạy lại
-- phải DELETE trước, không dùng ON DUPLICATE KEY UPDATE.
INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`) VALUES
('kg', 'g', 1000, NULL),
('l', 'ml', 1000, NULL),
('muỗng canh', 'ml', 15, NULL),
('muỗng cà phê', 'ml', 5, NULL),
('chén', 'ml', 250, NULL),
('bát', 'ml', 300, NULL);

-- KHÔNG seed `ingredients` ở đây.
--
-- 15 dòng nguyên liệu mẫu cũ đã được bỏ: nguồn sự thật duy nhất bây giờ là
-- sql/seed_ingredients.sql (290 dòng sinh từ dataset/ingredients_to_translate.csv
-- bằng tools/gen_seed_sql.py, dinh dưỡng lấy từ USDA FoodData Central).
-- Giữ cả hai sẽ gây hai vấn đề:
--   1. 7 tên trùng nhau (Trứng gà, Nước mắm, Tiêu đen, Tỏi, Hành tím, Cà chua,
--      Rau muống) -> seed phải ON DUPLICATE KEY UPDATE và sẽ ghi đè base_unit
--      của 'Trứng gà' từ 'quả' thành 'g'.
--   2. 7 tên còn lại (Thịt heo ba chỉ, Ức gà, Gạo tẻ, Đường, Tôm sú,
--      Sữa tươi, Bột mì) sẽ nằm cạnh bản chi tiết hơn của CSV
--      (Thịt heo ba rọi, Ức gà có da, Gạo trắng, Đường cát trắng, Tôm,
--      Sữa tươi nguyên kem, Bột mì đa dụng) -> người dùng thấy hai lựa chọn
--      gần trùng nghĩa cho cùng một thứ.
--      'Cá hồi' của bản mẫu cũ đã được thêm lại vào CSV qua
--      tools/add_salmon.py (fdc_id 175167) nên không mất nguyên liệu này.
--
-- Chạy seed sau khi container mysql đã healthy:
--   docker cp sql/seed_ingredients.sql smartrecipe-mysql:/tmp/seed.sql
--   docker exec smartrecipe-mysql sh -c 'mysql -uroot -proot --default-character-set=utf8mb4 < /tmp/seed.sql'

-- ==========================================
-- Chuẩn hóa collation toàn bộ 18 bảng
-- ==========================================
-- MYSQL_DATABASE trong docker-compose tạo DB trước khi script này chạy, với
-- collation mặc định của server (utf8mb4_0900_ai_ci). Các bảng tạo trong DB đó
-- kế thừa ai_ci, khiến JOIN giữa các bảng sẽ ném ERROR 1267 (Illegal mix of
-- collations) nếu sau này cần so sánh hai cột text với nhau.
-- CONVERT TO CHARACTER SET áp dụng cho cả bảng lẫn từng cột text — an toàn
-- vì DB đang rỗng, chi phí bằng 0.
ALTER TABLE `ai_suggestion_logs`  CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `aisles`              CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `cooking_journals`    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `follows`             CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `grocery_items`       CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `grocery_list_recipes` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `grocery_lists`       CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `ingredients`         CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `recipe_comments`     CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `recipe_ingredients`  CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `recipe_likes`        CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `recipe_steps`        CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `recipe_tags`         CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `recipes`             CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `tags`                CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `unit_conversions`    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `user_pantry`         CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;
ALTER TABLE `users`               CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;

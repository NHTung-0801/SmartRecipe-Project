-- Script khởi tạo Cơ sở dữ liệu cho dự án Smart Recipe & Grocery Platform
-- Hỗ trợ MySQL / TiDB

CREATE DATABASE IF NOT EXISTS `smart_recipe_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
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
    `name` VARCHAR(100) NOT NULL,
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
    `status` ENUM('PRIVATE', 'PUBLIC') NOT NULL DEFAULT 'PRIVATE',
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
    `instruction` TEXT NOT NULL,
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
    `content` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE
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

INSERT INTO `aisles` (`name`) VALUES 
('Rau củ quả'), 
('Thịt, Gia cầm'), 
('Hải sản'), 
('Gia vị & Nước chấm'), 
('Đồ khô & Gạo'), 
('Sữa & Trứng');

INSERT INTO `tags` (`name`) VALUES 
('Ăn chay'), 
('Giảm cân'), 
('Dưới 30 phút'), 
('Món kho'), 
('Món canh'), 
('Ăn sáng');

INSERT INTO `unit_conversions` (`from_unit`, `to_unit`, `multiplier`, `ingredient_id`) VALUES
('kg', 'g', 1000, NULL),
('l', 'ml', 1000, NULL),
('muỗng canh', 'ml', 15, NULL),
('muỗng cà phê', 'ml', 5, NULL),
('chén', 'ml', 250, NULL),
('bát', 'ml', 300, NULL);

-- Nguyên liệu mẫu (Seed ingredients)
INSERT INTO `ingredients` (`name`, `base_unit`, `calories_per_100g`, `protein`, `fat`, `carbs`, `aisle_id`) VALUES
('Thịt heo ba chỉ', 'g', 518.00, 9.34, 53.01, 0.00, 2),
('Ức gà', 'g', 165.00, 31.02, 3.57, 0.00, 2),
('Trứng gà', 'quả', 155.00, 12.56, 10.61, 1.12, 6),
('Gạo tẻ', 'g', 130.00, 2.69, 0.28, 28.17, 5),
('Hành tím', 'g', 40.00, 1.10, 0.10, 9.34, 1),
('Tỏi', 'g', 149.00, 6.36, 0.50, 33.06, 4),
('Nước mắm', 'ml', 35.00, 5.06, 0.00, 3.64, 4),
('Đường', 'g', 387.00, 0.00, 0.00, 99.80, 4),
('Cà chua', 'g', 18.00, 0.88, 0.20, 3.89, 1),
('Rau muống', 'g', 19.00, 2.60, 0.20, 3.14, 1),
('Tôm sú', 'g', 99.00, 24.00, 0.30, 0.00, 3),
('Cá hồi', 'g', 208.00, 20.42, 13.42, 0.00, 3),
('Sữa tươi', 'ml', 61.00, 3.15, 3.25, 4.80, 6),
('Bột mì', 'g', 364.00, 10.33, 0.98, 76.31, 5),
('Tiêu đen', 'g', 251.00, 10.39, 3.26, 63.95, 4);

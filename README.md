# 🍳 SmartRecipe & Grocery Platform

> **Nền tảng Quản lý và Chia sẻ Công thức Nấu ăn Thông minh** — Đồ án Thực tập Tốt nghiệp (TTTN)

Một web application hiện đại đóng vai trò như **trợ lý bếp núc cá nhân toàn diện**: quản lý tủ nguyên liệu, tự động tạo danh sách đi chợ từ thực đơn, gợi ý công thức từ AI dựa trên đồ sắp hết hạn, và kết nối cộng đồng yêu ẩm thực.

---

## 📋 Mục lục

- [Mục tiêu & Đối tượng](#-mục-tiêu--đối-tượng)
- [Tổng quan hệ thống](#-tổng-quan-hệ-thống)
- [Tech Stack](#-tech-stack)
- [Cấu trúc Monorepo](#-cấu-trúc-monorepo)
- [Tiến độ dự án (6 Sprints)](#-tiến-độ-dự-án-6-sprints)
- [Pipeline Dữ liệu Nguyên liệu](#-pipeline-dữ-liệu-nguyên-liệu-usda--việt-nam)
- [Thiết lập môi trường](#-thiết-lập-môi-trường-local)
- [Nạp Dữ liệu Nguyên liệu](#-nạp-dữ-liệu-nguyên-liệu)
- [Tài liệu chi tiết](#-tài-liệu-chi-tiết)

---

## 🎯 Mục tiêu & Đối tượng

### Vấn đề cần giải quyết
Người Việt thường gặp ba bài toán lặp đi lặp lại hàng ngày:
1. **"Hôm nay nấu gì?"** — Không biết làm món gì với đồ đang có trong tủ.
2. **Lãng phí thực phẩm** — Rau củ, thịt cá mua về nhiều, hết hạn mà không dùng hết.
3. **Đi chợ thiếu hoặc thừa** — Không nhớ đã có gì, mua trùng hoặc quên nguyên liệu.

### Đối tượng phục vụ
| Nhóm | Nhu cầu |
|---|---|
| Người nội trợ, sinh viên, dân văn phòng | Tự nấu tại nhà, tiết kiệm thời gian lên thực đơn và mua sắm |
| Người quan tâm sức khỏe / dinh dưỡng | Kiểm soát lượng Calo và Macro (Đạm, Béo, Tinh bột) |
| Cộng đồng yêu ẩm thực | Chia sẻ công thức, tìm kiếm cảm hứng, giao lưu thực đơn |

---

## 🏛 Tổng quan hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                       NGƯỜI DÙNG                             │
└───────────────────────────┬─────────────────────────────────┘
                            │ Browser
┌───────────────────────────▼─────────────────────────────────┐
│              FRONTEND — React 19 / Vite 8                    │
│  13 trang · 30+ components · CSS Modules + Tailwind v4       │
│  Zustand (auth state) · TanStack Query (server state)        │
│  Axios + JWT auto-refresh interceptor                        │
│         localhost:5173                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API / JSON
┌───────────────────────────▼─────────────────────────────────┐
│              BACKEND — Spring Boot 4 / Java 21               │
│  13 controllers · 18 repositories · Spring Security + JWT    │
│  Layered Architecture: Controller → Service → Repository     │
│         localhost:8080                                        │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
┌──────────────▼──────────┐    ┌───────────────▼──────────────┐
│  MySQL 8.0 (Docker)     │    │  Redis 7 (Docker)            │
│  18 bảng                │    │  JWT blacklist               │
│  290 nguyên liệu USDA   │    │  API cache (5-60 phút)       │
│  utf8mb4_0900_as_ci     │    │  AI rate limiting            │
│  localhost:3306          │    │  localhost:6379               │
└─────────────────────────┘    └──────────────────────────────┘
               │
┌──────────────▼──────────┐    ┌──────────────────────────────┐
│  Google Gemini AI        │    │  Cloudinary                  │
│  gemini-2.0-flash        │    │  Lưu trữ ảnh công thức       │
│  Gợi ý công thức         │    │  và ảnh đại diện             │
│  JSON structured output  │    └──────────────────────────────┘
└─────────────────────────┘
```

### 6 Module Cốt lõi

| # | Module | Tính năng chính |
|---|---|---|
| 1 | **Auth & Profiles** | Đăng nhập JWT + Refresh Token, phân quyền ADMIN/USER, quản lý hồ sơ, theo dõi nhau |
| 2 | **Recipe Engine** | CRUD công thức, tính Calo/Macro tự động, chế độ nấu step-by-step, xuất Word, clone & chia sẻ |
| 3 | **Virtual Pantry** | Tủ nguyên liệu 9 kệ hàng, theo dõi hạn dùng, cảnh báo sắp hết, quy đổi đơn vị tự động |
| 4 | **Smart Grocery** | Tạo danh sách từ thực đơn, gộp trùng, trừ đồ sẵn có, Shopping Mode, tự động cập nhật tủ |
| 5 | **AI Assistant** | Gemini gợi ý công thức Zero-Waste từ tủ lạnh, rate limiting 10 lần/ngày/user qua Redis |
| 6 | **Community** | Feed công thức, like, bình luận, theo dõi người dùng, nhật ký nấu ăn có ảnh + đánh giá sao |

---

## 🛠 Tech Stack

### Frontend
| Công nghệ | Phiên bản | Vai trò |
|---|---|---|
| React | 19.2 | UI Framework |
| Vite | 8.2 | Build tool + HMR |
| React Router DOM | 7.18 | Client-side routing |
| TanStack Query | 5.101 | Server state, caching, auto-refetch |
| Zustand | 5.0 | Client state (auth persistence) |
| Axios | 1.19 | HTTP client + JWT interceptor |
| React Hook Form + Zod | 7.84 / 4.4 | Form & validation |
| Tailwind CSS v4 | 4.3 | Utility styling |
| Lucide React | 1.28 | Icon library |
| Vitest + Testing Library | 4.1 / 16.3 | Unit testing |
| OxLint | 1.75 | Linter (Rust-based, nhanh hơn ESLint) |

### Backend
| Công nghệ | Phiên bản | Vai trò |
|---|---|---|
| Spring Boot | 4.1.0 | Framework |
| Java | 21 | Ngôn ngữ |
| Spring Data JPA + Hibernate | - | ORM |
| Spring Security + jjwt | 0.11.5 | Authentication & Authorization |
| Spring Data Redis | - | Caching & rate limiting |
| MySQL Connector/J | - | JDBC driver |
| Lombok | - | Boilerplate reduction |
| Jackson | - | JSON serialization |
| Cloudinary | 1.36.0 | Cloud image storage |
| Apache POI | 5.2.3 | Export file Word (.docx) |
| spring-dotenv | 4.0.0 | `.env` file support |

### Infrastructure
| Công nghệ | Vai trò |
|---|---|
| Docker & Docker Compose | Local containerization |
| MySQL 8.0 | Relational database |
| Redis 7 | In-memory cache & rate limiting |
| Nginx | Frontend hosting (production) |
| Google Gemini API | AI recipe generation |
| Cloudinary CDN | Image storage & delivery |

---

## 📁 Cấu trúc Monorepo

```
SmartRecipe-Project/
│
├── smartrecipe-backend/        # Spring Boot API (Java 21)
│   ├── src/main/java/          # Source code (9 packages)
│   ├── src/main/resources/     # application.yaml
│   ├── .docker/Dockerfile      # Production Docker image
│   ├── pom.xml                 # Maven dependencies
│   └── README.md               # ← Chi tiết backend
│
├── smartrecipe-frontend/       # React SPA (Vite 8)
│   ├── src/                    # Source code (pages, components, services...)
│   ├── vite.config.js
│   ├── package.json
│   └── README.md               # ← Chi tiết frontend
│
├── sql/                        # Database scripts
│   ├── init_database.sql       # Khởi tạo 18 bảng + 9 kệ + 6 tags + unit conversions
│   └── seed_ingredients.sql    # 290 nguyên liệu từ USDA (sinh bởi tools/)
│
├── Dataset/                    # Dữ liệu gốc USDA FoodData Central
│   ├── FoodData_Central_sr_legacy_food_csv_2018-04/
│   │   ├── food.csv            # ~8.000 thực phẩm thô
│   │   ├── food_nutrient.csv   # ~600.000 dòng dinh dưỡng (36 MB)
│   │   ├── food_category.csv   # 25 nhóm thực phẩm
│   │   ├── nutrient.csv        # Định nghĩa 150+ chất dinh dưỡng
│   │   └── food_portion.csv    # Khẩu phần tham chiếu
│   ├── ingredients_to_translate.csv  # 290 nguyên liệu sau xử lý (đã dịch)
│   └── dropped_ingredients.csv       # ~1.500 nguyên liệu đã loại + lý do
│
├── tools/                      # Python data pipeline scripts
│   ├── clean_ingredients.py    # Giai đoạn 1: Lọc + join dinh dưỡng từ USDA
│   ├── suggest_keep.py         # Giai đoạn 2: Luật lọc nguyên liệu phù hợp bếp Việt
│   ├── collapse_groups.py      # Giai đoạn 2: Gộp nhóm biến thể (bò xay 70% → bò xay)
│   ├── export_batches.py       # Giai đoạn 2: Chia batch để dịch thủ công
│   ├── translate_helper.py     # Giai đoạn 2: Hỗ trợ dịch Anh → Việt
│   ├── assign_aisles.py        # Giai đoạn 3: Gán 9 kệ hàng theo 2 lớp logic
│   ├── add_missing_essentials.py # Thêm nguyên liệu thiết yếu bị lọc nhầm
│   ├── add_salmon.py           # Thêm Cá hồi từ USDA fdc_id 175167
│   ├── repair_csv.py           # Sửa CSV bị Excel làm hỏng encoding
│   ├── verify_dataset.py       # Kiểm tra toàn vẹn dataset trước khi seed
│   └── gen_seed_sql.py         # Giai đoạn 4: Sinh seed_ingredients.sql
│
├── docs/                       # Tài liệu thiết kế & kế hoạch
│   ├── project_master_plan.md
│   ├── implementation_plan.md
│   ├── sprint4_plan.md
│   └── ...
│
├── backup/                     # Database backups trước khi thay đổi lớn
├── docker-compose.yml          # Định nghĩa 4 services (mysql, redis, backend, frontend)
└── README.md                   # ← File này
```

---

## 📊 Tiến độ dự án (6 Sprints)

Chiến lược phát triển: **Backend trước → Frontend sau** cho mỗi Sprint.

```
Sprint 1 ████████████████████ 100%  Auth & Security (JWT, Login, Register)
Sprint 2 ████████████████████ 100%  Users, Profile, Master Data, Redis Cache
Sprint 3 ████████████████████ 100%  Recipe Engine (CRUD, Feed, Clone, Export)
Sprint 4 ████████████████████ 100%  Pantry & Smart Grocery List
Sprint 5 ██████████████████░░  90%  AI Assistant, Cooking Journal (đang hoàn thiện)
Sprint 6 ░░░░░░░░░░░░░░░░░░░░   0%  Community, Deploy
```

### ✅ Sprint 1 — Auth & Security
- JWT Access Token (24h) + Refresh Token (7d) + tự động refresh phía client
- `SecurityConfig`, `JwtProvider`, `JwtAuthFilter`
- API: `POST /auth/register`, `/auth/login`, `/auth/refresh`
- UI: `LoginPage.jsx`, `RegisterPage.jsx`, `ProtectedRoute`

### ✅ Sprint 2 — Users & Master Data
- Quản lý profile, upload avatar qua Cloudinary
- Redis Cache cho Master Data (`ingredients`, `aisles`, `tags`, `unit_conversions`)
- Component `IngredientAutocomplete` + `UnitAutocomplete` phía frontend

### ✅ Sprint 3 — Recipe Engine
- CRUD công thức (DRAFT / PRIVATE / PUBLIC / DELETED soft-delete)
- Feed cộng đồng phân trang, tìm kiếm theo tên/tag/nguyên liệu
- Clone công thức, Like/Unlike, bình luận
- Chế độ nấu step-by-step (`CookingMode.jsx`)
- Xuất công thức ra Word (Apache POI)
- 5/5 unit tests service xanh (JUnit 5 + Mockito)

### ✅ Sprint 4 — Pantry & Smart Grocery
- Tủ nguyên liệu nhóm theo **9 kệ hàng** động (không hard-code)
- Thuật toán quy đổi đơn vị (BFS graph: kg→g, ml→g theo density)
- Tạo grocery list từ công thức: tổng cần − đã có = cần mua
- Shopping Mode full-screen + confetti khi hoàn thành
- Tự động cập nhật tủ khi đánh dấu "Đã hoàn thành đi chợ"
- 9/9 unit tests Pantry service xanh

### 🔄 Sprint 5 — AI Assistant & Cooking Journal (đang hoàn thiện)
- ✅ Gemini `gemini-2.0-flash` tích hợp qua `GeminiClient`
- ✅ Rate limiting AI 10 lần/ngày/user qua Redis
- ✅ 3-layer ingredient matching: Exact → Token → Auto-create
- ✅ `CookingJournalPage.jsx` với Timeline UI + `JournalDetailPage.jsx`
- ✅ Xử lý lỗi `AiServiceException` (503) + `AccessDeniedException` (403 thay vì 500)
- ✅ `GET /ai/history`, `GET /ai/remaining` — 38/38 unit test backend xanh
- ✅ Phân quyền `POST /ingredients` chỉ ADMIN; user thường dùng `POST /ingredients/quick`
- ✅ Test runner frontend: Vitest + Testing Library — 17/17 test xanh
- 🔄 Bộ lọc admin cho nguyên liệu `calories = 0` (loại trừ nhóm gia vị như Muối)

### ⏳ Sprint 6 — Community & Deploy
- API Like, Comment với nested threads
- Notification system
- Deploy: Vercel (Frontend), Railway (Backend), PlanetScale/TiDB (MySQL)

---

## 🔬 Pipeline Dữ liệu Nguyên liệu: USDA → Việt Nam

Đây là một trong những phần kỹ thuật phức tạp nhất của dự án — xây dựng bộ dữ liệu 290 nguyên liệu tiếng Việt **có nguồn gốc rõ ràng, dinh dưỡng chính xác** từ cơ sở dữ liệu khoa học quốc tế.

### Nguồn dữ liệu gốc

**USDA FoodData Central — SR Legacy 2018** ([Tải về](https://fdc.nal.usda.gov/download-foods.html))

| File | Kích thước | Nội dung |
|---|---|---|
| `food.csv` | 793 KB | ~8.000 thực phẩm với mã `fdc_id` và `food_category_id` |
| `food_nutrient.csv` | **36 MB** | ~600.000 dòng — mỗi dòng là 1 chất dinh dưỡng của 1 thực phẩm |
| `food_category.csv` | 1 KB | 25 nhóm thực phẩm của USDA |
| `nutrient.csv` | 21 KB | Định nghĩa 150+ chất dinh dưỡng (id, tên, đơn vị) |
| `food_portion.csv` | 919 KB | Khẩu phần tiêu chuẩn tham chiếu |

### Pipeline xử lý (4 giai đoạn)

```
USDA SR Legacy (~8.000 thực phẩm)
          │
          ▼ Giai đoạn 1: clean_ingredients.py
┌─────────────────────────────────────────┐
│  • Lọc 14/25 category phù hợp bếp Việt │
│  • Join food + food_nutrient → lấy     │
│    Calo, Protein, Fat, Carb per 100g   │
│  • Lọc thực phẩm chế biến sẵn,        │
│    thương mại, không có dinh dưỡng     │
│  • Tính density (g/ml) cho chất lỏng   │
│    (dựa trên food_portion.csv)         │
│  → ~1.800 dòng ứng viên               │
└─────────────────────────────────────────┘
          │
          ▼ Giai đoạn 2: Lọc thủ công + bán tự động
┌─────────────────────────────────────────┐
│  suggest_keep.py — Luật loại:           │
│  • Thịt thú lạ (emu, ostrich, bison)   │
│  • Phân loại Mỹ quá chi tiết           │
│    ("trimmed to 1/4" fat", "choice")   │
│  • Nội tạng ít dùng, đồ ăn chế biến   │
│  • Đồ uống công nghiệp, cồn            │
│  → ~350 dòng                           │
│                                        │
│  collapse_groups.py — Gộp biến thể:   │
│  • "Thịt bò xay 70%/80%/90% nạc"     │
│    → "Thịt bò xay" (giữ 80% làm chuẩn)│
│  • "Ức gà có da / không da"           │
│    → tách thành 2 nguyên liệu riêng   │
│  → ~310 dòng                          │
│                                        │
│  export_batches.py → 6 batch           │
│  Dịch thủ công Anh → Việt             │
│  (vi_batch_001.txt đến _251.txt)      │
└─────────────────────────────────────────┘
          │
          ▼ Giai đoạn 3: assign_aisles.py
┌─────────────────────────────────────────┐
│  Hai lớp gán kệ hàng:                  │
│                                        │
│  Lớp 1 — Category Map (USDA → kệ VN): │
│  Cat 1 Dairy/Egg    → kệ 6 Sữa&Trứng  │
│  Cat 2 Spices/Herbs → kệ 4 Gia vị     │
│  Cat 4 Fats/Oils    → kệ 8 Dầu mỡ    │
│  Cat 5,10,13 Meat   → kệ 2 Thịt       │
│  Cat 9 Fruits       → kệ 7 Trái cây   │
│  Cat 11 Vegetables  → kệ 1 Rau củ     │
│  Cat 12 Nuts/Seeds  → kệ 9 Hạt        │
│  Cat 15 Fish        → kệ 3 Hải sản    │
│  Cat 16 Legumes     → kệ 5 Đồ khô    │
│  Cat 19 Sweets      → kệ 5 Đồ khô    │
│  Cat 20 Grains      → kệ 5 Đồ khô    │
│                                        │
│  Lớp 2 — Override theo ngữ nghĩa:     │
│  Nước tương, miso (Cat16) → kệ 4      │
│  Nước cốt dừa (Cat12) → kệ 5         │
│  Rong biển (Cat11) → kệ 5            │
│  (USDA phân theo nguồn gốc,           │
│   người đi chợ tìm theo vị trí)       │
└─────────────────────────────────────────┘
          │
          ▼ Giai đoạn 4: gen_seed_sql.py
┌─────────────────────────────────────────┐
│  Validate trước khi sinh:              │
│  • Tên rỗng / vượt VARCHAR(100)        │
│  • Trùng tuyệt đối                     │
│  • Trùng casefold() (theo as_ci)       │
│  • aisle_id ngoài 1-9                  │
│  • Số âm hoặc không parse được        │
│  → sys.exit() nếu bất kỳ lỗi nào     │
│                                        │
│  Sinh ra seed_ingredients.sql:         │
│  • SET NAMES utf8mb4 (không BOM)      │
│  • ON DUPLICATE KEY UPDATE             │
│    (không ghi đè base_unit của admin) │
│  • 15 unit_conversions ml→g           │
│    (gắn ingredient_id cụ thể qua      │
│     subquery theo tên)                │
└─────────────────────────────────────────┘
          │
          ▼ Kết quả cuối cùng
  290 nguyên liệu  |  9 kệ hàng  |  15 quy đổi density
  base_unit = 'g' cho 290/290 dòng
  4 cặp tên nguy hiểm được tách đúng:
  Dầu dừa (892 kcal) ≠ Đậu đũa (47 kcal)
  Dâu tây (32 kcal)  ≠ Đậu tây (333 kcal)
```

### Thiết kế Database cho Collation tiếng Việt

Một vấn đề kỹ thuật quan trọng được phát hiện và xử lý trong quá trình xây dựng:

MySQL 8.0 mặc định dùng `utf8mb4_0900_ai_ci` (accent-insensitive) — khiến `'Dầu dừa' = 'Đậu đũa'` trả về `TRUE` và gây `ERROR 1062 Duplicate entry` khi seed.

**Giải pháp:** Toàn bộ 18 bảng dùng `utf8mb4_0900_as_ci`:
- `as` (accent-sensitive): `Dầu dừa ≠ Đậu đũa` ✅
- `ci` (case-insensitive): `tỏi = Tỏi` ✅ (tự nhiên với tên nguyên liệu)

---

## ⚙️ Thiết lập môi trường Local

### Yêu cầu
- [Docker Desktop](https://www.docker.com/products/docker-desktop) 4.x+
- Java 21 JDK
- Node.js 20+ / npm 10+
- Python 3.10+ (chỉ cần nếu muốn chạy lại data pipeline)

### Bước 1 — Khởi động Database & Cache

```bash
# Tại thư mục gốc của project
docker-compose up -d mysql-db redis-cache
```

> **Lần đầu:** MySQL tự chạy `sql/init_database.sql` — tạo 18 bảng, 9 kệ hàng, 6 tags, 6 unit conversions.

### Bước 2 — Cấu hình Backend

```bash
cd smartrecipe-backend
cp .env.example .env    # Điền GEMINI_API_KEY, Cloudinary credentials
```

### Bước 3 — Chạy Backend

```bash
# Trong smartrecipe-backend/
mvn spring-boot:run
```

API tại `http://localhost:8080`.

### Bước 4 — Nạp 290 Nguyên liệu

```powershell
# PowerShell (Windows) — dùng docker cp để tránh lỗi encoding
docker cp sql/seed_ingredients.sql smartrecipe-mysql:/tmp/seed.sql
docker exec smartrecipe-mysql sh -c 'mysql -uroot -proot --default-character-set=utf8mb4 smart_recipe_db < /tmp/seed.sql'
docker exec smartrecipe-mysql rm -f /tmp/seed.sql
```

### Bước 5 — Chạy Frontend

```bash
cd smartrecipe-frontend
npm install
cp .env.example .env    # VITE_API_BASE_URL=http://localhost:8080/api/v1
npm run dev
```

Ứng dụng tại `http://localhost:5173`.

### Bước 6 — Chạy Test

```bash
# Backend: 38 test (JUnit 5 + Mockito), không cần MySQL/Redis đang chạy
cd smartrecipe-backend
./mvnw test

# Frontend: 17 test (Vitest + Testing Library, môi trường jsdom)
cd smartrecipe-frontend
npm test          # chạy một lượt
npm run test:watch
```

---

## 🔬 Nạp Dữ liệu Nguyên liệu

Nếu cần chạy lại toàn bộ data pipeline (ví dụ: cập nhật nguồn USDA):

```bash
# Yêu cầu: pip install pandas numpy

# Giai đoạn 1: Lọc từ USDA raw
python tools/clean_ingredients.py

# Giai đoạn 2: Lọc theo bếp Việt + gộp biến thể
python tools/suggest_keep.py --apply
python tools/collapse_groups.py --apply

# Giai đoạn 3: Gán kệ hàng
python tools/assign_aisles.py --apply

# Giai đoạn 4: Sinh SQL
python tools/gen_seed_sql.py --apply
# → Tạo ra sql/seed_ingredients.sql

# Kiểm tra dataset trước khi seed
python tools/verify_dataset.py
```

---

## 📝 Biến môi trường

### Backend (`.env` trong `smartrecipe-backend/`)

```env
GEMINI_API_KEY=your_gemini_api_key_here

JWT_SECRET=your_256_bit_secret_key_here
JWT_EXPIRATION=86400000          # 24 giờ (ms)
JWT_REFRESH_EXPIRATION=604800000 # 7 ngày (ms)

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Frontend (`.env` trong `smartrecipe-frontend/`)

```env
VITE_API_BASE_URL=http://localhost:8080/api/v1
```

---

## 📚 Tài liệu chi tiết

| Tài liệu | Nội dung |
|---|---|
| [Backend README](./smartrecipe-backend/README.md) | Kiến trúc, API endpoints, luồng Auth, luồng AI, Redis cache |
| [Frontend README](./smartrecipe-frontend/README.md) | Kiến trúc, routing, state management, luồng đi chợ, design system |
| [docs/project_master_plan.md](./docs/project_master_plan.md) | Kế hoạch tổng thể 6 Sprints |
| [docs/implementation_plan.md](./docs/implementation_plan.md) | Kế hoạch triển khai chi tiết |
| [docs/sprint4_plan.md](./docs/sprint4_plan.md) | Thiết kế Pantry & Grocery |
| [sql/init_database.sql](./sql/init_database.sql) | DDL 18 bảng + seed data từ điển |
| [sql/seed_ingredients.sql](./sql/seed_ingredients.sql) | 290 nguyên liệu từ USDA |

---

## 🗃 Database Schema — Tóm tắt

| Nhóm | Bảng | Mô tả |
|---|---|---|
| **Auth** | `users`, `follows` | Tài khoản, mối quan hệ theo dõi |
| **Recipe** | `recipes`, `recipe_steps`, `recipe_ingredients`, `recipe_likes`, `recipe_comments`, `recipe_tags`, `tags` | Công thức và tương tác |
| **Ingredient** | `ingredients`, `aisles`, `unit_conversions` | Nguyên liệu, 9 kệ hàng, bảng quy đổi đơn vị |
| **Pantry** | `user_pantry` | Tủ nguyên liệu cá nhân |
| **Grocery** | `grocery_lists`, `grocery_items`, `grocery_list_recipes` | Danh sách đi chợ |
| **AI & Journal** | `ai_suggestion_logs`, `cooking_journals` | Lịch sử AI và nhật ký nấu ăn |

**Tổng:** 18 bảng · 290 nguyên liệu · collation `utf8mb4_0900_as_ci`

---

## 🤝 Tác giả

Dự án được phát triển trong khuôn khổ **Thực tập Tốt nghiệp (TTTN)**.

> Dữ liệu dinh dưỡng trích xuất từ **USDA FoodData Central SR Legacy 2018** — nguồn dữ liệu khoa học công khai của Bộ Nông nghiệp Hoa Kỳ ([fdc.nal.usda.gov](https://fdc.nal.usda.gov)).

---

*SmartRecipe & Grocery Platform — Full-stack Web Application · Spring Boot 4 · React 19 · Gemini AI*

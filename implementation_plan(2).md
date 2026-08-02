# 📋 Kế hoạch Phát triển Dự án Smart Recipe & Grocery Platform

---

## Tiến độ Hiện tại

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| Kiến trúc & Tài liệu | ✅ Hoàn thành | `implementation_plan.md`, `init_database.sql`, mô tả dự án |
| Git Repos (3 repos) | ✅ Hoàn thành | Root, Backend, Frontend — đã push lên GitHub |
| Backend Boilerplate | ✅ Hoàn thành | Spring Boot 4.1.0, Java 21, pom.xml đã sửa lỗi |
| Frontend Boilerplate | ✅ Hoàn thành | Vite + React, Tailwind, Axios, Zustand, TanStack Query, React Hook Form + Zod |
| Docker & Database | ✅ Hoàn thành | `docker-compose.yml` (MySQL 8 + Redis 7), DB đã khởi tạo thành công 17 bảng |
| Backend `application.yaml` | ✅ Hoàn thành | Kết nối MySQL `localhost:3306`, Redis `localhost:6379` |
| **Entity classes (Backend)** | ✅ Hoàn thành | Đã ánh xạ 17 entities |
| **Security & JWT (Backend)** | ✅ Hoàn thành | Đã thiết lập hoàn chỉnh |
| **API Endpoints (Backend)** | ✅ Đang thực hiện | Hoàn thành Auth, Profile & Master Data (Sprint 1, 2) |
| **Giao diện (Frontend)** | ✅ Đang thực hiện | Hoàn thành Auth, Profile & Master Data (Sprint 1, 2) |

---

## Lộ trình Phát triển (6 Sprints)

> Chiến lược: **Backend trước, Frontend sau**. Mỗi Sprint xây dựng xong Backend API → viết Frontend tương ứng.

---

### 🟢 Sprint 1 — Nền tảng & Xác thực (Foundation & Auth)
**Mục tiêu:** Xây dựng toàn bộ Entity, cấu trúc package, Security JWT, và module Đăng ký/Đăng nhập.

#### Backend (ưu tiên cao nhất)
- [x] **Tạo cấu trúc package:** `entity`, `repository`, `service`, `controller`, `dto`, `exception`, `config`, `security`
- [x] **Tạo 17 Entity classes** ánh xạ từ `init_database.sql`:
  - `User`, `Aisle`, `Ingredient`, `Recipe`, `RecipeStep`, `RecipeIngredient`, `Tag`, `RecipeTag`
  - `UserPantry`, `GroceryList`, `GroceryItem`, `GroceryListRecipe`, `UnitConversion`
  - `CookingJournal`, `AiSuggestionLog`, `RecipeLike`, `RecipeComment`
- [x] **Tạo Enum classes:** `Role` (ADMIN, USER), `RecipeStatus` (PRIVATE, PUBLIC), `Difficulty` (EASY, MEDIUM, HARD), `GroceryListStatus` (ACTIVE, COMPLETED), `AiSuggestionType` (ZERO_WASTE, FEASIBLE_FINDER)
- [x] **Tạo cấu trúc Response chuẩn:** `ApiResponse<T>` wrapper (success, message, data, timestamp)
- [x] **Tạo Exception handling:** `GlobalExceptionHandler`, `ResourceNotFoundException`, `UnauthorizedException`, `DuplicateResourceException`
- [x] **Cấu hình Security:**
  - `SecurityConfig.java` (SecurityFilterChain, CORS, CSRF off, stateless session)
  - `JwtProvider.java` (tạo/xác minh Access Token & Refresh Token)
  - `JwtAuthFilter.java` (OncePerRequestFilter)
  - `UserDetailsServiceImpl.java` (load user từ DB)
- [x] **API Auth (Module đầu tiên):**
  - `AuthController`: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`
  - `AuthService`: logic đăng ký (BCrypt), đăng nhập (kiểm tra & trả JWT), refresh token (Redis), logout (blacklist)
  - DTOs: `RegisterRequest`, `LoginRequest`, `RefreshTokenRequest`, `AuthResponse`
  - Repositories: `UserRepository`

#### Frontend (sau khi Backend Auth xong)
- [x] Tạo trang `LoginPage.jsx` và `RegisterPage.jsx`
- [x] Tích hợp gọi API Auth qua `authService.js`
- [x] Cấu hình Protected Route (chuyển hướng về Login nếu chưa đăng nhập)
- [x] Tạo `Header.jsx` (hiển thị avatar/username, nút Đăng xuất)

---

### 🔵 Sprint 2 — Quản lý Người dùng & Nguyên liệu (Users & Master Data)
**Mục tiêu:** API quản lý profile + CRUD dữ liệu từ điển (nguyên liệu, quầy hàng, thẻ tag).

#### Backend
- [x] **API Users:** `GET /users/me`, `PUT /users/me`, `POST /users/me/avatar`, `GET /users/{id}`
- [x] **API Ingredients:** `GET /ingredients`, `GET /ingredients/search`, `POST /ingredients` (ADMIN)
- [x] **API Aisles, Tags, UnitConversions:** CRUD cơ bản
- [x] **Redis Cache:** Cache danh sách `ingredients`, `aisles`, `tags`, `unit_conversions`
- [x] **Cloudinary Integration:** Upload ảnh avatar

#### Frontend
- [x] Trang `ProfilePage.jsx` (xem/sửa thông tin cá nhân, upload avatar)
- [x] Component Autocomplete tìm kiếm nguyên liệu

---

### 🟡 Sprint 3 — Công thức Nấu ăn (Recipes)
**Mục tiêu:** CRUD công thức, bao gồm bước nấu, nguyên liệu, tag, chia sẻ cộng đồng.

#### Backend
- [ ] **API Recipes:** CRUD đầy đủ (`POST`, `GET`, `PUT`, `DELETE`)
- [ ] `GET /recipes/my` — công thức cá nhân (phân trang)
- [ ] `GET /recipes/public` — feed cộng đồng (phân trang, cache Redis 10 phút)
- [ ] `GET /recipes/search` — tìm kiếm theo từ khoá, tags, difficulty
- [ ] `POST /recipes/{id}/clone` — clone công thức từ cộng đồng
- [ ] Upload ảnh công thức (Cloudinary)

#### Frontend
- [ ] Trang `MyRecipesPage.jsx` (danh sách công thức cá nhân + nút tạo mới)
- [ ] Form tạo/sửa công thức (Multi-step: thông tin chung → nguyên liệu → bước nấu → tag)
- [ ] Trang `RecipeDetailPage.jsx` (xem chi tiết, tính dinh dưỡng)
- [ ] Trang `CommunityFeedPage.jsx` (feed công thức cộng đồng, infinite scroll)

---

### 🟠 Sprint 4 — Tủ lạnh & Đi chợ (Pantry & Grocery)
**Mục tiêu:** Quản lý kho nguyên liệu cá nhân + tạo danh sách đi chợ thông minh.

#### Backend
- [ ] **API Pantry:** `GET`, `POST`, `PUT`, `DELETE` + `GET /pantry/low-stock`
- [ ] **API Grocery:** Tạo phiên đi chợ, tự động tính toán `final_to_buy = total_needed - pantry_deducted`
- [ ] Logic gộp nguyên liệu từ nhiều công thức + quy đổi đơn vị

#### Frontend
- [ ] Trang `PantryPage.jsx` (quản lý kho, cảnh báo sắp hết)
- [ ] Trang `GroceryPage.jsx` (tạo phiên đi chợ, checklist mua sắm)

---

### 🔴 Sprint 5 — Nhật ký & AI (Cooking Journal & AI)
**Mục tiêu:** Ghi nhật ký nấu ăn (tự động trừ kho) + tích hợp Gemini AI gợi ý món.

#### Backend
- [ ] **API Cooking Journals:** CRUD + trigger trừ nguyên liệu từ tủ lạnh
- [ ] **API AI Suggestions:** `POST /ai/suggest` (gọi Gemini API, cache Redis 24h)
- [ ] Rate limiting: 10 lần gợi ý/giờ/user (Redis counter)

#### Frontend
- [ ] Trang `CookingJournalPage.jsx` (lịch sử nấu ăn, đánh giá, ghi chú)
- [ ] Trang `AiSuggestionPage.jsx` (chọn nguyên liệu → nhận gợi ý từ AI → lưu thành công thức)

---

### 🟣 Sprint 6 — Cộng đồng & Hoàn thiện (Community & Polish)
**Mục tiêu:** Tương tác xã hội (like, comment) + trang chủ + triển khai.

#### Backend
- [ ] **API Like:** `POST /recipes/{id}/like` (toggle like/unlike)
- [ ] **API Comments:** CRUD bình luận trên công thức
- [ ] Tối ưu hiệu suất tổng thể (N+1 query, cache strategy)

#### Frontend
- [ ] Component Like/Comment trên `RecipeDetailPage`
- [ ] Trang `HomePage.jsx` (tổng quan: công thức mới, phổ biến, cảnh báo tủ lạnh)
- [ ] Responsive design (mobile-friendly)
- [ ] Deploy: Vercel (Frontend), Render.com (Backend), TiDB (DB), Upstash (Redis)

---

## Đề xuất Bắt đầu

> [!IMPORTANT]
> **Bạn nên bắt đầu từ Sprint 1** — đây là nền tảng (Entity + Security + Auth) mà mọi Sprint sau đều phụ thuộc vào.
> 
> Trong Sprint 1, thứ tự thực hiện ở Backend sẽ là:
> 1. Tạo cấu trúc package (thư mục)
> 2. Tạo 17 Entity classes + Enum
> 3. Tạo cấu trúc Response chuẩn (`ApiResponse`) + Exception handling
> 4. Cấu hình Spring Security + JWT
> 5. Viết API Auth (Register, Login, Refresh, Logout)
> 6. Test API bằng Postman hoặc curl
>
> Bấm **Proceed** để tôi bắt tay vào Sprint 1 ngay.

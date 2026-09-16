# 🚀 KẾ HOẠCH TỔNG THỂ & TIẾN ĐỘ DỰ ÁN (PROJECT MASTER PLAN)
**Tên đề tài:** Nền tảng Quản lý và Chia sẻ Công thức Nấu ăn Thông minh tích hợp AI (Smart Recipe & Grocery Platform)

---

## 🌟 PHẦN 1: MÔ TẢ TỔNG QUAN DỰ ÁN

Hệ thống Web Application hiện đại đóng vai trò như một trợ lý bếp núc cá nhân toàn diện. Hệ thống giúp người dùng quản lý công thức nấu ăn, tính toán dinh dưỡng, quản lý kho tủ lạnh tự động, hỗ trợ lên danh sách đi chợ và kết nối cộng đồng yêu ẩm thực.

### 🎯 Đối tượng phục vụ (Target Users)
- **Người nội trợ, sinh viên, dân văn phòng:** Nhu cầu tự nấu ăn tại nhà, muốn tiết kiệm thời gian lên thực đơn và mua sắm.
- **Người quan tâm sức khỏe / dinh dưỡng:** Muốn kiểm soát lượng Calo và Macro (Đạm, Béo, Tinh bột) hàng ngày.
- **Cộng đồng yêu ẩm thực:** Chia sẻ công thức, tìm kiếm cảm hứng và giao lưu thực đơn.

### 🧩 6 Module Cốt lõi
1. **Phân quyền & Quản lý Tài khoản (Auth & Profiles):** Đăng nhập JWT, quản lý hồ sơ, phân quyền ADMIN/USER.
2. **Quản lý Công thức & Dinh dưỡng (Recipe Engine):** Quản lý CRUD công thức, phân loại Tag, tự động tính toán Calo/Macro, chế độ nấu ăn từng bước (Step-by-step).
3. **Quản lý Kho Tủ lạnh Động (Dynamic Virtual Pantry):** Quản lý nguyên liệu có sẵn, quy đổi đơn vị tự động, tự động nhập/xuất kho khi đi chợ hoặc nấu ăn xong.
4. **Đi chợ Thông minh (Smart Grocery List):** Tự động bóc tách nguyên liệu từ thực đơn tuần, thuật toán gộp nhóm nguyên liệu trùng lặp, đối chiếu trừ đi đồ có sẵn trong tủ lạnh.
5. **Nhật ký & Trợ lý AI (Journal & AI):** Ghi chép lịch sử nấu nướng. Tích hợp Gemini AI với 2 tính năng: 
   - *Zero-Waste (Giải cứu tủ lạnh)*: Sinh ra công thức từ thực phẩm thừa.
   - *Feasible Recipe Finder*: Gợi ý món ăn từ danh sách nguyên liệu nhập vào.
6. **Cộng đồng (Social Hub):** Bảng tin (Newsfeed) chia sẻ công thức, thả tim, bình luận và chức năng Clone (nhân bản) công thức công khai về sổ tay cá nhân.

---

## 📊 PHẦN 2: TIẾN ĐỘ DỰ ÁN (PROJECT PROGRESS)

Bảng dưới đây theo dõi sát sao tiến trình hiện tại của toàn bộ dự án.

| Hạng mục Lớn | Trạng thái | Chi tiết hoàn thành |
|---|---|---|
| **Môi trường & Database** | ✅ Hoàn thành | Đã thiết lập Docker MySQL 8, Redis 7. Khởi tạo xong 17 bảng CSDL. |
| **Boilerplate Backend** | ✅ Hoàn thành | Spring Boot 3, cấu hình `.env`, Hibernate, kết nối DB & Cache. |
| **Boilerplate Frontend** | ✅ Hoàn thành | Vite + React, Tailwind, Zustand, TanStack Query v5, Axios. |
| **Sprint 1 (Auth)** | ✅ Hoàn thành | Xong toàn bộ Security JWT, API Đăng nhập/Đăng ký, Giao diện Login/Register. |
| **Sprint 2 (Users)** | ✅ Hoàn thành | Xong API Profile, Cloudinary, Master Data (Ingredients, Aisles, Tags, UnitConversions) + Redis Cache + Frontend Autocomplete. |
| **Sprint 3 (Recipes)** | ✅ Hoàn thành MVP | Backend CRUD/search/export/clone/like và giao diện Recipe đã có; contract FE/BE đã đối chiếu, 5 test service Recipe chạy xanh. |
| **Sprint 4 (Pantry & Grocery)**| ✅ Hoàn thành MVP | Pantry đã hoàn thiện theo lot + base unit. Grocery đã hoàn thiện các tính năng danh sách đi chợ, gộp nhóm và tự động cập nhật kho. Đang trong giai đoạn hoàn thiện test. |
| **Sprint 5 (Journal & AI)** | ✅ Hoàn thành | Đã xong Cooking Journals (tự động trừ kho FEFO), Gemini AI integration (Rate limit Redis, fallback parsing, mapping nguyên liệu), giao diện Nhật ký và Gợi ý AI. |
| **Sprint 6 (Community & Polish)** | 🟡 Hoạt động ~85% | Đã xong Hybrid Guest/Member, Bento Spotlight 5s, Trang Đặc quyền /features, Hệ thống Thông báo In-App, Comment UX Warm Palette. Còn Task 5.2 Admin Users. |
| **Triển khai Đám mây (Cloud)** | ✅ Hoàn thành | Đã hoàn tất triển khai kiến trúc Cloud: Frontend (Vercel), Backend Service (Render/Docker), Cơ sở dữ liệu TiDB Serverless, Upstash Redis. |

---

## 🗺 PHẦN 3: KẾ HOẠCH TRIỂN KHAI CHI TIẾT (6 SPRINTS)

Chiến lược: **Backend trước, Frontend sau**. Mỗi Sprint xây dựng xong Backend API sẽ tiến hành viết Frontend tương ứng.

### 🟢 Sprint 1: Nền tảng & Xác thực (Foundation & Auth) - `[✅ ĐÃ HOÀN THÀNH]`
**Mục tiêu:** Xây dựng toàn bộ Entity, cấu trúc package, Security JWT, và module Auth.
- [x] Tạo 17 Entity classes ánh xạ từ `init_database.sql`.
- [x] Tạo cấu trúc Response chuẩn (`ApiResponse<T>`) và Exception handling.
- [x] Cấu hình Security (SecurityFilterChain, JwtProvider, JwtAuthFilter).
- [x] API Auth (`/register`, `/login`, `/refresh`, `/logout`).
- [x] Giao diện `LoginPage.jsx`, `RegisterPage.jsx` và cấu hình Protected Route.

### 🔵 Sprint 2: Quản lý Người dùng & Nguyên liệu (Users & Master Data) - `[✅ ĐÃ HOÀN THÀNH]`
**Mục tiêu:** API quản lý profile, Cloudinary, và CRUD dữ liệu từ điển (nguyên liệu, thẻ tag).
- [x] API Users (`GET /users/me`, `PUT /users/me`, `POST /users/me/avatar`).
- [x] Tích hợp Cloudinary Upload Ảnh và Giao diện `ProfilePage.jsx`.
- [x] Cấu hình Redis Cache cho Master Data (`CacheConfig.java`).
- [x] Khởi tạo Repositories & API cho `Ingredients`, `Aisles`, `Tags`, `UnitConversions`.
- [x] Frontend component `IngredientAutocomplete` để tìm kiếm nguyên liệu.

### 🟡 Sprint 3: Công thức Nấu ăn (Recipes) - `[✅ ĐÃ HOÀN THÀNH]`
**Mục tiêu:** Quản lý CRUD công thức, bước nấu, nguyên liệu con, chia sẻ công thức.
- [x] Backend: API CRUD Recipes, Feed cộng đồng (Cache Redis), Tìm kiếm phân trang.
- [x] Backend: Logic Clone công thức.
- [x] Frontend: `MyRecipesPage.jsx`, Form đa bước (Multi-step) tạo công thức.
- [x] Frontend: `RecipeDetailPage.jsx` (Hiển thị chi tiết + tính toán Macro/Calo).
- [x] Đối chiếu contract API/UI và test service các luồng ownership, soft delete, clone, like/unlike (5/5 xanh).

### 🟠 Sprint 4: Tủ lạnh & Đi chợ (Pantry & Grocery) - `[✅ ĐÃ HOÀN THÀNH]`
**Mục tiêu:** Quản lý kho nguyên liệu cá nhân + tạo danh sách đi chợ thông minh.
- [x] Backend: API quản lý Tủ lạnh (`Pantry`), cảnh báo sắp hết nguyên liệu.
- [x] Backend: Thuật toán tạo Phiên đi chợ (Gộp nguyên liệu, quy đổi đơn vị, trừ hao đồ có sẵn).
- [x] Frontend: `PantryPage.jsx` (Quản lý kho theo Lot + Expiry Date).
- [x] Frontend: `GroceryPage.jsx` (Tạo danh sách, tick chọn món đồ đã mua, nhóm theo Kệ hàng Aisle).
- [x] Tích hợp: Thêm vào danh sách đi chợ từ Recipe và tự động cập nhật Tủ lạnh.
- [x] Nghiệm thu tự động Pantry: ownership, đơn vị/định lượng, expiry merge/update và low-stock (10/10 test xanh).

### 🔴 Sprint 5: Nhật ký & Trợ lý AI (Cooking Journal & AI) - `[✅ ĐÃ HOÀN THÀNH]`
**Mục tiêu:** Ghi nhận lịch sử nấu ăn và tích hợp Gemini AI.
- [x] Backend: API Cooking Journals (khi lưu nhật ký -> trigger tự động trừ nguyên liệu khỏi tủ lạnh theo thuật toán FEFO).
- [x] Backend: Tích hợp Gemini REST API (`/ai/suggest`, `/ai/suggest-pantry`), xử lý Prompt, trích xuất JSON an toàn và đối chiếu nguyên liệu vào database.
- [x] Backend: Áp dụng Rate Limiting cho AI API qua Redis (10 lần/ngày/user).
- [x] Frontend: `CookingJournalPage.jsx` và Modal ghi nhận nhật ký nấu ăn.
- [x] Frontend: `AiSuggestionPage.jsx` (Gợi ý món ăn từ tủ lạnh hoặc danh sách nhập tay, lưu thành công thức cá nhân).
- [x] Bộ Unit Test Backend: `AiServiceImplTest` (Rate limit, parse error recovery, name matching).

### 🟣 Sprint 6: Cộng đồng, Khám phá & Hoàn thiện (Community & Polish) - `[🟡 ĐẠT ~85%]`
**Mục tiêu:** Tương tác xã hội, mô hình Hybrid Guest/Member, thông báo và quản trị Admin.
- [x] Backend: Mở quyền truy cập công khai trong `SecurityConfig` cho xem công thức, bình luận và profile tác giả.
- [x] Backend: Hệ thống Thông báo In-App (`Notification` Entity, Controller, Service, mark-as-read, unread count).
- [x] Frontend: Mô hình Hybrid Guest/Member trên `App.jsx`, mở xem tự do `/`, `/recipes/:id`, `/features`.
- [x] Frontend: `TopHeader.jsx` và `Sidebar.jsx` tự động biến đổi theo trạng thái đăng nhập.
- [x] Frontend: Trang "Đặc quyền thành viên" (`/features` - `BenefitsPage.jsx`) với 4 trụ cột hệ sinh thái.
- [x] Frontend: Nâng cấp `HomePage.jsx` Bento Editorial Discovery (Top 3 Spotlight xoay 5s, bộ lọc Tag-First).
- [x] Frontend: Chuông thông báo thời gian thực với Badge số lượng, Dropdown popover (`NotificationDropdown.jsx`) và tự động cập nhật 30s.
- [x] Frontend: Hoàn thiện trải nghiệm Comment (Modal xóa `ConfirmModal.jsx`, giao diện nút Sửa/Hủy phong cách Warm Palette).
- [x] Admin Panel: Dashboard KPI tổng quan, Duyệt công thức (`AdminRecipes.jsx`), Quản lý nguyên liệu (`AdminIngredients.jsx`).
- [ ] **Task 5.2 Admin Tồn đọng:**
  - [ ] Frontend: Xây dựng `AdminUsers.jsx` thay thế `AdminPlaceholder.jsx`.
  - [ ] Backend: API quản lý Người dùng (`GET /api/v1/admin/users`, ban/unban, role update).
  - [ ] Admin Ingredients: Cho phép gán kệ hàng (`aisleId`) khi duyệt nguyên liệu mới.
- [x] Triển khai Deployment Môi trường Cloud (Vercel Frontend, TiDB Serverless Database, Render/Docker Backend).

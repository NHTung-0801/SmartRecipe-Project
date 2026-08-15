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
| **Sprint 5 (Journal & AI)** | ❌ Chưa bắt đầu | |
| **Sprint 6 (Community)** | ❌ Chưa bắt đầu | |

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

### 🟡 Sprint 3: Công thức Nấu ăn (Recipes) - `[✅ HOÀN THÀNH MVP]`
**Mục tiêu:** Quản lý CRUD công thức, bước nấu, nguyên liệu con, chia sẻ công thức.
- [x] Backend: API CRUD Recipes, Feed cộng đồng (Cache Redis), Tìm kiếm phân trang.
- [x] Backend: Logic Clone công thức.
- [x] Frontend: `MyRecipesPage.jsx`, Form đa bước (Multi-step) tạo công thức.
- [x] Frontend: `RecipeDetailPage.jsx` (Hiển thị chi tiết + tính toán Macro/Calo).
- [x] Đối chiếu contract API/UI và test service các luồng ownership, soft delete, clone, like/unlike (5/5 xanh).
- [ ] Kiểm thử UI/API thủ công với dữ liệu thực và xử lý các cảnh báo lint còn lại.

### 🟠 Sprint 4: Tủ lạnh & Đi chợ (Pantry & Grocery) - `[✅ HOÀN THÀNH MVP]`
**Mục tiêu:** Quản lý kho nguyên liệu cá nhân + tạo danh sách đi chợ thông minh.
- [x] Backend: API quản lý Tủ lạnh (`Pantry`), cảnh báo sắp hết nguyên liệu.
- [x] Backend: Thuật toán tạo Phiên đi chợ (Gộp nguyên liệu, quy đổi đơn vị, trừ hao đồ có sẵn).
- [x] Frontend: `PantryPage.jsx` (Quản lý kho).
- [x] Frontend: `GroceryPage.jsx` (Tạo danh sách, tick chọn món đồ đã mua) và các Component liên quan.
- [x] Tích hợp: Thêm vào danh sách đi chợ từ Recipe và tự động cập nhật Tủ lạnh.
- [x] Nghiệm thu tự động Pantry: ownership, đơn vị/định lượng, expiry merge/update và low-stock (9/9 test xanh).
- [ ] Hoàn thiện Unit Test cho Grocery và kiểm thử UI/API thủ công với dữ liệu thực.

### 🔴 Sprint 5: Nhật ký & Trợ lý AI (Cooking Journal & AI) - `[❌ CHƯA BẮT ĐẦU]`
**Mục tiêu:** Ghi nhận lịch sử nấu ăn và tích hợp Gemini AI.
- [ ] Backend: API Cooking Journals (khi lưu nhật ký -> trigger tự động trừ nguyên liệu khỏi tủ lạnh).
- [ ] Backend: Tích hợp Gemini REST API (`/ai/suggest`), xử lý Prompt và map dữ liệu JSON trả về vào chuẩn Entity.
- [ ] Backend: Áp dụng Rate Limiting cho AI API qua Redis (VD: 10 lần/ngày/user).
- [ ] Frontend: `CookingJournalPage.jsx`.
- [ ] Frontend: `AiSuggestionPage.jsx` (Chat/Nhập liệu nhận gợi ý và nút "Lưu thành Công thức").

### 🟣 Sprint 6: Cộng đồng & Hoàn thiện (Community & Polish) - `[❌ CHƯA BẮT ĐẦU]`
**Mục tiêu:** Tương tác xã hội và triển khai (Deployment).
- [ ] Backend: API Like, Comment trên công thức.
- [ ] Frontend: Component Bảng tin `HomePage.jsx` và khu vực Comment.
- [ ] Tối ưu hóa: Xử lý N+1 Query trong JPA, Responsive UI cho Mobile.
- [ ] Deploy: Vercel (Frontend), Render.com/Railway (Backend), TiDB Serverless (MySQL).

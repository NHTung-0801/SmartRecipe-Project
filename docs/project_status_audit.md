# 📋 SMART RECIPE — BÁO CÁO TOÀN DIỆN TIẾN ĐỘ & KIẾN TRÚC HỆ THỐNG
*(Project Progress, Architecture & Code Health Audit)*

> **Ngày cập nhật:** 11/09/2026  
> **Phiên bản hệ thống:** v1.2-sprint6  
> **Trạng thái Git:** Sạch (`working tree clean`), submodule Backend & Frontend đồng bộ commit mới nhất.  
> **Mục đích tài liệu:** Lưu giữ bức tranh toàn cảnh về tiến trình hoàn thiện, ánh xạ mã nguồn và tiêu chí kiểm thử để bất kỳ lập trình viên hoặc AI Agent nào tiếp quản dự án đều có thể nắm bắt và rà soát tức thì.

---

## 🧭 PHẦN 1: BẢNG TỔNG QUAN TIẾN ĐỘ 6 SPRINTS

| Sprint | Chủ đề chính | Trạng thái | Điểm nhấn kỹ thuật đã nghiệm thu |
|:---:|---|:---:|---|
| **Sprint 1** | **Foundation & Security** | ✅ 100% | Spring Security 6 + Stateless JWT, Refresh Token, BCrypt, Base `ApiResponse<T>`, Global Exception Handler, `LoginPage`, `RegisterPage`. |
| **Sprint 2** | **Users & Master Data** | ✅ 100% | Quản lý Profile, Upload Avatar Cloudinary, Master Data (Nguyên liệu, Kệ hàng, Đơn vị, Quy đổi), Redis Caching, Autocomplete tìm nguyên liệu. |
| **Sprint 3** | **Recipe Engine** | ✅ 100% | CRUD đa bước công thức nấu ăn, tính toán Calo/Macro tự động theo khẩu phần, Nhân bản (Clone) công thức công khai, Thả tim, Feed khám phá. |
| **Sprint 4** | **Pantry & Grocery** | ✅ 100% | Tủ lạnh ảo theo Lô (Lot) & Hạn sử dụng, Cảnh báo thực phẩm sắp hết hạn, Danh sách đi chợ thông minh tự gộp nguyên liệu trùng và trừ tồn kho tủ lạnh. |
| **Sprint 5** | **Cooking Journal & AI** | ✅ 100% | Tích hợp Google Gemini AI (`/ai/suggest`, `/ai/suggest-pantry`), Giới hạn Rate Limit qua Redis (10 lần/ngày), Tự động trừ kho theo thuật toán FEFO khi lưu nhật ký nấu. |
| **Sprint 6** | **Community & Experience** | 🟡 ~85% | Mô hình Hybrid Guest/Member, Bento Spotlight 5s, Trang `/features`, Chuông thông báo In-App real-time, Modal xóa đồng bộ. Còn Task 5.2 Admin Users. |
| **Cloud Hosting** | **Triển khai Đám mây & CI/CD** | ✅ 100% | Frontend trên Vercel CDN, Backend Web Service trên Render/Docker, Cơ sở dữ liệu TiDB Serverless, Upstash Redis. |

---

## 🗺️ PHẦN 2: MA TRẬN ROUTING, GIAO DIỆN & API BACKEND

Dưới đây là bản đồ chi tiết kết nối giữa **Giao diện người dùng (Frontend)**, **Tầng dịch vụ (Backend API)** và **Quyền hạn truy cập (Access Control)**:

### 1. Khu vực Công chúng & Trải nghiệm Hybrid (Guest & Member)
| Tuyến đường (URL) | Component Frontend | Backend Endpoints chính | Quyền hạn | Mô tả trải nghiệm |
|---|---|---|:---:|---|
| `/` | [`HomePage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/HomePage.jsx) | `GET /api/v1/recipes/public`<br>`GET /api/v1/tags`<br>`GET /api/v1/recipes/liked-ids` | Public | Bento Spotlight (3 món top 1-2-3 tự xoay 5s), Thẻ chủ đề Tag-first, Lọc Phổ biến / Mới nhất. |
| `/recipes/:id` | [`RecipeDetailPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RecipeDetailPage.jsx) | `GET /api/v1/recipes/{id}`<br>`GET /api/v1/recipes/{id}/comments`<br>`GET /api/v1/recipes/similar` | Public | Xem đầy đủ nguyên liệu, bước nấu, dinh dưỡng, bình luận. Nếu khách thao tác Like/Clone/Đi chợ -> Bật thông báo nhắc đăng nhập. |
| `/features` | [`BenefitsPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/BenefitsPage.jsx) | *(Static presentation)* | Public | Giới thiệu 4 trụ cột công nghệ (Tủ lạnh, AI Chef, Đi chợ 1-Click, Sổ tay) kích thích người dùng đăng ký. |
| `/users/:id` | [`UserProfilePage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/UserProfilePage.jsx) | `GET /api/v1/users/{id}/profile` | Public | Hồ sơ đầu bếp công khai, danh sách công thức công khai đã đăng, huy hiệu bếp trưởng. |
| `/login`, `/register` | [`LoginPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/LoginPage.jsx), [`RegisterPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RegisterPage.jsx) | `POST /api/v1/auth/login`<br>`POST /api/v1/auth/register` | Public (Unauth) | Đăng nhập/Đăng ký tài khoản, lưu trữ JWT và thông tin user vào Zustand store. |

### 2. Khu vực Thành viên đã Đăng nhập (Authenticated Members)
| Tuyến đường (URL) | Component Frontend | Backend Endpoints chính | Nghiệp vụ cốt lõi |
|---|---|---|---|
| `/recipes/new`<br>`/recipes/:id/edit` | [`RecipeFormPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RecipeFormPage.jsx) | `POST /api/v1/recipes`<br>`PUT /api/v1/recipes/{id}`<br>`POST /api/v1/recipes/{id}/image` | Soạn thảo công thức đa bước, thêm nguyên liệu kèm đơn vị, tính calo tự động, upload ảnh bìa. |
| `/recipes` | [`MyRecipesPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/MyRecipesPage.jsx) | `GET /api/v1/recipes/my` | Quản lý sổ tay công thức cá nhân (Công khai, Riêng tư, Bản nháp). |
| `/pantry` | [`PantryPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/PantryPage.jsx) | `GET /api/v1/pantry`<br>`POST /api/v1/pantry/items`<br>`GET /api/v1/pantry/expiring` | Quản lý kho tủ lạnh theo hạn dùng, dọn dẹp đồ hết hạn 1-click qua `ExpiryAlertBanner`. |
| `/grocery` | [`GroceryPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/GroceryPage.jsx) | `GET /api/v1/grocery-lists/active`<br>`POST /api/v1/grocery-lists/generate`<br>`POST /api/v1/grocery-lists/{id}/complete` | Đi chợ theo kệ hàng siêu thị, tick chọn mua, bấm Hoàn tất tự động nhập kho tủ lạnh. |
| `/journal` | [`CookingJournalPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/CookingJournalPage.jsx) | `GET /api/v1/journals`<br>`POST /api/v1/journals` | Nhật ký nấu nướng: Lưu cảm nhận, đánh giá sao, tự động kích hoạt trừ nguyên liệu trong tủ theo FEFO. |
| `/ai-suggestion` | [`AiSuggestionPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/AiSuggestionPage.jsx) | `POST /api/v1/ai/suggest`<br>`POST /api/v1/ai/suggest-pantry` | Gemini AI Chef: Gợi ý công thức từ thực phẩm tồn tủ hoặc nhập tay, chuyển thành công thức cá nhân. |
| *(Header Popover)* | [`NotificationDropdown.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/layout/NotificationDropdown.jsx) | `GET /api/v1/notifications`<br>`GET /api/v1/notifications/unread-count`<br>`PATCH /api/v1/notifications/read-all` | Chuông thông báo góc trên màn hình: Polling 30s tự động báo khi có người bình luận hoặc trả lời. |

### 3. Phân hệ Quản trị viên (Admin Panel)
| Tuyến đường (URL) | Component Frontend | Backend Endpoints chính | Tình trạng |
|---|---|---|:---:|
| `/admin/dashboard` | [`AdminDashboard.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminDashboard.jsx) | `GET /api/v1/admin/stats` | ✅ Hoạt động (KPI Row 1) |
| `/admin/recipes` | [`AdminRecipes.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminRecipes.jsx) | `GET /api/v1/admin/recipes`<br>`PATCH /api/v1/admin/recipes/{id}/status` | ✅ Hoạt động (Duyệt/Ẩn/Xóa) |
| `/admin/ingredients` | [`AdminIngredients.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminIngredients.jsx) | `GET /api/v1/admin/ingredients`<br>`PATCH /api/v1/admin/ingredients/{id}` | 🟡 Hoạt động (Cần thêm chọn Aisle) |
| `/admin/users` | [`AdminPlaceholder.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminPlaceholder.jsx) | *Chưa có* | ❌ Cần xây dựng `AdminUsers.jsx` |

---

## ⚙️ PHẦN 3: CÁC LUỒNG XỬ LÝ NGHIỆP VỤ ĐẶC TRƯNG

### 1. Điều hướng Hybrid & Bảo vệ trải nghiệm Khách
- **Cơ chế:** Khách truy cập không bị đá về `/login`.
- **Thành phần thích ứng:**
  - `TopHeader.jsx`: Khách -> Hiện 2 nút `[Đăng nhập]` & `[Đăng ký miễn phí]`. Thành viên -> Hiện Bell (thông báo), Heart (yêu thích), Avatar.
  - `Sidebar.jsx`: Khách -> Chỉ hiển thị 2 menu `Khám phá` và `Đặc quyền thành viên`. Thành viên -> Hiển thị đầy đủ 7 menu làm bếp và nút `+ Lên thực đơn`.
  - `RecipeDetailPage.jsx`: Bọc hàm `handleLike`, `handleClone`, `handleAddToGroceryList` bằng kiểm tra `currentUser`. Nếu chưa đăng nhập, hiển thị toast nhắc nhở nhẹ nhàng thay vì báo lỗi.

### 2. Chuông Thông báo In-App (Notifications)
- **Cơ chế sinh thông báo:** Khi người dùng B bình luận vào công thức của người dùng A, hoặc trả lời bình luận của người dùng C, Backend tự động sinh bản ghi trong bảng `notifications`.
- **Cơ chế hiển thị:**
  - Frontend dùng `useNotificationStore` thực hiện polling mỗi 30 giây khi người dùng đăng nhập (`isAuthenticated = true`).
  - Icon chuông hiển thị badge số đỏ khi `unreadCount > 0`.
  - Dropdown hiển thị danh sách thông báo phong cách Warm Palette, click vào tự đánh dấu đã đọc và điều hướng thẳng tới công thức.

### 3. Tự động Khấu trừ Tủ lạnh theo FEFO (First Expired, First Out)
- **Cơ chế:** Khi người dùng ghi nhận món ăn đã nấu xong trong `CookingJournal`, Backend kích hoạt `PantryService.deductIngredientsForRecipe`.
- **Thuật toán:**
  1. Duyệt từng nguyên liệu trong công thức.
  2. Tìm các lô nguyên liệu tương ứng trong tủ lạnh của người dùng, sắp xếp theo `expiryDate ASC` (lô hết hạn trước được ưu tiên trừ trước).
  3. Quy đổi đơn vị (vd: kg -> g, quả -> quả) thông qua `UnitNormalizationService`.
  4. Trừ dần số lượng cho đến khi đủ định lượng món ăn. Nếu lô hết sạch, xóa khỏi tủ.

### 4. Đi chợ Thông minh (Smart Grocery Aggregation)
- **Cơ chế:** Khi tạo danh sách đi chợ từ 1 hoặc nhiều công thức:
  1. Hệ thống tự động gộp các nguyên liệu trùng lặp lại thành 1 dòng duy nhất.
  2. Đối chiếu với kho tủ lạnh: Lượng cần mua = (Tổng lượng công thức cần) - (Lượng đang có sẵn trong tủ).
  3. Phân nhóm nguyên liệu theo Kệ hàng (`Aisles` - Gia vị, Rau củ, Thịt cá) để người dùng đi chợ theo tuyến đường tối ưu.

---

## 🧪 PHẦN 4: CHỈ SỐ SỨC KHỎE MÃ NGUỒN & KIỂM THỬ

```
[MÃ NGUỒN BACKEND]
  ├── Unit Tests: 38/38 tests XANH (100% BUILD SUCCESS)
  │   ├── AiServiceImplTest: Rate Limit (3 tests), Get History (2 tests), Save AI Recipe (6 tests), Suggest (3 tests)
  │   ├── PantryServiceImplTest: Khấu trừ FEFO, gộp hạn dùng, cảnh báo hết hạn (10 tests)
  │   ├── GroceryServiceImplTest: Tạo giỏ, gom nhóm kệ hàng (4 tests)
  │   ├── RecipeServiceImplTest: CRUD, quyền tác giả, clone, like (5 tests)
  │   └── UnitNormalizationServiceTest: Quy đổi đơn vị (4 tests)
  └── Framework: Spring Boot 3.3.x + Spring Data JPA + H2 / MySQL

[MÃ NGUỒN FRONTEND]
  ├── Unit Tests: 17/17 tests XANH (Vitest 4/4 suites passed)
  │   ├── ExpiryAlertBanner.test.jsx: 5 tests
  │   ├── ConfirmModal.test.jsx: 4 tests
  │   ├── AddPantryItemModal.test.jsx: 4 tests
  │   └── ingredientService.test.js: 4 tests
  ├── Build: Vite Build thành công (3.16s, gzip nén tối ưu)
  └── Linter: Oxlint 0 ERRORS (0 lỗi chặn), 114 cảnh báo biến/import phụ.
```

---

## 📌 PHẦN 5: DANH MỤC CÔNG VIỆC TỒN ĐỌNG (BACKLOG FOR NEXT SESSIONS)

Khi tiếp tục phiên làm việc mới, các kỹ sư/AI agent hãy ưu tiên giải quyết các mục sau:

1. **Hoàn thiện Sprint 6 Task 5.2 (Admin Users & Aisle Assignment):**
   - **Frontend:** Xây dựng `src/pages/admin/AdminUsers.jsx` (bảng danh sách người dùng, tìm kiếm theo email/tên, nút Khóa/Mở khóa tài khoản, đổi quyền USER/ADMIN). Cập nhật `App.jsx` thay thế `AdminPlaceholder`.
   - **Backend:** Bổ sung trong `AdminController.java`:
     - `GET /api/v1/admin/users`: Lấy danh sách người dùng có phân trang và tìm kiếm.
     - `PATCH /api/v1/admin/users/{id}/status`: Khóa hoặc kích hoạt lại tài khoản.
     - `PATCH /api/v1/admin/users/{id}/role`: Nâng quyền Admin hoặc hạ xuống User.
   - **Admin Ingredients:** Bổ sung dropdown chọn `aisleId` vào `ReviewModal` của `AdminIngredients.jsx` và cập nhật `PATCH /api/v1/admin/ingredients/{id}` ở Backend để lưu `aisleId`.

2. **Triển khai Tính năng Quên mật khẩu qua Email OTP:**
   - Đọc đặc tả kỹ thuật chi tiết tại [`docs/forgot_password_email_otp_plan.md`](file:///d:/TTTN/SmartRecipe-Project/docs/forgot_password_email_otp_plan.md).
   - Cấu hình Gmail SMTP (`spring-boot-starter-mail`), tạo bảng `password_reset_otp`, API gửi mã và API đặt lại mật khẩu kèm modal frontend tại `/login`.

3. **Dọn dẹp Linter:**
   - Xóa bỏ các biến và import dư thừa đã được liệt kê trong báo cáo `oxlint` tại `GroceryPage.jsx` và `RecipeFormPage.jsx`.

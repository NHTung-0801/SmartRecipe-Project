# 🍳 SMART RECIPE & GROCERY PLATFORM — KẾ HOẠCH TỔNG THỂ & BÁO CÁO TOÀN DIỆN DỰ ÁN
*(Comprehensive Project Master Plan, Architecture, Sprint Progress & System Specification)*

> **Đề tài:** Nền tảng Quản lý và Chia sẻ Công thức Nấu ăn Thông minh tích hợp Trợ lý AI (Smart Recipe & Grocery Platform)  
> **Cập nhật:** Tháng 09/2026  
> **Phiên bản hệ thống:** v1.3-production-ready  
> **Trạng thái kiểm thử:** 100% BUILD SUCCESS (Backend: 39/39 Unit Tests xanh; Frontend: 17/17 Vitest xanh; Production Build: 1.98s)  
> **Kiến trúc triển khai:** Umbrella Monorepo (Git Submodules) — Cloud Hybrid (Vercel + Render + TiDB Serverless + Upstash Redis)

---

## 📑 MỤC LỤC

1. [TỔNG QUAN DỰ ÁN & VẤN ĐỀ THỰC TIỄN](#1-tổng-quan-dự-án--vấn-đề-thực-tiễn)
2. [KIẾN TRÚC HỆ THỐNG & CÔNG NGHỆ (TECH STACK)](#2-kiến-trúc-hệ-thống--công-nghệ-tech-stack)
3. [MÔ HÌNH CƠ SỞ DỮ LIỆU & PIPELINE DỮ LIỆU NGUYÊN LIỆU (USDA)](#3-mô-hình-cơ-sở-dữ-liệu--pipeline-dữ-liệu-nguyên-liệu-usda)
4. [BÁO CÁO CHI TIẾT TIẾN ĐỘ 6 SPRINTS](#4-báo-cáo-chi-tiết-tiến-độ-6-sprints)
   - [Sprint 1: Nền tảng, Xác thực & Phân quyền (Auth & Security)](#-sprint-1-nền-tảng-xác-thực--phân-quyền-auth--security)
   - [Sprint 2: Quản lý Người dùng & Dữ liệu Từ điển (Users & Master Data)](#-sprint-2-quản-lý-người-dùng--dữ-liệu-từ-điển-users--master-data)
   - [Sprint 3: Động cơ Công thức & Dinh dưỡng Động (Recipe Engine)](#-sprint-3-động-cơ-công-thức--dinh-dưỡng-động-recipe-engine)
   - [Sprint 4: Tủ lạnh Ảo & Đi chợ Thông minh (Pantry & Smart Grocery)](#-sprint-4-tủ-lạnh-ảo--đi-chợ-thông-minh-pantry--smart-grocery)
   - [Sprint 5: Nhật ký Nấu nướng & Trợ lý Đầu bếp AI (Journal & Gemini AI)](#-sprint-5-nhật-ký-nấu-nướng--trợ-lý-đầu-bếp-ai-journal--gemini-ai)
   - [Sprint 6: Trải nghiệm Cộng đồng, Khám phá Hybrid & Quản trị Admin Toàn diện](#-sprint-6-trải-nghiệm-cộng-đồng-khám-phá-hybrid--quản-trị-admin-toàn-diện)
5. [MA TRẬN ROUTING, GIAO DIỆN & KẾT NỐI API](#5-ma-trận-routing-giao-diện--kết-nối-api)
6. [HẠ TẦNG ĐÁM MÂY & CI/CD PIPELINE (DEVOPS)](#6-hạ-tầng-đám-mây--cicd-pipeline-devops)
7. [CHỈ SỐ SỨC KHỎE MÃ NGUỒN & KIỂM THỬ (CODE HEALTH & QUALITY GATES)](#7-chỉ-số-sức-khỏe-mã-nguồn--kiểm-thử-code-health--quality-gates)
8. [LỘ TRÌNH PHÁT TRIỂN TIẾP THEO (FUTURE ROADMAP)](#8-lộ-trình-phát-triển-tiếp-theo-future-roadmap)

---

## 1. TỔNG QUAN DỰ ÁN & VẤN ĐỀ THỰC TIỄN

### 1.1 Bài toán Đặt ra
Trong nhịp sống hiện đại, người nấu ăn gia đình, sinh viên và dân văn phòng thường xuyên đối mặt với 3 vấn đề gây lãng phí thời gian và tiền bạc:
1. **"Hôm nay ăn gì?":** Mất nhiều thời gian suy nghĩ món ăn, trong khi tủ lạnh có sẵn đồ nhưng không biết kết hợp ra sao.
2. **Lãng phí thực phẩm (Food Waste):** Thực phẩm mua về tích trữ trong tủ lạnh hay bị quên lãng, quá hạn sử dụng dẫn tới phải vứt bỏ.
3. **Đi chợ kém hiệu quả:** Không nắm rõ đồ còn/hết trong tủ, dẫn đến mua thừa nguyên liệu sẵn có hoặc mua thiếu gia vị cần thiết.

### 1.2 Giải pháp Smart Recipe & Grocery Platform
Hệ thống là một **Web Application Trợ lý Bếp núc Cá nhân Toàn diện**:
* Quản lý tủ lạnh ảo theo từng lô (lot) và hạn sử dụng, cảnh báo đồ sắp hết hạn.
* Tự động sinh danh sách đi chợ thông minh từ công thức, tự trừ tồn kho tủ lạnh và nhóm theo kệ hàng siêu thị.
* Tích hợp Trợ lý AI Gemini sáng tạo món ăn từ thực phẩm tồn tủ (Zero-Waste cooking).
* Tự động khấu trừ kho tủ lạnh theo thuật toán **FEFO (First Expired, First Out)** khi ghi nhận nhật ký nấu ăn.
* Không gian cộng đồng chia sẻ công thức, nhân bản (Clone) công thức về sổ tay cá nhân và hệ thống quản trị Admin Panel hoàn chỉnh.

---

## 2. KIẾN TRÚC HỆ THỐNG & CÔNG NGHỆ (TECH STACK)

### 2.1 Kiến trúc Tổng thể (Umbrella Repository Architecture)
Dự án được cấu trúc theo mô hình **Umbrella Repository** quản lý 2 submodules độc lập:
* **Root Repository (`SmartRecipe-Project`):** Chứa tài liệu tổng thể, pipeline dữ liệu USDA, cấu hình Docker Compose và CI orchestration.
* **Backend Submodule (`smartrecipe-backend`):** Spring Boot 3 / Java 21 RESTful API Service.
* **Frontend Submodule (`smartrecipe-frontend`):** React 19 / Vite 8 Single Page Application.

```
┌─────────────────────────────────────────────────────────────┐
│                       NGƯỜI DÙNG                             │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS / Browser
┌───────────────────────────▼─────────────────────────────────┐
│         FRONTEND (React 19, Vite 8, Tailwind v4, Zustand)   │
│         Hosted on Vercel Edge CDN Network                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ RESTful APIs / JSON (Axios + JWT)
┌───────────────────────────▼─────────────────────────────────┐
│         BACKEND (Spring Boot 3.3.x, Java 21, Spring Security)│
│         Hosted on Render.com (Docker Container Service)      │
└──────────────┬───────────────────────────────┬──────────────┘
               │ JDBC                          │ Jedis / Lettuce
┌──────────────▼──────────┐    ┌───────────────▼──────────────┐
│ TiDB Serverless (Cloud) │    │ Upstash Redis (Cloud)        │
│ MySQL 8.0-compatible    │    │ JWT Blacklist & API Cache    │
│ 18 Bảng quan hệ         │    │ Rate Limit AI (10 req/ngày)  │
└─────────────────────────┘    └──────────────────────────────┘
               │                               │
┌──────────────▼──────────┐    ┌───────────────▼──────────────┐
│ Google Gemini AI API    │    │ Cloudinary Image CDN         │
│ gemini-2.0-flash        │    │ Lưu trữ ảnh đại diện, ảnh    │
│ Trợ lý gợi ý món ăn     │    │ món ăn & nhật ký nấu         │
└─────────────────────────┘    └──────────────────────────────┘
```

### 2.2 Chi tiết Tech Stack

| Tầng | Công nghệ chính | Phiên bản | Vai trò kỹ thuật |
|---|---|---|---|
| **Frontend Core** | React | 19.2.x | UI Library xây dựng Single Page Application hiện đại |
| **Build & Tooling** | Vite | 8.2.x | Bundler siêu tốc, Hot Module Replacement (HMR) |
| **State Management** | Zustand & TanStack Query | v5 | Quản lý Client State (Auth, UI) và Server State (Cache, Auto-refetch) |
| **Styling** | Vanilla CSS Modules + Tailwind CSS | v4.3.x | Kiểm soát tối đa thẩm mỹ Warm Terracotta Palette và responsive linh hoạt |
| **Form & Validation**| React Hook Form + Zod | 7.84 / 4.4 | Xử lý Form phức tạp, validate phía client |
| **Backend Core** | Spring Boot | 3.3.x | Nền tảng Web MVC & RESTful API chuẩn doanh nghiệp |
| **Ngôn ngữ** | Java | 21 (LTS) | Virtual Threads, Pattern Matching, Switch Expressions |
| **Bảo mật** | Spring Security + jjwt | 0.11.5 | Xác thực Stateless JWT, Refresh Token rotation, Phân quyền Role-based |
| **Data Access** | Spring Data JPA + Hibernate | - | ORM, HikariCP Connection Pool, Transaction Management |
| **Bộ nhớ đệm** | Spring Data Redis | 7.x | Caching danh mục, Rate Limiting AI, Session management |
| **Cơ sở dữ liệu** | MySQL 8.0 / TiDB Serverless | - | Lưu trữ quan hệ ACID, hỗ trợ chuẩn utf8mb4 |
| **Tích hợp Ngoài** | Google Gemini SDK, Cloudinary, Apache POI | - | AI Cooking Assistant, CDN lưu trữ ảnh, Xuất công thức ra Word (.docx) |

---

## 3. MÔ HÌNH CƠ SỞ DỮ LIỆU & PIPELINE DỮ LIỆU NGUYÊN LIỆU (USDA)

### 3.1 Bản đồ 18 Thực thể Dữ liệu (Entity Mapping)
Hệ thống chuẩn hóa 18 Entity đảm bảo tính toàn vẹn tham chiếu:
1. `users`: Tài khoản, thông tin cá nhân, mật khẩu BCrypt, vai trò `USER` / `ADMIN`.
2. `recipes`: Thông tin món ăn, thời gian nấu/chuẩn bị, độ khó, trạng thái (`DRAFT`, `PRIVATE`, `PUBLIC`, `DELETED`).
3. `recipe_ingredients`: Định lượng nguyên liệu cho từng công thức, đơn vị nấu.
4. `recipe_steps`: Các bước nấu tuần tự, tiêu đề, hướng dẫn và ảnh minh họa.
5. `recipe_tags` & `tags`: Phân loại món ăn theo chủ đề (Món chay, Món nhanh, Bữa sáng...).
6. `recipe_likes`: Quản lý lượt yêu thích và thống kê độ phổ biến.
7. `recipe_comments`: Cấu trúc bình luận dạng cây (hỗ trợ `parent_id` cho thảo luận lồng nhau).
8. `ingredients`: Từ điển nguyên liệu chuẩn, đơn vị gốc (`baseUnit`), giá trị dinh dưỡng trên 100g (Calo, Protein, Fat, Carbs) và liên kết Kệ hàng.
9. `aisles`: 9 Kệ hàng siêu thị (Gia vị, Rau củ, Thịt cá, Đồ khô...) hỗ trợ tối ưu lộ trình mua sắm.
10. `unit_conversions`: Ma trận quy đổi đơn vị (kg $\leftrightarrow$ g, ml $\leftrightarrow$ l, quả $\leftrightarrow$ g...).
11. `user_pantries`: Kho tủ lạnh ảo quản lý theo từng lô (`lot`), số lượng thực tế và ngày hết hạn (`expiryDate`).
12. `grocery_lists`: Phiên đi chợ (Trạng thái `ACTIVE`, `COMPLETED`), tự sinh từ thực đơn.
13. `grocery_items`: Chi tiết các món cần mua, phân nhóm theo Aisle và trạng thái đã tick chọn mua.
14. `cooking_journals`: Nhật ký lưu giữ kỷ niệm nấu nướng, đánh giá sao, cảm nhận hương vị và ảnh thành phẩm.
15. `ai_suggestion_logs`: Nhật ký theo dõi prompt và kết quả gợi ý của Gemini AI.
16. `follows`: Mối quan hệ theo dõi giữa các đầu bếp trong cộng đồng.
17. `notifications`: Thông báo in-app (khi có bình luận, follow, clone công thức).
18. `password_reset_otp`: Bảng quản lý mã xác thực OTP khôi phục mật khẩu.

### 3.2 Pipeline Xử lý Dữ liệu Nguyên liệu (USDA FoodData Central $\rightarrow$ Bếp Việt)
Để tính năng tính Calo và Macro đạt độ tin cậy khoa học tuyệt đối, hệ thống xây dựng pipeline trích xuất từ **USDA FoodData Central SR Legacy**:
* **Nguồn dữ liệu:** `food.csv` (~8.000 món) và `food_nutrient.csv` (36 MB, ~600.000 dòng dinh dưỡng).
* **Giai đoạn 1 (`clean_ingredients.py`):** Lọc 14/25 nhóm thực phẩm phù hợp; join lấy 4 chỉ số Calo, Protein, Fat, Carbs trên 100g.
* **Giai đoạn 2 (`suggest_keep.py` & `collapse_groups.py`):** Lọc bỏ đồ đóng hộp Tây phương không thông dụng; gộp các biến thể thịt/rau; dịch thuật sang tiếng Việt bản địa.
* **Giai đoạn 3 (`assign_aisles.py`):** Gán tự động vào 9 kệ hàng siêu thị chuẩn xác.
* **Giai đoạn 4 (`gen_seed_sql.py`):** Sinh file nạp dữ liệu `seed_ingredients.sql` gồm **290 nguyên liệu** hoàn hảo về dinh dưỡng.

---

## 4. BÁO CÁO CHI TIẾT TIẾN ĐỘ 6 SPRINTS

### 🟢 Sprint 1: Nền tảng, Xác thực & Phân quyền (Auth & Security)
* **Trạng thái:** ✅ Hoàn thành 100%
* **Điểm nhấn kỹ thuật:**
  - Triển khai Stateless JWT Authentication với Access Token (thời hạn 24 giờ) và Refresh Token (7 ngày).
  - Tự động chặn và refresh token qua Axios Interceptor phía Frontend không làm gián đoạn người dùng.
  - Phân quyền nghiêm ngặt theo Role (`USER`, `ADMIN`) qua `@PreAuthorize("hasRole('...')")`.
  - Bộ chuẩn hóa phản hồi `ApiResponse<T>` đồng nhất toàn hệ thống kèm `GlobalExceptionHandler` bắt gọn lỗi validation, 401, 403, 404, 500.
  - Giao diện `LoginPage.jsx`, `RegisterPage.jsx` phong cách Warm Editorial, bảo vệ các route nhạy cảm qua `ProtectedRoute`.

### 🔵 Sprint 2: Quản lý Người dùng & Dữ liệu Từ điển (Users & Master Data)
* **Trạng thái:** ✅ Hoàn thành 100%
* **Điểm nhấn kỹ thuật:**
  - Quản lý hồ sơ cá nhân (`/profile`), đổi tên hiển thị, tiểu sử và cập nhật ảnh đại diện trực tiếp lên Cloudinary CDN.
  - Tích hợp Redis Caching cho dữ liệu từ điển: `@Cacheable` trên danh sách kệ hàng, thẻ tag và bảng quy đổi đơn vị.
  - Component tìm kiếm nguyên liệu `IngredientAutocomplete.jsx` với cơ chế Debounce 300ms, hiển thị đơn vị gốc và kệ hàng tương ứng.

### 🟡 Sprint 3: Động cơ Công thức & Dinh dưỡng Động (Recipe Engine)
* **Trạng thái:** ✅ Hoàn thành 100%
* **Điểm nhấn kỹ thuật:**
  - Soạn thảo công thức đa bước (Multi-step Form): Thông tin chung $\rightarrow$ Định lượng nguyên liệu $\rightarrow$ Các bước nấu có ảnh $\rightarrow$ Gắn thẻ và chọn chế độ hiển thị.
  - **Tính toán Dinh dưỡng Động:** Hệ thống tự động tính tổng Calo, Protein, Chất béo, Tinh bột dựa trên khối lượng thực tế của từng nguyên liệu đối chiếu với dữ liệu dinh dưỡng 100g, tự động chia đều theo khẩu phần (`baseServings`).
  - **Nhân bản Công thức (Clone):** Cho phép người dùng sao chép bất kỳ công thức công khai nào về sổ tay riêng để tùy biến khẩu vị. Khi clone, hệ thống tự động gửi thông báo đến tác giả gốc.
  - Chế độ nấu ăn từng bước toàn màn hình (`CookingMode.jsx`) giúp người nấu dễ quan sát khi đứng bếp.
  - Xuất bản công thức ra file Word (`.docx`) chuẩn mẫu in ấn thông qua Apache POI.

### 🟠 Sprint 4: Tủ lạnh Ảo & Đi chợ Thông minh (Pantry & Smart Grocery)
* **Trạng thái:** ✅ Hoàn thành 100%
* **Điểm nhấn kỹ thuật:**
  - **Mô hình Tủ lạnh theo Lô (Option C):** Quản lý thực phẩm theo cặp `(user, ingredient, expiryDate)`. Cho phép cùng một nguyên liệu có nhiều hạn sử dụng khác nhau.
  - `ExpiryAlertBanner.jsx`: Hệ thống trực quan phân màu cảnh báo: Xanh (an toàn), Vàng (sắp hết hạn trong 3 ngày), Đỏ (đã hết hạn). Hỗ trợ nút dọn dẹp đồ hỏng 1-click.
  - **Thuật toán Đi chợ Thông minh (Smart Aggregation):**
    1. Trích xuất toàn bộ nguyên liệu từ các công thức được chọn vào thực đơn.
    2. Gộp các nguyên liệu trùng lặp về cùng một đơn vị đo thông qua `UnitNormalizationService` (đồ thị BFS).
    3. Đối chiếu kho tủ lạnh: `Lượng cần mua = (Tổng lượng công thức) - (Lượng đang có sẵn)`.
    4. Phân nhóm danh sách mua sắm theo 9 Kệ hàng siêu thị giúp tối ưu lộ trình di chuyển khi đi mua sắm.
  - **Shopping Mode & Auto-Stocking:** Giao diện đi chợ hỗ trợ tick chọn các món đã mua; khi bấm "Hoàn tất đi chợ", hệ thống tự động nhập kho các mặt hàng vừa mua vào Tủ lạnh ảo.

### 🔴 Sprint 5: Nhật ký Nấu nướng & Trợ lý Đầu bếp AI (Journal & Gemini AI)
* **Trạng thái:** ✅ Hoàn thành 100%
* **Điểm nhấn kỹ thuật:**
  - **Khấu trừ Tủ lạnh theo thuật toán FEFO (First Expired, First Out):** Khi người dùng ghi nhận món ăn đã nấu xong qua `CookingJournal` hoặc `CookingMode`, hệ thống tự động tìm các lô nguyên liệu tương ứng sắp hết hạn nhất để trừ dần số lượng, đảm bảo chống lãng phí thực phẩm.
  - **Tích hợp Google Gemini AI:**
    - *Zero-Waste Mode:* Phân tích danh sách đồ sắp hết hạn trong tủ lạnh để gợi ý món ăn tối ưu nhất.
    - *Feasible Recipe Finder:* Gợi ý món ăn ngon từ bất kỳ danh sách nguyên liệu nào người dùng nhập vào.
  - **Kiểm soát Tần suất (Rate Limiting) qua Redis:** Giới hạn mỗi người dùng tối đa 10 lượt gọi AI/ngày, tự động reset chuẩn xác vào lúc 00:00 múi giờ Việt Nam (`Asia/Ho_Chi_Minh`).
  - **Khả năng Phục hồi Lỗi (Error Resilience):** Bọc JSON parser an toàn, tự động sửa lỗi và đối chiếu tên nguyên liệu AI sinh ra với Database; nếu nguyên liệu chưa có, tự động tạo mới ở trạng thái chờ duyệt.
  - Giao diện Sổ tay Nhật ký dạng Timeline luân phiên cùng trang Chi tiết nhật ký [`JournalDetailPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/JournalDetailPage.jsx).

### 🟣 Sprint 6: Trải nghiệm Cộng đồng, Khám phá Hybrid & Quản trị Admin Toàn diện
* **Trạng thái:** ✅ Hoàn thành 98%
* **Điểm nhấn kỹ thuật:**
  - **Mô hình Trải nghiệm Hybrid (Guest & Member):**
    - Khách vãng lai xem tự do trang chủ `/`, chi tiết công thức `/recipes/:id`, trang đặc quyền `/features`.
    - `TopHeader.jsx` và `Sidebar.jsx` tự động co giãn: khách thấy nút Đăng ký/Đăng nhập và 2 menu cơ bản; thành viên thấy đầy đủ 7 công cụ làm bếp, chuông thông báo và nút `+ Lên thực đơn`.
    - Khách thao tác Like/Clone/Đi chợ được nhắc nhở đăng nhập lịch sự qua Toast thông báo, tuyệt đối không bị văng lỗi.
  - **Trang Đặc quyền Thành viên (`/features` - `BenefitsPage.jsx`):** Trình bày 4 trụ cột công nghệ (Tủ lạnh thông minh, Trợ lý AI, Đi chợ 1-Click, Sổ tay nhật ký) kích thích chuyển đổi người dùng.
  - **Bento Spotlight Khám phá:** Trang chủ hiển thị 3 món nổi bật tự động xoay chuyển sau 5 giây, tích hợp bộ lọc chuyển đổi giữa *Mới nhất* và *Phổ biến nhất* (`likeCount`).
  - **Hệ thống Chuông Thông báo In-App:** Tự động gửi thông báo khi có người bình luận, trả lời hoặc nhân bản công thức; chuông thông báo hiển thị badge đỏ và cập nhật tự động mỗi 30 giây.
  - **Phân hệ Quản trị viên (Admin Panel) Hoàn chỉnh:**
    1. `AdminDashboard.jsx`: Thống kê KPI tổng quan, phân bố độ khó, chỉ số chống lãng phí tủ lạnh và biểu đồ AI.
    2. `AdminRecipes.jsx`: Kiểm duyệt công thức (Duyệt công khai / Ẩn riêng tư / Xóa).
    3. `AdminIngredients.jsx` & `ReviewModal.jsx`: Duyệt nguyên liệu mới, bổ sung dinh dưỡng và gán Kệ hàng siêu thị (`aisleId`).
    4. `AdminUsers.jsx`: Quản lý danh sách người dùng, slide-out drawer xem hồ sơ & chỉ số hoạt động, nâng/hạ quyền `USER` $\leftrightarrow$ `ADMIN` có chốt chặn an toàn (không tự hạ quyền chính mình, không xóa admin duy nhất).
    5. `AdminMasterData.jsx`: CRUD Kệ hàng, Thẻ tag, Quy đổi đơn vị.
    6. `AdminSettings.jsx`: Giám sát toàn bộ nhật ký AI Logs và xuất dữ liệu ra file CSV.

---

## 5. MA TRẬN ROUTING, GIAO DIỆN & KẾT NỐI API

### 5.1 Tuyến đường Công cộng (Public & Guest Access)
| URL Tuyến đường | Component Frontend | Endpoint Backend chính | Quyền hạn | Mô tả chức năng |
|---|---|---|:---:|---|
| `/` | [`HomePage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/HomePage.jsx) | `GET /api/v1/recipes/public`<br>`GET /api/v1/tags` | Public | Bento Spotlight xoay 5s, lọc Mới nhất / Phổ biến nhất |
| `/recipes/:id` | [`RecipeDetailPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RecipeDetailPage.jsx) | `GET /api/v1/recipes/{id}`<br>`GET /api/v1/recipes/{id}/comments` | Public | Xem nguyên liệu, bước nấu, calo, bình luận |
| `/features` | [`BenefitsPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/BenefitsPage.jsx) | *(Static presentation)* | Public | Khám phá 4 trụ cột công nghệ nền tảng |
| `/users/:id` | [`UserProfilePage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/UserProfilePage.jsx) | `GET /api/v1/users/{id}/profile` | Public | Hồ sơ đầu bếp công khai và danh sách món ăn đã chia sẻ |
| `/login`, `/register` | [`LoginPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/LoginPage.jsx), [`RegisterPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RegisterPage.jsx) | `POST /api/v1/auth/login`<br>`POST /api/v1/auth/register` | Unauthenticated | Đăng nhập/Đăng ký, lưu trữ JWT vào Zustand store |

### 5.2 Tuyến đường Thành viên (Authenticated Members)
| URL Tuyến đường | Component Frontend | Endpoint Backend chính | Nghiệp vụ cốt lõi |
|---|---|---|---|
| `/recipes/new`<br>`/recipes/:id/edit` | [`RecipeFormPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RecipeFormPage.jsx) | `POST /api/v1/recipes`<br>`PUT /api/v1/recipes/{id}` | Soạn thảo công thức đa bước, tính calo tự động, upload ảnh bìa |
| `/recipes` | [`MyRecipesPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/MyRecipesPage.jsx) | `GET /api/v1/recipes/my` | Quản lý sổ tay công thức cá nhân (Công khai / Riêng tư / Bản nháp) |
| `/pantry` | [`PantryPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/PantryPage.jsx) | `GET /api/v1/pantry`<br>`POST /api/v1/pantry/items` | Quản lý kho tủ lạnh theo Lot và Hạn dùng, dọn dẹp đồ hết hạn 1-click |
| `/grocery` | [`GroceryPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/GroceryPage.jsx) | `GET /api/v1/grocery-lists/active`<br>`POST /api/v1/grocery-lists/generate` | Danh sách đi chợ thông minh tự gộp nguyên liệu, trừ tồn kho tủ lạnh |
| `/grocery/history` | [`GroceryHistoryPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/GroceryHistoryPage.jsx) | `GET /api/v1/grocery-lists/history` | Xem lại lịch sử các phiên đi chợ trước đây |
| `/journal` | [`CookingJournalPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/CookingJournalPage.jsx) | `GET /api/v1/journals`<br>`POST /api/v1/journals` | Nhật ký nấu nướng Timeline: Tự động trừ kho tủ lạnh theo FEFO |
| `/journal/:id` | [`JournalDetailPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/JournalDetailPage.jsx) | `GET /api/v1/journals/{id}` | Xem chi tiết kỷ niệm nấu ăn, đánh giá sao, link về công thức gốc |
| `/ai-suggestion` | [`AiSuggestionPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/AiSuggestionPage.jsx) | `POST /api/v1/ai/suggest`<br>`POST /api/v1/ai/suggest-pantry` | Gợi ý món ăn thông minh từ thực phẩm thừa hoặc nhập tay |
| *(Header Popover)* | [`NotificationDropdown.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/layout/NotificationDropdown.jsx) | `GET /api/v1/notifications`<br>`PATCH /api/v1/notifications/read-all` | Chuông thông báo in-app tự động polling cập nhật mỗi 30s |

### 5.3 Tuyến đường Quản trị viên (Admin Panel - Phân quyền Role: ADMIN)
| URL Tuyến đường | Component Frontend | Endpoint Backend chính | Quyền hạn | Chức năng kiểm duyệt & quản trị |
|---|---|---|:---:|---|
| `/admin/login` | [`AdminLoginPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminLoginPage.jsx) | `POST /api/v1/auth/login` | Public | Đăng nhập Admin riêng biệt, tự ping đánh thức server Render |
| `/admin/dashboard` | [`AdminDashboard.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminDashboard.jsx) | `GET /api/v1/admin/stats` | ADMIN | Dashboard tổng quan KPI, tỷ lệ chống lãng phí, hoạt động AI |
| `/admin/recipes` | [`AdminRecipes.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminRecipes.jsx) | `GET /api/v1/admin/recipes`<br>`PATCH /api/v1/admin/recipes/{id}/status` | ADMIN | Kiểm duyệt công thức: Duyệt công khai, Ẩn riêng tư, Xóa |
| `/admin/ingredients` | [`AdminIngredients.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminIngredients.jsx) | `GET /api/v1/admin/ingredients/pending-review`<br>`PATCH /api/v1/admin/ingredients/{id}` | ADMIN | Duyệt nguyên liệu mới, bổ sung dinh dưỡng và gán Kệ hàng |
| `/admin/users` | [`AdminUsers.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminUsers.jsx) | `GET /api/v1/admin/users`<br>`PATCH /api/v1/admin/users/{id}/role` | ADMIN | Quản lý người dùng, xem drawer chi tiết, nâng/hạ quyền có guard |
| `/admin/masterdata` | [`AdminMasterData.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminMasterData.jsx) | `GET/POST/PUT/DELETE /api/v1/aisles, tags, unit-conversions` | ADMIN | Quản trị từ điển danh mục Kệ hàng, Thẻ tag, Quy đổi đơn vị |
| `/admin/settings` | [`AdminSettings.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/admin/AdminSettings.jsx) | `GET /api/v1/admin/ai-logs` | ADMIN | Theo dõi chi tiết prompt AI Gemini, xuất dữ liệu ra file CSV |

---

## 6. HẠ TẦNG ĐÁM MÂY & CI/CD PIPELINE (DEVOPS)

### 6.1 Kiến trúc Triển khai Thực tế (Cloud Infrastructure)
* **Frontend:** Triển khai trên **Vercel Edge Network**, tích hợp tự động xây dựng từ nhánh `main` của repository frontend.
* **Backend:** Triển khai dưới dạng **Docker Web Service trên Render.com**, tự động nạp biến môi trường bảo mật.
* **Database:** **TiDB Serverless** (MySQL-compatible cluster tại Singapore), dung lượng 25 GiB, tự động co giãn và sao lưu.
* **Redis Cache:** **Upstash Redis Serverless** (yêu cầu kết nối TLS/SSL), phụ trách rate limit và session.
* **Storage:** **Cloudinary Media Cloud**, phân phối ảnh qua mạng phân phối nội dung toàn cầu.

### 6.2 Hệ thống CI/CD Workflows (GitHub Actions)
1. `.github/workflows/ci-root.yml`: Kiểm tra tính toàn vẹn của Umbrella repository, kiểm tra rò rỉ file bí mật `.env`, đối chiếu con trỏ submodules.
2. `smartrecipe-backend/.github/workflows/ci-backend.yml`: Chạy tự động khi có commit/PR: Cài đặt JDK 21, chạy toàn bộ 39 unit tests, đóng gói Maven JAR.
3. `smartrecipe-backend/.github/workflows/cd-backend.yml`: Tự động gọi Deploy Hook kích hoạt Render build container mới khi merge vào `main`.
4. `smartrecipe-frontend/.github/workflows/ci-frontend.yml`: Cài đặt Node.js 20, kiểm tra cú pháp với Oxlint, chạy 17 Vitest tests và kiểm tra `npm run build`.
5. `smartrecipe-frontend/.github/workflows/cd-frontend.yml`: Triển khai tự động lên Vercel Production.

---

## 7. CHỈ SỐ SỨC KHỎE MÃ NGUỒN & KIỂM THỬ (CODE HEALTH & QUALITY GATES)

### 7.1 Bộ Kiểm thử Tự động Backend (JUnit 5 + Mockito)
```
[INFO] Results:
[INFO] Tests run: 39, Failures: 0, Errors: 0, Skipped: 0
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
```
[INFO] Results:
[INFO] 
[INFO] Tests run: 47, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```
* **AuthServiceImplOtpTest (8 tests):** Kiểm tra gửi OTP thành công với Redis TTL 10 phút, kiểm tra email không tồn tại, chống spam cooldown 60 giây, kiểm tra OTP hết hạn, OTP sai, bảo vệ chống Brute-force khóa sau 5 lần sai, xác nhận mật khẩu không khớp, và đổi mật khẩu thành công kèm dọn dẹp Redis keys (Single-use).
* **AiServiceImplTest (14 tests):** Kiểm tra Rate Limit Redis (3 tests), Lịch sử gợi ý (2 tests), Khớp tên nguyên liệu 2 chiều và cơ chế tạo mới chờ duyệt (6 tests), Chịu lỗi khi AI trả về JSON hỏng (3 tests).
* **PantryServiceImplTest (10 tests):** Kiểm tra quy đổi đơn vị g/kg, ml/l, gộp lô cùng hạn sử dụng, cảnh báo sắp hết hạn và thuật toán khấu trừ FEFO.
* **RecipeServiceImplTest (7 tests):** Kiểm tra toàn diện CRUD, phân quyền tác giả, tính toán dinh dưỡng, Like/Unlike, Clone công thức và khấu trừ kho khi nấu.
* **GroceryServiceImplTest (4 tests):** Kiểm tra thuật toán gộp nguyên liệu trùng, trừ hao đồ tồn kho và phân nhóm theo kệ hàng siêu thị.
* **UnitNormalizationServiceTest (4 tests):** Kiểm tra thuật toán tìm đường đi ngắn nhất (BFS) quy đổi đơn vị.

### 7.2 Bộ Kiểm thử Tự động Frontend (Vitest + React Testing Library)
```
 ✓ src/services/__tests__/ingredientService.test.js (4 tests)
 ✓ src/components/pantry/__tests__/ExpiryAlertBanner.test.jsx (5 tests)
 ✓ src/components/ui/__tests__/ConfirmModal.test.jsx (4 tests)
 ✓ src/components/pantry/__tests__/AddPantryItemModal.test.jsx (4 tests)

 Test Files  4 passed (4)
      Tests  17 passed (17)
```
* Kiểm tra hành vi UI cảnh báo hết hạn, modal xác nhận xóa, thêm nguyên liệu tủ lạnh tự động gán baseUnit và bắt lỗi validate form.
* **Production Build:** `vite build` tạo bundle nén Gzip tối ưu hoàn tất trong **2.17 giây**, 0 lỗi.

---

## 8. LỘ TRÌNH PHÁT TRIỂN TIẾP THEO (FUTURE ROADMAP)

### 8.1 Tính năng Quên mật khẩu qua Email OTP [ĐÃ TRIỂN KHAI HOÀN TẤT 100%]
*(Chi tiết đặc tả kỹ thuật xem tại [`docs/forgot_password_email_otp_plan.md`](./forgot_password_email_otp_plan.md))*
* **Dịch vụ Email:** Tích hợp `spring-boot-starter-mail` qua Gmail SMTP Server (`smtp.gmail.com:587`, TLS). Có cơ chế Fallback in mã OTP ra server console phục vụ môi trường test local khi chưa điền App Password Gmail.
* **Kiến trúc Redis Cache Siêu gọn:** Sử dụng **Redis In-Memory Cache (TTL: 10 phút)** để lưu trữ mã OTP tạm thời; **không thêm Entity/Bảng mới**, giữ nguyên 18 bảng CSDL sạch sẽ 100%.
* **Bảo mật Đa lớp:** Cooldown 60 giây chống spam nút gửi mã (`otp:cooldown:{email}`), đếm số lần sai và tự động khóa mã nếu nhập sai quá 5 lần (`otp:attempts:{email}`). Xóa sạch các key Redis ngay sau khi đổi mật khẩu thành công (Single-use).
* **Trải nghiệm Frontend Hoàn chỉnh:** Modal 2 bước `ForgotPasswordModal.jsx` phong cách Warm Terracotta `#a13923` tại `/login` kèm đồng hồ đếm ngược 60 giây và tự động điền email sau khi khôi phục thành công.

### 8.2 Nghiệm thu Báo cáo Tốt nghiệp
* Đồng bộ con trỏ Submodules trên remote repository gốc.
* Hoàn thiện cuốn Báo cáo Thực tập Tốt nghiệp (khớp nối các sơ đồ tuần tự, bảng cơ sở dữ liệu và kết quả kiểm thử từ tài liệu này vào file báo cáo `.docx`).


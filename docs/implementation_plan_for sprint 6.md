# 📋 KẾ HOẠCH TOÀN DIỆN SPRINT 6 — CỘNG ĐỒNG, KHÁM PHÁ & TRẢI NGHIỆM THÀNH VIÊN

> **Phiên bản:** 2.0 (Cập nhật ngày 09/09/2026)  
> **Mục tiêu chiến lược:**  
> 1. Thiết kế cơ chế phân tách trải nghiệm giữa **Khách vãng lai (Guest)** và **Thành viên (Member)**.  
> 2. Mở cửa trang **Khám phá** và **Chi tiết món ăn** cho khách xem tự do mà tuyệt đối không sinh lỗi.  
> 3. Xây dựng trang chuyên biệt **"Đặc quyền thành viên" (`/features`)** để giới thiệu giá trị cốt lõi của SmartRecipe và kích thích người dùng đăng ký.  
> 4. Tự động hóa **Sidebar & Topbar** linh hoạt theo trạng thái đăng nhập.  
> 5. Hoàn thiện tương tác cộng đồng (Comment, Like, Follow) và dữ liệu thực tế cho Admin Panel.

---

## 💡 BỐI CẢNH & Ý TƯỞNG THIẾT KẾ CỐT LÕI (Product Design Context)

### 1. Vấn đề của thiết kế cũ:
- Trước đây, ứng dụng bọc toàn bộ trang chủ `/` bằng `<ProtectedRoute>`, dẫn đến việc khách chưa đăng nhập vừa vào web đã bị ép chuyển hướng về `/login`.
- Khách chưa hề biết SmartRecipe có những món ăn nào, giao diện ra sao, tính năng tiện lợi thế nào mà đã bị bắt tạo tài khoản -> Tỷ lệ thoát trang (bounce rate) cực kỳ cao.

### 2. Ý tưởng giải pháp — Mô hình Hybrid thông minh:
Hệ thống sẽ hoạt động linh hoạt theo **2 trạng thái người dùng**:

```
                              ┌───────────────────────────────────────────────┐
                              │            NGƯỜI DÙNG TRUY CẬP                │
                              └──────────────────────┬────────────────────────┘
                                                     │
                         Kiểm tra isAuthenticated qua useAuthStore
                                                     │
                        ┌────────────────────────────┴────────────────────────────┐
                        ▼                                                         ▼
         【 TRẠNG THÁI: CHƯA ĐĂNG NHẬP 】                           【 TRẠNG THÁI: ĐÃ ĐĂNG NHẬP 】
         (Khách vãng lai / Guest)                                  (Thành viên / Member)
  ┌──────────────────────────────────────────┐              ┌──────────────────────────────────────────┐
  │ 1. TOPBAR:                               │              │ 1. TOPBAR:                               │
  │    - Ẩn Avatar, Bell, Heart.             │              │    - Hiện đầy đủ: Tìm kiếm, Bell, Heart, │
  │    - Hiện 2 nút: [Đăng nhập] & [Đăng ký] │              │      Avatar cá nhân dẫn tới Profile.     │
  │                                          │              │                                          │
  │ 2. SIDEBAR (Chỉ còn 2 nút gọn gàng):    │              │ 2. SIDEBAR (Full công cụ làm bếp):       │
  │    - 🧭 Khám phá (Trang xem món ăn công  │              │    - Ẩn nút "Đặc quyền thành viên".      │
  │      khai, tìm kiếm, lọc danh mục).      │              │    - Hiện đủ 7 menu cá nhân:             │
  │    - ✨ Đặc quyền thành viên (Dẫn tới     │              │      + Khám phá                          │
  │      trang giới thiệu hệ sinh thái       │              │      + Công thức của tôi                 │
  │      và lý do nên đăng ký).              │              │      + Tủ nguyên liệu cá nhân            │
  │    - Ẩn nút "+ Lên thực đơn".            │              │      + Đi chợ                            │
  │                                          │              │      + Nhật ký nấu ăn                    │
  │ 3. XEM CHI TIẾT MÓN ĂN (/recipes/:id):   │              │      + Trợ lý đầu bếp AI                 │
  │    - Xem thoải mái nguyên liệu, các      │              │      + Cài đặt                           │
  │      bước, dinh dưỡng, bình luận.        │              │    - Hiện nút "+ Lên thực đơn".          │
  │    - Bấm Like / Clone / Đi chợ -> Nhắc   │              │                                          │
  │      đăng nhập nhẹ nhàng, không crash.   │              │ 3. ĐẦY ĐỦ QUYỀN HẠN: Thích, Bình luận,  │
  └──────────────────────────────────────────┘              │    Clone, Nấu ăn, Quản lý tủ lạnh.      │
                                                            └──────────────────────────────────────────┘
```

---

## 📌 BẢN KẾ HOẠCH CHI TIẾT TỪNG PHẦN

---

### 🚀 GIAI ĐOẠN 1: MỞ TUYẾN ĐƯỜNG CÔNG KHAI & ĐIỀU HƯỚNG AN TOÀN

#### Task 1.1: Cập nhật Router trong `App.jsx`
- **File:** [`src/App.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/App.jsx)
- **Hành động:**
  1. Tháo `<ProtectedRoute>` ra khỏi route `/` (để khách xem được `HomePage`).
  2. Tháo `<ProtectedRoute>` ra khỏi route `/recipes/:id` (để khách xem được `RecipeDetailPage`).
  3. Thêm route công khai mới: `/features` trỏ tới `BenefitsPage` (được bọc trong `AppLayout`).
  4. Vẫn giữ nguyên `<ProtectedRoute>` cho các route cá nhân:
     - `/recipes`, `/recipes/new`, `/recipes/:id/edit`
     - `/pantry`, `/grocery`, `/grocery/history`
     - `/journal`, `/journal/:id`
     - `/ai-suggestion`, `/profile`

#### Task 1.2: Bảo vệ chống lỗi khi khách thao tác trên `RecipeDetailPage.jsx`
- **File:** [`src/pages/RecipeDetailPage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/RecipeDetailPage.jsx)
- **Hành động:**
  - Thêm điều hướng đăng nhập thân thiện ở 3 hàm hành động:
    ```javascript
    // 1. Thích công thức
    const handleLike = async () => {
      if (!currentUser) {
        toast.info('Vui lòng đăng nhập để lưu công thức yêu thích!');
        navigate('/login');
        return;
      }
      // ... logic like/unlike
    };

    // 2. Clone công thức
    const handleClone = async () => {
      if (!currentUser) {
        toast.info('Vui lòng đăng nhập để sao chép công thức vào sổ tay cá nhân!');
        navigate('/login');
        return;
      }
      // ... logic clone
    };

    // 3. Thêm vào danh sách đi chợ
    const handleAddToGroceryList = async () => {
      if (!currentUser) {
        toast.info('Vui lòng đăng nhập để tự động tạo danh sách đi chợ!');
        navigate('/login');
        return;
      }
      // ... logic grocery
    };
    ```

---

### 🎨 GIAI ĐOẠN 2: ĐỘNG HÓA HEADER & SIDEBAR THEO TRẠNG THÁI ĐĂNG NHẬP

#### Task 2.1: Cập nhật `TopHeader.jsx` (Hiển thị nút Đăng nhập / Đăng ký cho khách)
- **File:** [`src/components/layout/TopHeader.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/layout/TopHeader.jsx)
- **Hành động:**
  - Lấy `isAuthenticated = useAuthStore((s) => s.isAuthenticated);`
  - Nếu `!isAuthenticated`:
    - Ẩn icon Bell, Heart và Avatar.
    - Render cụm nút:
      - Nút **`Đăng nhập`** (viền nhẹ hoặc chữ màu nâu đất `text-[#3d271d]`, hover chuyển màu).
      - Nút **`Đăng ký miễn phí`** (nền màu cam đỏ `bg-[#a13923] text-white rounded-full px-4 py-2 text-sm font-bold shadow-md hover:bg-[#8b311e]`).
  - Nếu `isAuthenticated`: Giữ nguyên Avatar, Bell, Heart như hiện nay.

#### Task 2.2: Cập nhật `Sidebar.jsx` (Ẩn thanh công cụ, chỉ hiện 2 nút cho khách)
- **File:** [`src/components/layout/Sidebar.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/layout/Sidebar.jsx)
- **Hành động:**
  - Lấy `isAuthenticated = useAuthStore((s) => s.isAuthenticated);`
  - Nếu `!isAuthenticated`:
    - Danh sách menu chỉ gồm **2 mục duy nhất**:
      1. `Khám phá` (`/`, icon: `LayoutDashboard` hoặc `Compass`)
      2. `Đặc quyền thành viên` (`/features`, icon: `Sparkles` với hiệu ứng màu vàng cam nổi bật)
    - Ẩn toàn bộ nút `+ Lên thực đơn` ở chân sidebar (hoặc thay bằng card nhỏ mời gọi đăng ký).
  - Nếu `isAuthenticated`:
    - Ẩn mục `Đặc quyền thành viên`.
    - Hiển thị đầy đủ 7 menu công cụ cá nhân và nút `+ Lên thực đơn`.

---

### ✨ GIAI ĐOẠN 3: XÂY DỰNG TRANG "ĐẶC QUYỀN THÀNH VIÊN" (`BenefitsPage.jsx`)

#### Task 3.1: Tạo trang `BenefitsPage.jsx` và CSS Module `BenefitsPage.module.css`
- **File mới:**
  - `src/pages/BenefitsPage.jsx`
  - `src/styles/pages/BenefitsPage.module.css`
- **Cấu trúc nội dung trang:**
  1. **Hero Header:**
     - Badge nhỏ: *"Hệ sinh thái thông minh cho căn bếp của bạn"*
     - Tiêu đề chính: *"Nấu ăn thông minh hơn, tiết kiệm hơn cùng Smart Recipe"*
     - Mô tả: Giới thiệu ngắn gọn cách Smart Recipe đồng hành từ lúc kiểm tra tủ lạnh, lên thực đơn, đi siêu thị cho đến khi hoàn thành món ăn.
     - Cụm nút CTA: `[ Đăng ký tài khoản miễn phí ]` & `[ Khám phá món ăn ngay ]`.
  2. **4 Trụ Cột Đặc Quyền Công Nghệ (Core Pillars Cards):**
     - 🧊 **Tủ nguyên liệu thông minh (Smart Pantry):**
       - Tự động theo dõi số lượng và ngày hết hạn.
       - Cảnh báo thực phẩm sắp hỏng -> Chống lãng phí tiền bạc của gia đình.
     - 🤖 **Trợ lý đầu bếp AI (AI Chef):**
       - Nhập những nguyên liệu sẵn có trong tủ, AI sáng tạo công thức nấu ăn tức thì.
       - Không còn cảnh đứng trước tủ lạnh băn khoăn *"Hôm nay ăn gì?"*.
     - 🛒 **Đi chợ 1-Click thông minh (Smart Grocery):**
       - Bấm 1 nút là chuyển toàn bộ nguyên liệu công thức vào danh sách mua sắm.
       - Tự động gom món theo kệ hàng siêu thị (Gia vị, Rau củ, Thịt tươi) giúp đi chợ nhanh gấp 3 lần.
     - 📖 **Sổ tay & Nhật ký ẩm thực (Cooking Journal):**
       - Lưu trữ công thức yêu thích, chấm điểm món ăn, ghi chú bí quyết riêng.
       - Tự động tính toán hàm lượng calo, protein, chất béo theo từng khẩu phần.
  3. **Bảng so sánh trực quan (Trước & Sau khi dùng Smart Recipe):**
     - So sánh giữa cách nấu ăn truyền thống (hay quên đồ, đồ ăn hết hạn, mất thời gian suy nghĩ) vs Trải nghiệm Smart Recipe.
  4. **Call To Action Banner (Chân trang):**
     - Khối màu ấm áp kêu gọi: *"Bắt đầu hành trình nấu ăn thông minh ngay hôm nay"* kèm nút đăng ký nổi bật.

---

### 🛡️ GIAI ĐOẠN 4: VÁ LỖ HỔNG SECURITY & BÌNH LUẬN CỘNG ĐỒNG

#### Task 4.1: Mở quyền truy cập công khai trong `SecurityConfig.java` [x] (ĐÃ HOÀN THÀNH)
- **File Backend:** [`SecurityConfig.java`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/security/SecurityConfig.java)
- **Hành động:** Cấp phép công khai không cần JWT:
  ```java
  .requestMatchers(HttpMethod.GET, "/api/v1/recipes/{id:\\d+}/comments").permitAll()
  .requestMatchers(HttpMethod.GET, "/api/v1/users/{id:\\d+}/profile").permitAll()
  ```
  *(Đảm bảo khách vào xem công thức hoặc hồ sơ người nấu không bị dính lỗi `401 Unauthorized`).*

#### Task 4.2: Sửa lỗi nhận diện chủ sở hữu bình luận trong `CommentItem.jsx` [x] (ĐÃ HOÀN THÀNH)
- **File Frontend:** [`CommentItem.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/comment/CommentItem.jsx)
- **Hành động:** Sử dụng `currentUser = useAuthStore(s => s.user)` để so sánh `currentUser.id === comment.author?.id`.
  *(Khắc phục triệt để lỗi `Number(payload.sub) = NaN` khiến tác giả không thấy nút Sửa/Xóa bình luận).*

#### Task 4.3: Nhúng `CommentSection` vào `RecipeDetailPage.jsx` [x] (ĐÃ HOÀN THÀNH)
- Nhúng component bình luận bên dưới khối "Món ngon tương tự". Khách vãng lai xem được bình luận; người đã đăng nhập có thể gửi bình luận, trả lời, sửa, xóa.
- Nâng cấp UX: Thay `window.confirm` bằng modal đồng bộ [`ConfirmModal.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/ui/ConfirmModal.jsx) và chuyển cụm nút Lưu/Hủy sang tông màu ấm Warm Palette.

#### Task 4.4: Dựng Author Card & Nút Follow trên `RecipeDetailPage.jsx` [x] (ĐÃ HOÀN THÀNH)
- Bổ sung khối thông tin Tác giả (Avatar, Tên hiển thị, Username, ngày đăng) và nhúng `FollowButton.jsx` bên cạnh tên tác giả.

#### Task 4.5: Hệ thống Thông báo In-App (In-App Notifications) [x] (ĐÃ HOÀN THÀNH)
- **Backend:** 
  - Entity [`Notification.java`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/entity/Notification.java) (recipient, actor, recipe, comment, type, title, message, isRead, createdAt).
  - Tự động phát thông báo khi có người bình luận công thức hoặc phản hồi bình luận của tác giả.
  - Các API: `GET /api/v1/notifications`, `GET /api/v1/notifications/unread-count`, `PATCH /api/v1/notifications/{id}/read`, `PATCH /api/v1/notifications/read-all`.
- **Frontend:**
  - Chuông thông báo trên [`TopHeader.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/layout/TopHeader.jsx) với chấm đỏ/badge đếm số lượng chưa đọc.
  - Dropdown Popover [`NotificationDropdown.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/layout/NotificationDropdown.jsx) phong cách Warm Cooking, cho phép đọc từng mục hoặc đánh dấu đã đọc tất cả.
  - Quản lý trạng thái bằng [`useNotificationStore.js`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/store/useNotificationStore.js) với cơ chế polling tự động 30 giây khi người dùng đang đăng nhập.

---

### 📊 GIAI ĐOẠN 5: TRANG KHÁM PHÁ (TRENDING) & HOÀN THIỆN ADMIN

#### Task 5.1: Backend & Frontend hỗ trợ lọc công thức Phổ biến nhất (Trending) [x] (ĐÃ HOÀN THÀNH)
- Backend [`RecipeController.java`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/controller/RecipeController.java) & [`RecipeServiceImpl.java`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/RecipeServiceImpl.java): Nhận tham số `sortBy` (`createdAt` | `likeCount`). Đã kiểm thử API hoạt động chuẩn xác.
- Frontend [`HomePage.jsx`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/HomePage.jsx): Nâng cấp toàn diện theo phong cách **Bento Editorial Discovery** gồm Bento Spotlight (auto-rotate 5s, hover tạm dừng), 6 thẻ ảnh chủ đề ẩm thực, Tab chuyển đổi "🔥 Phổ biến nhất" & "🕐 Mới nhất", huy hiệu thứ hạng 🏆 #1, và khối bài viết chuyên sâu từ Bếp trưởng.

#### Task 5.2: Hoàn thiện dữ liệu Admin Panel (Tồn đọng - Đang thực hiện)
- [x] **Admin Ingredients & Recipes:** Đã có giao diện duyệt công thức (`AdminRecipes.jsx`), quản lý dinh dưỡng nguyên liệu (`AdminIngredients.jsx`).
- [ ] **Admin Users:** Xây dựng component `AdminUsers.jsx` và API `GET /api/v1/admin/users`, khóa/mở tài khoản để thay thế màn hình `AdminPlaceholder`.
- [ ] **Admin Ingredients:** Bổ sung chọn Kệ hàng (`aisleId`) cho cả Backend `AdminController` và Frontend `ReviewModal`.
- [ ] **Admin Dashboard:** Bổ sung hàng KPI 2 (AI Calls, Nhật ký nấu, Cảnh báo tủ lạnh).

---

## 🗓️ BẢNG TIẾN TRÌNH THỰC HIỆN ĐỀ XUẤT

```
[BƯỚC 1] Router & Bảo vệ khách (App.jsx + RecipeDetailPage.jsx)
    │
    ▼
[BƯỚC 2] Dynamic Header & Sidebar (TopHeader.jsx + Sidebar.jsx)
    │
    ▼
[BƯỚC 3] Xây dựng trang "Đặc quyền thành viên" (BenefitsPage.jsx + CSS)
    │
    ▼
[BƯỚC 4] SecurityConfig permitAll & Nhúng Comment vào RecipeDetailPage
    │
    ▼
[BƯỚC 5] Author Card + Nút Like / Follow trên RecipeDetail
    │
    ▼
[BƯỚC 6] Tabs Mới nhất / Phổ biến nhất (HomePage + Backend Sort)
    │
    ▼
[BƯỚC 7] Admin Panel: Kệ hàng Aisle + KPI Dashboard + Trang Quản lý User
```

---

## ✅ TIÊU CHÍ NGHIỆM THU TỔNG THỂ

1. **Khách vãng lai:**
   - Vào web xem được ngay trang Khám phá `/` và mở chi tiết món bất kỳ `/recipes/:id`.
   - Sidebar của khách chỉ có đúng 2 nút: `Khám phá` và `Đặc quyền thành viên`.
   - Bấm vào `Đặc quyền thành viên` mở ra trang giới thiệu đẹp mắt với đầy đủ 4 tiện ích cốt lõi và nút Đăng ký.
   - Topbar của khách hiển thị rõ ràng 2 nút `[Đăng nhập]` và `[Đăng ký]`.
   - Bấm Like, Clone, hoặc Thêm vào giỏ chợ -> Hiện thông báo nhắc đăng nhập, không văng lỗi.
2. **Thành viên đã đăng nhập:**
   - Sidebar tự động ẩn `Đặc quyền thành viên`, hiện lại đầy đủ 7 menu công cụ cá nhân và nút `+ Lên thực đơn`.
   - Topbar hiển thị Avatar cá nhân, Chuông thông báo, Yêu thích.
   - Bình luận, trả lời, sửa, xóa bình luận của mình trơn tru.
   - Quản lý công thức, tủ lạnh, đi chợ, trợ lý AI hoạt động bình thường.
3. **Quản trị viên (Admin):**
   - Không còn màn hình khung rỗng "Module đang phát triển", có thể quản lý danh sách người dùng và gán kệ hàng cho nguyên liệu.

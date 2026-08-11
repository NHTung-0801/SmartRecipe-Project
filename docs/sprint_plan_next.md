# Sprint Plan - Các bước tiếp theo

> **Sprint:** Sprint 3+ (Module Bình luận + Hồ sơ người dùng + Tủ lạnh & Đi chợ + AI)
> **Ngày cập nhật:** 10/08/2026
> **Trạng thái hiện tại:** Pantry MVP đã hoàn thiện theo phương án C (lot + base unit + ownership + FEFO-ready). Grocery là module tiếp theo.

---

## 📊 TỔNG QUAN TIẾN ĐỘ DỰ ÁN

| Module | Sprint | Trạng thái |
|--------|--------|------------|
| Auth (Đăng ký / Đăng nhập / Refresh Token) | Sprint 1 | ✅ Hoàn thành |
| Master Data (Ingredient, Aisle, Tag, UnitConversion) | Sprint 1 | ✅ Hoàn thành |
| Recipe CRUD + Listing + Search | Sprint 2 | ✅ Hoàn thành |
| Like / Unlike + Clone | Sprint 2 | ✅ Hoàn thành |
| Upload ảnh (Cloudinary) | Sprint 2 (bổ sung) | ✅ Hoàn thành |
| **Comment (Bình luận)** | Sprint 3 | ✅ Vừa hoàn thành |
| **User Profile + Follow** | Sprint 3 | ✅ Hoàn thành |
| **Pantry (Tủ lạnh ảo)** | Sprint 4 | ✅ Hoàn thành MVP, đã có test nghiệp vụ |
| **Grocery (Đi chợ thông minh)** | Sprint 4 | ✅ Hoàn thành |
| **Cooking Journal + AI (Gemini)** | Sprint 5 | ❌ Chưa làm |
| **Notification** | Sprint 5 | ❌ Chưa làm |
| **Testing + Deployment** | Sprint 6 | ❌ Chưa làm |

---

## 🎯 KẾ HOẠCH CÁC BƯỚC TIẾP THEO

### ✅ ĐÃ HOÀN THÀNH: Module Bình luận (Comment)

Module bình luận đã được triển khai đầy đủ gồm:
- **Backend:** Entity `RecipeComment` (cập nhật thêm parent, replies dạng cây), DTO `CommentRequest` / `CommentResponse`, `RecipeCommentRepository`, `CommentService` + `CommentServiceImpl`, `CommentController` (GET/POST/PUT/DELETE).
- **Frontend:** `commentService.js`, `CommentSection.jsx`, `CommentItem.jsx` (hỗ trợ reply lồng, edit, delete), `CommentSection.module.css`, đã tích hợp vào `RecipeDetailPage.jsx`.

---

### ✅ ĐÃ HOÀN THÀNH: Hồ sơ người dùng (User Profile) + Follow

**Mức độ ưu tiên: CAO** - Đã hoàn thiện tính năng kết nối người dùng.

#### Backend (Đã hoàn thành):
- [x] **Endpoint `GET /api/v1/users/{id}/profile`** - Lấy thông tin profile.
- [x] **Endpoint `PUT /api/v1/users/profile`** - Cập nhật profile (displayName, bio, avatar).
- [x] **Entity `Follow`** - Fields: `follower` (User), `following` (User), `createdAt`.
- [x] **Repository `FollowRepository`** - Các hàm kiểm tra và đếm.
- [x] **Service `FollowService`** + **`FollowServiceImpl`**.
- [x] **Controller `FollowController`** - Các endpoint follow/unfollow và danh sách.

#### Frontend (Đã hoàn thành):
- [x] **Page `UserProfilePage.jsx`** - Hiển thị profile + danh sách công thức.
- [x] **Page `EditProfilePage.jsx`** - Form chỉnh sửa profile.
- [x] **Component `FollowButton.jsx`** - Nút Follow/Unfollow.
- [x] **Chỉnh sửa `Navbar.jsx`** - Thêm link đến profile.

---

### ✅ ĐÃ HOÀN THÀNH MVP: Pantry - Quản lý Tủ lạnh ảo (Virtual Pantry)

**Mức độ ưu tiên: CAO** - Module cốt lõi để hệ thống "thông minh", là nền tảng cho Grocery List và AI Zero-Waste.
Tương ứng với Sprint 4 trong `project_master_plan.md`.

#### Backend (Đã hoàn thành MVP):
- [x] Dùng entity `UserPantry` theo lot `user + ingredient + expiryDate`.
- [x] DTO `PantryRequest` / `PantryResponse` / `PantrySummaryResponse`; request nhận `unit`.
- [x] `PantryRepository` hỗ trợ ownership và tra lot cùng expiry.
- [x] `PantryService` + `PantryServiceImpl`: CRUD, filter, expiry summary, merge đúng lot, low-stock theo tổng ingredient.
- [x] `UnitNormalizationService`: chuẩn hóa alias, conversion hai chiều và chuỗi ngắn về `Ingredient.baseUnit`.
- [x] `PantryController`: mọi thao tác mutating lấy `userId` từ JWT principal.
- [x] Test: 9 case cho kg/g, lít/ml, reverse conversion, unit không hợp lệ, ownership, merge/tách lot và low-stock.
- [ ] Tự động trừ theo FEFO sẽ nối vào Grocery/Cooking Journal khi các module đó được triển khai.

#### Frontend (Đã hoàn thành MVP):
- [x] **Service `pantryService.js`**.
- [x] **Page `PantryPage.jsx`** - Giao diện quản lý tủ lạnh:
  - Danh sách nguyên liệu hiện có (kèm số lượng, đơn vị, ngày hết hạn).
  - Form thêm nguyên liệu (tích hợp `IngredientAutocomplete`).
  - Cảnh báo màu sắc (xanh: còn hạn, vàng: sắp hết hạn, đỏ: đã hết hạn).
  - Hiển thị từng lot theo FEFO, chỉnh/xóa đúng lot, thêm số lượng kèm unit.
- [ ] Nút "Thêm vào danh sách đi chợ" sẽ hoàn thiện cùng module Grocery.

---

### ✅ ĐÃ HOÀN THÀNH: Grocery - Danh sách đi chợ thông minh (Smart Grocery List)

**Mức độ ưu tiên: TRUNG BÌNH** - Tính năng tiện ích, tăng trải nghiệm người dùng.
Tương ứng với Sprint 4 trong `project_master_plan.md`.

#### Backend (Đã hoàn thành):
- [x] **Entity `GroceryList`** + **`GroceryItem`**:
  - `GroceryList`: `id`, `user`, `name`, `createdAt`, `completedAt`, `isCompleted`.
  - `GroceryItem`: `id`, `groceryList`, `ingredient`, `quantity`, `unit`, `isPurchased`, `aisle` (để sắp xếp theo gian hàng).
- [x] **Thuật toán thông minh trong `GroceryService`**:
  - Gộp nhóm nguyên liệu trùng lặp.
  - Quy đổi đơn vị về cùng 1 đơn vị trước khi gộp.
  - Đối chiếu với Pantry: tự động trừ đi nguyên liệu đã có sẵn.
  - Sắp xếp danh sách theo Aisle (gian hàng) để tiện đi chợ.
- [x] **Controller `GroceryController`** - Endpoints: CRUD grocery list, add/remove items, mark as purchased, complete list.

#### Frontend (Đã hoàn thành):
- [x] **Service `groceryService.js`**.
- [x] **Page `GroceryPage.jsx`**:
  - Tạo danh sách đi chợ mới (thủ công hoặc tự động từ meal plan).
  - Hiển thị danh sách theo nhóm Aisle.
  - Tick chọn món đã mua → tự động cập nhật Pantry.
  - Nút "Hoàn thành" → chuyển trạng thái + cập nhật Pantry.

---

### 🟢 ƯU TIÊN 4: Nâng cấp & Fix lỗi (Technical Debt)

- [x] **Unit Conversion cho Pantry** - Đã dùng `UnitConversionRepository` để chuẩn hóa quantity/threshold về base unit; phần dinh dưỡng/Grocery sẽ tái sử dụng.
- [ ] **Tối ưu search Recipe** - Thêm filter theo tag, difficulty, prepTime, cookTime vào `RecipeSearchRequest` và UI tương ứng.
- [ ] **Pagination UI** - Tích hợp phân trang cho `HomePage`, `MyRecipesPage`.
- [ ] **Loading skeletons** - Thêm skeleton loading cho các trang danh sách.
- [ ] **Error boundary** - Thêm React Error Boundary toàn cục.
- [ ] **Validation backend** - Kiểm tra `@Valid`, `@NotBlank`, `@NotNull` trên tất cả DTO request.
- [ ] **Cleanup cascade orphans** - Kiểm tra orphanRemoval và cascade type trong các entity Recipe.

---

### 🔵 ƯU TIÊN 5: Cooking Journal + AI (Gemini)

**Mức độ ưu tiên: THẤP** - Tính năng nâng cao, cần Pantry hoạt động ổn định trước.
Tương ứng với Sprint 5 trong `project_master_plan.md`.

- [ ] Backend: API Cooking Journals (lưu nhật ký → trigger trừ nguyên liệu khỏi Pantry).
- [ ] Backend: Tích hợp Gemini REST API (`/ai/suggest`), 2 chế độ: Zero-Waste (giải cứu tủ lạnh) và Feasible Recipe Finder.
- [ ] Backend: Rate Limiting cho AI API qua Redis (VD: 10 lần/ngày/user).
- [ ] Frontend: `CookingJournalPage.jsx` + `AiSuggestionPage.jsx`.

---

### ⚫ ƯU TIÊN 6: Infrastructure & DevOps

- [ ] **Docker Compose** - Xác nhận `docker-compose.yml` đầy đủ (MySQL, backend, frontend, Redis).
- [ ] **Environment Variables** - Tạo file `.env.example` cho backend và frontend.
- [ ] **CI/CD Pipeline** - GitHub Actions workflow (build + test).
- [ ] **API Rate Limiting** - Cấu hình rate limiter cho endpoint quan trọng.
- [ ] **Deploy** - Vercel (Frontend), Render.com/Railway (Backend).

---

## 📅 DỰ KIẾN PHÂN BỔ THỜI GIAN (CẬP NHẬT)

| Tuần | Nội dung | Ngày dự kiến | Ưu tiên |
|------|----------|--------------|---------|
| Tuần 1 (08/03 – 14/03) | ~~Module Comment, User Profile + Follow~~ → ✅ Đã xong. | 08/03 – 14/03 | 🔴 CAO |
| Tuần 2 (15/03 – 21/03) | Bắt đầu Pantry (Tủ lạnh ảo) | 15/03 – 21/03 | 🔴 CAO |
| Tuần 3 (22/03 – 28/03) | Hoàn thiện Pantry. Bắt đầu Grocery (Đi chợ thông minh) | 22/03 – 28/03 | 🟠 CAO |
| Tuần 4 (29/03 – 04/04) | Hoàn thiện Grocery. Bug fixes, tối ưu, unit conversion | 29/03 – 04/04 | 🟡 TRUNG BÌNH |
| Tuần 5+ (05/04 trở đi) | Cooking Journal + AI (Gemini), Notification, Testing, Deployment | 05/04+ | 🟢/🔵 THẤP |

---

## 📋 CHI TIẾT CÁC TASK SPRINT 3

### Module Comment (Backend) - Chi tiết

1. **Tạo entity `Comment`**
   ```java
   @Entity
   @Table(name = "comments")
   public class Comment {
       @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
       private Long id;
       
       @Column(nullable = false, columnDefinition = "TEXT")
       private String content;
       
       @ManyToOne(fetch = FetchType.LAZY)
       @JoinColumn(name = "parent_id")
       private Comment parent;
       
       @OneToMany(mappedBy = "parent", cascade = CascadeType.ALL, orphanRemoval = true)
       private List<Comment> replies = new ArrayList<>();
       
       @ManyToOne(fetch = FetchType.LAZY)
       @JoinColumn(name = "recipe_id", nullable = false)
       private Recipe recipe;
       
       @ManyToOne(fetch = FetchType.LAZY)
       @JoinColumn(name = "user_id", nullable = false)
       private User user;
       
       private LocalDateTime createdAt;
       private LocalDateTime updatedAt;
       
       @PrePersist void onCreate() { createdAt = updatedAt = LocalDateTime.now(); }
       @PreUpdate void onUpdate() { updatedAt = LocalDateTime.now(); }
   }
   ```

2. **Tạo DTO**
   - `CommentRequest.java`: content, parentId (optional)
   - `CommentResponse.java`: id, content, author (AuthorSummaryResponse), parentId, replies (List<CommentResponse>), createdAt

3. **Tạo Repository `CommentRepository`**
   ```java
   List<Comment> findByRecipeIdAndParentIsNullOrderByCreatedAtDesc(Long recipeId);
   long countByRecipeId(Long recipeId);
   ```

4. **Tạo Service `CommentService`** + impl
   - `Page<CommentResponse> getComments(Long recipeId, int page, int size)` (chỉ lấy root comments, replies load eager)
   - `CommentResponse createComment(Long recipeId, CommentRequest request, Long userId)`
   - `CommentResponse updateComment(Long commentId, CommentRequest request, Long userId)`
   - `void deleteComment(Long commentId, Long userId)`

5. **Tạo Controller `CommentController`**
   ```java
   @RestController
   @RequestMapping("/api/v1")
   public class CommentController {
       @GetMapping("/recipes/{recipeId}/comments")
       ResponseEntity<Page<CommentResponse>> getComments(@PathVariable Long recipeId, Pageable pageable);
       
       @PostMapping("/recipes/{recipeId}/comments")
       ResponseEntity<CommentResponse> createComment(@PathVariable Long recipeId, @Valid @RequestBody CommentRequest request, Principal principal);
       
       @PutMapping("/comments/{id}")
       ResponseEntity<CommentResponse> updateComment(@PathVariable Long id, @Valid @RequestBody CommentRequest request, Principal principal);
       
       @DeleteMapping("/comments/{id}")
       ResponseEntity<Void> deleteComment(@PathVariable Long id, Principal principal);
   }
   ```

### Module Follow (Backend) - Chi tiết

1. **Tạo entity `Follow`**
   ```java
   @Entity
   @Table(name = "follows", uniqueConstraints = @UniqueConstraint(columnNames = {"follower_id", "following_id"}))
   public class Follow {
       @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
       private Long id;
       
       @ManyToOne(fetch = FetchType.LAZY)
       @JoinColumn(name = "follower_id", nullable = false)
       private User follower;
       
       @ManyToOne(fetch = FetchType.LAZY)
       @JoinColumn(name = "following_id", nullable = false)
       private User following;
       
       private LocalDateTime createdAt;
       @PrePersist void onCreate() { createdAt = LocalDateTime.now(); }
   }
   ```

2. **Tạo Repository, Service, Controller** tương tự pattern đã có.

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Entity `RecipeComment`** đã được cập nhật với cấu trúc cây (parent-child, replies). Không cần tạo entity `Comment` mới như kế hoạch cũ.
2. **Bảng `comments`** - Cần cập nhật `init_database.sql` thêm cột `parent_id`, `updated_at` nếu chưa có.
3. **Bảng `follows`** - Cần thêm vào `init_database.sql`.
4. **Bảng `user_pantry`** đã chuyển sang lot-level; Grocery vẫn cần triển khai service/controller/frontend theo entity hiện có.
5. **Cloudinary config** - Đảm bảo biến môi trường `CLOUDINARY_URL` đã được cấu hình.
6. **Security** - Kiểm tra CORS config, JWT expiration, refresh token rotation.
7. **Database indexes** - Thêm index cho `recipe_id`, `parent_id` (comments), `follower_id`/`following_id` (follows), `user_id`/`ingredient_id` (pantries).

---

## 📝 GHI CHÚ KIỂM TRA TIẾN ĐỘ (CẬP NHẬT 10/08/2026)

| Mục | Trạng thái | Ghi chú |
|-----|-----------|---------|
| Auth | ✅ | Đầy đủ: đăng ký, đăng nhập, refresh token. |
| Master Data | ✅ | Ingredient, Aisle, Tag, UnitConversion: Backend & Frontend đầy đủ. |
| Recipe CRUD | ✅ | Create, read, update, soft delete, listing, search. |
| Clone | ✅ | Sao chép công thức về bộ sưu tập cá nhân. |
| Like/Unlike | ✅ | Thả tim công thức, hiển thị like count. |
| Upload ảnh | ✅ | Cloudinary upload, ImageUploadResponse, frontend UI. |
| **Comment** | ✅ | Entity (cây), DTO, Repository, Service, Controller, Frontend (CommentSection + CommentItem + CSS). Đã tích hợp vào RecipeDetailPage. |
| **User Profile** | ✅ | Đã hoàn thành GET/PUT profile, avatar, displayName, bio. |
| **Follow** | ✅ | Đã hoàn thành Entity, Repository, Service, Controller, FollowButton. |
| **Pantry** | ✅ MVP | Lot-level, base unit, ownership, expiry/summary/filter và frontend đã hoàn thiện; FEFO deduction chờ Grocery/Cooking Journal. |
| **Grocery** | ✅ | Đã hoàn thành (Backend CRUD, generate, complete, Frontend Components/Pages). |
| **AI (Gemini)** | ❌ | Cần làm: Zero-Waste, Feasible Recipe Finder. |
| UnitConversion thực tế | ✅ Pantry | Đã áp dụng vào quantity/threshold Pantry và có test; mở rộng sang Grocery/dinh dưỡng sau. |
| Pagination UI | ❌ | Chưa có phân trang cho danh sách. |
| Docker / CI/CD | ❌ | Chưa triển khai. |

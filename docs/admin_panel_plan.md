# Kế hoạch Admin Panel — SmartRecipe

> **Ngày lập:** 28/08/2026  
> **Ràng buộc:** Không thay đổi DB schema / entity. Mọi tính năng dựa hoàn toàn vào 18 entity hiện có.  
> **Trạng thái:** Bản kế hoạch, chưa triển khai.

---

## 1. Nguyên tắc thiết kế

- Admin Panel là **SPA riêng** tại route `/admin/*`, layout tách biệt hoàn toàn với user thường.
- **Guard:** Component `AdminGuard.jsx` kiểm tra `user.role === 'ADMIN'` — redirect về `/` nếu không phải.
- **Color scheme:** Dùng nguyên token CSS đã có (`--sr-primary: #a13923`, `--sr-surface: #fff8f4`) — không tạo theme mới.
- **Font:** Giữ `Plus Jakarta Sans` (heading) + `Be Vietnam Pro` (body) như toàn bộ app.
- Mọi API call gửi JWT như bình thường — backend đã phân quyền bằng `@PreAuthorize("hasRole('ADMIN')")`.

---

## 2. Cấu trúc Sidebar

```
/admin
├── 📊 Overview              ← Dashboard tổng quan hệ thống
├── 🥘 Nguyên liệu           ← Kiểm duyệt + phân tích (trọng tâm nhất)
├── 📋 Kiểm duyệt Công thức  ← Recipe moderation
├── 👥 Quản lý Người dùng    ← User management
├── ⚙️  Master Data           ← Kệ hàng, Tags, Unit Conversions
└── 🔧 Cài đặt Hệ thống      ← Gemini AI key, AI Logs, Bảo mật
```

---

## 3. Bản đồ nguồn dữ liệu (18 Entity)

| Entity | Module sử dụng |
|---|---|
| User | Dashboard KPIs, User Management, AI Logs |
| Recipe | Dashboard chart, Kiểm duyệt công thức |
| Ingredient | Module nguyên liệu, pending-review |
| Aisle | Master Data, phân bố kệ hàng |
| Tag | Master Data, tag cloud |
| UnitConversion | Master Data |
| UserPantry | Dashboard (sắp hết hạn), Inventory stats |
| GroceryList | Dashboard (ACTIVE count) |
| CookingJournal | Dashboard (rating TB), User activity, Recipe stats |
| AiSuggestionLog | AI Logs, Cài đặt, top users AI |
| Follow | User detail (follower/following count) |
| RecipeLike | Top công thức, User engagement |
| RecipeComment | Kiểm duyệt công thức (drawer) |
| RecipeIngredient | Nguyên liệu phổ biến nhất |
| RecipeStep | Xem chi tiết công thức trong Admin |
| RecipeTag | Tags usage count |

---

## 4. Chi tiết từng Module

---

### 4.1 Dashboard

#### KPI Row 1 — Nền tảng
| Card | Query | Entity |
|---|---|---|
| Tổng User (+ N mới/7 ngày) | COUNT(*) + WHERE createdAt >= now()-7d | User |
| Công thức PUBLIC (+ N/7 ngày) | COUNT(*) WHERE status='PUBLIC' | Recipe |
| Nguyên liệu cần duyệt 🔴 | WHERE calories=0 AND name NOT LIKE '%muối%' | Ingredient |
| Grocery Lists ACTIVE | COUNT(*) WHERE status='ACTIVE' | GroceryList |

#### KPI Row 2 — Engagement & AI
| Card | Query | Entity |
|---|---|---|
| Nhật ký nấu /7 ngày | COUNT(*) WHERE cookedAt >= now()-7d | CookingJournal |
| Rating trung bình | AVG(rating) | CookingJournal |
| AI calls hôm nay | COUNT(*) WHERE DATE(createdAt) = today | AiSuggestionLog |
| Sắp hết hạn (3 ngày) | COUNT(*) WHERE expiryDate BETWEEN today AND today+3 | UserPantry |

#### Charts
| Chart | Mô tả |
|---|---|
| Công thức tạo mới (30 ngày) | Bar chart GROUP BY DATE(created_at) |
| Phân bố độ khó | Pie: EASY / MEDIUM / HARD |
| Lượt gọi AI (7 ngày) | Bar chart GROUP BY DATE |
| Top 5 công thức nhiều Like | ORDER BY likeCount DESC |

---

### 4.2 Nguyên liệu (Trọng tâm nhất)

Luồng: **User quick-add** → calories=0 → **Admin duyệt** và bổ sung dinh dưỡng.

#### Tab 1: Chờ duyệt
- Filter: `calories = 0 AND name NOT LIKE '%muối%'`
- Bảng: Tên | Kệ hàng | baseUnit | Ngày tạo | Actions
- Actions: [Bổ sung dinh dưỡng] [Gán kệ] [Xóa]
- Quick-approve modal: form điền calories + protein + fat + carbs

#### Tab 2: Tất cả
- Search + Filter: Kệ hàng | Có/Thiếu dinh dưỡng
- Bảng: Tên | Kệ | Calories | Protein | Fat | Carbs | baseUnit | Actions
- Sortable columns

#### Tab 3: Phân tích Kệ hàng (mới)
- Grid 9 kệ, mỗi kệ: Tên + icon + số nguyên liệu + progress bar hoàn thiện
- Source: GROUP BY aisle_id FROM ingredients

#### Tab 4: Phổ biến nhất (mới)
- Top 20 nguyên liệu xuất hiện nhiều nhất trong recipe_ingredients
- Source: GROUP BY ingredient_id FROM recipe_ingredients ORDER BY COUNT DESC

#### Backend cần thêm (1 endpoint)
```
GET /api/v1/ingredients/pending-review   @PreAuthorize("hasRole('ADMIN')")
```

---

### 4.3 Kiểm duyệt Công thức

#### Bộ lọc
Status | Độ khó | Có ảnh | Khoảng ngày | Tìm tên/tác giả

#### Bảng — Cột đầy đủ
| Cột | Nguồn |
|---|---|
| Tên, Tác giả, Ngày tạo | Recipe |
| Độ khó, Status | Recipe.difficulty, Recipe.status |
| ❤ Lượt thích | Recipe.likeCount |
| 💬 Bình luận | COUNT(RecipeComment) |
| 🔁 Đã clone | COUNT(Recipe WHERE clonedFrom = id) |
| ⭐ Rating TB | AVG(CookingJournal.rating) |

#### Drawer chi tiết công thức
- Ảnh + tên + tags
- Phân bố rating 1-5 sao từ CookingJournal
- Danh sách bình luận gần đây
- Nút: Duyệt / Ẩn / Xóa

#### Backend cần thêm (AdminRecipeController)
```
GET    /api/v1/admin/recipes
PATCH  /api/v1/admin/recipes/{id}/status
DELETE /api/v1/admin/recipes/{id}
```

---

### 4.4 Quản lý Người dùng

#### KPI Cards
Tổng User | Admin accounts | Mới trong 7 ngày

#### Bảng
| Cột | Nguồn |
|---|---|
| Avatar + Username + Email, Role, Ngày tham gia | User |
| 📝 Công thức | COUNT(Recipe WHERE author_id) |
| 🍳 Nhật ký | COUNT(CookingJournal WHERE user_id) |
| 👥 Followers | COUNT(Follow WHERE following_id) |

#### Drawer User Detail (tabs)
- Công thức | Nhật ký | Cộng đồng | AI usage
- Actions: [Đổi Role USER ↔ ADMIN] [Xóa tài khoản]

> **Không có "Khóa tài khoản"** — User entity không có is_active. Có thể thêm sau nếu cần.

#### Backend cần thêm (AdminUserController)
```
GET    /api/v1/admin/users
GET    /api/v1/admin/users/{id}
PATCH  /api/v1/admin/users/{id}/role
DELETE /api/v1/admin/users/{id}
```

---

### 4.5 Master Data

#### Tab Kệ hàng (Aisles)
- Cột: Tên | Số nguyên liệu | % hoàn thiện dinh dưỡng | Actions
- Backend đã có: GET/POST/PUT/DELETE /aisles ✅

#### Tab Tags
- Cột: Tên | Số công thức dùng | Actions
- Visualization: Tag Cloud (size tỉ lệ count)
- Backend đã có: GET/POST /tags ✅

#### Tab Quy đổi Đơn vị
- Hiển thị dạng Matrix (nguyên liệu × đơn vị) thay vì list
- Backend đã có: GET/POST/PUT/DELETE /unit-conversions ✅

---

### 4.6 Cài đặt Hệ thống

#### Tab Gemini AI
- Hiển thị API Key (masked) + status Connected/Disconnected
- Daily limit: 10 calls/day/user

#### Tab AI Logs
- KPI: Tổng lượt | Tỷ lệ lưu thành công thức | ZERO_WASTE vs FEASIBLE_FINDER
- Bảng: User | Loại | Đã lưu? | Ngày | [Xem JSON]
- Top 5 users dùng AI nhiều nhất

#### Tab Bảo mật (Readonly)
- Thông tin cấu hình: JWT expiry, rate limit AI, DB collation

#### Backend cần thêm
```
GET /api/v1/admin/ai-logs
GET /api/v1/admin/ai-stats
```

---

## 5. Cấu trúc Frontend

```
src/
├── pages/admin/
│   ├── AdminLayout.jsx
│   ├── AdminDashboard.jsx
│   ├── AdminIngredients.jsx     ← 4 tabs
│   ├── AdminRecipes.jsx
│   ├── AdminUsers.jsx
│   ├── AdminMasterData.jsx      ← 3 tabs
│   └── AdminSettings.jsx        ← 3 tabs
├── components/admin/
│   ├── AdminGuard.jsx
│   ├── StatCard.jsx
│   ├── DataTable.jsx
│   ├── IngredientReviewModal.jsx
│   └── UserDetailDrawer.jsx
└── services/
    └── adminService.js
```

---

## 6. Tổng hợp Backend cần bổ sung

| Endpoint | Module | Trạng thái |
|---|---|---|
| GET /ingredients/pending-review | Nguyên liệu | ❌ Cần thêm |
| GET /admin/stats | Dashboard | ❌ Cần thêm |
| GET /admin/users | Users | ❌ Cần thêm |
| GET /admin/users/{id} | Users | ❌ Cần thêm |
| PATCH /admin/users/{id}/role | Users | ❌ Cần thêm |
| DELETE /admin/users/{id} | Users | ❌ Cần thêm |
| GET /admin/recipes | Recipes | ❌ Cần thêm |
| PATCH /admin/recipes/{id}/status | Recipes | ❌ Cần thêm |
| DELETE /admin/recipes/{id} | Recipes | ❌ Cần thêm |
| GET /admin/ai-logs | AI Logs | ❌ Cần thêm |
| GET /admin/ai-stats | AI Logs | ❌ Cần thêm |
| CRUD Ingredients (4 endpoints) | Nguyên liệu | ✅ Đã có |
| CRUD Aisles (3 endpoints) | Master Data | ✅ Đã có |
| CRUD UnitConversions (3 endpoints) | Master Data | ✅ Đã có |
| GET/POST Tags | Master Data | ✅ Đã có |

---

## 7. Thứ tự triển khai

| Bước | Việc | Ưu tiên |
|---|---|---|
| 1 | GET /ingredients/pending-review (backend) | 🔴 Cao |
| 2 | GET /admin/stats (backend) | 🔴 Cao |
| 3 | AdminLayout + AdminGuard + Routing (frontend) | 🔴 Cao |
| 4 | AdminIngredients.jsx — 4 tabs (frontend) | 🔴 Cao |
| 5 | AdminDashboard.jsx — 2 KPI rows + charts (frontend) | 🟡 Trung bình |
| 6 | AdminMasterData.jsx — Aisles + Tags + Units (frontend) | 🟡 Trung bình |
| 7 | AdminUserController (backend) + AdminUsers.jsx (frontend) | 🟡 Trung bình |
| 8 | AdminRecipeController (backend) + AdminRecipes.jsx (frontend) | 🟡 Trung bình |
| 9 | AI Logs backend + AdminSettings.jsx (frontend) | 🟢 Thấp |

> **MVP Admin (Bước 1-4):** 2 backend endpoint + 2 frontend file = Admin hoạt động thực sự.

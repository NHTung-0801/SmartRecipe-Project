# 🛒 KẾ HOẠCH TRIỂN KHAI GROCERY — SPRINT 4

> **Trạng thái hiện tại:** Đã hoàn thành triển khai. Tất cả các file Backend và Frontend đều đã được code và tích hợp thành công. Đang trong quá trình viết Unit Test.

---

## 📊 TÌNH TRẠNG HIỆN TẠI

### ✅ ĐÃ CÓ (7 file)

| # | File | Đường dẫn |
|---|------|-----------|
| 1 | `GroceryList.java` (Entity) | `smartrecipe-backend/.../entity/GroceryList.java` |
| 2 | `GroceryItem.java` (Entity) | `smartrecipe-backend/.../entity/GroceryItem.java` |
| 3 | `GroceryListRecipe.java` (Entity) | `smartrecipe-backend/.../entity/GroceryListRecipe.java` |
| 4 | `GroceryListStatus.java` (Enum) | `smartrecipe-backend/.../enums/GroceryListStatus.java` |
| 5 | `GroceryListRequest.java` (DTO) | `smartrecipe-backend/.../dto/request/GroceryListRequest.java` |
| 6 | `GroceryItemRequest.java` (DTO) | `smartrecipe-backend/.../dto/request/GroceryItemRequest.java` |
| 7 | `CompleteGroceryRequest.java` (DTO) | `smartrecipe-backend/.../dto/request/CompleteGroceryRequest.java` |
| 8 | `GroceryListResponse.java` (DTO) | `smartrecipe-backend/.../dto/response/GroceryListResponse.java` |
| 9 | `GroceryItemResponse.java` (DTO) | `smartrecipe-backend/.../dto/response/GroceryItemResponse.java` |
| 10 | `GroceryListRepository.java` | `smartrecipe-backend/.../repository/GroceryListRepository.java` |
| 11 | `GroceryItemRepository.java` | `smartrecipe-backend/.../repository/GroceryItemRepository.java` |
| 12 | `GroceryServiceImpl.java` | `smartrecipe-backend/.../service/impl/GroceryServiceImpl.java` |

### ❌ CÒN THIẾU (14 file)

#### Backend (3 file)
| # | File | Đường dẫn |
|---|------|-----------|
| 13 | `GroceryListRecipeRepository.java` | `smartrecipe-backend/.../repository/GroceryListRecipeRepository.java` |
| 14 | `GroceryService.java` (Interface) | `smartrecipe-backend/.../service/GroceryService.java` |
| 15 | `GroceryController.java` | `smartrecipe-backend/.../controller/GroceryController.java` |

#### Frontend (7 file mới)
| # | File | Đường dẫn |
|---|------|-----------|
| 16 | `groceryService.js` | `smartrecipe-frontend/src/services/groceryService.js` |
| 17 | `AisleGroupHeader.jsx` | `smartrecipe-frontend/src/components/grocery/AisleGroupHeader.jsx` |
| 18 | `GroceryItemRow.jsx` | `smartrecipe-frontend/src/components/grocery/GroceryItemRow.jsx` |
| 19 | `AddGroceryItemModal.jsx` | `smartrecipe-frontend/src/components/grocery/AddGroceryItemModal.jsx` |
| 20 | `CompleteConfetti.jsx` | `smartrecipe-frontend/src/components/grocery/CompleteConfetti.jsx` |
| 21 | `GroceryPage.jsx` | `smartrecipe-frontend/src/pages/GroceryPage.jsx` |
| 22 | `GroceryPage.module.css` | `smartrecipe-frontend/src/styles/pages/GroceryPage.module.css` |

#### Tích hợp (4 file sửa)
| # | File | Hành động |
|---|------|-----------|
| 23 | `App.jsx` | Thêm route `/grocery` |
| 24 | `Navbar.jsx` | Thêm link "🛒 Đi chợ" |
| 25 | `PantryPage.jsx` | Thêm nút "Tạo danh sách đi chợ" |
| 26 | `RecipeDetailPage.jsx` | Thêm nút "Thêm vào danh sách đi chợ" |

---

## 🎯 THỨ TỰ TRIỂN KHAI (5 bước)

```
BƯỚC 1: BACKEND — 3 file
  ├── 1.1 GroceryListRecipeRepository.java
  ├── 1.2 GroceryService.java (Interface)
  └── 1.3 GroceryController.java (10 endpoint)

BƯỚC 2: FRONTEND SERVICE — 1 file
  └── 2.1 groceryService.js

BƯỚC 3: FRONTEND COMPONENTS — 4 file
  ├── 3.1 AisleGroupHeader.jsx
  ├── 3.2 GroceryItemRow.jsx
  ├── 3.3 AddGroceryItemModal.jsx
  └── 3.4 CompleteConfetti.jsx

BƯỚC 4: FRONTEND PAGE + CSS — 2 file
  ├── 4.1 GroceryPage.jsx
  └── 4.2 GroceryPage.module.css

BƯỚC 5: TÍCH HỢP — 4 file sửa
  ├── 5.1 App.jsx (+ route /grocery)
  ├── 5.2 Navbar.jsx (+ link Đi chợ)
  ├── 5.3 PantryPage.jsx (+ nút Tạo danh sách đi chợ)
  └── 5.4 RecipeDetailPage.jsx (+ nút Thêm vào danh sách đi chợ)
```

---

## 📋 CHI TIẾT TỪNG BƯỚC

### BƯỚC 1: BACKEND — 3 file

#### 1.1 GroceryListRecipeRepository.java

```
Đường dẫn: smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/
           repository/GroceryListRecipeRepository.java

extends JpaRepository<GroceryListRecipe, Long>

Methods:
  - findByGroceryListId(Long groceryListId) → List<GroceryListRecipe>
  - deleteByGroceryListId(Long groceryListId) → void
```

#### 1.2 GroceryService.java (Interface)

```
Đường dẫn: smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/
           service/GroceryService.java

Methods (khớp với GroceryServiceImpl):
  - createList(Long userId, GroceryListRequest req) → GroceryListResponse
  - getMyLists(Long userId) → List<GroceryListResponse>
  - getList(Long userId, Long listId) → GroceryListResponse
  - deleteList(Long userId, Long listId) → void
  - addItem(Long userId, Long listId, GroceryItemRequest req) → GroceryItemResponse
  - updateItem(Long userId, Long listId, Long itemId, GroceryItemRequest req) → GroceryItemResponse
  - removeItem(Long userId, Long listId, Long itemId) → void
  - togglePurchased(Long userId, Long listId, Long itemId) → GroceryItemResponse
  - completeList(Long userId, Long listId, CompleteGroceryRequest req) → GroceryListResponse
  - generateFromRecipe(Long userId, Long recipeId, Integer servings) → GroceryListResponse
  - generateFromPantry(Long userId) → GroceryListResponse
```

#### 1.3 GroceryController.java

```
Đường dẫn: smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/
           controller/GroceryController.java

@RestController
@RequestMapping("/api/v1/grocery")

10 Endpoints:
  GET    /lists                              → getAllLists(Principal)
  GET    /lists/active                       → getActiveList(Principal)
  POST   /lists                              → createList(Principal, @Valid @RequestBody GroceryListRequest)
  GET    /lists/{id}                         → getListById(Principal, @PathVariable Long id)
  DELETE /lists/{id}                         → deleteList(Principal, @PathVariable Long id)
  POST   /lists/{id}/items                   → addItem(Principal, @PathVariable Long id, @Valid @RequestBody GroceryItemRequest)
  PUT    /items/{itemId}                     → updateItem(Principal, @PathVariable Long itemId, @Valid @RequestBody GroceryItemRequest)
  DELETE /items/{itemId}                     → removeItem(Principal, @PathVariable Long itemId)
  PATCH  /items/{itemId}/toggle              → togglePurchased(Principal, @PathVariable Long itemId)
  POST   /lists/{id}/complete               → completeList(Principal, @PathVariable Long id, @RequestBody CompleteGroceryRequest)
  POST   /lists/generate-from-pantry        → generateFromPantry(Principal)
  POST   /lists/generate-from-recipe/{recipeId} → generateFromRecipe(Principal, @PathVariable Long recipeId, @RequestParam(defaultValue="1") int servings)
```

---

### BƯỚC 2: FRONTEND SERVICE — groceryService.js

```
Đường dẫn: smartrecipe-frontend/src/services/groceryService.js

Sử dụng axios instance có sẵn (giống pantryService.js)

API calls:
  - getAllLists()                    → GET /api/v1/grocery/lists
  - getActiveList()                  → GET /api/v1/grocery/lists/active
  - createList(data)                 → POST /api/v1/grocery/lists
  - getList(id)                      → GET /api/v1/grocery/lists/{id}
  - deleteList(id)                   → DELETE /api/v1/grocery/lists/{id}
  - addItem(listId, data)            → POST /api/v1/grocery/lists/{listId}/items
  - updateItem(itemId, data)         → PUT /api/v1/grocery/items/{itemId}
  - removeItem(itemId)               → DELETE /api/v1/grocery/items/{itemId}
  - togglePurchased(itemId)          → PATCH /api/v1/grocery/items/{itemId}/toggle
  - completeList(listId, addToPantry) → POST /api/v1/grocery/lists/{listId}/complete
  - generateFromPantry()             → POST /api/v1/grocery/lists/generate-from-pantry
  - generateFromRecipe(recipeId, servings) → POST /api/v1/grocery/lists/generate-from-recipe/{recipeId}?servings={servings}
```

---

### BƯỚC 3: FRONTEND COMPONENTS — 4 file

#### 3.1 AisleGroupHeader.jsx

```
Props: aisleName (string)
Hiển thị: header nhóm gian hàng với icon và tên
  - 🥩 Thịt, cá
  - 🥬 Rau, củ, quả
  - 🍚 Đồ khô
  - 🧂 Gia vị
  - v.v...
```

#### 3.2 GroceryItemRow.jsx

```
Props: item (GroceryItemResponse), onToggle(), onEdit(), onRemove()
Hiển thị:
  - Checkbox (đã mua / chưa mua)
  - Tên nguyên liệu (gạch ngang nếu isBought = true)
  - Số lượng cần mua (finalToBuy + unit)
  - Badge Aisle (nhỏ, màu pastel)
  - Nút sửa (icon bút chì)
  - Nút xóa (icon thùng rác)
```

#### 3.3 AddGroceryItemModal.jsx

```
Props: isOpen, onClose, onSubmit(ingredientId, quantity, unit), listId
Hiển thị:
  - Modal với overlay
  - IngredientAutocomplete (chọn nguyên liệu)
  - Input số lượng (quantity)
  - Select đơn vị (unit) — lấy từ ingredient.baseUnit
  - Nút "Thêm" / "Hủy"
  - Xử lý loading state khi submit
```

#### 3.4 CompleteConfetti.jsx

```
Props: isActive (boolean)
Hiển thị: Hiệu ứng confetti khi hoàn thành danh sách
  - Sử dụng canvas-confetti hoặc CSS animation
  - Tự động tắt sau 3-5 giây
```

---

### BƯỚC 4: FRONTEND PAGE + CSS

#### 4.1 GroceryPage.jsx

```
Trang chính quản lý danh sách đi chợ:

State:
  - activeList (GroceryListResponse | null)
  - historyLists (GroceryListResponse[])
  - activeTab: 'ACTIVE' | 'HISTORY'
  - showAddItemModal: boolean
  - showCompleteConfetti: boolean

Layout:
  ┌─────────────────────────────────────────────┐
  │ 🛒 Đi chợ thông minh                        │
  │ [Tạo danh sách mới] [Tạo từ Tủ lạnh]        │
  ├─────────────────────────────────────────────┤
  │ Tab: [Đang hoạt động] [Lịch sử]             │
  ├─────────────────────────────────────────────┤
  │ (nếu ACTIVE)                                │
  │ ┌─ 🥩 Thịt, cá ─────────────────────────┐  │
  │ │ ☐ Thịt heo    500g     [✏️] [🗑️]     │  │
  │ │ ☑ Cá hồi      300g     [✏️] [🗑️]     │  │
  │ └────────────────────────────────────────┘  │
  │ ┌─ 🥬 Rau củ ───────────────────────────┐  │
  │ │ ☐ Cà rốt      200g     [✏️] [🗑️]     │  │
  │ └────────────────────────────────────────┘  │
  │                                             │
  │ [+ Thêm nguyên liệu]                        │
  │                                             │
  │ [Hoàn tất & Cập nhật Tủ lạnh] 🎉           │
  ├─────────────────────────────────────────────┤
  │ (nếu HISTORY)                               │
  │ Danh sách các list đã hoàn thành            │
  │ ┌──────────────────────────────────────┐    │
  │ │ 📋 Đi chợ ngày 10/08 - 5/8 món đã mua│    │
  │ └──────────────────────────────────────┘    │
  └─────────────────────────────────────────────┘

Empty state:
  Khi chưa có danh sách: hình minh họa + "Chưa có danh sách đi chợ nào"
  Nút "Tạo danh sách mới" và "Tạo từ Tủ lạnh" nổi bật

Skeleton loader khi đang load dữ liệu
```

#### 4.2 GroceryPage.module.css

```
Styles:
  - .pageContainer: full height, padding
  - .header: flex, title + action buttons
  - .tabs: tab navigation
  - .aisleGroup: mỗi nhóm gian hàng
  - .aisleHeader: tên gian hàng, sticky
  - .itemRow: flex row, checkbox + info + actions
  - .itemRowPurchased: gạch ngang, opacity giảm
  - .emptyState: căn giữa, icon lớn, text
  - .skeleton: animation loading
  - .confirmButton: nút xanh lớn "Hoàn tất"
  - Responsive: mobile friendly
```

---

### BƯỚC 5: TÍCH HỢP — 4 file sửa

#### 5.1 App.jsx

```diff
+ import GroceryPage from './pages/GroceryPage';

+ <Route
+   path="/grocery"
+   element={
+     <ProtectedRoute>
+       <AppLayout>
+         <GroceryPage />
+       </AppLayout>
+     </ProtectedRoute>
+   }
+ />
```

#### 5.2 Navbar.jsx

```diff
+ <Link
+   to="/grocery"
+   className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
+     isActive('/grocery')
+       ? 'bg-emerald-50 text-emerald-600'
+       : 'text-gray-600 hover:bg-gray-100'
+   }`}
+ >
+   🛒 <span className="hidden sm:inline">Đi chợ</span>
+ </Link>
```

#### 5.3 PantryPage.jsx

```diff
Trong ExpiryAlertBanner hoặc header:
+ Nút "Tạo danh sách đi chợ" → gọi groceryService.generateFromPantry() → navigate('/grocery')
```

#### 5.4 RecipeDetailPage.jsx

```diff
Trong phần header của công thức:
+ <button onClick={handleAddToGrocery}>
+   🛒 Thêm vào danh sách đi chợ
+ </button>
+ → gọi groceryService.generateFromRecipe(recipeId, servings) → navigate('/grocery')
```

---

## 📊 TỔNG KẾT

| Bước | Số file | Loại |
|:----:|:-------:|------|
| 1 | 3 | Backend (Repository, Service Interface, Controller) |
| 2 | 1 | Frontend Service |
| 3 | 4 | Frontend Components |
| 4 | 2 | Frontend Page + CSS |
| 5 | 4 | Tích hợp (sửa file có sẵn) |
| **Tổng** | **14** | **10 file mới + 4 file sửa** |

---

## 🎯 TIÊU CHÍ NGHIỆM THU

- [x] API tạo danh sách đi chợ hoạt động (POST /api/v1/grocery/lists)
- [x] API thêm item vào danh sách (POST /api/v1/grocery/lists/{id}/items) — tự động trừ Pantry
- [x] API toggle purchased (PATCH /api/v1/grocery/items/{id}/toggle)
- [x] API complete list + cập nhật Pantry (POST /api/v1/grocery/lists/{id}/complete)
- [x] API generate from recipe (POST /api/v1/grocery/lists/generate-from-recipe/{id})
- [x] API generate from pantry (POST /api/v1/grocery/lists/generate-from-pantry)
- [x] Frontend: Hiển thị danh sách items nhóm theo Aisle
- [x] Frontend: Checkbox đánh dấu đã mua, item bị gạch ngang
- [x] Frontend: Hiệu ứng confetti khi hoàn thành
- [x] Frontend: Nút "Tạo danh sách đi chợ" từ PantryPage
- [x] Frontend: Nút "Thêm vào danh sách đi chợ" từ RecipeDetailPage
- [x] Navbar có link "Đi chợ", App.jsx có route /grocery
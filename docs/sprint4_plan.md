# 🚀 SPRINT 4 — KẾ HOẠCH CHI TIẾT (ĐÃ CẬP NHẬT)

> **Ngày soạn:** 08/04/2026 — **Cập nhật:** 10/08/2026
> **Tổng thời gian dự kiến:** 3-4 tuần
> **Trạng thái hiện tại:** Pantry MVP đã hoàn thiện theo mô hình lot + base unit; Grocery chưa triển khai. Bộ 9 test nghiệp vụ Pantry/đơn vị đang chạy xanh.

---

## 📊 MỤC TIÊU SPRINT 4

Hoàn thiện 2 module cốt lõi giúp hệ thống trở nên "thông minh":

| # | Module | Mức độ ưu tiên | Mô tả |
|---|--------|---------------|-------|
| 1 | **Pantry (Tủ lạnh ảo)** | 🔴 CAO | Quản lý nguyên liệu tồn kho, cảnh báo hết hạn trong app, phân nhóm theo Aisle |
| 2 | **Grocery (Đi chợ thông minh)** | 🟡 TRUNG BÌNH | Danh sách đi chợ, gộp nhóm theo gian hàng, đồng bộ với Pantry |

---

## ✅ CẬP NHẬT KIẾN TRÚC PANTRY (PHƯƠNG ÁN C)

Thiết kế cũ “mỗi ingredient một dòng” đã được thay bằng mô hình **lot + base unit**:

- Mỗi `UserPantry` là một lot theo `userId + ingredientId + expiryDate`.
- Hai lot chỉ merge khi cùng ingredient và cùng expiry; khác expiry phải giữ riêng để hỗ trợ FEFO.
- Request nhận thêm `unit`; backend quy đổi `quantityAvailable` và `lowStockThreshold` về `Ingredient.baseUnit` trước khi lưu.
- `PUT/DELETE` luôn tra theo cả `pantryId + userId`; user khác nhận `404` và không thể sửa/xóa lot.
- API list trả lot-level, frontend không merge theo tên hoặc tự chọn expiry đại diện.
- Chi tiết quyết định nghiệp vụ và tiêu chí nghiệm thu: `pantry_plan_option_c.md`.

## ⚠️ LƯU Ý: Entity đã có sẵn — KHÔNG tạo lại Entity

Các Entity sau đã có trong codebase, chỉ cần **bổ sung 1 field** cho `UserPantry`:

| Entity | File | Trạng thái | Hành động |
|--------|------|:--:|-----------|
| `UserPantry` | `entity/UserPantry.java` | ✅ Có | **Sửa:** thêm `expiryDate` (LocalDate, nullable) |
| `GroceryList` | `entity/GroceryList.java` | ✅ Có | Giữ nguyên |
| `GroceryItem` | `entity/GroceryItem.java` | ✅ Có | Giữ nguyên |
| `GroceryListRecipe` | `entity/GroceryListRecipe.java` | ✅ Có | Giữ nguyên |
| `GroceryListStatus` | `enum/GroceryListStatus.java` | ✅ Có | Giữ nguyên (`ACTIVE`, `COMPLETED`) |

---

## 🗂️ PHẦN 1: PANTRY — TỦ LẠNH ẢO

### 1.1 Entity hiện tại & Thay đổi

#### UserPantry.java (hiện tại → sau khi sửa)

```java
@Entity
@Table(name = "user_pantry", indexes = {
    @Index(name = "idx_pantry_user_ingredient_expiry",
           columnList = "user_id,ingredient_id,expiry_date")
})
public class UserPantry {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ingredient_id", nullable = false)
    private Ingredient ingredient;

    @Column(name = "quantity_available", nullable = false, precision = 10, scale = 2)
    private BigDecimal quantityAvailable;

    @Column(name = "low_stock_threshold", precision = 10, scale = 2)
    private BigDecimal lowStockThreshold;

    // 🆕 THÊM MỚI:
    @Column(name = "expiry_date")
    private LocalDate expiryDate;  // NULL = không có hạn sử dụng (vd: gạo, muối, đường)
}
```

#### Cập nhật SQL (`init_database.sql`)

```sql
-- Bảng user_pantry: thêm 1 cột
ALTER TABLE `user_pantry` ADD COLUMN `expiry_date` DATE NULL AFTER `low_stock_threshold`;
```

> **Giải thích thiết kế hiện hành:**
> - Không còn unique `(user_id, ingredient_id)`; dùng index `(user_id, ingredient_id, expiry_date)` để cho phép nhiều lot.
> - `expiry_date`: NULL là lot không có hạn sử dụng và chỉ merge với lot NULL cùng ingredient.
> - Quantity/threshold được lưu theo `Ingredient.baseUnit`; trạng thái hết hạn được tính động khi trả DTO.

### 1.2 Logic cảnh báo ngày hết hạn (trong app)

#### Phân loại trạng thái (tính động, không lưu DB)

| Trạng thái | Điều kiện | Badge UI | Hành vi |
|------------|-----------|----------|---------|
| **FRESH** | `expiryDate == null` hoặc `còn > 7 ngày` | 🟢 Xanh lá | Bình thường |
| **EXPIRING_SOON** | `expiryDate` trong vòng **1-7 ngày** tới | 🟡 Vàng ⚠️ | Hiện banner cảnh báo vàng |
| **EXPIRED** | `expiryDate < hôm nay` | 🔴 Đỏ ❌ | Hiện banner cảnh báo đỏ |

#### Công thức tính trong PantryResponse

```java
// daysUntilExpiry: số ngày còn lại đến hạn
// null nếu expiryDate == null
// âm nếu đã hết hạn
public Long getDaysUntilExpiry() {
    if (expiryDate == null) return null;
    return ChronoUnit.DAYS.between(LocalDate.now(), expiryDate);
}

public String getStatus() {
    if (expiryDate == null) return "FRESH";
    long days = getDaysUntilExpiry();
    if (days < 0) return "EXPIRED";
    if (days <= 7) return "EXPIRING_SOON";
    return "FRESH";
}
```

#### Thông báo trong app — cách hiển thị

Khi người dùng mở trang PantryPage:

1. **ExpiryAlertBanner** (component riêng) — hiện ở đầu trang:
   ```
   ┌─────────────────────────────────────────────────────────┐
   │ ⚠️ Tủ lạnh của bạn cần chú ý!                            │
   │ 🔴 2 nguyên liệu đã hết hạn  •  🟡 3 nguyên liệu sắp hết │
   │ [Dọn tủ ngay]  [Tạo danh sách đi chợ]                    │
   └─────────────────────────────────────────────────────────┘
   ```
   - Nếu `expiredCount > 0`: banner nền đỏ nhạt
   - Nếu chỉ có `expiringSoonCount > 0`: banner nền vàng nhạt
   - Nếu không có gì: **ẩn hoàn toàn**

2. **PantryItemCard** — badge trạng thái trên từng item:
   - 🔴 "Đã hết hạn X ngày" — nền đỏ nhạt
   - 🟡 "Còn X ngày" — nền vàng nhạt
   - 🟢 "Còn tươi" — nền xanh nhạt (hoặc không badge)

3. **Sắp xếp trong PantryGrid** (mỗi nhóm Aisle):
   1. EXPIRED (đỏ) → đầu tiên
   2. EXPIRING_SOON (vàng) → thứ hai
   3. LOW_STOCK (dưới `lowStockThreshold`) → thứ ba
   4. FRESH (xanh) → cuối cùng

### 1.3 DTO

| DTO | Mục đích | Fields |
|-----|----------|--------|
| `PantryRequest.java` | Request thêm/sửa | `ingredientId`, `quantityAvailable`, `unit`, `lowStockThreshold`, `expiryDate` |
| `PantryResponse.java` | Response chi tiết | `id`, `ingredient` (IngredientResponse), `quantityAvailable`, `lowStockThreshold`, `expiryDate`, `daysUntilExpiry`, `status`, `aisleName` |
| `PantrySummaryResponse.java` | Tổng quan | `totalItems`, `expiringSoonCount`, `expiredCount`, `lowStockCount`, `freshCount` |

### 1.4 Repository

#### `PantryRepository.java`

```java
@Repository
public interface PantryRepository extends JpaRepository<UserPantry, Long> {
    
    // Lấy toàn bộ tủ của user, sắp xếp theo Aisle/ngày hết hạn
    @EntityGraph(attributePaths = {"ingredient", "ingredient.aisle"})
    List<UserPantry> findByUserIdOrderByIngredient_Aisle_NameAscExpiryDateAsc(Long userId);
    
    // Ownership và thao tác đúng lot
    Optional<UserPantry> findByIdAndUserId(Long id, Long userId);

    // Tìm lot cùng ingredient + expiry để merge
    Optional<UserPantry> findByUserIdAndIngredientIdAndExpiryDate(
        Long userId, Long ingredientId, LocalDate expiryDate);
    Optional<UserPantry> findByUserIdAndIngredientIdAndExpiryDateIsNull(
        Long userId, Long ingredientId);
    
    // Tìm nguyên liệu sắp hết hạn (trong vòng N ngày tới)
    @EntityGraph(attributePaths = {"ingredient", "ingredient.aisle"})
    List<UserPantry> findByUserIdAndExpiryDateBetween(Long userId, LocalDate start, LocalDate end);
    
    // Tìm nguyên liệu đã hết hạn
    List<UserPantry> findByUserIdAndExpiryDateBefore(Long userId, LocalDate date);
    
    // Đếm tổng số loại nguyên liệu trong tủ
    long countByUserId(Long userId);
    
    // Đếm số nguyên liệu sắp hết hạn (trong khoảng ngày)
    long countByUserIdAndExpiryDateBetween(Long userId, LocalDate start, LocalDate end);
    
    // Đếm số nguyên liệu đã hết hạn
    long countByUserIdAndExpiryDateBefore(Long userId, LocalDate date);
    
    // Xóa nguyên liệu đã hết hạn
    void deleteByUserIdAndExpiryDateBefore(Long userId, LocalDate date);
    
    // Đếm số nguyên liệu dưới ngưỡng
    @Query("SELECT COUNT(p) FROM UserPantry p WHERE p.user.id = :userId AND p.lowStockThreshold IS NOT NULL AND p.quantityAvailable <= p.lowStockThreshold")
    long countLowStockByUserId(@Param("userId") Long userId);
}
```

### 1.5 Service

#### `PantryService.java` + `PantryServiceImpl.java`

| Phương thức | Mô tả |
|-------------|-------|
| `addOrUpdateItem(Long userId, PantryRequest req)` | Chuẩn hóa unit; cộng dồn nếu cùng ingredient + expiry, nếu khác expiry tạo lot mới. |
| `updateItem(Long userId, Long pantryId, PantryRequest req)` | Cập nhật tuyệt đối đúng lot thuộc user; nếu đổi expiry trùng lot khác thì merge. |
| `removeItem(Long userId, Long pantryId)` | Xóa đúng lot thuộc user; user khác nhận 404. |
| `getMyPantry(Long userId, String filter)` | Lấy danh sách: ALL / EXPIRING_SOON / EXPIRED / LOW_STOCK. Nhóm theo Aisle. |
| `getExpiringSoon(Long userId, int days)` | Lấy danh sách sắp hết hạn trong `days` ngày tới. |
| `deleteAllExpired(Long userId)` | Xóa toàn bộ nguyên liệu đã hết hạn. |
| `getPantrySummary(Long userId)` | Tổng số loại, số sắp hết hạn, số đã hết hạn, số dưới ngưỡng. |

#### Logic quan trọng:

1. **Cộng dồn nguyên liệu (Merge):**
   - Chỉ cộng khi cùng `userId + ingredientId + expiryDate` sau khi chuẩn hóa quantity về base unit.
   - Khác expiry (kể cả `null`) là hai lot độc lập; không dùng MIN expiry để nhập chung.
   - `lowStockThreshold` được hiểu theo base unit và áp dụng nhất quán cho các lot cùng ingredient.

2. **Tính trạng thái tự động** (trong Service/Response, không lưu DB):
   - `EXPIRED`: `expiryDate < LocalDate.now()`
   - `EXPIRING_SOON`: `expiryDate` trong vòng 7 ngày tới
   - `FRESH`: còn lại hoặc `expiryDate == null`

3. **Nhóm theo Aisle:**
   ```java
   Map<String, List<PantryResponse>> groupedByAisle = pantries.stream()
       .collect(Collectors.groupingBy(
           p -> p.getIngredient().getAisle().getName(),
           LinkedHashMap::new,
           Collectors.mapping(this::toResponse, Collectors.toList())
       ));
   ```
   Sắp xếp trong mỗi nhóm: EXPIRED → EXPIRING_SOON → LOW_STOCK → FRESH.

### 1.6 Controller

#### `PantryController.java`

```java
@RestController
@RequestMapping("/api/v1/pantry")
public class PantryController {
    
    // GET /api/v1/pantry?filter=ALL|EXPIRING_SOON|EXPIRED|LOW_STOCK
    @GetMapping
    ResponseEntity<Map<String, List<PantryResponse>>> getMyPantry(
        Principal principal,
        @RequestParam(defaultValue = "ALL") String filter);
    
    // POST /api/v1/pantry/items
    @PostMapping("/items")
    ResponseEntity<PantryResponse> addItem(Principal principal, @Valid @RequestBody PantryRequest req);
    
    // PUT /api/v1/pantry/items/{id}
    @PutMapping("/items/{id}")
    ResponseEntity<PantryResponse> updateItem(Principal principal, @PathVariable Long id, @Valid @RequestBody PantryRequest req);
    
    // DELETE /api/v1/pantry/items/{id}
    @DeleteMapping("/items/{id}")
    ResponseEntity<Void> removeItem(Principal principal, @PathVariable Long id);
    
    // GET /api/v1/pantry/expiring-soon?days=7
    @GetMapping("/expiring-soon")
    ResponseEntity<List<PantryResponse>> getExpiringSoon(Principal principal, @RequestParam(defaultValue = "7") int days);
    
    // DELETE /api/v1/pantry/expired
    @DeleteMapping("/expired")
    ResponseEntity<Void> deleteAllExpired(Principal principal);
    
    // GET /api/v1/pantry/summary
    @GetMapping("/summary")
    ResponseEntity<PantrySummaryResponse> getSummary(Principal principal);
}
```

### 1.7 Frontend

| File | Mô tả |
|------|-------|
| `src/services/pantryService.js` | API calls: `getPantry(filter)`, `addItem(data)`, `updateItem(id, data)`, `removeItem(id)`, `getExpiringSoon(days)`, `deleteAllExpired()`, `getSummary()` |
| `src/pages/PantryPage.jsx` | Trang chính: SummaryBar + ExpiryAlertBanner + PantryGrid + Empty state |
| `src/components/pantry/PantrySummaryBar.jsx` | Thanh thống kê: tổng, sắp hết hạn, đã hết hạn, dưới ngưỡng |
| `src/components/pantry/ExpiryAlertBanner.jsx` | Banner cảnh báo khi có item hết hạn/sắp hết hạn (trong app) |
| `src/components/pantry/PantryGrid.jsx` | Grid nhóm theo Aisle, mỗi nhóm có header tên Aisle |
| `src/components/pantry/PantryItemCard.jsx` | Card 1 nguyên liệu: tên, số lượng, ngày hết hạn, badge trạng thái, nút sửa/xóa |
| `src/components/pantry/AddPantryItemModal.jsx` | Modal thêm/sửa: chọn Ingredient (Autocomplete), số lượng, ngưỡng thấp, ngày hết hạn (date picker) |
| `src/styles/pages/PantryPage.module.css` | CSS cho toàn bộ PantryPage |

#### Yêu cầu UI:
- Giao diện chia theo nhóm / quầy (Aisle): Thịt cá, Rau củ, Đồ khô, Gia vị.
- Cảnh báo trong app: Banner vàng/đỏ ở đầu trang khi có item cần chú ý.
- Badge trạng thái trên từng card: 🟢 FRESH / 🟡 EXPIRING_SOON / 🔴 EXPIRED.
- Ô "Quick Add": Gõ nhanh tên nguyên liệu (tích hợp `IngredientAutocomplete`).
- Empty state: Hình minh họa khi tủ lạnh trống.
- Skeleton loader khi đang load dữ liệu.

---

## 🛒 PHẦN 2: GROCERY — ĐI CHỢ THÔNG MINH

### 2.1 Entity hiện tại (giữ nguyên)

#### GroceryList.java
```java
@Entity
@Table(name = "grocery_lists")
public class GroceryList {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private GroceryListStatus status;  // ACTIVE, COMPLETED

    @Column(length = 100)
    private String name;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "completed_at")
    private LocalDateTime completedAt;
}
```

#### GroceryItem.java
```java
@Entity
@Table(name = "grocery_items")
public class GroceryItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "grocery_list_id", nullable = false)
    private GroceryList groceryList;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ingredient_id", nullable = false)
    private Ingredient ingredient;

    @Column(name = "total_needed", nullable = false, precision = 10, scale = 2)
    private BigDecimal totalNeeded;       // Tổng lượng cần cho công thức

    @Column(name = "pantry_deducted", nullable = false, precision = 10, scale = 2)
    private BigDecimal pantryDeducted;    // Lượng đã có sẵn trong tủ

    @Column(name = "final_to_buy", nullable = false, precision = 10, scale = 2)
    private BigDecimal finalToBuy;        // Lượng thực tế cần mua

    @Builder.Default
    @Column(name = "is_bought")
    private Boolean isBought = false;
}
```

#### GroceryListRecipe.java
```java
@Entity
@Table(name = "grocery_list_recipes", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"grocery_list_id", "recipe_id"})
})
public class GroceryListRecipe {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "grocery_list_id", nullable = false)
    private GroceryList groceryList;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "recipe_id", nullable = false)
    private Recipe recipe;

    @Column(nullable = false)
    private Integer servings;
}
```

### 2.2 DTO

| DTO | Mục đích | Fields |
|-----|----------|--------|
| `GroceryListRequest.java` | Tạo/sửa list | `name` |
| `GroceryItemRequest.java` | Thêm/sửa item | `ingredientId`, `totalNeeded`, `pantryDeducted`, `finalToBuy` |
| `GroceryListResponse.java` | Response list | `id`, `name`, `status`, `items[]`, `totalItems`, `purchasedItems`, `createdAt`, `completedAt` |
| `GroceryItemResponse.java` | Response item | `id`, `ingredient` (IngredientResponse), `totalNeeded`, `pantryDeducted`, `finalToBuy`, `isBought`, `aisleName` |

### 2.3 Repository

#### `GroceryListRepository.java`

```java
@Repository
public interface GroceryListRepository extends JpaRepository<GroceryList, Long> {
    List<GroceryList> findByUserIdOrderByCreatedAtDesc(Long userId);
    Optional<GroceryList> findByIdAndUserId(Long id, Long userId);
    
    // Danh sách đang active
    Optional<GroceryList> findByUserIdAndStatus(Long userId, GroceryListStatus status);
    List<GroceryList> findByUserIdAndStatusOrderByCreatedAtDesc(Long userId, GroceryListStatus status);
}
```

#### `GroceryItemRepository.java`

```java
@Repository
public interface GroceryItemRepository extends JpaRepository<GroceryItem, Long> {
    @EntityGraph(attributePaths = {"ingredient", "ingredient.aisle"})
    List<GroceryItem> findByGroceryListIdOrderByIngredient_Aisle_NameAsc(GroceryList groceryList);
    
    Optional<GroceryItem> findByIdAndGroceryListId(Long id, Long groceryListId);
    void deleteByGroceryListId(Long groceryListId);
}
```

### 2.4 Service

#### `GroceryService.java` + `GroceryServiceImpl.java`

| Phương thức | Mô tả |
|-------------|-------|
| `createList(Long userId, GroceryListRequest req)` | Tạo danh sách đi chợ mới (status = ACTIVE). Nếu đã có list ACTIVE → trả về list đó. |
| `getActiveList(Long userId)` | Lấy danh sách đang active (chưa hoàn thành). |
| `getListById(Long userId, Long listId)` | Lấy chi tiết 1 danh sách (kèm items). |
| `getAllLists(Long userId)` | Lấy lịch sử tất cả danh sách. |
| `deleteList(Long userId, Long listId)` | Xóa danh sách. |
| `addItem(Long userId, Long listId, GroceryItemRequest req)` | Thêm item vào list. Tự động set `aisleName` từ Ingredient. |
| `updateItem(Long itemId, GroceryItemRequest req)` | Sửa item. |
| `removeItem(Long itemId)` | Xóa item khỏi list. |
| `togglePurchased(Long itemId)` | Đánh dấu đã mua / bỏ đánh dấu. |
| `completeList(Long userId, Long listId, boolean addToPantry)` | Hoàn thành danh sách. Nếu `addToPantry=true` → cập nhật Pantry. |
| `generateFromPantry(Long userId)` | Tự động sinh danh sách từ tủ lạnh (item sắp hết hạn + dưới ngưỡng). |
| `generateFromRecipe(Long userId, Long recipeId, int servings)` | Tạo danh sách từ công thức, đối chiếu Pantry. |

#### Logic quan trọng:

1. **Tự động sinh từ Pantry:**
   ```
   POST /api/v1/grocery/lists/generate-from-pantry
   
   1. Lấy tất cả item EXPIRED + EXPIRING_SOON + LOW_STOCK từ Pantry
   2. Tạo GroceryList mới tên "Đi chợ từ tủ lạnh - {ngày}"
   3. Với mỗi item:
      - Nếu EXPIRED/EXPIRING_SOON: finalToBuy = quantityAvailable (thay thế)
      - Nếu LOW_STOCK: finalToBuy = lowStockThreshold * 2 - quantityAvailable
      - pantryDeducted = 0 (vì đây là gợi ý, không đối chiếu)
   4. Trả về GroceryListResponse
   ```

2. **Tạo danh sách từ Recipe:**
   ```
   POST /api/v1/grocery/lists/generate-from-recipe/{recipeId}?servings=4
   
   1. Lấy RecipeIngredients của recipe
   2. Nhân quantity với (servings / recipe.baseServings)
   3. Với mỗi RecipeIngredient:
      - totalNeeded = lượng cần sau khi nhân servings
      - Tra Pantry: pantryDeducted = MIN(totalNeeded, quantityAvailable trong tủ)
      - finalToBuy = totalNeeded - pantryDeducted
      - Nếu finalToBuy <= 0 → bỏ qua (đã đủ trong tủ)
   4. Tạo GroceryList mới, thêm GroceryListRecipe để ghi nhận nguồn
   5. Trả về GroceryListResponse
   ```

3. **Complete List → Cập nhật Pantry:**
   ```
   POST /api/v1/grocery/lists/{id}/complete  { "addToPantry": true }
   
   1. FOR EACH item IN list WHERE isBought = TRUE:
        CALL PantryService.addOrUpdateItem(userId, ingredientId, finalToBuy)
   2. SET list.status = COMPLETED, completedAt = NOW()
   3. Trả về GroceryListResponse
   ```

4. **Sắp xếp theo Aisle (Gian hàng):**
   - Khi thêm item, tự động lấy `aisleName` từ `Ingredient.getAisle().getName()`.
   - Trả về danh sách đã sắp xếp `ORDER BY aisleName ASC`.
   - Giúp người dùng đi siêu thị không phải đi vòng vèo.

### 2.5 Controller

#### `GroceryController.java`

```java
@RestController
@RequestMapping("/api/v1/grocery")
public class GroceryController {
    
    // GET /api/v1/grocery/lists
    @GetMapping("/lists")
    ResponseEntity<List<GroceryListResponse>> getAllLists(Principal principal);
    
    // GET /api/v1/grocery/lists/active
    @GetMapping("/lists/active")
    ResponseEntity<GroceryListResponse> getActiveList(Principal principal);
    
    // POST /api/v1/grocery/lists
    @PostMapping("/lists")
    ResponseEntity<GroceryListResponse> createList(Principal principal, @Valid @RequestBody GroceryListRequest req);
    
    // GET /api/v1/grocery/lists/{id}
    @GetMapping("/lists/{id}")
    ResponseEntity<GroceryListResponse> getListById(@PathVariable Long id, Principal principal);
    
    // DELETE /api/v1/grocery/lists/{id}
    @DeleteMapping("/lists/{id}")
    ResponseEntity<Void> deleteList(@PathVariable Long id, Principal principal);
    
    // POST /api/v1/grocery/lists/{id}/items
    @PostMapping("/lists/{id}/items")
    ResponseEntity<GroceryItemResponse> addItem(@PathVariable Long id, Principal principal, @Valid @RequestBody GroceryItemRequest req);
    
    // PUT /api/v1/grocery/items/{itemId}
    @PutMapping("/items/{itemId}")
    ResponseEntity<GroceryItemResponse> updateItem(@PathVariable Long itemId, @Valid @RequestBody GroceryItemRequest req);
    
    // DELETE /api/v1/grocery/items/{itemId}
    @DeleteMapping("/items/{itemId}")
    ResponseEntity<Void> removeItem(@PathVariable Long itemId);
    
    // PATCH /api/v1/grocery/items/{itemId}/toggle
    @PatchMapping("/items/{itemId}/toggle")
    ResponseEntity<GroceryItemResponse> togglePurchased(@PathVariable Long itemId);
    
    // POST /api/v1/grocery/lists/{id}/complete
    @PostMapping("/lists/{id}/complete")
    ResponseEntity<GroceryListResponse> completeList(@PathVariable Long id, Principal principal, @RequestBody CompleteGroceryRequest req);
    
    // POST /api/v1/grocery/lists/generate-from-pantry
    @PostMapping("/lists/generate-from-pantry")
    ResponseEntity<GroceryListResponse> generateFromPantry(Principal principal);
    
    // POST /api/v1/grocery/lists/generate-from-recipe/{recipeId}
    @PostMapping("/lists/generate-from-recipe/{recipeId}")
    ResponseEntity<GroceryListResponse> generateFromRecipe(@PathVariable Long recipeId, Principal principal, @RequestParam(defaultValue = "1") int servings);
}
```

### 2.6 Frontend

| File | Mô tả |
|------|-------|
| `src/services/groceryService.js` | API calls: CRUD list/item, toggle, complete, generate |
| `src/pages/GroceryPage.jsx` | Trang chính: danh sách các GroceryList + form tạo mới + nút "Tạo từ Tủ lạnh" |
| `src/components/grocery/GroceryItemRow.jsx` | Row 1 item: checkbox, tên, finalToBuy, badge Aisle, gạch ngang nếu đã mua |
| `src/components/grocery/AddGroceryItemModal.jsx` | Modal thêm item: chọn Ingredient, nhập số lượng cần |
| `src/components/grocery/CompleteConfetti.jsx` | Hiệu ứng confetti khi hoàn thành danh sách |
| `src/components/grocery/AisleGroupHeader.jsx` | Header nhóm Aisle trong danh sách |
| `src/styles/pages/GroceryPage.module.css` | CSS cho toàn bộ GroceryPage |

#### Yêu cầu UI:
- Giao diện dạng Checklist (To-do list).
- Các nguyên liệu tự động gom nhóm theo quầy hàng (Aisle).
- Nút tick "Đã mua" — item bị gạch ngang khi đã tick.
- Nút "Hoàn tất & Cập nhật Tủ lạnh" kèm hiệu ứng confetti.
- Tích hợp nút "Thêm vào danh sách đi chợ" từ PantryPage và RecipeDetailPage.
- Empty state khi chưa có danh sách nào.

---

## 🔗 DEPENDENCY & MỐI LIÊN KẾT GIỮA CÁC MODULE

```
                    ┌──────────┐
                    │  Recipe  │──── Tạo Grocery List từ Recipe ────┐
                    └──────────┘                                    │
                                                                     ▼
┌──────────┐      ┌──────────┐      ┌──────────────┐      ┌──────────────┐
│  Pantry  │◄─────│  Grocery │      │ Ingredient   │      │    Aisle     │
│ (Tủ lạnh)│      │  (Đi chợ)│      │ (Nguyên liệu)│      │  (Gian hàng) │
└──────────┘      └──────────┘      └──────────────┘      └──────────────┘
      ▲                  │                  ▲                      ▲
      │                  │                  │                      │
      └── Complete List ─┘                  └──────────┬───────────┘
       (tự động cập nhật)                              │
                                             ┌──────────────────┐
                                             │   Ingredient     │
                                             │  (baseUnit)      │
                                             └──────────────────┘
```

**Luồng hoạt động chính:**
1. User mở PantryPage → thấy ExpiryAlertBanner (nếu có item hết hạn/sắp hết hạn)
2. Bấm "Tạo danh sách đi chợ" → hệ thống tự sinh Grocery List từ Pantry
3. Hoặc: User xem Recipe → bấm "Thêm vào danh sách đi chợ" → tạo Grocery List từ Recipe
4. User đi chợ, tick từng món đã mua
5. Bấm "Hoàn tất & Cập nhật Tủ lạnh" → tự động cập nhật Pantry + hiệu ứng confetti

---

## 📋 CHECKLIST TASK CHI TIẾT

### PHASE A: CHUẨN BỊ (Sửa Entity + SQL)
- [ ] A1. Sửa `UserPantry.java` — thêm field `expiryDate` (LocalDate, nullable)
- [ ] A2. Cập nhật `init_database.sql` — thêm cột `expiry_date DATE NULL` vào bảng `user_pantry`

### PHASE B: PANTRY BACKEND
- [ ] B1. Tạo `PantryRequest.java` DTO
- [ ] B2. Tạo `PantryResponse.java` DTO (kèm `daysUntilExpiry`, `status`, `aisleName`)
- [ ] B3. Tạo `PantrySummaryResponse.java` DTO
- [ ] B4. Tạo `PantryRepository` với tất cả query methods
- [ ] B5. Tạo `PantryService` interface
- [ ] B6. Implement `PantryServiceImpl`:
  - [ ] B6a. `addOrUpdateItem` (cộng dồn, cập nhật expiryDate gần nhất)
  - [ ] B6b. `updateItem`
  - [ ] B6c. `removeItem`
  - [ ] B6d. `getMyPantry` (nhóm theo Aisle, filter theo status, sắp xếp)
  - [ ] B6e. `getExpiringSoon`
  - [ ] B6f. `deleteAllExpired`
  - [ ] B6g. `getPantrySummary`
- [ ] B7. Tạo `PantryController`
- [ ] B8. Test tất cả API với Postman

### PHASE C: PANTRY FRONTEND
- [ ] C1. Tạo `src/services/pantryService.js`
- [ ] C2. Tạo `src/pages/PantryPage.jsx` (trang chính)
- [ ] C3. Tạo `src/components/pantry/PantrySummaryBar.jsx`
- [ ] C4. Tạo `src/components/pantry/ExpiryAlertBanner.jsx` (thông báo trong app)
- [ ] C5. Tạo `src/components/pantry/PantryGrid.jsx` (nhóm theo Aisle)
- [ ] C6. Tạo `src/components/pantry/PantryItemCard.jsx`
- [ ] C7. Tạo `src/components/pantry/AddPantryItemModal.jsx`
- [ ] C8. Tạo `src/styles/pages/PantryPage.module.css`

### PHASE D: GROCERY BACKEND
- [ ] D1. Tạo `GroceryListRequest.java` + `GroceryItemRequest.java` DTO
- [ ] D2. Tạo `GroceryListResponse.java` + `GroceryItemResponse.java` DTO
- [ ] D3. Tạo `GroceryListRepository` + `GroceryItemRepository`
- [ ] D4. Tạo `GroceryService` interface
- [ ] D5. Implement `GroceryServiceImpl`:
  - [ ] D5a. `createList` / `getActiveList` / `getListById` / `getAllLists` / `deleteList`
  - [ ] D5b. `addItem` / `updateItem` / `removeItem` / `togglePurchased`
  - [ ] D5c. `completeList` (cập nhật Pantry)
  - [ ] D5d. `generateFromPantry`
  - [ ] D5e. `generateFromRecipe`
- [ ] D6. Tạo `GroceryController`
- [ ] D7. Tạo `CompleteGroceryRequest` DTO (nếu cần thiết)
- [ ] D8. Test tất cả API với Postman

### PHASE E: GROCERY FRONTEND
- [ ] E1. Tạo `src/services/groceryService.js`
- [ ] E2. Tạo `src/pages/GroceryPage.jsx` (trang chính)
- [ ] E3. Tạo `src/components/grocery/AisleGroupHeader.jsx`
- [ ] E4. Tạo `src/components/grocery/GroceryItemRow.jsx`
- [ ] E5. Tạo `src/components/grocery/AddGroceryItemModal.jsx`
- [ ] E6. Tạo `src/components/grocery/CompleteConfetti.jsx`
- [ ] E7. Tạo `src/styles/pages/GroceryPage.module.css`

### PHASE F: TÍCH HỢP & HOÀN THIỆN
- [ ] F1. Cập nhật `App.jsx` — thêm route `/pantry` và `/grocery`
- [ ] F2. Cập nhật `Navbar.jsx` — thêm link "Tủ lạnh" và "Đi chợ" vào menu
- [ ] F3. Tích hợp nút "Thêm vào danh sách đi chợ" trong `RecipeDetailPage.jsx`
- [ ] F4. Tích hợp nút "Tạo danh sách đi chợ" trong `PantryPage.jsx`
- [ ] F5. Test tích hợp end-to-end toàn bộ luồng

---

## 📊 TỔNG KẾT

| Layer | Tạo mới | Sửa | Tổng |
|-------|:--:|:--:|:--:|
| Entity | 0 | 1 (`UserPantry`) | 1 |
| DTO | 7 | 0 | 7 |
| Repository | 3 | 0 | 3 |
| Service | 4 | 0 | 4 |
| Controller | 2 | 0 | 2 |
| Frontend Service | 2 | 0 | 2 |
| Frontend Pages | 2 | 0 | 2 |
| Frontend Components | 7 | 0 | 7 |
| Frontend CSS | 2 | 0 | 2 |
| Config/Route | 0 | 2 (`App.jsx`, `Navbar.jsx`) | 2 |
| Integration | 0 | 2 (`RecipeDetailPage`, `PantryPage`) | 2 |
| Database | 0 | 1 (`init_database.sql`) | 1 |
| **Tổng** | **27** | **6** | **33 file** |

---

## 🎯 THỨ TỰ TRIỂN KHAI

```
Bước 1 (A): Sửa UserPantry (thêm expiryDate) + init_database.sql
Bước 2 (B): Tạo toàn bộ Pantry Backend (DTO → Repo → Service → Controller)
Bước 3 (C): Tạo Pantry Frontend (Service → Components → Page → CSS)
Bước 4 (D): Tạo toàn bộ Grocery Backend (DTO → Repo → Service → Controller)
Bước 5 (E): Tạo Grocery Frontend (Service → Components → Page → CSS)
Bước 6 (F): Tích hợp App.jsx + Navbar.jsx + RecipeDetailPage + PantryPage
```

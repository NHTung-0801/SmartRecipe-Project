# 🐛 KẾ HOẠCH SỬA LỖI - MODULE GROCERY

> **Ngày**: 2026-08-11  
> **Tổng số lỗi**: 11 (6 CRITICAL, 3 MEDIUM, 2 LOW)  
> **Thứ tự thực hiện**: Từ trên xuống dưới, sửa xong từng lỗi → kiểm thử → chuyển lỗi tiếp theo

---

## 📦 PHASE 1: BACKEND (Thêm endpoint + method thiếu)

---

### 🔧 LỖI 11: Kiểm tra enum `GroceryListStatus` đã tồn tại chưa

**Mức độ**: LOW (Blocker nếu thiếu - backend không compile)

**File cần kiểm tra**:
```
smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/enums/GroceryListStatus.java
```

**Nếu chưa tồn tại, tạo file mới:**
```java
package com.smartrecipe.smartrecipe_backend.enums;

public enum GroceryListStatus {
    ACTIVE,
    COMPLETED
}
```

**Verify**: `mvn compile` trong `smartrecipe-backend/` không báo lỗi.

---

### 🔧 LỖI 2 + 3: Thêm `updateList` và `clearItems` vào Backend

**Mức độ**: CRITICAL

#### Bước 1: Thêm vào `GroceryService.java`
**File**: `smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/GroceryService.java`

**Thêm 2 method signature:**
```java
GroceryListResponse updateList(Long userId, Long listId, GroceryListRequest request);
void clearItems(Long userId, Long listId);
```

#### Bước 2: Implement trong `GroceryServiceImpl.java`
**File**: `smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/GroceryServiceImpl.java`

**Thêm 2 method (sau `deleteList`, trước comment `// ---------- ITEM CRUD ----------`):**

```java
@Override
@Transactional
public GroceryListResponse updateList(Long userId, Long listId, GroceryListRequest request) {
    GroceryList list = groceryListRepository.findByIdAndUserId(listId, userId)
            .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy danh sách"));
    if (request.getName() != null && !request.getName().isBlank()) {
        list.setName(request.getName().trim());
    }
    list = groceryListRepository.save(list);
    return toListResponse(list);
}

@Override
@Transactional
public void clearItems(Long userId, Long listId) {
    GroceryList list = groceryListRepository.findByIdAndUserId(listId, userId)
            .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy danh sách"));
    if (list.getStatus() != GroceryListStatus.ACTIVE) {
        throw new BadRequestException("Chỉ có thể xóa trong danh sách đang hoạt động");
    }
    groceryItemRepository.deleteByGroceryListId(listId);
}
```

#### Bước 3: Thêm endpoint vào `GroceryController.java`
**File**: `smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/controller/GroceryController.java`

**Thêm trước dòng `// ---------- ITEM ENDPOINTS ----------`:**

```java
@PutMapping("/lists/{id}")
public ResponseEntity<Map<String, Object>> updateList(
        Principal principal,
        @PathVariable Long id,
        @Valid @RequestBody GroceryListRequest request) {
    GroceryListResponse list = groceryService.updateList(getUserId(principal), id, request);
    return ResponseEntity.ok(Map.of(
            "data", list,
            "message", "Đã cập nhật danh sách"
    ));
}

@DeleteMapping("/lists/{id}/items")
public ResponseEntity<Map<String, Object>> clearItems(
        Principal principal,
        @PathVariable Long id) {
    groceryService.clearItems(getUserId(principal), id);
    return ResponseEntity.ok(Map.of(
            "message", "Đã xóa tất cả nguyên liệu khỏi danh sách"
    ));
}
```

**Verify**: `mvn compile` thành công. Kiểm tra với Postman:
- `PUT http://localhost:8080/api/v1/grocery/lists/{id}` với body `{"name": "Tên mới"}` → trả về `200` + `{ data: {...}, message: "..." }`
- `DELETE http://localhost:8080/api/v1/grocery/lists/{id}/items` → trả về `200` + `{ message: "..." }`

---

## 📦 PHASE 2: FRONTEND SERVICE LAYER

---

### 🔧 LỖI 1 + 2 + 3 + 4 + 5 + 6: Sửa `groceryService.js`

**Mức độ**: CRITICAL  
**File**: `smartrecipe-frontend/src/services/groceryService.js`

**Thay thế TOÀN BỘ nội dung file:**

```js
import api from './api';

export const groceryService = {
  // ---------- LIST ----------
  getAllLists: async () => {
    const response = await api.get('/grocery/lists');
    return response.data.data; // unwrap wrapper
  },

  getActiveList: async () => {
    const response = await api.get('/grocery/lists/active');
    return response.data.data; // unwrap wrapper
  },

  createList: async (data) => {
    const response = await api.post('/grocery/lists', data);
    return response.data.data; // unwrap wrapper
  },

  getList: async (id) => {
    const response = await api.get(`/grocery/lists/${id}`);
    return response.data.data; // unwrap wrapper
  },

  deleteList: async (id) => {
    const response = await api.delete(`/grocery/lists/${id}`);
    return response.data;
  },

  updateList: async (listId, data) => {
    const response = await api.put(`/grocery/lists/${listId}`, data);
    return response.data.data; // unwrap wrapper
  },

  completeList: async (listId, addToPantry = false) => {
    const response = await api.post(`/grocery/lists/${listId}/complete`, { addToPantry });
    return response.data.data; // unwrap wrapper
  },

  clearItems: async (listId) => {
    const response = await api.delete(`/grocery/lists/${listId}/items`);
    return response.data;
  },

  // ---------- ITEM ----------
  addItem: async (listId, data) => {
    const response = await api.post(`/grocery/lists/${listId}/items`, data);
    return response.data.data; // unwrap wrapper
  },

  updateItem: async (itemId, listId, data) => {
    // listId gửi qua query param (theo backend @RequestParam)
    const response = await api.put(`/grocery/items/${itemId}`, data, { params: { listId } });
    return response.data.data; // unwrap wrapper
  },

  removeItem: async (itemId, listId) => {
    const response = await api.delete(`/grocery/items/${itemId}`, { params: { listId } });
    return response.data;
  },

  togglePurchased: async (itemId, listId) => {
    const response = await api.patch(`/grocery/items/${itemId}/toggle`, null, { params: { listId } });
    return response.data.data; // unwrap wrapper
  },

  // ---------- GENERATE ----------
  generateFromPantry: async () => {
    const response = await api.post('/grocery/lists/generate-from-pantry');
    return response.data.data; // unwrap wrapper
  },

  generateFromRecipe: async (recipeId, servings = 1) => {
    const response = await api.post(`/grocery/lists/generate-from-recipe/${recipeId}`, null, {
      params: { servings },
    });
    return response.data.data; // unwrap wrapper
  },
};
```

**Các thay đổi chính:**
| # | Thay đổi | Lý do |
|---|----------|-------|
| 1 | Tất cả method trả về `response.data.data` thay vì `response.data` | Unwrap API wrapper `{ data, message }` |
| 2 | Thêm `updateList(listId, data)` | Lỗi 2 - method bị thiếu |
| 3 | Thêm `clearItems(listId)` | Lỗi 3 - method bị thiếu |
| 4 | `updateItem(itemId, listId, data)` - listId là tham số riêng, gửi qua query param | Lỗi 6 - sai format |
| 5 | `removeItem(itemId, listId)` - giữ nguyên thứ tự (itemId trước) | Đã đúng, chỉ cần component gọi đúng |

---

## 📦 PHASE 3: FRONTEND COMPONENTS

---

### 🔧 LỖI 1 + 2 + 3 + 4 + 5 + 9: Sửa `GroceryPage.jsx`

**Mức độ**: CRITICAL  
**File**: `smartrecipe-frontend/src/pages/GroceryPage.jsx`

#### Sửa 1: Dòng 28-31 - Unwrap response (LỖI 1)
```jsx
// HIỆN TẠI (dòng 28-31):
const data = await groceryService.getActiveList();
setGroceryList(data);
setListName(data.name || 'Danh sách mua sắm');
setItems(data.items || []);

// SỬA THÀNH:
const data = await groceryService.getActiveList();
setGroceryList(data);
setListName(data.name || 'Danh sách mua sắm');
setItems(data.items || []);
// (Không cần đổi vì service đã unwrap, data giờ là object thực)
```

#### Sửa 2: Dòng 37 - Unwrap createList response (LỖI 1)
```jsx
// HIỆN TẠI (dòng 37):
const newList = await groceryService.createList({ name: 'Danh sách mua sắm của tôi' });

// SỬA THÀNH:
const newList = await groceryService.createList({ name: 'Danh sách mua sắm của tôi' });
// (Không cần đổi vì service đã unwrap)
```

#### Sửa 3: Dòng 75-77 - toggleItem → togglePurchased (LỖI 4)
```jsx
// HIỆN TẠI (dòng 75-77):
const handleToggleItem = async (item) => {
  try {
    await groceryService.toggleItem(groceryList.id, item.id);

// SỬA THÀNH:
const handleToggleItem = async (item) => {
  try {
    await groceryService.togglePurchased(item.id, groceryList.id);
```

#### Sửa 4: Dòng 100-101 - updateItem tham số (LỖI 6 + 9)
```jsx
// HIỆN TẠI (dòng 100-101):
const handleEditSubmit = async (data) => {
  await groceryService.updateItem(groceryList.id, editingItem.id, data);

// SỬA THÀNH:
const handleEditSubmit = async (data) => {
  await groceryService.updateItem(editingItem.id, groceryList.id, data);
```

#### Sửa 5: Dòng 107-109 - removeItem thứ tự tham số (LỖI 5)
```jsx
// HIỆN TẠI (dòng 107-109):
const handleRemoveItem = async (item) => {
  try {
    await groceryService.removeItem(groceryList.id, item.id);

// SỬA THÀNH:
const handleRemoveItem = async (item) => {
  try {
    await groceryService.removeItem(item.id, groceryList.id);
```

#### Sửa 6: Dòng 121 - updateList đã có (LỖI 2)
```jsx
// Dòng 121 - giữ nguyên code, service đã có method updateList:
await groceryService.updateList(groceryList.id, { name: listName.trim() });
```

#### Sửa 7: Dòng 134 - clearItems đã có (LỖI 3)
```jsx
// Dòng 134 - giữ nguyên code, service đã có method clearItems:
await groceryService.clearItems(groceryList.id);
```

#### Sửa 8: Dòng 158 - field name (LỖI 7 + 8)
```jsx
// HIỆN TẠI (dòng 157-158):
const text = items.map(i =>
  `${i.isBought ? '✅' : '⬜'} ${i.ingredientName} - ${i.finalToBuy || i.quantity} ${i.unit || ''}`

// SỬA THÀNH:
const text = items.map(i =>
  `${i.isBought ? '✅' : '⬜'} ${i.ingredient?.name || ''} - ${i.finalToBuy || i.totalNeeded} ${i.unit || ''}`
```

---

### 🔧 LỖI 7 + 8: Sửa `GroceryItemRow.jsx`

**Mức độ**: MEDIUM  
**File**: `smartrecipe-frontend/src/components/grocery/GroceryItemRow.jsx`

#### Sửa 1: Dòng 35 - ingredientName → ingredient?.name
```jsx
// HIỆN TẠI (dòng 35):
<span className={styles.name}>{item.ingredientName}</span>

// SỬA THÀNH:
<span className={styles.name}>{item.ingredient?.name || 'Không tên'}</span>
```

#### Sửa 2: Dòng 37 - quantity → totalNeeded
```jsx
// HIỆN TẠI (dòng 37):
{item.finalToBuy != null ? item.finalToBuy : item.quantity} {item.unit || ''}

// SỬA THÀNH:
{item.finalToBuy != null ? item.finalToBuy : item.totalNeeded} {item.unit || ''}
```

---

## 📦 PHASE 4: KIỂM TRA FILE THIẾU

---

### 🔧 LỖI 10: Kiểm tra `EditProfilePage.jsx`

**Mức độ**: LOW  
**File cần kiểm tra**: `smartrecipe-frontend/src/pages/EditProfilePage.jsx`

**Lệnh kiểm tra**:
```bash
ls smartrecipe-frontend/src/pages/EditProfilePage.jsx
```

**Nếu không tồn tại**, tạo file tối thiểu:
```jsx
import React from 'react';

const EditProfilePage = () => {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Edit Profile</h1>
      <p>Trang chỉnh sửa hồ sơ - đang phát triển</p>
    </div>
  );
};

export default EditProfilePage;
```

---

## ✅ KIỂM THỬ SAU KHI SỬA

### Backend
```bash
cd smartrecipe-backend
mvn compile          # Kiểm tra compile
mvn test             # Chạy unit test
```

### Frontend
```bash
cd smartrecipe-frontend
npm run build        # Kiểm tra build không lỗi
npm run dev          # Chạy dev server
```

### Test Case Manual

| # | Test | Kết quả mong đợi |
|---|------|-----------------|
| 1 | Truy cập `/grocery` | Hiển thị danh sách mua sắm, không báo lỗi `undefined` |
| 2 | Toggle checkbox item | Item chuyển trạng thái `isBought`, không crash |
| 3 | Thêm item mới | Item xuất hiện trong danh sách với tên và số lượng đúng |
| 4 | Sửa item | Cập nhật số lượng, gọi đúng API |
| 5 | Xóa item | Item biến mất khỏi danh sách |
| 6 | Đổi tên danh sách | Nhấn vào tiêu đề → nhập tên mới → Enter → lưu thành công |
| 7 | Xóa tất cả items | Tất cả items biến mất |
| 8 | Hoàn tất mua sắm | Hiệu ứng confetti, danh sách chuyển COMPLETED |
| 9 | Share danh sách | Copy text đúng format, có tên và số lượng |
| 10 | Truy cập `/profile` | Không crash (có `EditProfilePage`) |

---

## 📊 TIẾN ĐỘ THEO DÕI

| # | Lỗi | File | Trạng thái |
|---|-----|------|-----------|
| 1 | Response wrapper mismatch | `groceryService.js` | ⬜ Chưa sửa |
| 2 | Thiếu `updateList` | Backend + Frontend | ⬜ Chưa sửa |
| 3 | Thiếu `clearItems` | Backend + Frontend | ⬜ Chưa sửa |
| 4 | `toggleItem` → `togglePurchased` | `GroceryPage.jsx:77` | ⬜ Chưa sửa |
| 5 | `removeItem` sai thứ tự tham số | `GroceryPage.jsx:109` | ⬜ Chưa sửa |
| 6 | `updateItem` listId query param | `groceryService.js` + `GroceryPage.jsx:101` | ⬜ Chưa sửa |
| 7 | `ingredientName` → `ingredient?.name` | `GroceryItemRow.jsx:35` + `GroceryPage.jsx:158` | ⬜ Chưa sửa |
| 8 | `quantity` → `totalNeeded` | `GroceryItemRow.jsx:37` + `GroceryPage.jsx:158` | ⬜ Chưa sửa |
| 9 | `handleEditSubmit` sai tham số | `GroceryPage.jsx:101` | ⬜ Chưa sửa |
| 10 | Thiếu `EditProfilePage.jsx` | Kiểm tra + tạo nếu thiếu | ⬜ Chưa sửa |
| 11 | Thiếu `GroceryListStatus.java` | Kiểm tra + tạo nếu thiếu | ⬜ Chưa sửa |

---

> **Ghi chú**: Sửa theo thứ tự PHASE 1 → PHASE 2 → PHASE 3 → PHASE 4.  
> Mỗi phase sửa xong → build lại → verify trước khi chuyển phase tiếp theo.
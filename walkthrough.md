# 🔧 Walkthrough: Sprint 2 Bug Fixes

## Tổng quan
Đã sửa **14 lỗi** phát hiện trong Sprint 2 (3 nghiêm trọng, 6 trung bình, 5 nhỏ).

---

## Danh sách files đã thay đổi

### Backend (9 files modified, 2 files created)

| File | Thay đổi |
|---|---|
| [SecurityConfig.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/security/SecurityConfig.java) | **BUG-1**: Thêm `@EnableMethodSecurity` để `@PreAuthorize` hoạt động. **BUG-3**: Đổi `allowedOrigins("*")` → `allowedOriginPatterns("*")` + `allowCredentials(true)` |
| [UserServiceImpl.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/UserServiceImpl.java) | **BUG-6**: Thêm `@Transactional` class-level + `readOnly=true` cho `getUserProfile` |
| [IngredientServiceImpl.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/IngredientServiceImpl.java) | **BUG-4**: Bỏ `@Cacheable` trên `getAllIngredients(Page)` để tránh deserialization lỗi. **BUG-5**: Thêm `readOnly=true` cho các method read |
| [AisleServiceImpl.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/AisleServiceImpl.java) | **BUG-5**: Thêm `readOnly=true` cho `getAllAisles`, `getAisleById` |
| [TagServiceImpl.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/TagServiceImpl.java) | **BUG-5**: Thêm `readOnly=true`. **BUG-7**: Thêm method `updateTag()` với kiểm tra trùng tên |
| [TagService.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/TagService.java) | **BUG-7**: Thêm `updateTag(Integer id, String name)` vào interface |
| [UnitConversionServiceImpl.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/UnitConversionServiceImpl.java) | **BUG-5**: Thêm `readOnly=true` cho 3 method read |
| [AisleController.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/controller/AisleController.java) | **BUG-8**: Đổi `Map<String,String>` → `@Valid AisleRequest` DTO |
| [TagController.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/controller/TagController.java) | **BUG-7**: Thêm `PUT /{id}` endpoint. **BUG-8**: Đổi `Map` → `@Valid TagRequest` DTO |
| [CloudinaryServiceImpl.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/service/impl/CloudinaryServiceImpl.java) | **BUG-9**: Thêm validate file type (image/*), size (max 5MB), empty check |
| [CacheConfig.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/config/CacheConfig.java) | **MINOR-1**: Cấu hình TTL cho tất cả cache names (search 15min, master data 1hr) |
| [CloudinaryConfig.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/config/CloudinaryConfig.java) | **MINOR-2**: Bỏ đọc `.env` thủ công, thêm error message rõ ràng |
| [IngredientRequest.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/dto/request/IngredientRequest.java) | **MINOR-4**: Thêm `@NotNull` cho `caloriesPer100g`, `protein`, `fat`, `carbs` |
| **[NEW]** [AisleRequest.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/dto/request/AisleRequest.java) | **BUG-8**: DTO mới với `@NotBlank @Size` validation |
| **[NEW]** [TagRequest.java](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/dto/request/TagRequest.java) | **BUG-8**: DTO mới với `@NotBlank @Size` validation |

### Frontend (3 files modified)

| File | Thay đổi |
|---|---|
| [ProfilePage.jsx](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/pages/ProfilePage.jsx) | **BUG-2**: Thêm `reset()` + `useEffect` để sync form values khi API trả data |
| [IngredientAutocomplete.jsx](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/components/ui/IngredientAutocomplete.jsx) | **MINOR-3**: Thêm cleanup `useEffect` cho debounce timer |
| [useAuthStore.js](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/src/store/useAuthStore.js) | **MINOR-5**: Dùng `partialize` để chỉ persist `user` + `isAuthenticated`, tránh lưu token 2 lần |

---

## Verification

> [!IMPORTANT]
> Cần chạy lại backend (`mvn spring-boot:run`) và frontend (`npm run dev`) để verify các thay đổi hoạt động đúng.

### Kiểm tra quan trọng nhất:
1. **BUG-1**: Thử gọi `POST /api/v1/ingredients` với token USER (không phải ADMIN) → phải nhận 403 Forbidden
2. **BUG-2**: Mở trang Profile → form phải hiển thị đúng displayName và bio hiện tại
3. **BUG-9**: Thử upload file `.exe` qua API avatar → phải nhận lỗi validation

# Kế hoạch triển khai Pantry — Phương án C (Lot + Base Unit)

## Mục tiêu

Hoàn thiện Pantry theo mô hình quản lý từng lô nguyên liệu, chuẩn hóa số lượng về
`Ingredient.baseUnit`, giữ đúng ngày hết hạn, hỗ trợ FEFO cho Grocery/Cooking Journal
và để backend là nguồn sự thật duy nhất cho frontend.

## Thứ tự triển khai và kiểm thử (không thay đổi)

1. Sửa ownership cho `PUT/DELETE /api/v1/pantry/{id}`.
2. Chốt và triển khai mô hình đơn vị: lưu quantity theo base unit, nhận unit nhập vào,
   dùng `UnitConversionRepository` để quy đổi.
3. Sửa quy tắc merge quantity/expiry và thống nhất backend/frontend.
4. Viết test Pantry backend, ưu tiên authorization và business rules.
5. Cập nhật đồng bộ `sprint4_plan.md` và `sprint_plan_next.md` sau khi xác nhận thay đổi.
6. Nghiệm thu Recipe bằng test API/UI.

## Quyết định nghiệp vụ

### Quantity và unit

- Request nhận `quantityAvailable` theo `unit` người dùng chọn.
- Backend chuẩn hóa thành `quantityBase` theo `ingredient.baseUnit` trước khi lưu.
- Không tự đoán conversion khi thiếu dữ liệu; trả lỗi validation rõ ràng.
- Khối lượng/thể tích/đếm được là các nhóm đơn vị khác nhau; chỉ chuyển nhóm khi có
  conversion riêng cho ingredient.
- Backend dùng `BigDecimal`, không làm tròn giữa các bước; chỉ làm tròn ở kết quả cuối.

### Pantry lot

- Mỗi `UserPantry` là một lot: `userId + ingredientId + expiryDate`.
- Hai lot khác expiry (kể cả `null`) không merge.
- Hai request cùng ingredient và cùng expiry merge bằng phép cộng quantity đã chuẩn hóa.
- `POST /pantry` là thao tác thêm/cộng dồn; `PUT /pantry/{id}` là cập nhật tuyệt đối
  một lot; `DELETE` xóa đúng lot.
- `lowStockThreshold` được hiểu theo `baseUnit`. Trong giai đoạn chuyển tiếp vẫn giữ
  field trên lot để tương thích schema/API; service phải áp dụng cùng một giá trị khi
  tổng hợp theo ingredient.

### Expiry và FEFO

- `expiryDate < today`: `EXPIRED`.
- `today <= expiryDate <= today + 7`: `EXPIRING_SOON`.
- `expiryDate > today + 7`: `FRESH`.
- `expiryDate = null`: `FRESH`, không hạn.
- Khi trừ kho: bỏ qua lot đã hết hạn, dùng lot có expiry sớm nhất trước; lot không hạn
  dùng sau cùng.

### Backend/frontend contract

- Backend không nhóm theo tên nguyên liệu.
- Frontend không tự cộng quantity hoặc tự chọn expiry đại diện.
- API list có thể trả lot-level trước để tương thích; frontend chỉ hiển thị aggregate
  do backend cung cấp khi contract aggregate được hoàn thiện.
- `ingredientId` là khóa nghiệp vụ, không dùng `ingredient.name` làm khóa.

## Tiêu chí nghiệm thu

- User A không thể sửa/xóa lot của User B; endpoint trả `404` như resource không tồn tại.
- `1 kg + 500 g` của ingredient có base unit `g` cho kết quả `1500 g`.
- Hai expiry khác nhau được giữ thành hai lot.
- Hai request cùng expiry được cộng đúng.
- Expiry hôm nay là `EXPIRING_SOON`, không phải `EXPIRED`.
- Summary/low-stock không đếm trùng do merge theo tên ở backend/frontend.
- Build backend/frontend và bộ test Pantry chạy thành công.

## Phạm vi chuyển đổi dữ liệu

Schema hiện tại có unique `(user_id, ingredient_id)` và chưa có unit trong
`user_pantry`. Bước triển khai sẽ có migration riêng, không sửa lịch sử dữ liệu trực tiếp
trong `init_database.sql` nếu không cần; migration phải bảo toàn dữ liệu hiện có trước khi
đổi constraint.

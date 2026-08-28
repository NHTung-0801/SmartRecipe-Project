# Kế hoạch Cập nhật UI Cooking Journal (Timeline & Detail)

## Mục tiêu
- **Trang "Nhật ký nấu ăn" (Timeline)**: Hiển thị danh sách nhật ký dạng Timeline luân phiên (alternating timeline) với trục thời gian ở giữa. Thêm nút "Ghi nhận món mới" (New Entry) vào trang này.
- **Trang "Chi tiết nhật ký" (Journal Detail)**: Tạo một trang mới hoàn toàn `JournalDetailPage.jsx` khi click vào một card trên Timeline, thay vì chuyển sang trang Chi tiết công thức. Trang này sẽ có giao diện đẹp như bản tham khảo (Hero image, Ký ức, Đánh giá, Link về công thức gốc).
- **Luồng ghi nhận**: Xóa nút "Đã nấu xong" ở trang Chi tiết công thức, Modal ghi nhật ký sẽ được gọi từ trang Timeline và cần có thêm ô Tìm kiếm công thức.

> [!IMPORTANT]
> **User Review Required**
> Vui lòng xem xét các câu hỏi bên dưới về cấu trúc dữ liệu trước khi tôi bắt đầu code.

## Open Questions
> [!WARNING]
> **Vấn đề về Dữ liệu (Database Schema) cho trang Chi tiết nhật ký:**
> Bản thiết kế (mockup) trang Chi tiết nhật ký của bạn có rất nhiều thông tin phong phú như:
> - **Ký ức & Câu chuyện** (đoạn văn dài)
> - **Cảm nhận hương vị** (chia thành Nước dùng, Thịt bò, Bánh phở...)
> - **Đánh giá cá nhân chi tiết** (Thanh trượt Độ khó, Độ hài lòng)
> - **Ảnh quá trình** (nhiều ảnh)
> 
> Tuy nhiên, trong Database `CookingJournal` hiện tại của chúng ta chỉ có:
> - `rating` (số sao 1-5)
> - `iteration_notes` (Ghi chú chung 1 đoạn text)
> - `image_url` (1 ảnh duy nhất)
> 
> **Câu hỏi cho bạn:**
> 1. Bạn có muốn tôi **cập nhật lại Database Backend** (thêm các cột như `story`, `taste_notes`, `difficulty_rating`, `process_images`) để lưu trữ đầy đủ các thông tin này không? 
> 2. Hay bạn muốn tôi chỉ **tái sử dụng các trường hiện có** (dùng `iteration_notes` cho phần Ký ức, ẩn phần Cảm nhận hương vị và Ảnh quá trình đi)?

## Proposed Changes

### 1. Thay đổi Backend (Nếu bạn chọn cách 1 ở trên)
- Cập nhật entity `CookingJournal`, thêm các field mới.
- Cập nhật `JournalRequest` và `JournalResponse`.

### 2. Thay đổi Frontend Component
#### [MODIFY] `CookingJournalPage.jsx`
- Đổi giao diện thành Timeline luân phiên (trái-phải).
- Thêm nút "New Entry" (Thêm nhật ký) nổi bật ở góc hoặc sidebar.

#### [NEW] `JournalDetailPage.jsx`
- Giao diện chi tiết nhật ký bám sát mockup.
- Hiển thị Hero image, các block thông tin đánh giá.
- Nút nhỏ góc dưới: "Công thức gốc" link tới `/recipes/{id}`.

#### [MODIFY] `AddJournalModal.jsx`
- Thêm Autocomplete Search để tìm và chọn Recipe.
- Thêm các trường nhập liệu mới (nếu cập nhật DB) như Ký ức, Độ khó, Upload nhiều ảnh quá trình.

#### [MODIFY] `RecipeDetailPage.jsx` & `App.jsx`
- Xóa nút "ĐÃ NẤU XONG!" ở `RecipeDetailPage`.
- Thêm route `/journal/:id` vào `App.jsx`.

## Verification Plan
- Chạy lại ứng dụng frontend.
- Vào trang Nhật ký, xác nhận giao diện Timeline hiển thị đúng như hình mẫu.
- Bấm nút Thêm nhật ký, tìm một món và lưu lại, kiểm tra xem có hiện lên Timeline không.

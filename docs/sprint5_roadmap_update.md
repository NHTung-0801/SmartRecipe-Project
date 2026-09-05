# Cập nhật Tiến độ & Kế hoạch Sprint 5 (Cooking Journal & AI Gemini)
*(Ngày cập nhật: 24/08/2026)*

---

## 1. PHẦN ĐÃ HOÀN THÀNH ✅

### Backend — Cooking Journal & FEFO Deduction
- [x] `JournalRequest` / `JournalResponse` DTO
- [x] `CookingJournalRepository` (phân trang, đếm)
- [x] `JournalService` + `JournalServiceImpl` (CRUD)
- [x] FEFO Deduction trong `PantryService` (trừ kho tự động theo hạn sử dụng)
- [x] `JournalController` (GET list, GET detail, POST create, DELETE)
- [x] Tải ảnh thành quả lên Cloudinary

### Backend — AI Gemini Integration
- [x] `GeminiConfig` (RestClient, API Key, Model, Daily Limit)
- [x] `GeminiClient` (gọi Gemini API, parse response JSON)
- [x] `AiServiceImpl` — suggestFromPantry (Zero-Waste, ưu tiên sắp hết hạn)
- [x] `AiServiceImpl` — suggestFromInput (Custom Input)
- [x] `AiServiceImpl` — saveAiRecipe (lưu thành công thức thật)
- [x] Rate Limiting bằng bảng `ai_suggestion_logs` (10 lần/ngày/user)
- [x] Auto-matching nguyên liệu AI → DB bằng `findByNameContainingIgnoreCase`
- [x] **Auto-create nguyên liệu mới** nếu hệ thống chưa có (thay vì để null)
- [x] `AiController` (3 endpoints: suggest/pantry, suggest/custom, save/{logId})
- [x] `AiSuggestRequest` / `AiSuggestResponse` DTO
- [x] `RateLimitExceededException` + handler trả 429

### Frontend — Cooking Journal
- [x] `AddJournalModal` (form ghi nhật ký nấu ăn)
- [x] `CookingJournalPage` (timeline hành trình ẩm thực)
- [x] `JournalDetailPage` (chi tiết nhật ký, glassmorphism)
- [x] `journalService.js` (gọi API)
- [x] Nút "Cooked it!" trên `RecipeDetailPage`
- [x] Link "Nhật ký" trên Sidebar

---

## 2. PHẦN CÒN LẠI CẦN LÀM ⏳

### Task 4.2: Trang Trợ lý AI — Frontend (Kế tiếp)

#### 4.2a — Service Layer
- [ ] Tạo `aiService.js` trong `src/services/` để gọi 3 API:
  - `GET /api/v1/ai/suggest/pantry`
  - `POST /api/v1/ai/suggest/custom` (body: `{ ingredients: [...] }`)
  - `POST /api/v1/ai/save/{logId}`

#### 4.2b — Trang `AiSuggestionPage.jsx`
- [ ] **Tab 1 — "Giải cứu tủ lạnh" (Zero-Waste):**
  - Hiển thị preview nguyên liệu sắp hết hạn (gọi `pantryService` lấy data).
  - Nút bấm → gọi `suggestFromPantry`.
- [ ] **Tab 2 — "Tôi có..." (Custom Input):**
  - Ô Tag Input cho phép nhập nhiều nguyên liệu dạng chip/tag.
  - Nút "Gợi ý món" → gọi `suggestFromInput`.
- [ ] **Loading State:** Skeleton/Spinner + text "AI đang suy nghĩ..." (vì API mất 3-10s).
- [ ] **Xử lý lỗi 429:** Toast thông báo "Bạn đã hết 10 lượt hôm nay".

#### 4.2c — Routing & Navigation
- [ ] Thêm route `/ai-suggestion` vào `App.jsx` (ProtectedRoute + AppLayout).
- [ ] Thêm mục **"Trợ lý AI"** vào `Sidebar.jsx` (icon: `Sparkles` hoặc `Bot` từ lucide-react).

> ⚠️ **Phát hiện thiếu sót:** Hiện tại `App.jsx` chưa có route `/ai-suggestion` và `Sidebar.jsx` cũng chưa có link tới trang AI. Đây là bước bắt buộc phải làm cùng lúc với trang.

### Task 5.2: Hiển thị Kết quả AI & Lưu Công thức

#### 5.2a — Component `AiRecipeCard.jsx`
- [ ] Parse JSON từ Backend và hiển thị thành công thức trực quan:
  - Tên món, mô tả.
  - Danh sách nguyên liệu (tên, số lượng, đơn vị) — dạng bảng hoặc list.
  - Các bước nấu (step-by-step) — dạng timeline hoặc stepper.
  - Thông tin phụ: thời gian chuẩn bị, thời gian nấu, độ khó, khẩu phần.
- [ ] Badge hoặc label nhãn ghi "Được tạo bởi AI" để phân biệt rõ nguồn gốc.

#### 5.2b — Nút "Lưu thành công thức của tôi"
- [ ] Gọi API `POST /api/v1/ai/save/{logId}`.
- [ ] Sau khi lưu thành công → điều hướng tới `RecipeDetailPage` của công thức vừa tạo.
- [ ] Nếu đã lưu rồi (canSave = false hoặc API trả lỗi) → disable nút, hiển thị "Đã lưu".

---

## 3. CÁC VẤN ĐỀ BACKEND CẦN BỔ SUNG ĐỂ VẬN HÀNH TỐT HƠN ⚙️

Đây là những điểm tôi phát hiện sau khi rà soát source code thực tế, **nên xử lý trước hoặc trong lúc làm Frontend** để hệ thống chạy trơn tru:

### 3.1 — Xử lý lỗi khi Gemini API gặp sự cố (Error Resilience) ✅
> **Đã hoàn thành** *(xác nhận qua code review 05/09/2026)*
- [x] `AiServiceException.java` đã tạo (extend RuntimeException).
- [x] Handler trong `GlobalExceptionHandler` trả về HTTP 503 kèm message thân thiện.
- [x] `GeminiConfig` đã cấu hình `connectTimeout=5s`, `readTimeout=30s` qua `JdkClientHttpRequestFactory`.

### 3.2 — Endpoint lấy lịch sử gợi ý AI (AI History) ✅
> **Đã hoàn thành** *(xác nhận qua code review 05/09/2026)*
- [x] Endpoint `GET /api/v1/ai/history` đã có trong `AiController`.
- [x] `AiHistoryResponse.java` DTO đã tạo.
- [ ] Trên Frontend: hiển thị lịch sử gợi ý ở tab thứ 3 *(tùy chọn — có thể làm sau)*.

### 3.3 — Endpoint đếm lượt còn lại (Rate Limit Info) ✅
> **Đã hoàn thành** *(xác nhận qua code review 05/09/2026)*
- [x] Endpoint `GET /api/v1/ai/remaining` đã có trong `AiController`, trả về `{ used, limit, remaining }`.
- [x] `AiRemainingResponse.java` DTO đã tạo.
- [x] `AiSuggestionPage.jsx` gọi endpoint này khi mở trang để hiển thị counter.

---

## 4. ROADMAP MỞ RỘNG (Tùy chọn — Điểm cộng Đồ án) 🌟

| # | Tính năng | Mô tả | Ưu tiên |
| :---: | :--- | :--- | :---: |
| 1 | **Database Seeding** | Nhập 300-500 nguyên liệu Tiếng Việt kèm dinh dưỡng cơ bản bằng file `data.sql`. Giúp AI auto-match chính xác ~99% ngay từ lần đầu chạy. | Cao |
| 2 | **Admin Moderation** | Thêm cột `is_verified` (boolean) vào bảng `ingredients`. Nguyên liệu do AI tạo tự động sẽ có `is_verified = false`. Admin duyệt và bổ sung dinh dưỡng trên trang quản trị riêng. | Trung bình |
| 3 | **AI Prompt cải tiến** | Bổ sung yêu cầu AI ước lượng luôn dinh dưỡng per 100g cho mỗi nguyên liệu mới. Giảm tải công việc cho Admin. | Thấp |

---

## 5. THỨ TỰ TRIỂN KHAI ĐỀ XUẤT

| Bước | Công việc | Phụ thuộc | Ước lượng |
| :---: | :--- | :--- | :---: |
| 1 | Task 3.1 — Bổ sung `AiServiceException` + timeout RestClient | Không | 15 phút |
| 2 | Task 3.2 — Endpoint `GET /ai/history` | Không | 30 phút |
| 3 | Task 3.3 — Endpoint `GET /ai/remaining` | Không | 10 phút |
| 4 | Task 4.2a — Tạo `aiService.js` | Bước 1-3 | 15 phút |
| 5 | Task 4.2b — Trang `AiSuggestionPage.jsx` (2 tabs + loading) | Bước 4 | 1-2 giờ |
| 6 | Task 4.2c — Route + Sidebar | Bước 5 | 10 phút |
| 7 | Task 5.2a — Component `AiRecipeCard.jsx` | Bước 5 | 1 giờ |
| 8 | Task 5.2b — Lưu công thức + điều hướng | Bước 7 | 30 phút |

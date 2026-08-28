# Kế hoạch Triển khai Chi tiết Sprint 5: Cooking Journal & AI Gemini

Đây là bản kế hoạch chi tiết cho Sprint 5, được chia làm 2 phần lớn tương ứng với 2 luồng nghiệp vụ. Mỗi phần đã được bóc tách thành các Task cụ thể từ Backend đến Frontend để thực hiện theo trình tự.

> **Cập nhật:** 21/08/2026 — Đã sửa lỗi logic, bổ sung edge case, cải thiện JSON format AI, và thêm bước match nguyên liệu.

---

## PHẦN 1: COOKING JOURNAL & TỰ ĐỘNG TRỪ KHO (PANTRY DEDUCTION)

Mục tiêu: Cho phép người dùng lưu lại lịch sử nấu ăn và hệ thống tự động trừ nguyên liệu trong tủ lạnh ảo theo cơ chế FEFO (First Expire First Out).

### Danh sách Task Backend (Phần 1)

#### Task 1.1: Chuẩn bị DTO và Service cơ bản cho Journal
- [x] Tạo `JournalRequest` DTO (chứa `recipeId`, `actualServings`, `rating`, `iterationNotes`, `imageUrl`).
- [x] Tạo `JournalResponse` DTO (chứa id, recipe summary, cookedAt, rating, notes, imageUrl, actualServings, deductionSummary).
- [x] Tạo `CookingJournalRepository` (có hàm `findByUserIdOrderByCookedAtDesc`, `countByUserIdAndRecipeId`).
- [x] Khởi tạo `JournalService` interface và `JournalServiceImpl` với các hàm CRUD cơ bản (thêm, xóa, lấy danh sách phân trang).

> **Lưu ý:** Entity `CookingJournal.java` đã được tạo sẵn trong codebase, không cần tạo mới.

#### Task 2.1: Logic Tự động trừ kho (FEFO Deduction)
- [x] Trong `PantryService`, thêm hàm `deductIngredientsForRecipe(Long userId, Long recipeId, int actualServings)`.
- [x] Thuật toán chi tiết:
  1. Lấy `Recipe` từ DB, đọc `baseServings`.
  2. Tính tỷ lệ: `ratio = actualServings / baseServings`.
  3. Duyệt danh sách `RecipeIngredient` của công thức:
     - Tính `requiredQuantity = recipeIngredient.amount * ratio`.
       > ⚠️ Trường trong entity là `amount`, không phải `quantity`.
     - Quy đổi `requiredQuantity` từ `recipeIngredient.unit` sang `ingredient.baseUnit` thông qua `UnitNormalizationService.toBaseUnit()`.
  4. Tìm các lô `UserPantry` của user theo `ingredientId`, sort theo `expiryDate ASC` (FEFO).
  5. Vòng lặp trừ dần `requiredQuantity` vào các lô:
     - Nếu lô hiện tại đủ: trừ và dừng.
     - Nếu lô hiện tại không đủ: trừ hết lô đó (xóa lô), chuyển sang lô tiếp theo.
     - Nếu hết lô mà vẫn chưa trừ đủ: **trừ về 0 và dừng** (không báo lỗi).
  6. **Edge case quan trọng:**
     - Nếu nguyên liệu đó **không tồn tại trong Pantry** → **bỏ qua (skip)**, không báo lỗi.
     - Nếu kho **không đủ số lượng** → trừ hết những gì có, xóa lô rỗng, và vẫn cho lưu nhật ký bình thường.
     - Nếu `UnitNormalizationService` không thể quy đổi đơn vị (ví dụ: "củ" không quy được sang "g") → **bỏ qua** nguyên liệu đó.
- [x] Hàm trả về `List<DeductionDetail>` (ingredientName, deductedAmount, unit) để hiển thị cho user biết đã trừ những gì.
- [x] Viết Unit Test cho hàm `deductIngredientsForRecipe`:
  - Case 1: Trừ vừa đủ từ 1 lô duy nhất.
  - Case 2: Trừ vượt qua nhiều lô (lô 1 hết → nhảy sang lô 2).
  - Case 3: Kho không đủ → trừ về 0, không exception.
  - Case 4: Nguyên liệu không có trong kho → skip, không exception.
  - Case 5: Đơn vị không quy đổi được → skip, không exception.

#### Task 3.1: Hoàn thiện Controller và Tích hợp
- [x] Cập nhật hàm `createJournal` trong `JournalServiceImpl`:
  1. **Trừ kho trước** — gọi `deductIngredientsForRecipe()`.
  2. **Lưu nhật ký sau** — gọi `cookingJournalRepository.save()`.
  > ⚠️ Thứ tự quan trọng: Trừ kho trước, lưu nhật ký sau. Nếu trừ kho lỗi, cả transaction rollback nhờ `@Transactional`, tránh trường hợp nhật ký đã lưu nhưng kho chưa trừ.
- [x] Tạo `JournalController` với các endpoint:
  - `GET /api/v1/journals` — Lấy danh sách nhật ký của user hiện tại (phân trang).
  - `GET /api/v1/journals/{id}` — Lấy chi tiết 1 nhật ký.
  - `POST /api/v1/journals` — Tạo nhật ký mới + Tự động trừ kho. Response trả về `JournalResponse` kèm `deductionSummary`.
  - `DELETE /api/v1/journals/{id}` — Xóa nhật ký (không hoàn nguyên kho).

### Danh sách Task Frontend (Phần 1)

#### Task 4.1: Component "Cooked it!" (Đã nấu)
- [x] Tạo modal `AddJournalModal.jsx` chứa form:
  - Khẩu phần thực tế đã nấu (`actualServings`) — mặc định = `baseServings` của công thức.
  - Đánh giá sao (`rating`) — component 5 sao tương tác.
  - Ghi chú (`iterationNotes`) — textarea.
  - Tải ảnh lên (`imageUrl`) — dùng chung component Upload Cloudinary đã có.
- [x] Tích hợp nút **"Cooked it!"** vào trang `RecipeDetailPage.jsx` để mở modal trên.
- [x] Sau khi lưu thành công, hiển thị toast/thông báo kèm danh sách nguyên liệu đã trừ khỏi kho (từ `deductionSummary`).

#### Task 5.1: Trang Lịch sử Nấu ăn (Cooking Journal Page)
- [x] Tạo `journalService.js` để gọi các API `/api/v1/journals`.
- [x] Tạo trang `CookingJournalPage.jsx` hiển thị danh sách các món đã nấu dưới dạng timeline hoặc grid card:
  - Mỗi card gồm: Ảnh, tên món, ngày nấu, rating (sao), ghi chú.
  - Click vào card → điều hướng tới `RecipeDetailPage` của công thức tương ứng.
- [x] Thêm link trang này vào thanh điều hướng (Navbar / Sidebar).

---

## PHẦN 2: TRỢ LÝ AI GEMINI (ZERO-WASTE & CUSTOM INPUT)

Mục tiêu: Tích hợp API của Google Gemini để gợi ý món ăn thông minh từ dữ liệu tủ lạnh (Pantry) hoặc dữ liệu người dùng tự nhập. Lưu lại lịch sử gợi ý và cho phép lưu kết quả thành công thức.

### Danh sách Task Backend (Phần 2)

#### Task 1.2: Thiết lập kết nối Gemini & Rate Limiter
- [x] Thêm biến `GEMINI_API_KEY` vào `.env` và bind vào `application.yml` (ví dụ: `gemini.api-key`).
- [x] Tạo class `GeminiConfig` (@Configuration) khởi tạo `RestClient` với base URL và API key.
- [x] **Rate Limiting:** Sử dụng bảng `ai_suggestion_logs` đã có trong DB để đếm số lượt gọi:
  - Query: `SELECT COUNT(*) FROM ai_suggestion_logs WHERE user_id = ? AND created_at >= ?` (đầu ngày hôm nay).
  - Giới hạn: **10 lần/ngày/user**.
  - Nếu vượt giới hạn → trả lỗi `429 Too Many Requests`.
  > ⚠️ Dùng bảng log có sẵn thay vì tạo Redis counter riêng — đơn giản hơn, ít component hơn, và log vẫn được lưu để phân tích sau.

#### Task 2.2: Xây dựng AI Service (Prompt Engineering)
- [x] Tạo class `GeminiClient` sử dụng `RestClient` để gọi API POST tới:
  ```
  https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
  ```
- [x] Xây dựng **System Prompt** tĩnh, yêu cầu AI trả về kết quả dưới định dạng JSON **khớp với cấu trúc RecipeRequest** của hệ thống:
  ```json
  {
    "title": "Bò xào hành tây",
    "description": "Món bò xào thơm ngon, đơn giản...",
    "baseServings": 2,
    "prepTime": 10,
    "cookTime": 15,
    "difficulty": "EASY",
    "ingredients": [
      { "ingredientName": "Thịt bò", "amount": 200, "unit": "g" },
      { "ingredientName": "Hành tây", "amount": 1, "unit": "củ" }
    ],
    "steps": [
      { "stepNumber": 1, "instruction": "Thái thịt bò mỏng, ướp gia vị 10 phút..." },
      { "stepNumber": 2, "instruction": "Phi hành tím, xào thịt bò lửa lớn..." }
    ]
  }
  ```
  > ⚠️ Format cũ dùng `["100g thịt bò"]` (chuỗi text thuần) không thể parse tự động. Format mới tách riêng `ingredientName`, `amount`, `unit` để Backend dễ dàng map sang RecipeRequest.

- [x] Tạo `AiService` interface và `AiServiceImpl` với 2 hàm chính:
  - `suggestFromPantry(Long userId)`:
    1. Gọi `PantryService.getMyPantry()` lấy nguyên liệu còn hạn.
    2. Ưu tiên nguyên liệu sắp hết hạn (EXPIRING_SOON) lên đầu danh sách.
    3. Ghép danh sách vào Prompt → Gọi `GeminiClient`.
    4. Parse JSON response.
    5. **Lưu log** vào `AiSuggestionLog` với type = `ZERO_WASTE`, input = danh sách nguyên liệu, output = JSON response.
    6. Trả về kết quả.
  - `suggestFromInput(List<String> ingredients)`:
    1. Nhận danh sách nguyên liệu dạng text từ user.
    2. Ghép vào Prompt → Gọi `GeminiClient`.
    3. Parse JSON response.
    4. **Lưu log** vào `AiSuggestionLog` với type = `FEASIBLE_FINDER`.
    5. Trả về kết quả.

- [x] Tạo DTO:
  - `AiSuggestRequest` — chứa `List<String> ingredients` (cho mode custom input).
  - `AiSuggestResponse` — chứa `Long logId`, recipe data (title, description, ingredients, steps...), `boolean canSave`.

#### Task 3.2: Tạo AI Controller & Endpoint lưu công thức
- [x] Tạo `AiController` với các endpoints:
  - `GET /api/v1/ai/suggest/pantry` — Gợi ý từ tủ lạnh (Zero-Waste).
  - `POST /api/v1/ai/suggest/custom` — Gợi ý từ nguyên liệu nhập tay.
  - `POST /api/v1/ai/save/{logId}` — **Lưu kết quả AI thành công thức thật** (endpoint mới).
- [x] Logic endpoint `POST /api/v1/ai/save/{logId}`:
  1. Lấy `AiSuggestionLog` theo `logId`, đọc `outputResponse` (JSON).
  2. Parse JSON, duyệt `ingredients`:
     - **Match `ingredientName` với bảng `ingredients`** trong DB (tìm kiếm LIKE hoặc exact match).
     - Nếu tìm thấy → dùng `ingredientId` đó.
     - Nếu không tìm thấy → bỏ qua nguyên liệu đó hoặc dùng ID mặc định.
  3. Tạo `RecipeRequest` từ dữ liệu đã map, gọi `RecipeService.createRecipe()`.
  4. Cập nhật `AiSuggestionLog.savedRecipeId` = ID công thức vừa tạo.
  5. Trả về `RecipeResponse`.
  > ⚠️ Không gọi thẳng `POST /api/v1/recipes` từ Frontend vì AI chỉ trả tên nguyên liệu (text), không trả `ingredientId` (số). Cần Backend xử lý bước match tên → ID.
- [x] Xử lý trả về lỗi `429 Too Many Requests` nếu user vượt quá Rate Limit.

### Danh sách Task Frontend (Phần 2)

#### Task 4.2: Trang Trợ lý AI (AI Suggestion Page)
- [ ] Tạo `aiService.js` để gọi các API `/api/v1/ai/...`.
- [ ] Tạo trang `AiSuggestionPage.jsx` thiết kế giao diện có 2 tab hoặc 2 lựa chọn:
  - **Tab 1: "Giải cứu tủ lạnh" (Zero-Waste)**
    - Hiển thị preview danh sách nguyên liệu sắp hết hạn trong kho.
    - Nút bấm → gọi API `GET /api/v1/ai/suggest/pantry`.
  - **Tab 2: "Tôi có..." (Custom Input)**
    - Ô Textarea hoặc Tag input để nhập danh sách nguyên liệu.
    - Nút **"Gợi ý món"** → gọi API `POST /api/v1/ai/suggest/custom`.
- [ ] Xử lý giao diện Loading đẹp mắt (skeleton/spinner + text "AI đang suy nghĩ...") vì AI có thể mất 3-10s.
- [ ] Xử lý lỗi 429: Hiển thị thông báo "Bạn đã hết lượt gợi ý hôm nay (10/10). Hãy quay lại vào ngày mai!".

#### Task 5.2: Hiển thị kết quả & Lưu công thức
- [ ] Xây dựng component `AiRecipeCard.jsx` để parse JSON từ Backend và hiển thị thành một công thức hoàn chỉnh:
  - Tên món, mô tả.
  - Danh sách nguyên liệu (tên, số lượng, đơn vị).
  - Các bước nấu (step by step).
  - Thông tin phụ: thời gian, độ khó, khẩu phần.
- [ ] Thêm nút **"Lưu thành công thức của tôi"**:
  - Gọi API `POST /api/v1/ai/save/{logId}` (Backend xử lý match ingredientName → ingredientId).
  - Sau khi lưu thành công → điều hướng tới `RecipeDetailPage` của công thức vừa tạo.
  - Nếu đã lưu rồi → disable nút, hiển thị "Đã lưu".

---

## Thứ tự triển khai đề xuất

| Bước | Task | Phụ thuộc |
|------|------|-----------|
| 1 | Task 1.1 (Journal DTO + Service) | Không |
| 2 | Task 2.1 (FEFO Deduction + Unit Test) | Task 1.1 |
| 3 | Task 3.1 (Journal Controller + Tích hợp trừ kho) | Task 2.1 |
| 4 | Task 4.1 (Frontend "Cooked it!" Modal) | Task 3.1 |
| 5 | Task 5.1 (Frontend Journal Page) | Task 3.1 |
| 6 | Task 1.2 (Gemini Config + Rate Limiter) | Không |
| 7 | Task 2.2 (AI Service + Prompt Engineering) | Task 1.2 |
| 8 | Task 3.2 (AI Controller + Save endpoint) | Task 2.2 |
| 9 | Task 4.2 (Frontend AI Page) | Task 3.2 |
| 10 | Task 5.2 (Frontend AI Result + Save) | Task 3.2 |

# Kế hoạch Tích hợp Dataset Nguyên liệu & Chiến lược Quản lý Dữ liệu AI
## Hệ thống Smart Recipe

*(Ngày lập: 24/08/2026)*

---

## 1. Bối cảnh & Vấn đề

Hệ thống Smart Recipe tích hợp **AI Gemini** để gợi ý công thức nấu ăn. Khi AI gợi ý một nguyên liệu mà Database chưa có, hệ thống sẽ **tự động tạo mới** nguyên liệu đó (auto-create), nhưng các chỉ số dinh dưỡng (Calo, Protein, Fat, Carbs) đều bằng **0** — dẫn đến:

- Tính năng **tính toán dinh dưỡng** bị sai lệch cho các nguyên liệu mới.
- Kho dữ liệu nguyên liệu tăng trưởng "rác" (thiếu thông tin quan trọng).
- Admin phải nhập tay từng nguyên liệu mới → không hiệu quả.

**Mục tiêu của bản kế hoạch:** Tìm ra chiến lược tối ưu để hệ thống luôn có kho nguyên liệu phong phú, chính xác, và tự vận hành tốt với sự can thiệp tối thiểu.

---

## 2. Luồng hoạt động Auto-matching Nguyên liệu hiện tại

### 2.1 Cách hệ thống đang xử lý (Code thực tế trong `AiServiceImpl.java`)

Khi AI sinh ra một món ăn, nó trả về nguyên liệu dưới dạng Text (VD: `"Thịt bò thăn"`). Backend phải "dịch" từ Text sang ID trong Database:

```
AI trả về: { "ingredientName": "Thịt bò thăn", "amount": 200, "unit": "g" }
                        ↓
Backend: ingredientRepository.findByNameContainingIgnoreCase("Thịt bò thăn")
                        ↓
              ┌─── CÓ KẾT QUẢ ───→ Lấy ingredientId của match đầu tiên
              │
              └─── KHÔNG CÓ ──────→ TẠO MỚI nguyên liệu vào DB
                                    (name = "Thịt bò thăn", dinh dưỡng = 0)
                                    → Lấy ID vừa tạo
```

### 2.2 Cơ chế phòng tránh rủi ro (Fallback)

- **Chốt chặn 1 — Lưu dưới dạng DRAFT:** Toàn bộ công thức AI sinh ra luôn bị ép cứng `status = DRAFT` (Bản nháp). Dù có nguyên liệu bị thiếu dinh dưỡng, nó cũng không ảnh hưởng đến nội dung công khai.
- **Chốt chặn 2 — Human-in-the-loop:** Nguyên liệu mới vẫn được lưu xuống DB với đầy đủ tên. User có thể vào chỉnh sửa sau. Hệ thống không bao giờ crash.

### 2.3 Rủi ro sai số (Mismatch)

Dù dùng `LIKE` để tìm kiếm, đôi khi AI có thể sinh ra từ vựng địa phương hoặc biến thể:

| AI trả về | DB có sẵn | Kết quả matching |
| :--- | :--- | :--- |
| "Thịt bò" | "Thịt bò" | ✅ Khớp chính xác |
| "Thịt bò thăn" | "Thịt bò" | ❌ Không khớp (LIKE `%Thịt bò thăn%` ≠ "Thịt bò") |
| "Trái dứa" | "Quả thơm" | ❌ Từ đồng nghĩa, không khớp |
| "Nước mắm Phú Quốc" | Không có | ❌ Tạo mới với dinh dưỡng = 0 |

---

## 3. Các hướng nâng cấp đã đánh giá

### Hướng 1: Bắt AI "Đoán" luôn Dinh Dưỡng
- **Cách làm:** Sửa System Prompt, yêu cầu AI ước lượng luôn chỉ số dinh dưỡng per 100g cho mỗi nguyên liệu.
- **Đánh giá:** Nhanh nhất nhưng **không chính xác** — AI có thể "bịa" số liệu (hallucination). Không có nguồn trích dẫn cho báo cáo Đồ án. Cùng 1 nguyên liệu, hôm nay AI trả 250 calo, ngày mai 280 calo → dữ liệu không nhất quán.
- **Kết luận:** ❌ Không khuyến nghị làm nguồn dữ liệu chính.

### Hướng 2: Gắn cờ "Chờ Duyệt" (Admin Moderation)
- **Cách làm:** Thêm trường `is_verified` (boolean) vào bảng `ingredients`. AI tạo tự động → `false`. Admin duyệt → `true`.
- **Đánh giá:** Tư duy chuyên nghiệp (mô hình User-Generated Content + Moderation). Phù hợp cho hệ thống sản phẩm thực tế.
- **Kết luận:** ✅ Giá trị cao cho báo cáo Đồ án (thể hiện tư duy Data Governance).

### Hướng 3: Nhận diện Danh mục (Aisle) Tự động
- **Cách làm:** Yêu cầu AI phân loại nguyên liệu vào nhóm (Thịt, Rau, Gia vị...) khi gợi ý.
- **Đánh giá:** Hữu ích cho tính năng Danh sách đi chợ (nhóm nguyên liệu theo kệ hàng).
- **Kết luận:** ⏳ Nice-to-have, ưu tiên thấp.

### Hướng 4: Tải Dataset có sẵn từ bên ngoài (Database Seeding)
- **Cách làm:** Tải file CSV nguyên liệu (~300-500 dòng) từ Kaggle/USDA, dịch sang tiếng Việt, import vào DB bằng `data.sql`.
- **Đánh giá:** Xem phân tích chi tiết ở Mục 4 bên dưới.
- **Kết luận:** ✅ **PHƯƠNG PHÁP TỐI ƯU NHẤT** cho Đồ án.

---

## 4. Phân tích Chi tiết: Dataset vs. AI Gemini

### 4.1 So sánh hai phương pháp

| Tiêu chí | Dataset (Kaggle/USDA) | AI Gemini sinh dữ liệu |
| :--- | :--- | :--- |
| **Độ chính xác** | ⭐⭐⭐⭐⭐ — Kiểm chứng khoa học, trích dẫn được | ⭐⭐⭐ — Có thể hallucinate, không có nguồn |
| **Tốc độ truy vấn** | ⭐⭐⭐⭐⭐ — Nằm sẵn trong DB (vài ms) | ⭐⭐ — Phải gọi API (3-5s mỗi lần) |
| **Chi phí** | Miễn phí hoàn toàn | Tốn quota API (Free tier giới hạn 15 req/phút) |
| **Tính ổn định** | Không phụ thuộc bên thứ 3, chạy offline được | Google API sập → mất khả năng làm giàu dữ liệu |
| **Tính nhất quán** | Dữ liệu cố định, không thay đổi | Cùng 1 nguyên liệu, kết quả khác nhau mỗi lần |
| **Thách thức** | Cần dịch tên sang tiếng Việt | Không cần dịch |

### 4.2 Kết luận

> **Dataset làm nền tảng bắt buộc (backbone). AI Gemini chỉ đóng vai trò gợi ý công thức, không nên gánh vai trò "kho dữ liệu dinh dưỡng".**

Đây cũng chính xác là cách các ứng dụng thực tế như **MyFitnessPal**, **Yummly**, **Samsung Food** hoạt động: kho dữ liệu dinh dưỡng được xây dựng từ nguồn khoa học, không phải từ AI sinh ra.

---

## 5. Đối chiếu Schema Database với Dataset

Bảng `ingredients` trong hệ thống Smart Recipe:

| Trường trong DB | Kiểu dữ liệu | Dataset thường có | Cần xử lý gì? |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(100) | Tên tiếng Anh (VD: "Beef, tenderloin") | **Cần dịch** sang tiếng Việt |
| `base_unit` | VARCHAR(20) | Hầu hết là `g` hoặc `ml` | **Giữ nguyên** — đơn vị quốc tế |
| `calories_per_100g` | DECIMAL(10,2) | Cột `Energy (kcal)` per 100g | **Map thẳng**, không cần chuyển đổi |
| `protein` | DECIMAL(10,2) | Cột `Protein (g)` per 100g | **Map thẳng** |
| `fat` | DECIMAL(10,2) | Cột `Total lipid/fat (g)` per 100g | **Map thẳng** |
| `carbs` | DECIMAL(10,2) | Cột `Carbohydrate (g)` per 100g | **Map thẳng** |
| `aisle_id` | INTEGER (FK) | Có thể có cột `Food Group` | Cần map vào bảng `Aisle` |

**Nhận xét:** 4 trường dinh dưỡng map 1:1 với Dataset quốc tế mà không cần chuyển đổi. Công việc thực sự chỉ nằm ở **dịch tên nguyên liệu**.

---

## 6. Về Vấn đề Đơn vị Tiếng Việt

### 6.1 Hai tầng đơn vị trong hệ thống

| Tầng | Nằm ở đâu | Ví dụ | Ảnh hưởng bởi Dataset? |
| :--- | :--- | :--- | :---: |
| **Đơn vị gốc** (base_unit) | Bảng `ingredients` | `g`, `ml` | **Không** — đơn vị quốc tế, tiếng Việt cũng dùng |
| **Đơn vị công thức** | Bảng `recipe_ingredients` | `củ`, `quả`, `bó`, `thìa canh` | **Không** — đã có `UnitNormalizationService` quy đổi |

### 6.2 Kết luận

> Dataset **không ảnh hưởng** gì đến đơn vị tiếng Việt. `baseUnit` luôn là `g`/`ml` (quốc tế). Các đơn vị Việt Nam (củ, quả, bó, chén...) thuộc tầng công thức và đã được hệ thống `UnitNormalizationService` xử lý riêng.

---

## 7. Vai trò của Admin trong Quản lý Nguyên liệu

### 7.1 Admin có cần thiết không?

**Nếu đã có Dataset tốt (~300-500 nguyên liệu) → Admin gần như không cần can thiệp vào 95% trường hợp.** Cụ thể:

| Tình huống | Xảy ra ~% | Hệ thống tự xử lý? | Admin cần làm gì? |
| :--- | :---: | :---: | :--- |
| Nguyên liệu phổ biến (thịt, cá, rau...) | ~95% | ✅ Auto-match từ Dataset | Không cần |
| Nguyên liệu lạ/đặc sản (rau đắng đất, nấm truffle...) | ~5% | ✅ Tự tạo mới (dinh dưỡng = 0) | Bổ sung dinh dưỡng nếu muốn |

### 7.2 Nếu có Admin, Admin làm gì?

Vai trò Admin rất nhẹ nhàng, không phải cày cuốc nhập liệu:

| Công việc | Tần suất | Mô tả |
| :--- | :--- | :--- |
| **Duyệt nguyên liệu mới** | Tuần 1 lần | Lọc `is_verified = false`. Xem AI đã tạo tự động gì. Bổ sung dinh dưỡng, ấn "Duyệt". |
| **Gộp trùng lặp** | Khi phát hiện | AI có thể tạo "Hành lá" lẫn "Hành hoa" (cùng 1 thứ). Admin gộp thành 1. |
| **Phân loại Aisle** | Khi duyệt | Gán nguyên liệu mới vào đúng nhóm (Thịt, Rau, Gia vị...) cho Danh sách đi chợ. |

### 7.3 Đánh giá

| Góc nhìn | Cần Admin? | Lý do |
| :--- | :---: | :--- |
| **Vận hành hệ thống** | Không bắt buộc | Hệ thống đã tự xử lý đủ tốt, không crash, không mất dữ liệu |
| **Chất lượng dữ liệu** | Nên có | Để bổ sung dinh dưỡng cho nguyên liệu mới, gộp trùng lặp |
| **Giá trị Đồ án** | Rất nên có | Thể hiện tư duy Data Governance, phân quyền RBAC, mô hình vận hành thực tế |

### 7.4 Kết luận

> **Admin là "nice-to-have", không phải "must-have".** Hệ thống vẫn vận hành trơn tru mà không có Admin. Tuy nhiên, nếu đã có sẵn trang Admin, chỉ cần thêm 1 tab "Quản lý nguyên liệu" với CRUD cơ bản + bộ lọc `is_verified` → **giá trị trình bày trong báo cáo rất lớn** (thể hiện tư duy kiến trúc hệ thống hoàn chỉnh).

---

## 8. Nguồn Dataset Đề xuất

| Nguồn | Mô tả | Ưu điểm |
| :--- | :--- | :--- |
| **Kaggle — "USDA National Nutrient Database"** | Dataset chính thức Bộ Nông nghiệp Hoa Kỳ, hàng nghìn nguyên liệu | Uy tín cao, dữ liệu khoa học, miễn phí |
| **Kaggle — "Food and Nutrition Dataset"** | Tổng hợp nguyên liệu phổ biến với calo, protein, fat, carbs | Gọn nhẹ, dễ lọc |
| **USDA FoodData Central (fdc.nal.usda.gov)** | API + Download trực tiếp từ chính phủ Mỹ | Nguồn chính thống nhất, hoàn toàn miễn phí |
| **OpenFoodFacts** | Dự án mã nguồn mở, cộng đồng đóng góp | Miễn phí, mã nguồn mở |

---

## 9. Quy trình Thực hiện

```
[Kaggle CSV] → [Excel/Google Sheets] → [data.sql] → [Spring Boot DB]
      ↓                  ↓                   ↓
  Lọc 300-500       Dịch cột Name       INSERT INTO
  dòng phổ biến     sang tiếng Việt      ingredients(...)
```

### Bước 1: Tải Dataset
- Tải file CSV từ Kaggle (tìm "USDA nutrient database" hoặc "food nutrition dataset").

### Bước 2: Lọc & Chuẩn hóa
- Mở bằng Excel/Google Sheets.
- Lọc giữ lại ~300-500 nguyên liệu phổ biến nhất trong bếp Việt (thịt, cá, rau, gia vị, trái cây...).
- Xóa những thứ không liên quan (food additives, supplements...).

### Bước 3: Dịch sang Tiếng Việt
- Copy cột tên tiếng Anh → Paste vào ChatGPT/Gemini.
- Prompt: *"Dịch danh sách nguyên liệu thực phẩm sau sang tiếng Việt, giữ nguyên thứ tự dòng."*
- Dán kết quả đè lại cột name.

### Bước 4: Sinh câu lệnh SQL
- Dùng hàm nối chuỗi trong Excel để sinh ra các câu `INSERT INTO`:
  ```sql
  INSERT INTO ingredients (name, base_unit, calories_per_100g, protein, fat, carbs)
  VALUES ('Thịt bò thăn', 'g', 250.00, 26.00, 15.00, 0.00);
  ```

### Bước 5: Đưa vào Spring Boot
- Lưu thành file `data.sql`, đặt vào `src/main/resources/`.
- Cấu hình `application.yml`:
  ```yaml
  spring:
    sql:
      init:
        mode: always  # hoặc never sau lần chạy đầu tiên
  ```
- Khi Server khởi động → Spring Boot tự động đọc `data.sql` và insert dữ liệu.

### Ước lượng thời gian: **1-2 tiếng** (thủ công, làm 1 lần duy nhất).

---

## 10. Mô hình Kiến trúc 3 Tầng Dữ liệu (Tổng kết)

```
┌──────────────────────────────────────────────────────────────────┐
│              TẦNG 1: DATASET GỐC (Backbone)                     │
│   300-500 nguyên liệu từ USDA/Kaggle                            │
│   → Dinh dưỡng chính xác, trích dẫn khoa học                    │
│   → Import 1 lần bằng data.sql                                  │
│   → Phủ sóng ~95% nguyên liệu phổ biến trong bếp Việt           │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│          TẦNG 2: AI GEMINI (Bổ sung tự động)                     │
│   Khi AI gợi ý nguyên liệu lạ mà DB chưa có (~5% trường hợp)   │
│   → Tự động tạo mới vào DB (dinh dưỡng tạm = 0)                │
│   → Công thức vẫn lưu được, user vẫn dùng bình thường           │
│   → Đánh dấu is_verified = false (nếu có tính năng Admin)       │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│        TẦNG 3: ADMIN MODERATION (Tùy chọn — Kiểm duyệt)        │
│   Admin lọc nguyên liệu chưa duyệt (is_verified = false)        │
│   → Bổ sung dinh dưỡng, sửa tên, gộp trùng lặp                 │
│   → Đánh dấu is_verified = true                                 │
│   → Nice-to-have, không bắt buộc cho hệ thống hoạt động         │
└──────────────────────────────────────────────────────────────────┘
```

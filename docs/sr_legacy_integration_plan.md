# Kế hoạch Thực thi: Tích hợp USDA SR Legacy bằng Python Script
*(Bản đề xuất 7 bước chuyên sâu)*

## Đề xuất Dữ liệu
Dùng **USDA FoodData Central → SR Legacy** (`food.csv` + `food_nutrient.csv` + `nutrient.csv`). 
**Lý do:** Có cột phân loại `food_category_id` để tách nguyên liệu thô khỏi món chế biến, chuẩn per-100g sẵn, public domain, và trích dẫn được trong báo cáo. Dataset Kaggle kia có thể giữ làm nguồn đối chiếu chéo.

---

## Vấn đề schema phải chốt trước khi import

Ba điểm này quyết định cấu trúc file seed, nên chốt trước khi bắt tay làm sạch:

1. **`ingredients.name` chưa có unique constraint.** Đã xác nhận trong `init_database.sql` (dòng 26–36): chỉ có PK `id` và FK `aisle_id`. `IngredientServiceImpl.createIngredient()` chống trùng bằng `findFirstByNameIgnoreCase` ở tầng application, nhưng `AiServiceImpl` auto-create thì không kiểm tra gì. Không có unique index thì `INSERT ... ON DUPLICATE KEY UPDATE` trong file seed cũng không hoạt động — nó cần một unique key để phát hiện trùng. Phải thêm index trước.

2. **`base_unit` chỉ được phép là `g` hoặc `ml`.** Seed hiện tại đã vi phạm: `('Trứng gà', 'quả', ...)` ở dòng 262. Mà `unit_conversions` (dòng 250–256) chỉ có kg→g, l→ml, muỗng canh→ml, muỗng cà phê→ml, chén→ml, bát→ml — **không có đường nào dẫn tới `quả`**. Nên `UnitNormalizationService.toBaseUnit()` sẽ ném `BadRequestException` cho mọi công thức dùng trứng với đơn vị khác "quả". Dataset mới phải giữ `g`/`ml` tuyệt đối, và nên sửa luôn dòng trứng gà thành `g` + thêm conversion `quả → g` (~50g/quả, có `ingredient_id` riêng).

3. **Chỉ có 6 aisle, không phủ hết category của dataset.** Danh sách hiện tại: Rau củ quả, Thịt & Gia cầm, Hải sản, Gia vị & Nước chấm, Đồ khô & Gạo, Sữa & Trứng. Không có chỗ cho Trái cây riêng, Đồ uống, Bánh/Snack, Dầu mỡ. Hai lựa chọn: hoặc chỉ giữ nguyên liệu thuộc 6 nhóm này, hoặc thêm 2–3 aisle (Trái cây, Dầu & Chất béo, Đồ uống). Tôi nghiêng về thêm aisle, vì "Rau củ quả" gộp cà chua với chuối sẽ làm tính năng danh sách đi chợ nhóm theo kệ hàng mất ý nghĩa.

---

## Kế hoạch làm sạch — 7 bước

### Về công cụ làm sạch
Với 400 dòng và các bước khử trùng + validate Atwater ở trên, Excel sẽ rất mệt và không lặp lại được. Khuyên dùng một script Python dùng một lần (pandas), đặt ở `tools/clean_ingredients.py`, không commit vào backend — nó không phải phần của ứng dụng. Lợi ích thực tế: khi phát hiện lỗi ở dòng 250, bạn sửa quy tắc rồi chạy lại toàn bộ trong 2 giây thay vì làm lại thủ công. Backend không cần thêm dependency nào.

**Bước 1 — Lọc theo tầng phân loại, không lọc bằng mắt.** Giữ lại chỉ các food category tương ứng nguyên liệu thô. Với USDA SR Legacy, giữ: Dairy and Egg Products, Spices and Herbs, Fats and Oils, Poultry Products, Sausages (bỏ), Finfish and Shellfish Products, Vegetables and Vegetable Products, Fruits and Fruit Juices, Pork Products, Beef Products, Legumes and Legume Products, Cereal Grains and Pasta, Nut and Seed Products. Bỏ toàn bộ: Baked Products, Sweets, Beverages (trừ sữa), Fast Foods, Meals/Entrees, Restaurant Foods, Baby Foods.

**Bước 2 — Bỏ dòng có tên chỉ ra món đã chế biến.** Ngay trong nhóm nguyên liệu vẫn lẫn món nấu. Lọc bỏ theo từ khóa trong tên: `cooked`, `boiled`, `fried`, `baked`, `roasted`, `canned`, `candied`, `breaded`, `with sauce`, `dish`, `casserole`, `salad`. Giữ `raw`. Sau đó bỏ hậu tố `, raw` khỏi tên.

**Bước 3 — Khử trùng lặp về một đại diện.** Táo có 7 biến thể → chọn 1 dòng `raw` làm đại diện, đặt tên `Táo`. Quy tắc: nhóm theo từ khóa gốc của tên, ưu tiên dòng có `raw`, nếu nhiều dòng raw thì lấy dòng có `description` ngắn nhất. Đây là bước tốn công nhất và là chỗ quyết định chất lượng cuối cùng.

**Bước 4 — Ép kiểu và validate 4 cột số.** Với mỗi cột `calories`, `protein`, `fat`, `carbs`: strip khoảng trắng, thay `,` thập phân thành `.`, bỏ ký tự đơn vị dính kèm, chuỗi rỗng/`-`/`N/A` → `0`. Sau đó chạy 3 kiểm tra sanity:
- `0 ≤ calories ≤ 900` (cao nhất là dầu ăn ~884)
- `protein + fat + carbs ≤ 100` (mỗi cột là g/100g, tổng không thể vượt 100)
- Đối chiếu Atwater: `4×protein + 9×fat + 4×carbs` phải xấp xỉ `calories`, sai lệch > 25% thì đánh dấu review tay

Kiểm tra thứ 3 là cái bắt được lỗi lệch cột hoặc lệch đơn vị hiệu quả nhất. Lưu ý dataset Kaggle còn có `iron` và `vitamin_c` — schema không có 2 trường này, drop luôn (đừng mở rộng schema chỉ vì dataset có sẵn cột).

**Bước 5 — Dịch tên sang tiếng Việt, làm theo lô có kiểm soát.** Đừng dán 400 dòng vào một prompt duy nhất — AI hay bỏ dòng hoặc đổi thứ tự, và bạn sẽ không biết dòng nào lệch. Làm thế này:
- Chia lô 50 dòng, mỗi dòng có prefix số thứ tự: `1. Beef, tenderloin`
- Prompt yêu cầu trả về đúng định dạng `số. tên tiếng Việt`, giữ nguyên số
- Sau mỗi lô, assert số dòng trả về = số dòng gửi đi, và số thứ tự khớp
- Chuẩn hóa tên theo cách người Việt gọi trong bếp, không dịch từng chữ: `Beef, tenderloin` → `Thịt bò thăn`, không phải `Bò, thăn`
- Tên phải ≤ 100 ký tự (giới hạn `VARCHAR(100)`)

Sau khi dịch, chạy lại khử trùng trên **tên tiếng Việt** — nhiều tên tiếng Anh khác nhau sẽ dịch về cùng một tên Việt (`Scallion` và `Green onion` đều là `Hành lá`).

**Bước 6 — Đối chiếu với 15 nguyên liệu đang có trong DB.** Seed hiện tại đã có Thịt heo ba chỉ, Ức gà, Trứng gà, Gạo tẻ, Hành tím, Tỏi, Nước mắm, Đường, Cà chua, Rau muống, Tôm sú, Cá hồi, Sữa tươi, Bột mì, Tiêu đen. Phải quyết định: file seed mới ghi đè giá trị dinh dưỡng của chúng, hay bỏ qua. Tôi khuyên ghi đè bằng `ON DUPLICATE KEY UPDATE` để có một nguồn sự thật duy nhất — nhưng chỉ khả thi sau khi đã thêm unique index ở bước 1.

**Bước 7 — Sinh file SQL, không dùng `spring.sql.init.mode: always`.** Kế hoạch trong docs (bước 5, mục 9) đề xuất `data.sql` + `mode: always`. Cách này sẽ chạy lại mỗi lần khởi động app và nhân bản dữ liệu, vì project dùng `ddl-auto: update` (`application.yaml` dòng 17) và seed qua Docker mount (`docker-compose.yml` dòng 15), không phải qua Spring SQL init. Thay bằng: tạo `sql/seed_ingredients.sql`, chạy một lần bằng `docker exec`.
Yêu cầu bắt buộc cho file này — `sql/` đã có tới 4 file `fix_*.sql` mà theo tên gọi là để sửa dữ liệu tiếng Việt bị lỗi, nên charset là rủi ro đã từng xảy ra:
- Lưu UTF-8 **không BOM**
- Mở đầu bằng `SET NAMES utf8mb4;`
- Dùng `INSERT ... ON DUPLICATE KEY UPDATE` để chạy lại được nhiều lần
- Escape dấu nháy đơn trong tên (`Bơ đậu phộng` an toàn, nhưng tên có `'` thì phải `\'`)

---

## Thứ tự thực thi đề xuất

1. Thêm unique index `ingredients.name` + sửa `base_unit` của Trứng gà + thêm conversion `quả → g`
2. Chốt danh sách aisle (giữ 6 hay thêm 3)
3. Tải USDA SR Legacy, viết script làm sạch, chạy bước 1–4
4. Dịch tên theo lô, khử trùng lần 2
5. Sinh `sql/seed_ingredients.sql`, chạy qua `docker exec`, verify `SELECT COUNT(*)` + kiểm tra ngẫu nhiên 10 dòng xem tiếng Việt có hiển thị đúng
6. Sau khi có backbone rồi mới sửa matching trong `AiServiceImpl` — vì logic matching cần dataset thật để test cho có ý nghĩa. 

*Điểm 6 quan trọng: hiện `AiServiceImpl:218` dùng `findByNameContainingIgnoreCase` rồi lấy `matches.get(0)`, nên AI trả "Hành" sẽ match sai vào "Hành tím". Với 15 nguyên liệu thì lỗi này ít lộ; với 400 nguyên liệu thì nó sẽ sai thường xuyên. Sửa sau khi có dataset sẽ test được thực chất.*

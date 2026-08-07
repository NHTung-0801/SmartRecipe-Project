# 🎨 TÀI LIỆU YÊU CẦU THIẾT KẾ GIAO DIỆN (UI/UX DESIGN BRIEF)

**Tên dự án:** Smart Recipe & Grocery Platform (Nền tảng Quản lý và Chia sẻ Công thức Nấu ăn Thông minh tích hợp AI)
**Nền tảng:** Web Application (Responsive cho cả Desktop, Tablet và Mobile - Ưu tiên Mobile-first).

---

## 1. TỔNG QUAN DỰ ÁN & MỤC TIÊU THIẾT KẾ

**Smart Recipe** đóng vai trò như một "trợ lý bếp núc cá nhân". Hệ thống giúp người dùng quản lý công thức, tính toán lượng Calo/Dinh dưỡng tự động, quản lý kho nguyên liệu trong tủ lạnh và kết nối với cộng đồng. Đặc biệt, ứng dụng có tích hợp AI để gợi ý món ăn từ đồ thừa trong tủ lạnh (Zero-Waste).

**🎨 Phong cách thiết kế (Design Vibe):**
- **Hiện đại & Ấm cúng (Modern & Cozy):** Mang lại cảm giác như bước vào một gian bếp thông minh nhưng rất gần gũi, ấm áp. Thiết kế không quá "công nghiệp" mà thiên về sự mềm mại, thân thiện.
- **Kích thích vị giác & Cảm xúc:** Sử dụng hình ảnh tràn viền, bo góc tròn (border-radius lớn) kết hợp với đổ bóng siêu mềm (soft drop-shadows) để các thành phần như nổi lên mặt trang.
- **Màu sắc (Color Palette - Tông Ấm):**
  - *Primary:* Màu Cam Đất (Terracotta), Vàng Gỗ (Wood), hoặc Be (Beige) để tạo sự ấm cúng.
  - *Background:* Màu kem sữa hoặc trắng ngà (Off-white/Cream) thay vì trắng tinh (pure white) để tránh chói mắt. Có thể dùng gradient rất nhạt làm nền.
- **Thành phần UI (UI Elements):** 
  - Ưu tiên Glassmorphism (Kính mờ) nhưng với tông ấm và độ blur mượt mà. 
  - Các đường viền mỏng (hairline borders) để phân tách nội dung thanh lịch.

---

## 2. CÁC THÀNH PHẦN CHUNG (GLOBAL COMPONENTS)

1. **Thanh điều hướng (Navbar / Sidebar):**
   - *Desktop:* Top Navbar hoặc Sidebar cố định bên trái.
   - *Mobile:* Bottom Navigation Bar (Home, Pantry, Grocery, AI Assistant, Profile) để tiện thao tác bằng ngón cái.
2. **Cards (Thẻ nội dung):**
   - **Recipe Card (Thẻ công thức):** Hình món ăn lớn, tên món, avatar tác giả, lượt like, thẻ tag (VD: Keto, Vegan), thời gian nấu, và lượng Calo.
   - **Ingredient Card (Thẻ nguyên liệu):** Hình icon nguyên liệu, tên, số lượng tồn kho, cảnh báo sắp hết (màu đỏ/vàng).
3. **Empty States & Skeletons:**
   - Hình minh họa dễ thương khi tủ lạnh trống, hoặc khi chưa có công thức nào.
   - Khung xương (Skeleton loader) nhấp nháy khi đang chờ gọi API.

---

## 3. CHI TIẾT TỪNG MÀN HÌNH (SCREEN-BY-SCREEN REQUIREMENTS)

### Module 1: Xác thực & Hồ sơ (Auth & Profiles)
- **1.1. Login / Register:**
  - Split-screen (Desktop): Một nửa là hình ảnh món ăn đẹp mắt ngẫu nhiên, một nửa là Form đăng nhập.
  - Hỗ trợ nút "Đăng nhập bằng Google/Facebook" (dự trù UI).
- **1.2. My Profile:**
  - Ảnh Cover (Cover photo) và Ảnh đại diện (Avatar - hình tròn).
  - Các thống kê: Số công thức đã tạo, Số người theo dõi.
  - Tab view: Lịch sử nấu ăn (Journal), Công thức đã lưu (Saved Recipes).

### Module 2: Cộng đồng & Khám phá (Community Feed)
- **2.1. Home / Explore (Bảng tin):**
  - **Hero Section:** Thanh tìm kiếm lớn ở giữa màn hình (Tìm món ăn, nguyên liệu...).
  - **Quick Filters (Chip buttons):** Dưới thanh tìm kiếm là các bộ lọc nhanh (Ăn sáng, Giảm cân, Dưới 30 phút, Đồ ngọt...).
  - **Feed:** Danh sách các `Recipe Card` trình bày dạng Grid (Desktop) hoặc List cuộn dọc (Mobile).
  - Nút **"Clone (Lưu về sổ tay)"** hiển thị rõ ràng trên mỗi card.

### Module 3: Chi tiết & Khởi tạo Công thức (Recipe Engine)
- **3.1. Chi tiết Công thức (Recipe Detail Page):**
  - *Phần đầu:* Ảnh món ăn tràn viền (Hero Image), tiêu đề, tên tác giả, nút Like/Share/Clone.
  - *Thống kê Dinh dưỡng:* Hiển thị dạng biểu đồ tròn nhỏ hoặc các khối vuông (Calories, Protein, Fat, Carbs).
  - *Phần thân (Chia 2 cột trên Desktop, cuộn dọc trên Mobile):*
    - **Cột Trái (Nguyên liệu):** Checklist nguyên liệu (có checkbox để tick khi đang đi mua hoặc chuẩn bị).
    - **Cột Phải (Cách làm):** Các bước nấu (Step 1, Step 2...) được thiết kế nổi bật. Có chế độ **"Cooking Mode"** (Focus Mode: Màn hình tối đi, chữ to ra, chỉ vuốt qua lại từng bước một để xem lúc tay đang ướt).
- **3.2. Form Tạo Công thức (Multi-step Form):**
  - Giao diện nhập liệu chia làm nhiều bước có thanh Progress Bar ở trên:
    - *Bước 1:* Thông tin (Tên, Ảnh cover, Độ khó, Thời gian).
    - *Bước 2:* Thêm nguyên liệu (Ô search Autocomplete, chọn định lượng, đơn vị).
    - *Bước 3:* Thêm các bước nấu (Có thể kéo thả xếp lại thứ tự - Drag & Drop).
    - *Bước 4:* Preview & Đăng tải (Chọn Public/Private).

### Module 4: Tủ lạnh ảo (Virtual Pantry)
- **4.1. My Pantry (Kho nguyên liệu):**
  - Giao diện chia theo nhóm / quầy (Aisle): Thịt cá, Rau củ, Đồ khô, Gia vị.
  - **Cảnh báo tồn kho:** Những món sắp hết sẽ có highlight màu vàng/đỏ.
  - Ô "Quick Add": Nút scan Barcode (giả lập UI) hoặc gõ nhanh tên nguyên liệu nạp vào tủ.
  - Cấu trúc thẻ nhỏ (Mini-card) cho từng nguyên liệu để tiết kiệm diện tích.

### Module 5: Đi chợ Thông minh (Smart Grocery List)
- **5.1. Grocery List Page:**
  - Giao diện dạng Checklist (To-do list).
  - Các nguyên liệu tự động được gom nhóm theo quầy hàng (Aisle) để người dùng đi siêu thị không phải đi vòng vèo. VD: Nhóm rau củ (Cà chua, Hành tây) xếp cạnh nhau.
  - Nút tick "Đã mua". Sau khi đi chợ xong, bấm "Hoàn tất & Cập nhật Tủ lạnh" (có hiệu ứng pháo giấy/confetti thành công).

### Module 6: Trợ lý AI (AI Assistant & Zero-Waste)
- **6.1. Màn hình AI Chat / Gợi ý món ăn:**
  - Giao diện giống cửa sổ Chatbot (Tương tự ChatGPT).
  - Các nút gợi ý nhanh (Prompts): "Tôi còn 2 quả trứng và 1 quả cà chua, tôi có thể nấu gì?", "Gợi ý mâm cơm 50k".
  - *Kết quả trả về:* AI render ra một `Recipe Card` đặc biệt. Có nút bấm "Lưu thành công thức cá nhân" ngay bên dưới.

---

## 4. TƯƠNG TÁC & HIỆU ỨNG ĐỘNG (DYNAMIC ANIMATIONS & MICRO-INTERACTIONS)
Để ứng dụng có cảm giác cao cấp (Premium feel) và vô cùng đẹp mắt, Designer cần thiết kế chi tiết các hiệu ứng chuyển động sau:

1. **Staggered Animations (Hiệu ứng xuất hiện nối tiếp):** Khi vào trang Home hoặc List Công thức, các Recipe Cards không xuất hiện cùng lúc, mà trượt lên (fade-in & slide-up) lần lượt từng thẻ một (delay ~50ms).
2. **Hover & Parallax Effects:** 
   - Khi trỏ chuột vào `Recipe Card`, ảnh món ăn sẽ từ từ scale (zoom in nhẹ), đồng thời thẻ tự động nổi bổng lên (shadow đậm và lớn hơn).
   - Hiệu ứng Parallax nhẹ ở các banner lớn (Hero Image) khi cuộn trang.
3. **Thả tim (Heart Burst):** Khi bấm nút Like/Lưu, icon trái tim không chỉ đổi màu mà phải có hiệu ứng nổ (burst/pop) văng ra các hạt nhỏ (particles), kết hợp rung nhẹ (haptic feedback mô phỏng).
4. **Liquid / Morphing Transitions:** Khi mở Modal (ví dụ: xem chi tiết ảnh), card tự biến đổi hình khối (morph) mượt mà phóng to thành một trang toàn màn hình (Hero transition).
5. **Kéo thả mượt mà (Smooth Drag & Drop):** Trong màn hình tạo công thức, khi kéo thả đổi vị trí các bước nấu, các phần tử xung quanh tự động trượt mềm mại để nhường chỗ, không bị giật cục.
6. **Dynamic Skeletons:** Skeleton loader không chỉ nhấp nháy xám nhàm chán, mà có hiệu ứng ánh sáng lướt qua (Shimmer effect) lấp lánh như sóng nước tông màu kem ấm.
7. **Success Confetti:** Bắn pháo giấy rực rỡ khi tạo xong một công thức mới hoặc mua xong danh sách đi chợ, tạo cảm giác thành tựu (gamification) cho người dùng.

## 5. FILE BÀN GIAO YÊU CẦU TỪ DESIGNER
- **Figma File:** Chứa toàn bộ các màn hình (Desktop & Mobile).
- **Design System / Style Guide:** Định nghĩa rõ màu sắc (Hex codes), Typography (Tên font, kích cỡ Heading, Body), Icons set (Dùng bộ icon nào: Lucide, Phosphor, FontAwesome...).
- **Component Library:** Chứa các components có thể tái sử dụng (Buttons, Inputs, Cards) với đầy đủ các trạng thái (Normal, Hover, Disabled, Error).

# 🍳 SmartRecipe & Grocery Platform

> **Nền tảng Quản lý Thực đơn, Tủ nguyên liệu Thông minh & Đi chợ Tối ưu**  
> *Đồ án Thực tập Tốt nghiệp (TTTN) — Trường Đại học Giao thông Vận tải TP. Hồ Chí Minh (UTH)*  
> Tích hợp sâu **Google Gemini AI**, quy đổi đơn vị theo đồ thị BFS, cơ chế trừ kho theo hạn dùng (FEFO) và Trung tâm Quản trị (Admin Portal) toàn diện.

---

## 🌐 Trải nghiệm Trực tuyến & Liên kết Triển khai (Live Demo)

Hệ thống đã được đóng gói container và triển khai thành công trên môi trường **Cloud Production (Hybrid Cloud)**:

| Thành phần | Môi trường Triển khai | Trạng thái | Đường dẫn Trực tiếp |
|---|---|:---:|---|
| **Frontend Web App** | **Vercel Edge CDN** | ![Deploy](https://img.shields.io/badge/Vercel-Live-brightgreen?logo=vercel) | [🌐 smartrecipe-platform.vercel.app](https://smartrecipe-platform.vercel.app) |
| **Backend REST API** | **Render Web Service (Docker)** | ![Deploy](https://img.shields.io/badge/Render-Active-brightgreen?logo=render) | [⚡ smartrecipe-backend.onrender.com/api/v1](https://smartrecipe-backend.onrender.com/api/v1) |
| **API Health Check** | **Spring Boot Actuator** | ![Health](https://img.shields.io/badge/Health-UP-brightgreen) | [🩺 /actuator/health](https://smartrecipe-backend.onrender.com/actuator/health) |
| **Database Cloud** | **TiDB Cloud Serverless** | ![Database](https://img.shields.io/badge/TiDB-Distributed%20MySQL-blue?logo=mysql) | Cluster Serverless (19 bảng · Collation chuẩn) |
| **In-Memory Cache** | **Upstash Redis** | ![Redis](https://img.shields.io/badge/Upstash-Redis%207%20TLS-red?logo=redis) | Cache phân tán, Rate Limiting, OTP Session |

> 💡 **Tài khoản Trải nghiệm Nhanh:**
> - **Người dùng thường (User):** `kiritohackiem05` (hoặc đăng ký tài khoản mới miễn phí)
> - **Quản trị viên (Admin):** `admin` (truy cập cổng quản trị tại `/admin/login`)

---

## 🧭 Khám phá 2 Trụ cột Dự án: Backend & Frontend

Dự án được tổ chức theo kiến trúc **Umbrella Repository** quản lý 2 kho mã nguồn độc lập thông qua **Git Submodules**. Hãy truy cập tài liệu chi tiết của từng phần:

```
SmartRecipe-Project (Root Umbrella)
├── 📦 smartrecipe-backend/   ──► RESTful API, AI Engine, FEFO Pantry, 15 Controllers, 48 Tests
└── 🎨 smartrecipe-frontend/  ──► React 19 SPA, 21 Màn hình (Admin + User), TanStack Query, 17 Tests
```

<table width="100%">
<tr>
<td width="50%" valign="top">

### ⚙️ [smartrecipe-backend/](https://github.com/NHTung-0801/smartrecipe-backend)
**Spring Boot 4.1.0 & Java 21 LTS**
- **15 REST Controllers & 19 JPA Repositories**
- **Google Gemini AI Engine:** Gợi ý thực đơn Zero-Waste & Custom Prompt
- **Thuật toán Khớp nguyên liệu 3 lớp:** Exact $\rightarrow$ Token Match $\rightarrow$ Auto-Create
- **Quy đổi đơn vị bằng Đồ thị BFS:** Chuẩn hóa thìa, muỗng, bát, quả về `g` / `ml`
- **Trừ kho thông minh FEFO:** Tự động xuất lô nguyên liệu cận date trước khi nấu
- **Bảo mật:** Stateless JWT (24h/7d) + Xác thực OTP Email qua Gmail SMTP
- **Admin Portal API:** Dashboard KPI, kiểm duyệt công thức, phân quyền an toàn
- **Kiểm thử tự động:** **48 Unit Tests** độc lập (JUnit 5 + Mockito)

👉 **[Đọc tài liệu Backend API chi tiết](https://github.com/NHTung-0801/smartrecipe-backend#readme)**

</td>
<td width="50%" valign="top">

### 🎨 [smartrecipe-frontend/](https://github.com/NHTung-0801/smartrecipe-frontend)
**React 19, Vite 8 & Tailwind CSS v4**
- **21 Trang Giao diện:** 15 trang người dùng + 6 trang Admin Portal chuyên sâu
- **Thiết kế Ấm áp Độc bản:** Tone màu gạch nung `#a13923`, card bo góc mềm mại
- **Chế độ Nấu ăn Từng bước (Cooking Mode):** Giao diện rảnh tay, hẹn giờ tích hợp
- **Shopping Mode & Confetti:** Trải nghiệm đi chợ toàn màn hình với hiệu ứng ăn mừng
- **Đồng bộ Dữ liệu Tối ưu:** TanStack Query v5 + Zustand (Auth persistence)
- **Cơ chế Token Refresh Tự động:** Axios Interceptor với hàng đợi chống race-condition
- **Kiểm thử giao diện:** **17 Vitest Tests** (Testing Library + jsdom)

👉 **[Đọc tài liệu Frontend UI/UX chi tiết](https://github.com/NHTung-0801/smartrecipe-frontend#readme)**

</td>
</tr>
</table>

---

## 📋 Mục lục

- [Trải nghiệm Trực tuyến & Liên kết Triển khai (Live Demo)](#-trải-nghiệm-trực-tuyến--liên-kết-triển-khai-live-demo)
- [Khám phá 2 Trụ cột Dự án: Backend & Frontend](#-khám-phá-2-trụ-cột-dự-án-backend--frontend)
- [Hệ thống Repositories (Git Submodules)](#-hệ-thống-repositories-git-submodules)
- [Bài toán & Đối tượng phục vụ](#-bài-toán--đối-tượng-phục-vụ)
- [Kiến trúc Tổng thể Hệ thống (End-to-End)](#-kiến-trúc-tổng-thể-hệ-thống-end-to-end)
- [Hệ thống 6 Module Cốt lõi](#-hệ-thống-6-module-cốt-lõi)
- [Tech Stack Toàn diện](#-tech-stack-toàn-diện)
- [Cấu trúc Thư mục Dự án](#-cấu-trúc-thư-mục-dự-án)
- [Tiến độ Dự án (6 Sprints Hoàn thiện)](#-tiến-độ-dự-án-6-sprints-hoàn-thiện)
- [Pipeline Dữ liệu Nguyên liệu (USDA FoodData Central)](#-pipeline-dữ-liệu-nguyên-liệu-usda-fooddata-central)
- [Mô hình Cơ sở Dữ liệu (19 Bảng)](#-mô-hình-cơ-sở-dữ-liệu-19-bảng)
- [Hướng dẫn Cài đặt & Chạy cục bộ](#-hướng-dẫn-cài-đặt--chạy-cục-bộ)
  - [Cách 1: Chạy Full-stack với Docker Compose](#cách-1-chạy-full-stack-với-docker-compose-nhanh-nhất)
  - [Cách 2: Chạy Tách biệt cho Lập trình viên (Developer Mode)](#cách-2-chạy-tách-biệt-cho-lập-trình-viên-developer-mode)
- [Nạp & Chạy lại Data Pipeline (Python Tools)](#-nạp--chạy-lại-data-pipeline-python-tools)
- [Hệ thống Kiểm thử Tự động (65 Tests)](#-hệ-thống-kiểm-thử-tự-động-65-tests)
- [Biến môi trường (Environment Variables)](#-biến-môi-trường-environment-variables)
- [Quy trình Triển khai CI/CD (GitHub Actions)](#-quy-trình-triển-khai-cicd-github-actions)
- [Tài liệu Chi tiết Tham khảo](#-tài-liệu-chi-tiết-tham-khảo)
- [Tác giả & Bản quyền](#-tác-giả--bản-quyền)

---

## 🔗 Hệ thống Repositories (Git Submodules)

Dự án được tổ chức theo kiến trúc **Umbrella Repository** quản lý 2 kho mã nguồn độc lập thông qua **Git Submodules**:

| Repository | GitHub Link | Công nghệ chính | Vai trò |
|---|---|---|---|
| **Mẹ (Root)** | [SmartRecipe-Project](https://github.com/NHTung-0801/SmartRecipe-Project) | Git Submodules, Docker Compose | Quản lý tài liệu tổng thể, data pipeline USDA, orchestration toàn dự án |
| **Backend** | [smartrecipe-backend](https://github.com/NHTung-0801/smartrecipe-backend) | Spring Boot 4.1.0, Java 21, TiDB / MySQL, Redis | Cung cấp RESTful API, AI Gemini integration, Auth JWT, Business logic |
| **Frontend** | [smartrecipe-frontend](https://github.com/NHTung-0801/smartrecipe-frontend) | React 19, Vite 8, Tailwind v4, Zustand | Giao diện người dùng SPA, trải nghiệm nấu ăn, AI Assistant UI, Admin Portal |

> 💡 **Cách clone trọn vẹn cả 3 repository trong 1 lệnh:**
> ```bash
> git clone --recurse-submodules https://github.com/NHTung-0801/SmartRecipe-Project.git
> ```
> *Nếu đã clone trước đó mà chưa có submodule, chỉ cần chạy:* `git submodule update --init --recursive`

---

## 🎯 Bài toán & Đối tượng phục vụ

### 3 Nỗi đau thường trực trong căn bếp hiện đại:
1. **"Hôm nay nấu gì?"**: Người nội trợ mất từ 30-45 phút mỗi ngày suy nghĩ thực đơn phù hợp với các nguyên liệu tản mát trong tủ lạnh.
2. **Lãng phí thực phẩm (Food Waste)**: Thực phẩm mua về hay bị bỏ quên ở góc tủ, hết hạn sử dụng và buộc phải vứt bỏ, gây lãng phí kinh tế và tạo gánh nặng môi trường.
3. **Đi chợ rời rạc**: Mua sắm không kế hoạch dẫn đến việc mua thừa món đã có hoặc quên gia vị thiết yếu, phải đi lại nhiều lần.

### Đối tượng phục vụ
| Nhóm đối tượng | Nhu cầu & Lợi ích |
|---|---|
| **Người nội trợ, gia đình trẻ** | Tự nấu tại nhà, quản lý hạn dùng thực phẩm, tiết kiệm thời gian lên thực đơn và mua sắm |
| **Sinh viên, dân văn phòng** | Nấu ăn tiện lợi, chống lãng phí đồ ăn thừa, gợi ý món nhanh theo nguyên liệu sẵn có |
| **Người quan tâm sức khỏe / Eat Clean** | Kiểm soát lượng Calo và Macro (Đạm, Béo, Tinh bột) chính xác theo gram thực tế |
| **Cộng đồng đầu bếp gia đình** | Chia sẻ công thức, tìm kiếm cảm hứng, tương tác mạng xã hội và lưu nhật ký nấu nướng |

---

## 🏛 Kiến trúc Tổng thể Hệ thống (End-to-End)

```
                               ┌─────────────────────────────────────────┐
                               │             CLIENT BROWSER              │
                               │        Desktop / Tablet / Mobile        │
                               └────────────────────┬────────────────────┘
                                                    │ HTTPS
                               ┌────────────────────▼────────────────────┐
                               │           VERCEL EDGE NETWORK           │
                               │  • React 19 SPA (Static Hosting)        │
                               │  • Client-side Routing (React Router 7) │
                               │  • TanStack Query Server-State Cache    │
                               │  • Axios Interceptor + Token Refresh    │
                               └────────────────────┬────────────────────┘
                                                    │ HTTPS / JSON API (Bearer JWT)
                               ┌────────────────────▼────────────────────┐
                               │        RENDER.COM (Docker Container)    │
                               │  • Spring Boot 4.1.0 / Eclipse Temurin  │
                               │  • Spring Security + Stateless JWT      │
                               │  • 15 REST Controllers / 18 Services   │
                               │  • BFS Unit Normalization & FEFO Engine │
                               │  • Global Exception Handler             │
                               └───────┬─────────────┬─────────────┬─────┘
                                       │             │             │
                    ┌──────────────────┘             │             └──────────────────┐
                    ▼ JDBC                           ▼ Redis Protocol                 ▼ HTTPS
┌──────────────────────────────────────┐  ┌──────────────────────┐  ┌───────────────────────────────────┐
│     TiDB CLOUD (Serverless MySQL)    │  │  UPSTASH REDIS 7     │  │        EXTERNAL CLOUD SERVICES    │
│  • 19 Quan hệ bảng ACID              │  │  • Master Data Cache │  │  • Google Gemini 2.0 Flash AI     │
│  • Collation: utf8mb4_unicode_ci     │  │  • AI Daily Limit    │  │  • Cloudinary CDN (Lưu trữ ảnh)   │
│  • 297 Nguyên liệu USDA & Việt Nam   │  │  • OTP Session (5m)  │  │  • Gmail SMTP TLS (Gửi mã OTP)    │
└──────────────────────────────────────┘  └──────────────────────┘  └───────────────────────────────────┘
```

---

## 🌟 Hệ thống 6 Module Cốt lõi

| # | Phân hệ (Module) | Công nghệ chính | Tính năng nổi bật |
|:---:|---|---|---|
| **1** | **Xác thực & Mạng xã hội** | JWT, Redis, Gmail SMTP | Đăng ký, đăng nhập, cấp lại access token tự động, khôi phục mật khẩu bằng OTP qua email, theo dõi tác giả (Follow/Unfollow), trang cá nhân công khai. |
| **2** | **Quản lý Kho Tủ lạnh (Pantry)** | Spring Data JPA, FEFO Engine | Nhóm nguyên liệu theo 9 quầy hàng siêu thị, tự động cộng dồn số lượng, tính ngày hết hạn, thanh cảnh báo cận hạn, dọn sạch đồ hỏng 1-click. |
| **3** | **Trợ lý AI Ẩm thực (Gemini)** | Google Gemini API, Redis | Chế độ gợi ý Zero-Waste (tận dụng đồ cận date) và Chế độ gợi ý tự do; lưu công thức AI vào hệ thống qua Thuật toán Khớp nguyên liệu 3 lớp; giới hạn 10 lượt/ngày. |
| **4** | **Công thức & Chế biến** | Apache POI, Cloudinary | Đăng tải công thức kèm hình ảnh từng bước; tính toán dinh dưỡng động theo gram; Chế độ nấu ăn (Cooking Mode) toàn màn hình; sao chép (clone) công thức; xuất file Word (`.docx`). |
| **5** | **Đi chợ Thông minh (Grocery)** | BFS Graph Normalization | Tự động tính toán (Cần - Có = Mua) từ thực đơn chọn nấu; quy đổi đa bước mọi đơn vị đo; Shopping Mode tick chọn khi mua hàng; tự động đồng bộ vào tủ khi hoàn tất. |
| **6** | **Trung tâm Quản trị (Admin Portal)** | Spring Security Role, Dashboard KPI | Dashboard chỉ số lãng phí thực phẩm; hàng đợi duyệt công thức cộng đồng; chuẩn hóa dinh dưỡng cho nguyên liệu mới do AI tạo ra; quản lý tài khoản có chốt an toàn. |

---

## 🛠 Tech Stack Toàn diện

### Frontend (Client-side & Admin Portal)
| Công nghệ | Phiên bản | Vai trò & Mục đích |
|---|:---:|---|
| **React** | `19.2` | UI Framework hiện đại nhất, tận dụng React Compiler & Server Actions |
| **Vite** | `8.2` | Build tool siêu tốc + Hot Module Replacement (HMR) |
| **React Router DOM** | `7.18` | Định tuyến client-side, bảo vệ route phân quyền (User / Admin) |
| **TanStack Query** | `5.101` | Quản lý server-state, caching, background refetching, optimistic updates |
| **Zustand** | `5.0` | Quản lý client-state (Auth, User Session, Local Storage sync) |
| **Axios** | `1.19` | HTTP Client + Interceptor tự động làm mới JWT Token khi hết hạn |
| **React Hook Form + Zod** | `7.84 / 4.4` | Quản lý form hiệu năng cao, xác thực schema chuẩn hóa |
| **Tailwind CSS v4** | `4.3` | Utility styling thế hệ mới, tối ưu hóa CSS bundle |
| **Lucide React** | `1.28` | Thư viện icon đồng bộ, sắc nét |
| **Vitest + Testing Library**| `4.1 / 16.3`| 17 ca kiểm thử giao diện trong môi trường jsdom |

### Backend (RESTful API & Microservices)
| Công nghệ | Phiên bản | Vai trò & Mục đích |
|---|:---:|---|
| **Spring Boot** | `4.1.0` | Framework lõi cho hệ thống RESTful API |
| **Java LTS** | `21` | Tận dụng Virtual Threads, Pattern Matching, Record |
| **Spring Data JPA** | Hibernate 6 | Mapping thực thể quan hệ, custom native queries |
| **Spring Security + JJWT**| `0.11.5` | Stateless Authentication, bộ lọc JwtAuthFilter, mã hóa BCrypt |
| **Spring Data Redis** | `7.x` | Bộ đệm tầng ứng dụng, Rate Limit gọi AI, phiên OTP 5 phút |
| **Google Gemini API** | `gemini-2.0-flash` | Trợ lý AI gợi ý món ăn Zero-Waste từ ảnh & tủ lạnh |
| **Spring Mail** | Gmail SMTP | Gửi mã OTP khôi phục mật khẩu qua cổng TLS 587 |
| **Cloudinary** | `1.36.0` | CDN lưu trữ và tối ưu hóa hình ảnh món ăn, avatar |
| **Apache POI** | `5.2.3` | Xuất tài liệu công thức ra file Word (`.docx`) chuẩn format |
| **dotenv-java** | `3.0.0` | Tự động nạp biến môi trường từ file `.env` |
| **JUnit 5 + Mockito** | `5.x` | 48 ca kiểm thử đơn vị độc lập hoàn toàn với database |

### Hạ tầng & Triển khai Đám mây
| Công nghệ | Vai trò & Nền tảng |
|---|---|
| **Docker & Docker Compose** | Đóng gói container multi-stage cho cả 4 services local |
| **Vercel Edge Network** | Hosting Frontend React 19 với CDN phân tán toàn cầu |
| **Render Web Service** | Hosting Backend Spring Boot 4 trên nền Docker Alpine |
| **TiDB Cloud Serverless** | Cơ sở dữ liệu phân tán tương thích chuẩn MySQL 8.0 |
| **Upstash Redis** | Caching và lưu trữ phiên phân tán hỗ trợ giao thức SSL |
| **GitHub Actions** | Tự động hóa kiểm thử (CI) và triển khai liên tục (CD) |

---

## 📁 Cấu trúc Thư mục Dự án

```
SmartRecipe-Project/                      # 🔗 Umbrella Repository
│
├── smartrecipe-backend/                  # 🔗 Git Submodule → github.com/NHTung-0801/smartrecipe-backend
│   ├── src/main/java/                    # Source code Java 21 (15 Controllers, 19 Entities, 18 Services)
│   ├── src/main/resources/               # application.yaml & seed data
│   ├── src/test/java/                    # 48 Unit Test Suites (JUnit 5 + Mockito)
│   ├── .docker/Dockerfile                # Production Docker image (Render/Cloud)
│   ├── .env                              # Biến môi trường local (nạp qua dotenv-java, git-ignored)
│   ├── pom.xml                           # Maven dependencies
│   └── README.md                         # ← [Chi tiết kiến trúc & API Backend](./smartrecipe-backend/README.md)
│
├── smartrecipe-frontend/                 # 🔗 Git Submodule → github.com/NHTung-0801/smartrecipe-frontend
│   ├── src/                              # Source code React 19 SPA (21 trang, 35+ components)
│   ├── src/test/                         # 17 Vitest Test Suites
│   ├── vite.config.js                    # Vite 8 bundle configuration
│   ├── package.json                      # Dependencies & NPM scripts
│   └── README.md                         # ← [Chi tiết kiến trúc & Component Frontend](./smartrecipe-frontend/README.md)
│
├── sql/                                  # Database migration scripts
│   ├── init_database.sql                 # Khởi tạo 19 bảng + 9 kệ + 12 tags + unit conversions
│   ├── seed_ingredients.sql              # 290 nguyên liệu gốc từ USDA (sinh bởi tools/)
│   └── export_local_data.sql             # Snapshot đầy đủ: 297 nguyên liệu, 9 recipes, 15 journals, 53 pantry items
│
├── Dataset/                              # Dữ liệu gốc USDA FoodData Central
│   ├── FoodData_Central_sr_legacy_food_csv_2018-04/
│   │   ├── food.csv                      # ~8.000 thực phẩm thô
│   │   ├── food_nutrient.csv             # ~600.000 dòng dinh dưỡng (36 MB)
│   │   ├── food_category.csv             # 25 nhóm thực phẩm
│   │   ├── nutrient.csv                  # Định nghĩa 150+ chất dinh dưỡng
│   │   └── food_portion.csv              # Khẩu phần tham chiếu
│   ├── ingredients_to_translate.csv      # 290 nguyên liệu sau xử lý (đã dịch tiếng Việt)
│   └── dropped_ingredients.csv           # ~1.500 nguyên liệu đã loại + lý do
│
├── tools/                                # Python data pipeline scripts (USDA → Vietnamese Dataset)
│   ├── clean_ingredients.py              # Giai đoạn 1: Lọc + join dinh dưỡng từ USDA
│   ├── suggest_keep.py                   # Giai đoạn 2: Luật lọc nguyên liệu phù hợp bếp Việt
│   ├── collapse_groups.py                # Giai đoạn 2: Gộp nhóm biến thể (bò xay 70% → bò xay)
│   ├── export_batches.py                 # Giai đoạn 2: Chia batch để dịch thủ công
│   ├── translate_helper.py               # Giai đoạn 2: Hỗ trợ dịch Anh → Việt
│   ├── assign_aisles.py                  # Giai đoạn 3: Gán 9 kệ hàng theo 2 lớp logic
│   ├── add_missing_essentials.py         # Thêm nguyên liệu thiết yếu bị lọc nhầm
│   ├── add_salmon.py                     # Thêm Cá hồi từ USDA fdc_id 175167
│   ├── repair_csv.py                     # Sửa CSV bị Excel làm hỏng encoding
│   ├── verify_dataset.py                 # Kiểm tra toàn vẹn dataset trước khi seed
│   └── gen_seed_sql.py                   # Giai đoạn 4: Sinh seed_ingredients.sql
│
├── docs/                                 # Tài liệu kế hoạch & kiến trúc
│   ├── project_master_plan.md            # Kế hoạch tổng thể 6 Sprints
│   └── BaoCaoThucTapTotNghiep_*.docx     # Báo cáo Thực tập Tốt nghiệp chính thức
│
├── .github/workflows/                    # CI/CD Workflows
│   ├── ci-backend.yml                    # CI: Test & Build JAR
│   └── cd-backend.yml                    # CD: Trigger Render Deploy Hook
│
├── .gitmodules                           # Đăng ký Git Submodules cho backend và frontend
├── docker-compose.yml                    # Định nghĩa 4 services (mysql, redis, backend, frontend)
└── README.md                             # ← File tài liệu tổng quan này
```

---

## 📊 Tiến độ Dự án (6 Sprints Hoàn thiện)

Chiến lược phát triển: **Backend trước → Frontend sau** cho mỗi Sprint. Toàn bộ 6 Sprints đã hoàn tất 100%:

```
Sprint 1 ████████████████████ 100%  Auth & Security (JWT, Login, Register)
Sprint 2 ████████████████████ 100%  Users, Profile, Master Data, Redis Cache
Sprint 3 ████████████████████ 100%  Recipe Engine (CRUD, Feed, Clone, Export Word)
Sprint 4 ████████████████████ 100%  Pantry & Smart Grocery List (Quy đổi đơn vị BFS)
Sprint 5 ████████████████████ 100%  AI Assistant, Unit Normalization, Dynamic Nutrition, Journal
Sprint 6 ████████████████████ 100%  CI/CD Pipeline, Cloud Deployment (Vercel + Render + TiDB)
```

### ✅ Sprint 1 — Auth & Security
- JWT Access Token (24h) + Refresh Token (7d) + cơ chế tự động refresh token phía client chống race-condition.
- `SecurityConfig`, `JwtProvider`, `JwtAuthFilter`.
- API: `POST /auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/forgot-password`, `/auth/reset-password`.
- UI: `LoginPage.jsx`, `RegisterPage.jsx`, `ForgotPasswordPage.jsx`, `ResetPasswordPage.jsx`, `ProtectedRoute`.

### ✅ Sprint 2 — Users & Master Data
- Quản lý profile, đổi mật khẩu, xóa tài khoản, upload avatar qua Cloudinary.
- Redis Cache cho Master Data (`ingredients`, `aisles`, `tags`, `unit_conversions`).
- Component `IngredientAutocomplete` + `UnitAutocomplete` phía frontend.

### ✅ Sprint 3 — Recipe Engine
- CRUD công thức (DRAFT / PRIVATE / PUBLIC / DELETED soft-delete).
- Feed cộng đồng phân trang, tìm kiếm theo tên/tag/nguyên liệu.
- Clone công thức, Like/Unlike, bình luận đa cấp.
- Chế độ nấu step-by-step (`CookingMode.jsx`) toàn màn hình.
- Xuất công thức ra file Word `.docx` chuyên nghiệp (Apache POI).
- 7/7 unit tests Recipe service xanh (JUnit 5 + Mockito).

### ✅ Sprint 4 — Pantry & Smart Grocery
- Tủ nguyên liệu nhóm theo **9 kệ hàng** động (không hard-code).
- Thuật toán quy đổi đơn vị (BFS graph: kg→g, ml→g theo density).
- Tạo grocery list từ công thức: tổng cần − đã có = cần mua.
- Shopping Mode full-screen + hiệu ứng confetti khi hoàn thành.
- Tự động cập nhật tủ khi đánh dấu "Hoàn tất đi chợ".
- 10/10 unit tests Pantry service xanh.

### ✅ Sprint 5 — AI Assistant, Dynamic Nutrition & Cooking Journal
- ✅ **Google Gemini AI:** Tích hợp `gemini-2.0-flash` / `gemini-3-flash-preview` qua `GeminiClient`.
- ✅ **Khả năng chịu lỗi (Error Resilience):** `AiServiceException` (HTTP 503), timeout 30s qua `JdkClientHttpRequestFactory`.
- ✅ **Rate Limiting & Timezone:** 10 lượt/ngày/user qua Redis, tự động reset chuẩn xác lúc 00:00 múi giờ `Asia/Ho_Chi_Minh`.
- ✅ **Lịch sử gợi ý AI:** Endpoint `GET /api/v1/ai/history`, Tab "Lịch sử gợi ý AI" trên UI hỗ trợ xem lại và lưu công thức vào sổ tay.
- ✅ **Chuẩn hóa đơn vị & Dinh dưỡng AI:** Gemini ước tính calo/macro per-ingredient; `UnitNormalizationService` tự động đổi `quả`, `muỗng`, `chén` $\rightarrow$ baseUnit grams khi lưu.
- ✅ **Tính toán Dinh dưỡng Động (Dynamic Nutrition):** Tính chính xác calo/đạm/béo/carb từ dataset và tỉ lệ gram thực tế; loại bỏ hoàn toàn giá trị tĩnh/mock.
- ✅ **Tự động nạp `.env`:** Nạp cấu hình tự động khi khởi động qua `dotenv-java`, bảo vệ bí mật 100% không lưu vào git.

### ✅ Sprint 6 — CI/CD Pipeline, Cloud Deployment & Admin Portal
- ✅ **Admin Portal:** Xây dựng trọn vẹn 6 màn hình quản trị chuyên sâu (Dashboard KPI, Duyệt công thức, Duyệt nguyên liệu, Quản lý thành viên, Giám sát AI logs, Thiết lập hệ thống).
- ✅ **Thiết lập GitHub Actions CI:** Tự động chạy 48 tests Backend và 17 tests Frontend trên mỗi commit.
- ✅ **Triển khai Cloud Production:**
  - Frontend: Vercel Edge Network (`smartrecipe-platform.vercel.app`).
  - Backend: Render Docker Web Service (`smartrecipe-backend.onrender.com`).
  - Database: TiDB Cloud Serverless (MySQL 8.0 protocol).
  - Cache: Upstash Redis (TLS enabled).

---

## 🔬 Pipeline Dữ liệu Nguyên liệu: USDA FoodData Central

Xây dựng bộ dữ liệu 297+ nguyên liệu tiếng Việt **có nguồn gốc rõ ràng, dinh dưỡng chính xác** từ cơ sở dữ liệu khoa học quốc tế.

### Nguồn dữ liệu gốc
**USDA FoodData Central — SR Legacy 2018** ([Tải về](https://fdc.nal.usda.gov/download-foods.html))
- `food.csv`: ~8.000 thực phẩm với mã `fdc_id` và `food_category_id`.
- `food_nutrient.csv`: **36 MB** (~600.000 dòng — mỗi dòng là 1 chất dinh dưỡng của 1 thực phẩm).
- `food_category.csv`: 25 nhóm thực phẩm của USDA.
- `nutrient.csv`: Định nghĩa 150+ chất dinh dưỡng (id, tên, đơn vị).
- `food_portion.csv`: Khẩu phần tiêu chuẩn tham chiếu.

### Pipeline xử lý (4 giai đoạn)

```
USDA SR Legacy (~8.000 thực phẩm)
          │
          ▼ Giai đoạn 1: clean_ingredients.py
┌─────────────────────────────────────────┐
│  • Lọc 14/25 category phù hợp bếp Việt │
│  • Join food + food_nutrient → lấy     │
│    Calo, Protein, Fat, Carb per 100g   │
│  • Lọc thực phẩm chế biến sẵn,        │
│    thương mại, không có dinh dưỡng     │
│  • Tính density (g/ml) cho chất lỏng   │
│    (dựa trên food_portion.csv)         │
│  → ~1.800 dòng ứng viên               │
└─────────────────────────────────────────┘
          │
          ▼ Giai đoạn 2: Lọc thủ công + bán tự động
┌─────────────────────────────────────────┐
│  suggest_keep.py — Luật loại:           │
│  • Thịt thú lạ (emu, ostrich, bison)   │
│  • Phân loại Mỹ quá chi tiết           │
│    ("trimmed to 1/4" fat", "choice")   │
│  • Nội tạng ít dùng, đồ ăn chế biến   │
│  • Đồ uống công nghiệp, cồn            │
│  → ~350 dòng                           │
│                                        │
│  collapse_groups.py — Gộp biến thể:   │
│  • "Thịt bò xay 70%/80%/90% nạc"     │
│    → "Thịt bò xay" (giữ 80% làm chuẩn)│
│  • "Ức gà có da / không da"           │
│    → tách thành 2 nguyên liệu riêng   │
│  → ~310 dòng                          │
│                                        │
│  export_batches.py → 6 batch           │
│  Dịch thủ công Anh → Việt             │
│  (vi_batch_001.txt đến _251.txt)      │
└─────────────────────────────────────────┘
          │
          ▼ Giai đoạn 3: assign_aisles.py
┌─────────────────────────────────────────┐
│  Hai lớp gán kệ hàng:                  │
│                                        │
│  Lớp 1 — Category Map (USDA → kệ VN): │
│  Cat 1 Dairy/Egg    → kệ 6 Sữa&Trứng  │
│  Cat 2 Spices/Herbs → kệ 4 Gia vị     │
│  Cat 4 Fats/Oils    → kệ 8 Dầu mỡ    │
│  Cat 5,10,13 Meat   → kệ 2 Thịt       │
│  Cat 9 Fruits       → kệ 7 Trái cây   │
│  Cat 11 Vegetables  → kệ 1 Rau củ     │
│  Cat 12 Nuts/Seeds  → kệ 9 Hạt        │
│  Cat 15 Fish        → kệ 3 Hải sản    │
│  Cat 16 Legumes     → kệ 5 Đồ khô    │
│  Cat 19 Sweets      → kệ 5 Đồ khô    │
│  Cat 20 Grains      → kệ 5 Đồ khô    │
│                                        │
│  Lớp 2 — Override theo ngữ nghĩa:     │
│  Nước tương, miso (Cat16) → kệ 4      │
│  Nước cốt dừa (Cat12) → kệ 5         │
│  Rong biển (Cat11) → kệ 5            │
│  (USDA phân theo nguồn gốc,           │
│   người đi chợ tìm theo vị trí)       │
└─────────────────────────────────────────┘
          │
          ▼ Giai đoạn 4: gen_seed_sql.py
┌─────────────────────────────────────────┐
│  Validate trước khi sinh:              │
│  • Tên rỗng / vượt VARCHAR(100)        │
│  • Trùng tuyệt đối                     │
│  • Trùng casefold() (theo as_ci)       │
│  • aisle_id ngoài 1-9                  │
│  • Số âm hoặc không parse được        │
│  → sys.exit() nếu bất kỳ lỗi nào     │
│                                        │
│  Sinh ra seed_ingredients.sql:         │
│  • SET NAMES utf8mb4 (không BOM)      │
│  • ON DUPLICATE KEY UPDATE             │
│    (không ghi đè base_unit của admin) │
│  • 15 unit_conversions ml→g           │
│    (gắn ingredient_id cụ thể qua      │
│     subquery theo tên)                │
└─────────────────────────────────────────┘
          │
          ▼ Kết quả cuối cùng
  297 nguyên liệu  |  9 kệ hàng  |  15 quy đổi density
  base_unit = 'g' cho tất cả dòng
  4 cặp tên nguy hiểm được tách đúng:
  Dầu dừa (892 kcal) ≠ Đậu đũa (47 kcal)
  Dâu tây (32 kcal)  ≠ Đậu tây (333 kcal)
```

### Thiết kế Database cho Collation tiếng Việt
MySQL 8.0 mặc định dùng `utf8mb4_0900_ai_ci` (accent-insensitive) — khiến `'Dầu dừa' = 'Đậu đũa'` trả về `TRUE` và gây `ERROR 1062 Duplicate entry` khi seed.

**Giải pháp:** Toàn bộ 19 bảng dùng `utf8mb4_unicode_ci` / `utf8mb4_0900_as_ci`:
- `as` (accent-sensitive): `Dầu dừa ≠ Đậu đũa` ✅
- `ci` (case-insensitive): `tỏi = Tỏi` ✅ (tự nhiên với tên nguyên liệu)

---

## 🗃 Mô hình Cơ sở Dữ liệu (19 Bảng)

Cơ sở dữ liệu gồm **19 bảng** chuẩn hóa quan hệ 3NF:

| Nhóm | Bảng | Mô tả & Nhiệm vụ |
|---|---|---|
| **Auth & Social** | `users`, `follows` | Tài khoản, vai trò (USER, ADMIN), quan hệ theo dõi giữa người dùng |
| **Recipe** | `recipes`, `recipe_steps`, `recipe_ingredients`, `recipe_likes`, `recipe_comments`, `recipe_tags`, `tags` | Công thức, bước làm, định lượng nguyên liệu, lượt like, bình luận, phân loại tags |
| **Ingredient** | `ingredients`, `aisles`, `unit_conversions` | 297+ nguyên liệu dinh dưỡng USDA, 9 kệ hàng siêu thị, bảng quy đổi đơn vị theo đồ thị |
| **Pantry** | `user_pantry` | Tủ nguyên liệu cá nhân, số lượng tồn và ngày hết hạn từng lô |
| **Grocery** | `grocery_lists`, `grocery_items`, `grocery_list_recipes` | Danh sách đi chợ cha, các mặt hàng cần mua gom theo quầy, liên kết tới công thức đã chọn |
| **AI & Journal** | `ai_suggestion_logs`, `cooking_journals` | Lịch sử prompt/response của Gemini AI và nhật ký nấu ăn thực tế kèm ảnh thành phẩm |
| **Notification** | `notifications` | Thông báo tương tác (like, comment, follow) |

**9 kệ hàng (Aisles)** theo lối siêu thị Việt Nam:
1. Rau củ (74 món) · 2. Thịt & Gia cầm (47 món) · 3. Hải sản (28 món) · 4. Gia vị & Nước chấm (36 món) · 5. Đồ khô & Gạo (32 món) · 6. Sữa & Trứng (19 món) · 7. Trái cây (34 món) · 8. Dầu mỡ & Chất béo (9 món) · 9. Các loại Hạt (11 món).

---

## ⚙️ Hướng dẫn Cài đặt & Chạy cục bộ

### Yêu cầu hệ thống
- [Docker Desktop](https://www.docker.com/products/docker-desktop) 4.x+
- Java 21 JDK (Eclipse Temurin khuyến nghị)
- Node.js 20+ & npm 10+
- Python 3.10+ (chỉ cần nếu muốn chạy lại data pipeline)

### Bước 0 — Clone dự án kèm Submodules

```bash
# Clone toàn bộ repo mẹ và tự động kéo 2 repo con Backend + Frontend
git clone --recurse-submodules https://github.com/NHTung-0801/SmartRecipe-Project.git
cd SmartRecipe-Project

# Nếu đã clone trước đó mà chưa có thư mục con:
git submodule update --init --recursive
```

---

### Cách 1: Chạy Full-stack với Docker Compose (Nhanh nhất)

Khởi động toàn bộ 4 dịch vụ (MySQL, Redis, Backend, Frontend) chỉ bằng 1 câu lệnh:

```bash
docker-compose up -d --build
```

- **Frontend Web App:** Mở trình duyệt tại `http://localhost:3000`
- **Backend REST API:** Sẵn sàng tại `http://localhost:8080/api/v1`
- **MySQL Database:** `localhost:3306` (user: `root`, pass: `root`, db: `smart_recipe_db`)
- **Redis Cache:** `localhost:6379`

---

### Cách 2: Chạy Tách biệt cho Lập trình viên (Developer Mode)

Tối ưu nhất cho quá trình phát triển với Hot-Reload:

#### Bước 1: Khởi động Database & Cache qua Docker
```bash
docker-compose up -d mysql-db redis-cache
```

#### Bước 2: Nạp dữ liệu mẫu hoàn chỉnh
```bash
# Nạp toàn bộ 19 bảng và dữ liệu mẫu (Users, Ingredients, Recipes, Journals, Pantry)
docker exec -i smartrecipe-mysql mysql -uroot -proot smart_recipe_db < sql/export_local_data.sql
```

#### Bước 3: Cấu hình và Chạy Backend (Spring Boot 4 / Java 21)
```bash
cd smartrecipe-backend
cp .env.example .env    # Điền GEMINI_API_KEY và các cấu hình

# Chạy trên Windows PowerShell:
.\mvnw spring-boot:run

# Chạy trên Linux/macOS:
./mvnw spring-boot:run
```
*API sẽ chạy tại `http://localhost:8080`*

#### Bước 4: Cài đặt và Chạy Frontend (React 19 / Vite 8)
```bash
cd ../smartrecipe-frontend
npm install
cp .env.example .env    # VITE_API_BASE_URL=http://localhost:8080/api/v1
npm run dev
```
*Frontend sẽ chạy tại `http://localhost:5173`*

---

## 🔬 Nạp & Chạy lại Data Pipeline (Python Tools)

Nếu bạn muốn chạy lại toàn bộ quy trình xử lý dữ liệu từ nguồn thô của USDA:

```bash
# Cài đặt thư viện xử lý dữ liệu
pip install pandas numpy

# Giai đoạn 1: Lọc thô từ USDA
python tools/clean_ingredients.py

# Giai đoạn 2: Lọc theo bếp Việt + gộp biến thể
python tools/suggest_keep.py --apply
python tools/collapse_groups.py --apply

# Giai đoạn 3: Gán 9 kệ hàng
python tools/assign_aisles.py --apply

# Giai đoạn 4: Sinh file SQL seed
python tools/gen_seed_sql.py --apply
# → Tạo ra file sql/seed_ingredients.sql

# Kiểm tra tính toàn vẹn của dữ liệu trước khi nạp
python tools/verify_dataset.py
```

---

## 🧪 Hệ thống Kiểm thử Tự động (65 Tests)

Toàn bộ hệ thống được bảo vệ bởi **65 ca kiểm thử tự động**, đạt tỷ lệ 100% Pass:

```
SmartRecipe Test Suite
├── ⚙️ Backend (JUnit 5 + Mockito): 48 Tests
│   ├── AiServiceImplTest ............ 14 tests (Rate limit, JSON parsing, 3-layer match)
│   ├── PantryServiceImplTest ........ 10 tests (FEFO deduction, auto-aggregate)
│   ├── AuthServiceImplOtpTest ........ 8 tests (OTP generate, Redis TTL, SMTP mail)
│   ├── RecipeServiceImplTest ......... 7 tests (Owner authorization, status workflow)
│   ├── GroceryServiceImplTest ........ 4 tests (Pantry subtraction, aisle sorting)
│   ├── UnitNormalizationTest ......... 4 tests (BFS graph conversion, aliases)
│   └── BackendApplicationTests ....... 1 test  (Context loading)
│
└── 🎨 Frontend (Vitest + JSDOM): 17 Tests
    ├── AddPantryItemModal.test ....... 5 tests (Form validation, submit handler)
    ├── ExpiryAlertBanner.test ........ 5 tests (Dynamic warning styling, cleanup trigger)
    ├── ConfirmModal.test ............. 4 tests (DOM rendering, confirm/cancel events)
    └── useAuthStore.test ............. 3 tests (Login state, logout, token purge)
```

```bash
# Chạy kiểm thử Backend:
cd smartrecipe-backend && ./mvnw test

# Chạy kiểm thử Frontend:
cd smartrecipe-frontend && npm test
```

---

## 📝 Biến môi trường (Environment Variables)

### Backend (`.env` trong `smartrecipe-backend/`)
```env
# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# JWT Security
JWT_SECRET=your_very_long_secret_key_here_at_least_256_bits
JWT_EXPIRATION=86400000          # 24 giờ (ms)
JWT_REFRESH_EXPIRATION=604800000 # 7 ngày (ms)

# Gmail SMTP gửi mã OTP
SPRING_MAIL_USERNAME=your_gmail@gmail.com
SPRING_MAIL_PASSWORD=your_app_password

# Cloudinary (lưu trữ ảnh)
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
```

### Frontend (`.env` trong `smartrecipe-frontend/`)
```env
# URL trỏ tới Backend API
VITE_API_BASE_URL=http://localhost:8080/api/v1
```

---

## 🔄 Quy trình Triển khai CI/CD (GitHub Actions)

Dự án áp dụng mô hình tự động hóa kiểm thử và phát hành liên tục:

```
[ Git Push / PR ] ──► GitHub Actions Runner
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    [ CI Backend ]                   [ CI Frontend ]
    • Setup Temurin JDK 21           • Setup Node.js 20
    • Maven Dependency Cache         • npm ci & Lint
    • Chạy 48 JUnit Unit Tests       • Chạy 17 Vitest Tests
    • Package Production JAR         • Vite Production Bundle
            │                               │
            └───────────────┬───────────────┘
                            │ Both CI Passed & Merged to 'main'
            ┌───────────────┴───────────────┐
            ▼                               ▼
    [ CD Backend - Render ]          [ CD Frontend - Vercel ]
    • Trigger Render Deploy Hook     • Auto Deploy to Vercel Edge
    • Build Docker Container Image   • Instant Cache Invalidation
    • Health Check /actuator/health  • Live on smartrecipe-platform.vercel.app
    • Live on smartrecipe-backend.onrender.com
```

---

## 📚 Tài liệu Chi tiết Tham khảo

| Tài liệu | Mô tả nội dung |
|---|---|
| [🔗 Backend Repo](https://github.com/NHTung-0801/smartrecipe-backend) | Kho mã nguồn Backend (Spring Boot 4, Java 21, REST API) |
| [🔗 Frontend Repo](https://github.com/NHTung-0801/smartrecipe-frontend) | Kho mã nguồn Frontend (React 19, Vite 8, Tailwind v4, SPA) |
| [📖 Backend README](https://github.com/NHTung-0801/smartrecipe-backend#readme) | Kiến trúc, 15 API controllers, luồng Auth, luồng AI, Redis cache, trừ kho FEFO |
| [📖 Frontend README](https://github.com/NHTung-0801/smartrecipe-frontend#readme) | Kiến trúc, 21 màn hình (6 trang Admin), routing, state management, design system |
| [docs/project_master_plan.md](./docs/project_master_plan.md) | Kế hoạch phát triển tổng thể 6 Sprints và kiến trúc Hybrid Cloud |
| [sql/init_database.sql](./sql/init_database.sql) | DDL 19 bảng + seed data quầy hàng và thẻ phân loại khởi tạo |
| [sql/seed_ingredients.sql](./sql/seed_ingredients.sql) | 290 nguyên liệu gốc từ USDA FoodData Central |
| [sql/export_local_data.sql](./sql/export_local_data.sql) | Toàn bộ dữ liệu mẫu đầy đủ đồng bộ từ môi trường local |

---

## 🤝 Tác giả & Bản quyền

- **Sinh viên thực hiện:** Nguyễn Hoàng Tùng
- **Mã sinh viên:** 064205002222
- **Ngành:** Công nghệ Thông tin
- **Trường:** Trường Đại học Giao thông Vận tải TP. Hồ Chí Minh (UTH)

---

*SmartRecipe Platform — Giải pháp Công nghệ Ẩm thực Thông minh vì Sức khỏe và Môi trường xanh.*

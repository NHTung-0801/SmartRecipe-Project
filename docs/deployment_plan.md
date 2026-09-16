# 🚀 KẾ HOẠCH TRIỂN KHAI (DEPLOYMENT PLAN)
**Dự án:** Smart Recipe & Grocery Platform
**Phiên bản:** 1.0  
**Ngày tạo:** 05/09/2026  
**Trạng thái:** ✅ **ĐÃ HOÀN TẤT TRIỂN KHAI MÔI TRƯỜNG CLOUD** (Vercel, TiDB Serverless, Render Web Service, Upstash Redis, Cloudinary)

---

## 📐 TỔNG QUAN KIẾN TRÚC TRIỂN KHAI

```
Internet
   ├── Vercel (CDN) ──── Frontend React (smartrecipe.vercel.app)
   │                          │
   └── Render.com ─────── Backend Spring Boot (:8080)
                               ├── TiDB Serverless (MySQL 25GiB free)
                               ├── Upstash Redis   (10K cmd/ngày free)
                               └── Cloudinary      (Image Storage)
```

---

## 🗂️ BẢNG TÓM TẮT NỀN TẢNG

| Thành phần | Nền tảng | Gói | Ghi chú |
|-----------|----------|-----|---------|
| **Frontend** (React/Vite) | **Vercel** | Free | Auto deploy từ GitHub |
| **Backend** (Spring Boot) | **Render.com** | Free Web Service | Sleep sau 15 phút không dùng |
| **Database** (MySQL) | **TiDB Serverless** | Free | 25 GiB, MySQL-compatible 100% |
| **Cache + Session** (Redis) | **Upstash** | Free | 10,000 lệnh/ngày, 256 MB |
| **Lưu trữ ảnh** | **Cloudinary** | Free | Đã tích hợp sẵn |
| **AI API** | **Google Gemini** | Free tier | Đã tích hợp sẵn |

---

## 📋 BIẾN MÔI TRƯỜNG CẦN CHUẨN BỊ

### Backend (Render.com Environment Variables)

| Biến | Giá trị mẫu | Lấy từ đâu |
|------|------------|-----------|
| `SPRING_DATASOURCE_URL` | `jdbc:mysql://<host>:4000/smart_recipe_db?useSSL=true&...` | TiDB Dashboard |
| `SPRING_DATASOURCE_USERNAME` | `<tidb_user>` | TiDB Dashboard |
| `SPRING_DATASOURCE_PASSWORD` | `<tidb_password>` | TiDB Dashboard |
| `SPRING_DATA_REDIS_HOST` | `<random>.upstash.io` | Upstash Dashboard |
| `SPRING_DATA_REDIS_PORT` | `6379` | Upstash Dashboard |
| `SPRING_DATA_REDIS_PASSWORD` | `<upstash_password>` | Upstash Dashboard |
| `SPRING_DATA_REDIS_SSL_ENABLED` | `true` | Upstash yêu cầu TLS |
| `JWT_SECRET` | `<random_64_char_string>` | Tự tạo |
| `JWT_EXPIRATION` | `86400000` | 24 giờ (ms) |
| `JWT_REFRESH_EXPIRATION` | `604800000` | 7 ngày (ms) |
| `GEMINI_API_KEY` | `<your_gemini_key>` | Google AI Studio |
| `GEMINI_MODEL` | `gemini-3-flash-preview` | Giữ nguyên |
| `CLOUDINARY_CLOUD_NAME` | `<cloud_name>` | Cloudinary Dashboard |
| `CLOUDINARY_API_KEY` | `<api_key>` | Cloudinary Dashboard |
| `CLOUDINARY_API_SECRET` | `<api_secret>` | Cloudinary Dashboard |

### Frontend (Vercel Environment Variables)

| Biến | Giá trị | Ghi chú |
|------|---------|---------|
| `VITE_API_BASE_URL` | `https://<your-app>.onrender.com/api/v1` | URL backend trên Render |

---

## 🛠️ CHUẨN BỊ TRƯỚC KHI DEPLOY

```bash
# Build thử frontend
cd smartrecipe-frontend && npm run build

# Build thử backend
cd smartrecipe-backend && ./mvnw clean package -DskipTests
```

> ⚠️ **Không deploy nếu build fail!**

---

## 🗄️ PHẦN 1 — THIẾT LẬP DATABASE (TiDB Serverless)

### 1.1 Tạo tài khoản và cluster
1. https://tidbcloud.com → Đăng ký bằng GitHub
2. **Create Cluster** → **Serverless** → Tên: `smartrecipe-db` → Region: Singapore

### 1.2 Lấy thông tin kết nối
Cluster → **Connect** → **General** → **MySQL**:
- Host: `<random>.tidbcloud.com`, Port: `4000`
- User và Password (copy ngay — password chỉ hiện 1 lần)

### 1.3 Tạo database (SQL Editor trên web)
```sql
CREATE DATABASE IF NOT EXISTS smart_recipe_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 1.4 Connection String cho Backend
```
jdbc:mysql://<host>:4000/smart_recipe_db?useSSL=true&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3&serverTimezone=UTC&allowPublicKeyRetrieval=true
```

---

## ⚡ PHẦN 2 — THIẾT LẬP REDIS (Upstash)

### 2.1 Tạo database
1. https://upstash.com → Đăng ký bằng GitHub
2. **Create Database** → **Redis** → Tên: `smartrecipe-redis` → Region: Singapore → Free plan

### 2.2 Lấy thông tin kết nối
Database → tab **Details**:
- Endpoint (Host): `<random>.upstash.io`, Port: `6379`
- Password: copy từ dashboard

---

## ☁️ PHẦN 3 — DEPLOY BACKEND (Render.com)

### 3.1 Tạo Web Service
1. https://render.com → Đăng ký bằng GitHub
2. **New** → **Web Service** → Chọn repository GitHub

### 3.2 Cấu hình

| Trường | Giá trị |
|--------|---------|
| Name | `smartrecipe-backend` |
| Region | Singapore |
| Branch | `main` |
| Root Directory | `smartrecipe-backend` |
| Runtime | `Java` |
| Build Command | `./mvnw clean package -DskipTests` |
| Start Command | `java -jar target/smartrecipe-backend-0.0.1-SNAPSHOT.jar` |
| Plan | Free |

### 3.3 Environment Variables
Tab **Environment** → thêm toàn bộ biến từ bảng Backend ở trên.

### 3.4 Sau deploy
- URL: `https://smartrecipe-backend.onrender.com`
- Hibernate tự tạo schema, UnitConversionSeeder tự chạy lần đầu
- **Lưu ý:** Sleep sau 15 phút idle, cold start ~30 giây
- **Giải pháp keep-alive:** https://cron-job.org ping mỗi 14 phút

---

## 🌐 PHẦN 4 — DEPLOY FRONTEND (Vercel)

### 4.1 Tạo project
1. https://vercel.com → Đăng ký bằng GitHub
2. **Add New Project** → Import repository

### 4.2 Cấu hình

| Trường | Giá trị |
|--------|---------|
| Framework Preset | `Vite` |
| Root Directory | `smartrecipe-frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### 4.3 Environment Variable
```
VITE_API_BASE_URL = https://smartrecipe-backend.onrender.com/api/v1
```

### 4.4 Deploy
Click **Deploy** → URL: `https://smartrecipe-project.vercel.app`

---

## 🗃️ PHẦN 5 — IMPORT DỮ LIỆU SEED

> ⚠️ **Bước bắt buộc** — thiếu 293 nguyên liệu thì app không hoạt động được.

### Thứ tự thực hiện
```
1. Backend đã start trên Render → Hibernate tạo xong tables
2. Import seed_data.sql vào TiDB → 293 nguyên liệu + aisles
3. Kiểm tra qua API
```

### Lệnh import
```bash
# Từ máy local kết nối vào TiDB
mysql -h <tidb_host> -P 4000 -u <user> -p \
  --ssl-mode=VERIFY_IDENTITY \
  smart_recipe_db < smartrecipe-backend/src/main/resources/db/seed_data.sql
```

Hoặc dùng **TiDB SQL Editor** (Web UI): paste nội dung file `seed_data.sql` và chạy.

### Kiểm tra
```bash
curl "https://smartrecipe-backend.onrender.com/api/v1/ingredients?page=0&size=5"
# Kết quả mong đợi: JSON danh sách nguyên liệu
```

---

## 🔧 PHẦN 6 — THAY ĐỔI CODE TRƯỚC KHI DEPLOY

### 6.1 `application.yaml` — Hỗ trợ env vars đầy đủ

```yaml
spring:
  datasource:
    url: ${SPRING_DATASOURCE_URL:jdbc:mysql://localhost:3306/smart_recipe_db?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true}
    username: ${SPRING_DATASOURCE_USERNAME:root}
    password: ${SPRING_DATASOURCE_PASSWORD:root}
  data:
    redis:
      host: ${SPRING_DATA_REDIS_HOST:localhost}
      port: ${SPRING_DATA_REDIS_PORT:6379}
      password: ${SPRING_DATA_REDIS_PASSWORD:}
      ssl:
        enabled: ${SPRING_DATA_REDIS_SSL_ENABLED:false}
app:
  jwt:
    secret: ${JWT_SECRET:default_dev_secret}
    expirationMs: ${JWT_EXPIRATION:86400000}
    refreshExpirationMs: ${JWT_REFRESH_EXPIRATION:604800000}
gemini:
  api-key: ${GEMINI_API_KEY:}
  model: ${GEMINI_MODEL:gemini-3-flash-preview}
  daily-limit: 10
```

### 6.2 CORS — Cho phép domain Vercel

Trong `SecurityConfig.java`:
```java
config.setAllowedOriginPatterns(List.of(
    "http://localhost:5173",
    "https://*.vercel.app",
    "https://smartrecipe-project.vercel.app"  // URL thực tế sau khi có
));
```

### 6.3 Frontend `.env.production`

Tạo file `smartrecipe-frontend/.env.production`:
```env
VITE_API_BASE_URL=https://smartrecipe-backend.onrender.com/api/v1
```

---

## ✅ CHECKLIST DEPLOY ĐẦY ĐỦ

### Chuẩn bị tài khoản
- [ ] GitHub — code đã push lên `main`
- [ ] TiDB Serverless — đã tạo cluster `smartrecipe-db`
- [ ] Upstash — đã tạo Redis `smartrecipe-redis`
- [ ] Render.com — đã kết nối GitHub
- [ ] Vercel — đã kết nối GitHub
- [ ] Cloudinary — đã có (tích hợp từ trước)
- [ ] Google Gemini API Key — đã có

### Thay đổi code
- [ ] `application.yaml` đã dùng env vars đầy đủ
- [ ] CORS đã thêm domain Vercel
- [ ] `.env.production` đã tạo cho frontend
- [ ] Build frontend thành công: `npm run build`
- [ ] Build backend thành công: `./mvnw clean package -DskipTests`
- [ ] Commit và push toàn bộ thay đổi lên GitHub

### Deploy (theo thứ tự này)
- [ ] **1.** TiDB: Tạo database `smart_recipe_db`
- [ ] **2.** Upstash: Tạo Redis database
- [ ] **3.** Render: Deploy backend, cấu hình env vars, xác nhận start OK
- [ ] **4.** TiDB: Import `seed_data.sql`
- [ ] **5.** Vercel: Deploy frontend, cấu hình `VITE_API_BASE_URL`

### Kiểm tra sau deploy
- [ ] `GET /api/v1/ingredients` trả về danh sách nguyên liệu
- [ ] Đăng ký tài khoản mới thành công
- [ ] Đăng nhập thành công, nhận JWT token
- [ ] Tạo công thức và upload ảnh thành công
- [ ] AI suggestion hoạt động
- [ ] CORS không bị lỗi (F12 browser không có CORS error)
- [ ] Danh sách đi chợ và quy đổi đơn vị hoạt động đúng

---

## ⚠️ LƯU Ý QUAN TRỌNG

### Render Free Tier — Sleep Issue
Service sleep sau 15 phút, cold start ~30 giây khi có request đầu tiên.
Giải pháp: cron-job.org ping `GET /api/v1/ingredients?page=0&size=1` mỗi 14 phút.

### TiDB SSL bắt buộc
Port 4000, không phải 3306. Connection string phải có `sslMode=VERIFY_IDENTITY`.

### Admin quản lý dữ liệu sau deploy
Sau lần seed đầu tiên, Admin dùng Admin Panel trong ứng dụng để thêm/sửa nguyên liệu.
Không cần chạm SQL hay redeploy.

### Đồng bộ seed data từ local lên production
```bash
# Export local
docker exec smartrecipe-mysql mysqldump -uroot -proot \
  --no-tablespaces --skip-triggers --single-transaction \
  smart_recipe_db aisles ingredients unit_conversions \
  > smartrecipe-backend/src/main/resources/db/seed_data.sql

# Import vào TiDB
mysql -h <tidb_host> -P 4000 -u <user> -p --ssl-mode=VERIFY_IDENTITY \
  smart_recipe_db < smartrecipe-backend/src/main/resources/db/seed_data.sql
```

---

## 🔗 LINK THAM KHẢO

| Dịch vụ | Đăng ký | Tài liệu |
|--------|--------|---------|
| TiDB Serverless | https://tidbcloud.com | https://docs.pingcap.com/tidbcloud |
| Upstash Redis | https://upstash.com | https://docs.upstash.com/redis |
| Render.com | https://render.com | https://docs.render.com |
| Vercel | https://vercel.com | https://vercel.com/docs |
| Cloudinary | https://cloudinary.com | https://cloudinary.com/documentation |
| Google AI Studio | https://aistudio.google.com | https://ai.google.dev/docs |
| cron-job.org | https://cron-job.org | Keep Render alive |

---

## 📅 TIMELINE DỰ KIẾN

| Bước | Thời gian |
|------|----------|
| Tạo tài khoản 5 nền tảng | 30 phút |
| Thay đổi code + commit + push | 30 phút |
| Deploy backend lên Render | 15–20 phút (Java build lần đầu chậm) |
| Import seed data vào TiDB | 10 phút |
| Deploy frontend lên Vercel | 5 phút |
| Kiểm tra toàn bộ checklist | 30 phút |
| **Tổng cộng** | **~2 giờ** |

# Smart Recipe & Grocery Platform

Chào mừng đến với dự án **Smart Recipe & Grocery Platform**! Đây là một hệ thống web full-stack toàn diện giúp người dùng quản lý công thức nấu ăn, theo dõi nguyên liệu tủ lạnh, lên danh sách đi chợ tự động và nhận gợi ý món ăn thông minh từ AI.

## 🌟 Kiến trúc Tổng thể (System Architecture)

Dự án được chia làm 2 phần (monorepo structure với 3 Git repositories):
1. **Frontend (`/smartrecipe-frontend`)**: Giao diện người dùng (Client-side) được xây dựng bằng ReactJS, Vite và TailwindCSS.
2. **Backend (`/smartrecipe-backend`)**: Máy chủ API (Server-side) được xây dựng bằng Java Spring Boot, Hibernate và RESTful API.
3. **Database & Cache**: MySQL 8.0 (Relational Database) và Redis 7 (In-memory Cache & Session Management) chạy ngầm qua Docker.

## 🚀 Công nghệ Sử dụng (Tech Stack)

### 🖥 Frontend
- **Framework**: ReactJS 18
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand (Client State), TanStack Query (Server State)
- **Routing**: React Router DOM v6
- **Form & Validation**: React Hook Form + Zod

### ⚙️ Backend
- **Framework**: Java 21 + Spring Boot 3.x
- **Database Access**: Spring Data JPA / Hibernate
- **Security**: Spring Security + JWT (JSON Web Token)
- **Caching**: Spring Data Redis
- **AI Integration**: Gemini AI REST API
- **Cloud Storage**: Cloudinary (Hình ảnh)

### 🐳 DevOps & Deployment
- Docker & Docker Compose
- Nginx (Frontend Hosting)

---

## 🛠 Hướng dẫn Khởi chạy Môi trường Phát triển (Local Development)

### Yêu cầu hệ thống (Prerequisites)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Java 21 JDK (Cho Backend)
- Node.js 22 (Cho Frontend)

### Bước 1: Khởi động Cơ sở dữ liệu (MySQL & Redis)
Mở terminal tại thư mục gốc của dự án và chạy lệnh sau để bật CSDL qua Docker:
```bash
docker-compose up -d mysql-db redis-cache
```
> **Lưu ý**: Lần chạy đầu tiên, MySQL sẽ tự động nạp cấu trúc 17 bảng từ file `init_database.sql`.

### Bước 2: Chạy Backend (Spring Boot)
Xem hướng dẫn chi tiết tại: [smartrecipe-backend/README.md](./smartrecipe-backend/README.md)

### Bước 3: Chạy Frontend (ReactJS)
Xem hướng dẫn chi tiết tại: [smartrecipe-frontend/README.md](./smartrecipe-frontend/README.md)

---

## 📚 Tài liệu Thiết kế & Kế hoạch
- Toàn bộ thiết kế Database, API và Kế hoạch phát triển Sprint có thể xem tại file `implementation_plan.md`.
- File lược đồ CSDL tự động tạo: `init_database.sql`.

## 🤝 Tác giả
Dự án được phát triển trong khuôn khổ Thực tập tốt nghiệp (TTTN).

# ✅ CI/CD Setup — Walkthrough

## Những gì đã thực hiện

### Bước 0 — Chuẩn bị code (HOÀN THÀNH)

| File | Thay đổi |
|---|---|
| [`pom.xml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/pom.xml) | Thêm `spring-boot-starter-actuator` + `h2` (test scope) |
| [`application.yaml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/resources/application.yaml) | Toàn bộ datasource/redis/cloudinary dùng env vars với default fallback cho local |
| [`SecurityConfig.java`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/main/java/com/smartrecipe/smartrecipe_backend/security/SecurityConfig.java) | Thêm `.requestMatchers("/actuator/health").permitAll()` |
| [`application-test.yaml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/src/test/resources/application-test.yaml) | Profile test dùng H2 in-memory |

### Bước 4 — Workflow Files (HOÀN THÀNH)

| File | Repository | Tác dụng |
|---|---|---|
| [`.github/workflows/ci-backend.yml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/.github/workflows/ci-backend.yml) | Backend | 37 Mockito tests + build JAR |
| [`.github/workflows/cd-backend.yml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-backend/.github/workflows/cd-backend.yml) | Backend | Trigger Render Deploy Hook + health check retry |
| [`.github/workflows/ci-frontend.yml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/.github/workflows/ci-frontend.yml) | Frontend | ESLint + 17 Vitest + build dist |
| [`.github/workflows/cd-frontend.yml`](file:///d:/TTTN/SmartRecipe-Project/smartrecipe-frontend/.github/workflows/cd-frontend.yml) | Frontend | Deploy Vercel CLI production |
| [`.github/workflows/ci-root.yml`](file:///d:/TTTN/SmartRecipe-Project/.github/workflows/ci-root.yml) | Root | Check .env không bị commit + verify submodules |

### Verification kết quả

```
✅ mvn package -DskipTests → BUILD SUCCESS
✅ mvn test -Dtest=!BackendApplicationTests → 37 tests, 0 failures, 0 errors
✅ Build JAR thành công
```

---

## Việc anh cần làm (theo thứ tự)

> [!IMPORTANT]
> Các bước này anh phải tự thực hiện trước khi pipeline chạy được.

### Bước 1 — Đăng ký các dịch vụ
1. **TiDB Serverless** → https://tidbcloud.com (đăng ký + tạo cluster `smartrecipe-db`)
2. **Upstash Redis** → https://upstash.com (tạo DB `smartrecipe-redis`)
3. **Render.com** → https://render.com (tạo Web Service, trỏ vào repo `smartrecipe-backend`, Root Directory = `smartrecipe-backend`)
4. **Vercel** → https://vercel.com (import repo `smartrecipe-frontend`, Root Directory = `smartrecipe-frontend`)

### Bước 2 — Lấy secrets

**Render Deploy Hook URL:**
```
Render Dashboard → smartrecipe-backend service
→ Settings → Deploy Hooks → Create Deploy Hook
→ Copy URL dạng: https://api.render.com/deploy/srv-xxx?key=yyy
```

**Vercel tokens:**
```bash
# Chạy trong thư mục smartrecipe-frontend
npx vercel login
npx vercel link
# Sau đó đọc file .vercel/project.json → lấy orgId và projectId
```
Rồi vào Vercel Dashboard → Settings → Tokens → Create Token (scope: Full Account)

### Bước 3 — Nhập secrets vào GitHub

**Repo `smartrecipe-backend` → Settings → Secrets and variables → Actions:**
| Secret | Giá trị |
|---|---|
| `RENDER_DEPLOY_HOOK_URL` | URL lấy từ Render Deploy Hook |
| `BACKEND_HEALTH_URL` | `https://smartrecipe-backend.onrender.com/actuator/health` |

**Repo `smartrecipe-frontend` → Settings → Secrets and variables → Actions:**
| Secret | Giá trị |
|---|---|
| `VERCEL_TOKEN` | Token từ Vercel Dashboard |
| `VERCEL_ORG_ID` | orgId từ `.vercel/project.json` |
| `VERCEL_PROJECT_ID` | projectId từ `.vercel/project.json` |

**Quan trọng: Sau khi nhập secrets xong, báo tôi biết để commit toàn bộ thay đổi lên GitHub.**

---

## Sau khi pipeline chạy lần đầu

Vào GitHub → Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require status checks: `Test & Build JAR` (backend) và `Lint, Test & Build` (frontend)

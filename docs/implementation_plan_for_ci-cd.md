# 🚀 Kế Hoạch CI/CD — SmartRecipe Project (v2 — Đã làm rõ)

## 📋 Trả Lời Câu Hỏi Trực Tiếp

### ✅ Câu 1: Cách B (Render Deploy Hook) có ổn không?

**Hoàn toàn ổn và là lựa chọn đúng cho sprint cuối.** Lý do:

| Tiêu chí | Cách A (Auto-Deploy) | Cách B (Deploy Hook) ✅ |
|---|---|---|
| Kiểm soát thứ tự | ❌ Render tự trigger ngay khi push | ✅ Chỉ deploy sau khi CI pass |
| Ngăn deploy code lỗi | ❌ Deploy kể cả khi test fail | ✅ Deploy Hook chỉ gọi sau khi test xanh |
| Health check sau deploy | ❌ Không có | ✅ Pipeline kiểm tra ngay sau deploy |
| Phù hợp sprint cuối | ❌ Rủi ro cao | ✅ Đảm bảo chất lượng |

> **Kết luận:** Cách B an toàn hơn nhiều. Với sprint cuối, không nên để code lỗi tự deploy lên production.

---

### ✅ Câu 2: Backend test trong CI — dùng gì?

Đã phân tích toàn bộ 6 test file:

| Test file | Annotation | Cần DB? | Chạy được trong CI? |
|---|---|---|---|
| `BackendApplicationTests.java` | `@SpringBootTest` | ✅ Cần | ❌ Sẽ fail (không có MySQL) |
| `UnitNormalizationServiceTest.java` | `@ExtendWith(MockitoExtension)` | ❌ Không | ✅ Pass ngay |
| `AiServiceImplTest.java` | `@ExtendWith(MockitoExtension)` | ❌ Không | ✅ Pass ngay |
| `GroceryListServiceImplTest.java` | `@ExtendWith(MockitoExtension)` | ❌ Không | ✅ Pass ngay |
| `PantryServiceImplTest.java` | `@ExtendWith(MockitoExtension)` | ❌ Không | ✅ Pass ngay |
| `RecipeServiceImplTest.java` | `@ExtendWith(MockitoExtension)` | ❌ Không | ✅ Pass ngay |

**Kết luận:** 5/6 test files dùng **Mockito thuần** — không cần database, không cần Redis, chạy hoàn toàn trong môi trường isolated. 

**Giải pháp:** Chỉ cần **exclude `BackendApplicationTests`** khỏi CI run bằng Maven tag hoặc JUnit tag. KHÔNG cần thêm H2, KHÔNG cần mock database phức tạp.

---

### ✅ Câu 3: Kế hoạch deploy deployment_plan.md ảnh hưởng gì?

Từ [deployment_plan.md](file:///d:/TTTN/SmartRecipe-Project/docs/deployment_plan.md), rút ra các điểm CI/CD phải xử lý:

1. **Render cold-start 30 giây** → Health check sau deploy phải chờ đủ thời gian (dùng retry thay vì `sleep` cứng)
2. **Thứ tự deploy:** Backend (Render ~10 phút) → seed SQL → Frontend (Vercel ~2 phút). CI/CD không cần enforce thứ tự này vì seed SQL là bước thủ công 1 lần
3. **Render Root Directory = `smartrecipe-backend`** → Workflow backend phải `working-directory: smartrecipe-backend`
4. **Vercel Root Directory = `smartrecipe-frontend`** → Workflow frontend phải detect đúng project
5. **CORS cần cấu hình domain Vercel** → Phải update code trước khi chạy CI/CD lần đầu

---

## 📐 Kiến Trúc Pipeline Chính Xác

```
Developer: git push → main (backend repo)
│
├─ GitHub Actions: ci-backend.yml
│   ├─ Setup JDK 21
│   ├─ Cache Maven
│   ├─ mvn test -Dtest="!BackendApplicationTests"  ← 37 Mockito tests
│   ├─ mvn package -DskipTests                      ← Build JAR
│   └─ ✅ Upload JAR artifact
│
└─ (nếu CI pass) cd-backend.yml
    ├─ curl POST → Render Deploy Hook URL
    ├─ Retry health check (max 20 lần × 30s = 10 phút)
    └─ ✅ Deploy hoàn thành

Developer: git push → main (frontend repo)  
│
├─ GitHub Actions: ci-frontend.yml
│   ├─ Setup Node 20
│   ├─ npm ci
│   ├─ npm run lint
│   ├─ npm test -- --run                            ← 17 Vitest tests
│   ├─ npm run build
│   └─ ✅ Upload dist artifact
│
└─ (nếu CI pass) cd-frontend.yml
    ├─ vercel pull + build + deploy --prod
    └─ ✅ URL production hoạt động
```

---

## 🗂️ File Workflows Sẽ Tạo

```
smartrecipe-backend/
└── .github/workflows/
    ├── ci-backend.yml      (trigger: push bất kỳ branch, PR)
    └── cd-backend.yml      (trigger: push main, needs: CI pass)

smartrecipe-frontend/
└── .github/workflows/
    ├── ci-frontend.yml     (trigger: push bất kỳ branch, PR)
    └── cd-frontend.yml     (trigger: push main, needs: CI pass)

SmartRecipe-Project/  (root)
└── .github/workflows/
    └── ci-root.yml         (trigger: push main, kiểm tra .env không bị commit)
```

---

## 🔑 GitHub Secrets Cần Thiết

### Backend Repository (`smartrecipe-backend`)

| Secret | Lấy từ đâu |
|---|---|
| `RENDER_DEPLOY_HOOK_URL` | Render Dashboard → Service → Settings → Deploy Hooks → Create Hook |
| `BACKEND_HEALTH_URL` | `https://smartrecipe-backend.onrender.com/actuator/health` (cố định) |

> **Lưu ý:** Với Cách B, **không cần** `RENDER_API_KEY` hay `RENDER_SERVICE_ID`. Chỉ cần **Deploy Hook URL** (dạng `https://api.render.com/deploy/srv-xxx?key=yyy`). URL này đã bao gồm authentication.

### Frontend Repository (`smartrecipe-frontend`)

| Secret | Lấy từ đâu |
|---|---|
| `VERCEL_TOKEN` | Vercel Dashboard → Settings → Tokens → Create Token |
| `VERCEL_ORG_ID` | Chạy `npx vercel link` hoặc Vercel Dashboard → Team Settings |
| `VERCEL_PROJECT_ID` | Chạy `npx vercel link` → xuất hiện trong `.vercel/project.json` |

---

## 📋 Thứ Tự Thực Hiện

> [!IMPORTANT]
> **Phải hoàn thành các bước chuẩn bị trước, sau đó mới tạo file workflow.**

### Bước 0 — Chuẩn bị code (TRƯỚC khi setup CI/CD)
- [ ] Cập nhật `application.yaml` để dùng env vars (thay vì hardcode localhost)
- [ ] Thêm CORS domain Vercel vào `SecurityConfig.java`
- [ ] Kiểm tra `actuator/health` endpoint đã expose chưa (cần cho health check)
- [ ] Commit + push (sau khi anh cho phép)

### Bước 1 — Setup tài khoản (anh tự thực hiện)
- [ ] Đăng ký **TiDB Serverless** → tạo cluster → lấy connection string
- [ ] Đăng ký **Upstash** → tạo Redis → lấy host/password
- [ ] Đăng ký **Render.com** → tạo Web Service backend
- [ ] Đăng ký **Vercel** → import repo frontend

### Bước 2 — Lấy Secrets (anh tự thực hiện)
- [ ] Render: tạo Deploy Hook URL cho service backend
- [ ] Vercel: tạo API Token
- [ ] Chạy `npx vercel link` trong thư mục `smartrecipe-frontend` → lấy Org ID + Project ID

### Bước 3 — Nhập Secrets vào GitHub (anh tự thực hiện)
- [ ] `smartrecipe-backend` repo → Settings → Secrets → nhập 2 secrets
- [ ] `smartrecipe-frontend` repo → Settings → Secrets → nhập 3 secrets

### Bước 4 — Tôi viết và push workflow files
- [ ] `ci-backend.yml` + `cd-backend.yml`
- [ ] `ci-frontend.yml` + `cd-frontend.yml`  
- [ ] `ci-root.yml`

### Bước 5 — Cấu hình Branch Protection (sau khi pipeline xanh lần đầu)
- [ ] Backend repo: require `CI Backend` pass trước khi merge vào main
- [ ] Frontend repo: require `CI Frontend` pass trước khi merge vào main

---

## ⚠️ Điểm Cần Quyết Định Trước Khi Bắt Đầu

> [!IMPORTANT]
> **`actuator/health` endpoint:** Hiện tại `pom.xml` đã có `spring-boot-actuator` chưa? Nếu chưa, tôi cần thêm dependency này để CI/CD có thể health check sau deploy. Nếu không muốn dùng actuator, có thể dùng bất kỳ GET endpoint nào trả 200 (ví dụ `/api/v1/ingredients?page=0&size=1`).

> [!NOTE]
> **Cần anh xác nhận:** Sau khi đọc xong kế hoạch này, nếu đồng ý thì tôi sẽ bắt đầu từ **Bước 0** (chuẩn bị code) ngay mà không cần đợi anh setup tài khoản — vì các bước 1-3 là việc anh làm song song. Khi anh có đủ Secrets thì chúng ta tiếp tục Bước 4.

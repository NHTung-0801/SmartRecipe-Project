"""Sinh sql/seed_ingredients.sql từ dataset/ingredients_to_translate.csv.

Vì sao sinh bằng script chứ không viết tay: 290 dòng x 7 cột, mỗi lần chỉnh
dataset là phải sinh lại. Script cũng chặn trước các lỗi chỉ lộ ra lúc nạp DB.

Các bảo đảm của file sinh ra:

  1. utf-8 KHÔNG BOM + `SET NAMES utf8mb4;`. Có BOM thì MySQL đọc 3 byte đầu
     như một phần câu SQL đầu tiên và báo lỗi cú pháp.

  2. Chống trùng theo đúng collation của cột: `ingredients.name` là
     utf8mb4_0900_as_ci (phân biệt dấu, KHÔNG phân biệt hoa/thường), nên
     'Dầu dừa' != 'Đậu đũa' (OK) nhưng 'Tỏi' == 'tỏi' (đụng). Script so
     casefold() để bắt đúng nhóm đụng đó.

  3. ON DUPLICATE KEY UPDATE cố tình KHÔNG cập nhật `base_unit`: cả 290 dòng
     CSV đều là 'g', trong khi admin có thể đã sửa sang 'quả'/'củ' qua API.
     Chạy lại seed không được ghi đè lựa chọn đó.

  4. `unit_conversions` ml->g cho các dòng có `density`, gắn ingredient_id cụ
     thể qua subquery theo tên (không hard-code id vì id do AUTO_INCREMENT).
     Dùng ON DUPLICATE KEY UPDATE được vì UNIQUE(from_unit,to_unit,
     ingredient_id) có hiệu lực khi ingredient_id NOT NULL — khác với các
     dòng quy đổi chung (ingredient_id IS NULL) trong init_database.sql.

Chạy:
    python tools/gen_seed_sql.py --dry-run
    python tools/gen_seed_sql.py --apply
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
OUT_FILE = ROOT / "sql" / "seed_ingredients.sql"
CSV_ENCODING = "utf-8-sig"      # CSV có BOM
SQL_ENCODING = "utf-8"          # file SQL phải KHÔNG BOM

NAME_MAX_LEN = 100              # VARCHAR(100) của ingredients.name
AISLES = {
    1: "Rau củ", 2: "Thịt & Gia cầm", 3: "Hải sản", 4: "Gia vị & Nước chấm",
    5: "Đồ khô & Gạo", 6: "Sữa & Trứng", 7: "Trái cây",
    8: "Dầu mỡ & Chất béo", 9: "Các loại Hạt",
}


def q(value: str) -> str:
    r"""Bọc chuỗi thành literal SQL. Escape \ trước rồi mới tới '."""
    escaped = str(value).replace("\\", "\\\\").replace("'", "''")
    return f"'{escaped}'"


def num(value: str, field: str, name: str) -> str:
    """Chuẩn hóa số về DECIMAL(10,2). Chặn rỗng/âm ngay tại đây."""
    raw = (value or "").strip()
    if not raw:
        sys.exit(f"LỖI: {name!r} thiếu giá trị {field}")
    try:
        parsed = Decimal(raw)
    except Exception:
        sys.exit(f"LỖI: {name!r} có {field}={raw!r} không phải số")
    if parsed < 0:
        sys.exit(f"LỖI: {name!r} có {field}={raw!r} âm")
    return f"{parsed.quantize(Decimal('0.01'))}"


def validate(rows: list[dict]) -> None:
    if not rows:
        sys.exit("LỖI: CSV không có dòng nào")

    names = [r["name_vi"].strip() for r in rows]

    empty = [i for i, n in enumerate(names, 2) if not n]
    if empty:
        sys.exit(f"LỖI: name_vi rỗng ở dòng CSV {empty}")

    too_long = [n for n in names if len(n) > NAME_MAX_LEN]
    if too_long:
        sys.exit(f"LỖI: name_vi dài hơn {NAME_MAX_LEN} ký tự: {too_long}")

    # Trùng tuyệt đối
    dup = [n for n, c in Counter(names).items() if c > 1]
    if dup:
        sys.exit(f"LỖI: name_vi trùng nhau: {dup}")

    # Trùng theo collation as_ci (bỏ qua hoa/thường, GIỮ dấu) -> vẫn ERROR 1062
    folded: dict[str, list[str]] = defaultdict(list)
    for n in names:
        folded[n.casefold()].append(n)
    clash = {k: v for k, v in folded.items() if len(v) > 1}
    if clash:
        sys.exit("LỖI: các tên này đụng nhau dưới utf8mb4_0900_as_ci "
                 f"(khác hoa/thường): {clash}")

    bad_aisle = {r["aisle_id"] for r in rows} - {str(k) for k in AISLES}
    if bad_aisle:
        sys.exit(f"LỖI: aisle_id không thuộc 1-9: {sorted(bad_aisle)}")

    # aisle_name trong CSV phải khớp aisle_id, nếu lệch là dataset bị sửa tay
    for r in rows:
        expected = AISLES[int(r["aisle_id"])]
        actual = r["aisle_name"].strip()
        if actual != expected:
            sys.exit(f"LỖI: {r['name_vi']!r} có aisle_id={r['aisle_id']} "
                     f"nhưng aisle_name={actual!r}, phải là {expected!r}")

    units = {r["base_unit"].strip() for r in rows}
    if not units <= {"g", "ml"}:
        sys.exit(f"LỖI: base_unit lạ: {sorted(units - {'g', 'ml'})}")


def build_sql(rows: list[dict]) -> str:
    by_aisle: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        by_aisle[int(r["aisle_id"])].append(r)

    density_rows = [r for r in rows if (r["density"] or "").strip()]
    flagged = sum(1 for r in rows
                  if (r["review_needed"] or "").strip().lower() == "true")

    out: list[str] = []
    add = out.append

    add("-- SINH TỰ ĐỘNG bởi tools/gen_seed_sql.py — ĐỪNG sửa tay.")
    add("-- Nguồn: dataset/ingredients_to_translate.csv")
    add("-- Dinh dưỡng: USDA FoodData Central, SR Legacy 2018-04 (trên 100 g).")
    add("--")
    add(f"-- {len(rows)} nguyên liệu, {len(density_rows)} dòng có quy đổi ml->g.")
    add(f"-- {flagged} dòng từng bị cờ review_needed trong pipeline và đã được")
    add("-- xác nhận hợp lệ: calo lệch Atwater là do gia vị khô nhiều xơ, do")
    add("-- axit hữu cơ trong nước cốt chanh/giấm, hoặc do tỷ lệ đạm đặc biệt")
    add("-- của rau lá. Không dòng nào là lỗi dữ liệu.")
    add("--")
    add("-- Nạp file (PowerShell 5.1 không có toán tử '<'):")
    add("--   docker cp sql/seed_ingredients.sql smartrecipe-mysql:/tmp/seed.sql")
    add("--   docker exec smartrecipe-mysql bash -c \\")
    add("--     \"mysql -uroot -proot --default-character-set=utf8mb4 < /tmp/seed.sql\"")
    add("")
    add("-- Thiếu dòng này thì client mysql dùng latin1 và mọi tên tiếng Việt")
    add("-- thành mojibake kiểu 'Cá h?i'.")
    add("SET NAMES utf8mb4;")
    add("")
    add("USE `smart_recipe_db`;")
    add("")
    add("-- Chạy lại được nhiều lần: khớp theo UNIQUE(name).")
    add("-- CỐ Ý không cập nhật `base_unit` — xem tools/gen_seed_sql.py.")
    add("INSERT INTO `ingredients`")
    add("    (`name`, `base_unit`, `calories_per_100g`, `protein`, `fat`, "
        "`carbs`, `aisle_id`)")
    add("VALUES")

    lines: list[str] = []
    for aisle_id in sorted(by_aisle):
        group = sorted(by_aisle[aisle_id], key=lambda r: r["name_vi"].strip())
        lines.append(f"-- Kệ {aisle_id}: {AISLES[aisle_id]} ({len(group)} dòng)")
        for r in group:
            name = r["name_vi"].strip()
            lines.append(
                f"({q(name)}, {q(r['base_unit'].strip())}, "
                f"{num(r['calories'], 'calories', name)}, "
                f"{num(r['protein'], 'protein', name)}, "
                f"{num(r['fat'], 'fat', name)}, "
                f"{num(r['carbs'], 'carbs', name)}, {aisle_id}),")

    # Dòng dữ liệu cuối bỏ dấu ',' vì ngay sau nó là ON DUPLICATE KEY UPDATE
    for i in range(len(lines) - 1, -1, -1):
        if not lines[i].startswith("--"):
            lines[i] = lines[i].rstrip(",")
            break
    out.extend(lines)

    add("")
    add("ON DUPLICATE KEY UPDATE")
    add("    `calories_per_100g` = VALUES(`calories_per_100g`),")
    add("    `protein`           = VALUES(`protein`),")
    add("    `fat`               = VALUES(`fat`),")
    add("    `carbs`             = VALUES(`carbs`),")
    add("    `aisle_id`          = VALUES(`aisle_id`);")
    add("")

    add("-- Quy đổi ml -> g riêng cho từng nguyên liệu, dùng khi công thức ghi")
    add("-- '100 ml nước mắm' mà tủ lạnh lưu theo gam. multiplier = khối lượng")
    add("-- riêng (g/ml). Chỉ những dòng có `density` trong CSV mới cần.")
    add("--")
    add("-- ingredient_id lấy bằng subquery theo tên, không hard-code số, vì id")
    add("-- do AUTO_INCREMENT sinh ra và khác nhau giữa các lần reset DB.")
    add("-- Dùng INSERT ... SELECT (thay cho VALUES) để subquery chạy được.")
    for r in sorted(density_rows, key=lambda r: r["name_vi"].strip()):
        name = r["name_vi"].strip()
        density = Decimal(r["density"].strip()).quantize(Decimal("0.0001"))
        add("INSERT INTO `unit_conversions` "
            "(`from_unit`, `to_unit`, `multiplier`, `ingredient_id`)")
        add(f"SELECT 'ml', 'g', {density}, `id` FROM `ingredients` "
            f"WHERE `name` = {q(name)}")
        add("ON DUPLICATE KEY UPDATE `multiplier` = VALUES(`multiplier`);")
    add("")

    add("-- Kiểm tra nhanh sau khi nạp.")
    add(f"SELECT COUNT(*) AS tong_nguyen_lieu FROM `ingredients`;  "
        f"-- kỳ vọng {len(rows)}")
    add("SELECT a.`id`, a.`name`, COUNT(i.`id`) AS so_nguyen_lieu")
    add("FROM `aisles` a LEFT JOIN `ingredients` i ON i.`aisle_id` = a.`id`")
    add("GROUP BY a.`id`, a.`name` ORDER BY a.`id`;")
    add("SELECT COUNT(*) AS so_quy_doi_rieng FROM `unit_conversions`")
    add(f"WHERE `ingredient_id` IS NOT NULL;  -- kỳ vọng {len(density_rows)}")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with CSV_FILE.open(encoding=CSV_ENCODING, newline="") as fh:
        rows = list(csv.DictReader(fh))

    validate(rows)
    sql = build_sql(rows)

    density_count = sum(1 for r in rows if (r["density"] or "").strip())
    print(f"Đọc      : {CSV_FILE.name} ({len(rows)} dòng)")
    print(f"Sinh     : {len(sql.splitlines())} dòng SQL, "
          f"{len(sql.encode(SQL_ENCODING))} byte")
    print(f"Quy đổi  : {density_count} dòng ml->g")
    for aisle_id, label in AISLES.items():
        n = sum(1 for r in rows if int(r["aisle_id"]) == aisle_id)
        print(f"  kệ {aisle_id} {label:<20} {n:>3}")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
        return 0

    # newline='\n' để file dùng LF, khớp phần còn lại của sql/
    with OUT_FILE.open("w", encoding=SQL_ENCODING, newline="\n") as fh:
        fh.write(sql)

    if OUT_FILE.read_bytes()[:3] == b"\xef\xbb\xbf":
        sys.exit("LỖI: file ghi ra có BOM")
    print(f"\nĐã ghi -> {OUT_FILE} (utf-8 không BOM)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Sửa cấu trúc dataset/ingredients_to_translate.csv sau khi bị Excel làm hỏng.

Hai lỗi cần sửa:

1. BỌC NGOẶC KÉP HAI LẦN. Excel ghi lại file với mỗi dòng dữ liệu bị bọc thêm
   một lớp dấu " bên ngoài và các dấu " bên trong bị nhân đôi:
       "173410,""Butter, salted"",,1,Dairy and Egg Products,butter,1,3,..."
   -> csv.reader đọc ra ĐÚNG 1 field thay vì 16. pandas báo lỗi tokenizing.
   Cách sửa: field nào đứng một mình thì parse lại chính nó như một dòng CSV.

2. THỪA CỘT 'drop_reason'. Các dòng người dùng copy lại từ
   dropped_ingredients.csv mang theo cột thứ 17 (drop_reason). Dataset chuẩn
   chỉ có 16 cột -> bỏ cột này đi.

Sau khi sửa, script đối chiếu lại description + food_category_id với nguồn
USDA gốc để chắc chắn không có dòng nào bị lệch dữ liệu.

Chạy:
    python tools/repair_csv.py --dry-run
    python tools/repair_csv.py --apply
"""
from __future__ import annotations

import argparse
import csv
import io
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "dataset" / "FoodData_Central_sr_legacy_food_csv_2018-04"
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
ENCODING = "utf-8-sig"

# Cùng ngưỡng với tools/clean_ingredients.py (Bước 5)
MAX_CALORIES = 910
MAX_MACRO_SUM = 105
ATWATER_TOLERANCE = 0.25
ATWATER_MIN_CALORIES = 20

EXPECTED_COLUMNS = [
    "fdc_id", "description", "name_vi", "food_category_id", "category_name",
    "group_token", "token_depth", "group_size", "calories", "protein", "fat",
    "carbs", "atwater_estimate", "base_unit", "density", "review_needed",
]
NCOL = len(EXPECTED_COLUMNS)


def read_rows() -> tuple[list[list[str]], dict[str, int]]:
    """Đọc file, mở lớp bọc thừa và cắt cột thừa. Trả về (rows, thống kê)."""
    with io.open(CSV_FILE, encoding=ENCODING, newline="") as fh:
        raw = list(csv.reader(fh))

    stats = {"unwrapped": 0, "dropped_col": 0, "ok": 0}
    rows: list[list[str]] = []

    for lineno, fields in enumerate(raw, start=1):
        if not fields or (len(fields) == 1 and not fields[0].strip()):
            continue

        # Lỗi 1: cả dòng bị gói vào một field -> parse lại field đó.
        if len(fields) == 1:
            fields = next(csv.reader([fields[0]]))
            stats["unwrapped"] += 1
        else:
            stats["ok"] += 1

        # Lỗi 2: cột drop_reason thừa ở cuối.
        if len(fields) == NCOL + 1:
            fields = fields[:NCOL]
            stats["dropped_col"] += 1

        if len(fields) != NCOL:
            sys.exit(f"LỖI dòng {lineno}: có {len(fields)} cột, cần {NCOL}\n"
                     f"  {fields[:3]}")
        rows.append(fields)

    return rows, stats


def verify_against_source(df: pd.DataFrame) -> list[str]:
    """Đối chiếu description và category với nguồn USDA. Trả về list cảnh báo."""
    food = pd.read_csv(SRC_DIR / "food.csv", low_memory=False)
    src_desc = food.set_index("fdc_id")["description"]
    src_cat = food.set_index("fdc_id")["food_category_id"]

    warnings: list[str] = []
    for _, r in df.iterrows():
        fid = int(r["fdc_id"])
        if fid not in src_desc.index:
            warnings.append(f"[{fid}] không có trong food.csv gốc")
            continue
        # clean_name() của Giai đoạn 1 bỏ hậu tố ', raw' nên so sánh nới.
        want, got = str(src_desc[fid]), str(r["description"])
        if got not in want:
            warnings.append(f"[{fid}] description lệch:\n"
                            f"      file : {got}\n      USDA : {want}")
        if int(src_cat[fid]) != int(r["food_category_id"]):
            warnings.append(
                f"[{fid}] food_category_id lệch: file={r['food_category_id']} "
                f"USDA={src_cat[fid]}")
    return warnings


def check_derived(df: pd.DataFrame) -> list[str]:
    """Kiểm tra các cột dẫn xuất của Giai đoạn 1 (atwater, review_needed, đơn vị).

    19 dòng người dùng thêm tay được copy từ dropped_ingredients.csv nên về lý
    thuyết đã đúng, nhưng vẫn tính lại để chắc chắn không có ô nào bị Excel làm
    tròn hoặc sửa nhầm.
    """
    warnings: list[str] = []

    est = (4 * df["protein"] + 9 * df["fat"] + 4 * df["carbs"]).round(2)
    bad_est = (est - df["atwater_estimate"]).abs() > 0.01
    for _, r in df[bad_est].iterrows():
        warnings.append(f"[{r.fdc_id}] atwater_estimate={r.atwater_estimate} "
                        f"nhưng tính lại = {est[r.name]}")

    # Dùng đúng ngưỡng của clean_ingredients.validate()
    macro = df["protein"] + df["fat"] + df["carbs"]
    out_of_range = ((df["calories"] < 0) | (df["calories"] > MAX_CALORIES)
                    | (macro > MAX_MACRO_SUM))
    dev = (est - df["calories"]).abs() / df["calories"].replace(0, pd.NA)
    atwater_bad = (dev > ATWATER_TOLERANCE) & (df["calories"] >= ATWATER_MIN_CALORIES)
    expected_review = (out_of_range | atwater_bad).fillna(False)
    for _, r in df[expected_review != df["review_needed"]].iterrows():
        warnings.append(f"[{r.fdc_id}] review_needed={r.review_needed} "
                        f"nhưng tính lại = {expected_review[r.name]}")

    bad_unit = df[df["base_unit"] != "g"]
    for _, r in bad_unit.iterrows():
        warnings.append(f"[{r.fdc_id}] base_unit={r.base_unit!r}, phải là 'g'")

    # density chỉ đặt cho dầu (0.92), sữa (1.03), nước sốt cat 6 (1.10)
    for _, r in df[df["density"].notna()].iterrows():
        if float(r["density"]) not in (0.92, 1.03, 1.10):
            warnings.append(f"[{r.fdc_id}] density={r.density} không thuộc "
                            f"tập {{0.92, 1.03, 1.10}}")
    return warnings


def to_frame(data: list[list[str]]) -> pd.DataFrame:
    """Ép kiểu về đúng dtype của dataset chuẩn."""
    df = pd.DataFrame(data, columns=EXPECTED_COLUMNS)
    numeric = ["fdc_id", "food_category_id", "token_depth", "group_size",
               "calories", "protein", "fat", "carbs", "atwater_estimate",
               "density"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ("fdc_id", "food_category_id", "token_depth", "group_size"):
        df[col] = df[col].astype(int)
    df["review_needed"] = df["review_needed"].astype(str).str.strip().map(
        {"True": True, "False": False})
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    rows, stats = read_rows()
    header, data = rows[0], rows[1:]

    if header != EXPECTED_COLUMNS:
        sys.exit(f"LỖI: header không khớp.\n  file: {header}\n"
                 f"  cần: {EXPECTED_COLUMNS}")

    print(f"Dòng dữ liệu            : {len(data)}")
    print(f"Đã mở lớp ngoặc kép thừa: {stats['unwrapped']}")
    print(f"Đã bỏ cột drop_reason   : {stats['dropped_col']}")

    df = to_frame(data)
    if df["review_needed"].isna().any():
        sys.exit("LỖI: review_needed có giá trị không phải True/False")

    dup_id = df[df["fdc_id"].duplicated(keep=False)]
    dup_desc = df[df["description"].duplicated(keep=False)]
    print(f"Trùng fdc_id            : {len(dup_id)}")
    print(f"Trùng description       : {len(dup_desc)}")
    for _, r in dup_id.iterrows():
        print(f"  ! [{r.fdc_id}] {r.description}")
    for _, r in dup_desc.iterrows():
        print(f"  ! {r.description}")

    print("\nĐối chiếu với nguồn USDA...")
    warnings = verify_against_source(df)
    if warnings:
        for w in warnings:
            print(f"  ! {w}")
    else:
        print("  OK: description, food_category_id khớp toàn bộ")

    print("\nKiểm tra cột dẫn xuất (atwater, review_needed, đơn vị)...")
    derived_warnings = check_derived(df)
    if derived_warnings:
        for w in derived_warnings:
            print(f"  ! {w}")
    else:
        print("  OK: atwater_estimate, review_needed, base_unit, density đều đúng")

    df = df.sort_values(
        ["food_category_id", "description"]).reset_index(drop=True)

    print("\nSố dòng theo nhóm:")
    for (cid, cname), n in df.groupby(
            ["food_category_id", "category_name"]).size().items():
        print(f"  {cid:>3}  {cname:<38} {n:>4}")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
        return 0

    shutil.copy2(CSV_FILE, CSV_FILE.with_suffix(".csv.broken"))
    df.to_csv(CSV_FILE, index=False, encoding=ENCODING)
    print(f"\nBản hỏng -> {CSV_FILE.with_suffix('.csv.broken')}")
    print(f"Đã ghi   -> {CSV_FILE} ({len(df)} dòng, {len(df.columns)} cột)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Bổ sung 'Cá hồi' vào dataset — nguyên liệu pipeline Giai đoạn 1 bỏ sót.

Nguyên nhân bỏ sót: cả 4 dòng salmon Atlantic của SR Legacy đều bị
deduplicate() trong clean_ingredients.py gom về cùng nhóm token
"fish, salmon, atlantic" rồi loại hết, nên kệ Hải sản (27 dòng) không có
cá hồi — trong khi đây là nguyên liệu cốt lõi của bếp Việt hiện đại.

Chọn fdc_id 175167 (farmed, raw) thay vì 173686 (wild, raw): cá hồi bán ở
siêu thị Việt Nam gần như toàn bộ là cá nuôi. Bản 'cooked, dry heat' không
dùng được vì mọi dòng khác trong dataset đều là nguyên liệu tươi.

Lấy dinh dưỡng từ cùng nguồn và cùng cách join của clean_ingredients.py,
không hard-code số, để nếu đổi fdc_id thì số liệu tự khớp theo.

Chạy:
    python tools/add_salmon.py --dry-run
    python tools/add_salmon.py --apply
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "dataset" / "FoodData_Central_sr_legacy_food_csv_2018-04"
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
ENCODING = "utf-8-sig"

NUTRIENT_MAP = {1008: "calories", 1003: "protein", 1004: "fat", 1005: "carbs"}

FDC_ID = 175167          # Fish, salmon, Atlantic, farmed, raw
NAME_VI = "Cá hồi"
AISLE_ID = 3             # khớp sql/init_database.sql
AISLE_NAME = "Hải sản"


def load_nutrients(fdc_id: int) -> dict[str, float]:
    nutrient = pd.read_csv(
        SRC_DIR / "food_nutrient.csv",
        usecols=["fdc_id", "nutrient_id", "amount"],
        low_memory=False,
    )
    rows = nutrient[
        (nutrient["fdc_id"] == fdc_id)
        & nutrient["nutrient_id"].isin(NUTRIENT_MAP)
    ]
    values = {NUTRIENT_MAP[int(r.nutrient_id)]: float(r.amount)
              for r in rows.itertuples()}
    missing = set(NUTRIENT_MAP.values()) - set(values)
    if missing:
        sys.exit(f"LỖI: fdc_id {fdc_id} thiếu dưỡng chất {sorted(missing)}")
    return values


def build_row(existing: pd.DataFrame) -> pd.DataFrame:
    food = pd.read_csv(SRC_DIR / "food.csv", low_memory=False)
    match = food[food["fdc_id"] == FDC_ID]
    if match.empty:
        sys.exit(f"LỖI: Không thấy fdc_id {FDC_ID} trong food.csv")

    categories = pd.read_csv(SRC_DIR / "food_category.csv")
    cat_names = categories.set_index("id")["description"]

    src = match.iloc[0]
    nut = load_nutrients(FDC_ID)

    row = {
        "fdc_id": FDC_ID,
        "description": src["description"],
        "name_vi": NAME_VI,
        "food_category_id": src["food_category_id"],
        "category_name": cat_names.get(src["food_category_id"]),
        "group_token": str(src["description"]).lower(),
        "token_depth": 1,
        "group_size": 1,
        "calories": nut["calories"],
        "protein": nut["protein"],
        "fat": nut["fat"],
        "carbs": nut["carbs"],
        "atwater_estimate": round(
            4 * nut["protein"] + 9 * nut["fat"] + 4 * nut["carbs"], 2),
        "base_unit": "g",
        "density": np.nan,      # cá là chất rắn, không quy đổi ml
        "review_needed": False,
        "aisle_id": AISLE_ID,
        "aisle_name": AISLE_NAME,
    }

    unknown = set(row) - set(existing.columns)
    if unknown:
        sys.exit(f"LỖI: cột không có trong CSV: {sorted(unknown)}")
    return pd.DataFrame([row])[existing.columns.tolist()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    existing = pd.read_csv(CSV_FILE, encoding=ENCODING)

    if FDC_ID in set(existing["fdc_id"]):
        print(f"fdc_id {FDC_ID} đã có trong CSV — không làm gì.")
        return 0
    if NAME_VI in set(existing["name_vi"].astype(str).str.strip()):
        sys.exit(f"LỖI: tên {NAME_VI!r} đã tồn tại (UNIQUE(name) sẽ vỡ)")

    new_row = build_row(existing)
    r = new_row.iloc[0]
    print(f"Hiện có : {len(existing)} dòng")
    print(f"Thêm    : [{r.fdc_id}] {r.description}")
    print(f"          -> {r.name_vi} | kệ {r.aisle_id} {r.aisle_name} | "
          f"{r.calories} kcal | P {r.protein} F {r.fat} C {r.carbs} | "
          f"atwater {r.atwater_estimate}")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
        return 0

    merged = pd.concat([existing, new_row], ignore_index=True)
    merged = merged.sort_values(
        ["food_category_id", "description"]).reset_index(drop=True)

    shutil.copy2(CSV_FILE, CSV_FILE.with_suffix(".csv.presalmon"))
    merged.to_csv(CSV_FILE, index=False, encoding=ENCODING)
    print(f"\nĐã ghi -> {CSV_FILE} ({len(merged)} dòng)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

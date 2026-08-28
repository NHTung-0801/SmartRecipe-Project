"""Bổ sung các nguyên liệu nền của bếp Việt bị pipeline Giai đoạn 1 bỏ sót.

Nguyên nhân bỏ sót:
  1. Category 6 (Soups, Sauces and Gravies) không nằm trong KEEP_CATEGORIES
     của clean_ingredients.py -> mất nước mắm, dầu hào, tương ớt sriracha,
     tương đen hoisin. Đây là gia vị nền, không phải "món sốt pha sẵn".
  2. "Sugars, granulated" (đường cát trắng) khớp SWEETS_KEEP nhưng bị
     deduplicate() gom chung nhóm token "sugars" với "Sugars, brown" và bị loại.
  3. "Tofu, raw, regular" bị gom nhóm với "Tofu, raw, firm".

Script lấy lại đúng các fdc_id này từ nguồn USDA, join dinh dưỡng theo cùng
cách của clean_ingredients.py rồi nối vào dataset/ingredients_to_translate.csv.

Chạy:
    python tools/add_missing_essentials.py --dry-run
    python tools/add_missing_essentials.py --apply
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
DENSITY_SAUCE = 1.10  # nước mắm / nước tương / dầu hào

# fdc_id -> (tên hiển thị, category_name ghi đè nếu cần)
ESSENTIALS = {
    174531: "Sauce, fish, ready-to-serve",
    174529: "Sauce, oyster, ready-to-serve",
    171186: "Sauce, hot chile, sriracha",
    172886: "Sauce, hoisin, ready-to-serve",
    169655: "Sugars, granulated",
    172476: "Tofu, raw, regular, prepared with calcium sulfate",
}


def load_nutrients(fdc_ids: set[int]) -> pd.DataFrame:
    nutrient = pd.read_csv(
        SRC_DIR / "food_nutrient.csv",
        usecols=["fdc_id", "nutrient_id", "amount"],
        low_memory=False,
    )
    nutrient = nutrient[
        nutrient["fdc_id"].isin(fdc_ids)
        & nutrient["nutrient_id"].isin(NUTRIENT_MAP)
    ]
    pivot = nutrient.pivot_table(
        index="fdc_id", columns="nutrient_id", values="amount", aggfunc="first"
    ).rename(columns=NUTRIENT_MAP)
    for col in NUTRIENT_MAP.values():
        if col not in pivot.columns:
            pivot[col] = np.nan
    return pivot


def build_rows(existing: pd.DataFrame) -> pd.DataFrame:
    food = pd.read_csv(SRC_DIR / "food.csv", low_memory=False)
    categories = pd.read_csv(SRC_DIR / "food_category.csv")
    cat_names = categories.set_index("id")["description"]

    rows = food[food["fdc_id"].isin(ESSENTIALS)].copy()
    missing = set(ESSENTIALS) - set(rows["fdc_id"])
    if missing:
        sys.exit(f"LỖI: Không thấy fdc_id {sorted(missing)} trong food.csv")

    rows["category_name"] = rows["food_category_id"].map(cat_names)
    rows = rows.merge(
        load_nutrients(set(ESSENTIALS)),
        left_on="fdc_id", right_index=True, how="left",
    )

    cols = list(NUTRIENT_MAP.values())
    rows[cols] = rows[cols].fillna(0)

    rows["name_vi"] = np.nan
    rows["group_token"] = rows["description"].str.lower()
    rows["token_depth"] = 1
    rows["group_size"] = 1
    rows["atwater_estimate"] = (
        4 * rows["protein"] + 9 * rows["fat"] + 4 * rows["carbs"]
    ).round(2)
    rows["base_unit"] = "g"
    rows["density"] = np.where(
        rows["food_category_id"] == 6, DENSITY_SAUCE, np.nan)
    rows["review_needed"] = False

    return rows[existing.columns.tolist()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    existing = pd.read_csv(CSV_FILE, encoding=ENCODING)
    new_rows = build_rows(existing)

    already = new_rows["fdc_id"].isin(existing["fdc_id"])
    new_rows = new_rows[~already]

    print(f"Hiện có   : {len(existing)} dòng")
    print(f"Bổ sung   : {len(new_rows)} dòng")
    for _, r in new_rows.iterrows():
        print(f"  + [{r.fdc_id}] {r.description}  "
              f"({r.calories} kcal, cat {r.food_category_id})")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
        return 0

    merged = pd.concat([existing, new_rows], ignore_index=True)
    merged = merged.sort_values(
        ["food_category_id", "description"]).reset_index(drop=True)

    shutil.copy2(CSV_FILE, CSV_FILE.with_suffix(".csv.bak2"))
    merged.to_csv(CSV_FILE, index=False, encoding=ENCODING)
    print(f"\nĐã ghi -> {CSV_FILE} ({len(merged)} dòng)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

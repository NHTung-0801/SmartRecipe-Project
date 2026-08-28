"""Kiểm tra cuối dataset/ingredients_to_translate.csv trước khi sang bước dịch.

Chạy: python tools/verify_dataset.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "dataset" / "FoodData_Central_sr_legacy_food_csv_2018-04"
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
NUTRIENT_MAP = {1008: "calories", 1003: "protein", 1004: "fat", 1005: "carbs"}


def main() -> int:
    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
    problems: list[str] = []

    food = pd.read_csv(SRC_DIR / "food.csv", low_memory=False)
    src_desc = food.set_index("fdc_id")["description"]

    # 1. group_token = token_depth phần đầu của description GỐC (viết thường).
    #    Tách theo cùng cách clean_ingredients.assign_group_token(): split(",")
    #    rồi strip từng phần, nên "Water convolvulus,raw" (thiếu space sau phẩy)
    #    vẫn cho ra token 'water convolvulus'.
    #    Phải dùng description gốc chứ không phải cột description trong file, vì
    #    clean_name() đã cắt hậu tố ', raw' SAU khi group_token được tính.
    #    Riêng 6 dòng của add_missing_essentials.py đặt group_token = cả
    #    description viết thường với token_depth=1 -> chấp nhận cả hai dạng.
    for _, r in df.iterrows():
        original = str(src_desc[int(r["fdc_id"])]).lower()
        parts = [re.sub(r"\s+", " ", p).strip() for p in original.split(",")]
        by_depth = ", ".join(parts[: int(r["token_depth"])])
        if str(r["group_token"]) not in (by_depth, original):
            problems.append(f"[{r.fdc_id}] group_token={r.group_token!r} "
                            f"không khớp depth={r.token_depth} ({by_depth!r}) "
                            f"cũng không khớp description gốc")

    # 2. Dinh dưỡng phải khớp food_nutrient.csv gốc
    nut = pd.read_csv(SRC_DIR / "food_nutrient.csv", low_memory=False)
    nut = nut[nut["fdc_id"].isin(df["fdc_id"])
              & nut["nutrient_id"].isin(NUTRIENT_MAP)]
    pivot = nut.pivot_table(index="fdc_id", columns="nutrient_id",
                            values="amount", aggfunc="first"
                            ).rename(columns=NUTRIENT_MAP)
    merged = df.set_index("fdc_id").join(pivot, rsuffix="_src")
    for col in NUTRIENT_MAP.values():
        src = merged[f"{col}_src"].fillna(0)
        diff = (merged[col] - src).abs() > 0.01
        for fid in merged.index[diff]:
            problems.append(f"[{fid}] {col}: file={merged.loc[fid, col]} "
                            f"USDA={src[fid]}")

    print(f"Dòng: {len(df)} | Cột: {len(df.columns)}")
    print(f"name_vi còn trống: {int(df['name_vi'].isna().sum())}")
    print(f"base_unit != 'g' : {int((df['base_unit'] != 'g').sum())}")
    print(f"review_needed=True: {int(df['review_needed'].sum())}")

    if problems:
        print(f"\n{len(problems)} vấn đề:")
        for p in problems:
            print(f"  ! {p}")
        return 1
    print("\nOK: group_token và 4 chỉ số dinh dưỡng khớp nguồn USDA toàn bộ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

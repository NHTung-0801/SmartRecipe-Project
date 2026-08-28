"""Gán aisle_id cho từng nguyên liệu trong dataset.

Hai lớp logic, chạy tuần tự:

  Lớp 1 — CATEGORY_MAP: map thô theo food_category_id của USDA.
  Lớp 2 — DESCRIPTION_OVERRIDE: sửa các trường hợp USDA phân loại theo
          nguyên liệu gốc, còn người đi chợ lại tìm ở kệ khác.

Vì sao cần lớp 2: USDA nhét nước tương, miso, đậu hũ, chao, miến vào
"Legumes" vì chúng làm từ đậu nành; nhét nước cốt dừa vào "Nut and Seed".
Map thuần theo category sẽ cho ra "Rau củ: rau muống, cà chua, nước tương,
đậu hũ" — làm tính năng danh sách đi chợ nhóm theo kệ hàng mất ý nghĩa.

aisle_id phải khớp phần seed `aisles` trong sql/init_database.sql (9 kệ, id 1-9).
Đừng đổi thứ tự các kệ ở đó, vì cột aisle_id của CSV trỏ cứng vào id.

Chạy:
    python tools/assign_aisles.py --dry-run
    python tools/assign_aisles.py --apply
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
ENCODING = "utf-8-sig"

AISLES = {
    1: "Rau củ",              # đổi tên từ 'Rau củ quả'
    2: "Thịt & Gia cầm",      # đổi tên từ 'Thịt, Gia cầm'
    3: "Hải sản",
    4: "Gia vị & Nước chấm",
    5: "Đồ khô & Gạo",
    6: "Sữa & Trứng",
    7: "Trái cây",            # mới
    8: "Dầu mỡ & Chất béo",   # mới
    9: "Các loại Hạt",        # mới
}

# Lớp 1: food_category_id -> aisle_id
#
# Cat 16 (Legumes) map thẳng sang 5 'Đồ khô & Gạo' chứ không phải 1 'Rau củ':
# 13/20 dòng là đậu hạt khô, đậu hũ, chao, miến — đều ở kệ đồ khô. Chỉ 3 dòng
# cần override sang gia vị, thay vì phải override 17 dòng nếu để mặc định là 1.
CATEGORY_MAP = {
    1: 6,    # Dairy and Egg Products
    2: 4,    # Spices and Herbs
    4: 8,    # Fats and Oils
    5: 2,    # Poultry Products
    6: 4,    # Soups, Sauces, and Gravies
    9: 7,    # Fruits and Fruit Juices
    10: 2,   # Pork Products
    11: 1,   # Vegetables and Vegetable Products
    12: 9,   # Nut and Seed Products
    13: 2,   # Beef Products
    15: 3,   # Finfish and Shellfish Products
    16: 5,   # Legumes and Legume Products
    19: 4,   # Sweets (mật ong, đường -> kệ gia vị)
    20: 5,   # Cereal Grains and Pasta
}

# Lớp 2: (chuỗi con trong description, không phân biệt hoa thường) -> aisle_id
# Thứ tự có ý nghĩa: luật sau ghi đè luật trước nếu cùng khớp một dòng.
DESCRIPTION_OVERRIDE = [
    # Cat 16 -> gia vị: nước tương và miso là đồ nêm, không phải đậu khô
    ("miso", 4),
    ("soy sauce", 4),
    # Cat 12 -> gia vị: nước cốt dừa dùng để nấu, đứng cùng kệ nước chấm
    ("coconut cream", 4),
    ("coconut milk", 4),
    # Cat 12 -> trái cây: cùi dừa và nước dừa ăn/uống trực tiếp
    ("coconut meat", 7),
    ("coconut water", 7),
    # Cat 16 -> hạt: đậu phộng bán ở kệ hạt
    ("peanuts", 9),
    # Cat 11 -> đồ khô: nấm khô và rong biển khô ở kệ đồ khô, không phải rau tươi
    ("cloud ears, dried", 5),
    ("seaweed", 5),
]


def assign(df: pd.DataFrame) -> tuple[pd.Series, list[str]]:
    """Trả về (Series aisle_id, log các dòng bị override)."""
    unknown = set(df["food_category_id"]) - set(CATEGORY_MAP)
    if unknown:
        sys.exit(f"LỖI: food_category_id chưa có trong CATEGORY_MAP: {sorted(unknown)}")

    aisle = df["food_category_id"].map(CATEGORY_MAP)
    log: list[str] = []
    desc = df["description"].str.lower()

    for pattern, target in DESCRIPTION_OVERRIDE:
        hit = desc.str.contains(pattern, case=False, regex=False)
        for idx in df.index[hit]:
            before = aisle.at[idx]
            if before == target:
                continue
            log.append(f"  {df.at[idx, 'name_vi']:<24} "
                       f"{AISLES[before]:<20} -> {AISLES[target]:<20} "
                       f"(khớp {pattern!r})")
            aisle.at[idx] = target

    return aisle.astype(int), log


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(CSV_FILE, encoding=ENCODING)
    aisle, log = assign(df)

    print(f"Lớp 2 đã override {len(log)} dòng:")
    for line in log:
        print(line)

    print("\nPhân bố theo aisle:")
    counts = aisle.value_counts().sort_index()
    for aid, n in counts.items():
        print(f"  {aid}  {AISLES[aid]:<20} {n:>4}")
    print(f"  {'':3} {'TỔNG':<20} {int(counts.sum()):>4}")

    empty = [f"{aid} {name}" for aid, name in AISLES.items()
             if aid not in counts.index]
    if empty:
        print(f"\nCẢNH BÁO aisle không có nguyên liệu nào: {empty}")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
        return 0

    df["aisle_id"] = aisle
    df["aisle_name"] = aisle.map(AISLES)
    shutil.copy2(CSV_FILE, CSV_FILE.with_suffix(".csv.preaisle"))
    df.to_csv(CSV_FILE, index=False, encoding=ENCODING)
    print(f"\nBackup -> {CSV_FILE.with_suffix('.csv.preaisle')}")
    print(f"Đã ghi thêm cột aisle_id, aisle_name -> {CSV_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

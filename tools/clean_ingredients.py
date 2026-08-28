"""
Giai đoạn 1: Làm sạch dataset USDA SR Legacy -> file CSV chờ dịch tiếng Việt.

Nguồn : dataset/FoodData_Central_sr_legacy_food_csv_2018-04/
Đích  : dataset/ingredients_to_translate.csv

Script này CHỈ làm phần cơ học (lọc, gom nhóm, join dinh dưỡng, validate).
Việc chọn nguyên liệu nào dùng trong bếp Việt và dịch tên là bước làm tay
ở Giai đoạn 2.

Cách chạy:
    python tools/clean_ingredients.py
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --- Cấu hình đường dẫn ---
ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "dataset" / "FoodData_Central_sr_legacy_food_csv_2018-04"
OUT_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"

# --- Bước 1: Category nguyên liệu thô cần giữ ---
KEEP_CATEGORIES = {
    1: "Dairy and Egg Products",
    2: "Spices and Herbs",
    4: "Fats and Oils",
    5: "Poultry Products",
    9: "Fruits and Fruit Juices",
    10: "Pork Products",
    11: "Vegetables and Vegetable Products",
    12: "Nut and Seed Products",
    13: "Beef Products",
    15: "Finfish and Shellfish Products",
    16: "Legumes and Legume Products",
    19: "Sweets",
    20: "Cereal Grains and Pasta",
}

# Cat 19 gần như toàn bánh kẹo/siro pha sẵn, chỉ lấy chất tạo ngọt cơ bản.
SWEETS_KEEP = re.compile(
    r"^(?:sugars?, (?:granulated|brown|powdered)|honey|molasses)", re.IGNORECASE
)

# --- Bước 2: Từ khóa loại trừ món đã chế biến ---
# Chia 2 mức. HARD luôn loại. SOFT chỉ loại khi dòng đó KHÔNG chứa 'raw',
# vì có nguyên liệu thô hợp lệ mang nhãn phụ:
#   "Sweet potato, raw, unprepared (...)" -> phải giữ
# Dùng \b cho từ ngắn dễ khớp sai: 'dish' không có \b sẽ ăn luôn
# "Radishes" và "Gourd, dishcloth"; 'bar' sẽ ăn "barley".
HARD_EXCLUDE = [
    r"cooked", r"boiled", r"fried", r"baked", r"roasted", r"grilled",
    r"braised", r"steamed", r"canned", r"candied", r"breaded", r"with sauce",
    r"\bdish\b", r"casserole", r"\bsalad\b", r"dressing", r"mayonnaise",
    r"spread", r"imitation", r"filled", r"fortified",
    r"substitute", r"replacement", r"supplement",
    r"beverage", r"dessert", r"ice cream", r"topping", r"whipped",
    r"pudding", r"instant", r"reconstituted", r"formulated",
    r"cheese food", r"\bpuffs?\b", r"\bsticks?\b", r"au gratin",
    r"scalloped", r"o'brien", r"hash brown", r"\bkraft\b",
]
# 'sauce' loại món sốt pha sẵn, NHƯNG nước tương / nước mắm / sốt cá là gia vị
# nền của bếp Việt -> phải giữ. Chỉ loại 'sauce' khi không nằm trong nhóm này.
SAUCE_RE = re.compile(r"\bsauces?\b", re.IGNORECASE)
SAUCE_KEEP_RE = re.compile(r"soy sauce|fish sauce|oyster sauce", re.IGNORECASE)
SOFT_EXCLUDE = [
    r"\bunprepared\b", r"\bprepared\b", r"home-prepared", r"dry mix",
    r"\bfrozen\b",
]
# KHÔNG đưa r"\bmixed\b" vào SOFT: USDA đặt tên "Mollusks, squid, mixed species,
# raw" / "Mollusks, clam, mixed species, raw" -> mực và nghêu bị loại oan.
# Chỉ loại 'mixed' khi là món trộn thật sự (mixed vegetables, mixed nuts).
MIXED_DISH_RE = re.compile(
    r"\bmixed\b(?!\s+species)", re.IGNORECASE
)
HARD_RE = re.compile("|".join(HARD_EXCLUDE), re.IGNORECASE)
SOFT_RE = re.compile("|".join(SOFT_EXCLUDE), re.IGNORECASE)
RAW_RE = re.compile(r"\braw\b", re.IGNORECASE)

# Rác thương hiệu + sản phẩm công nghiệp. 179/829 dòng ở lần chạy trước rơi vào
# nhóm này (50 brand + 129 industrial), không dùng được cho bếp gia đình.
BRAND_RE = re.compile(
    r"\bSILK\b|HORMEL|CHOBANI|LIFEWAY|MORI-NU|Vitasoy|HOUSE FOODS|BOLTHOUSE|"
    r"OCEAN SPRAY|NAKED JUICE|CONCORD|\bPAM\b|HERSHEY|NESTLE|USDA Commodity",
    re.IGNORECASE,
)
INDUSTRIAL_RE = re.compile(
    r"\bindustrial\b|shortening|margarine|meatless|vegetarian|meat extender|"
    r"protein isolate|protein concentrate|partially defatted|"
    r"mechanically deboned|added solution|\bmeal\b, partially|"
    r"low linolenic|antifoaming|principal use",
    re.IGNORECASE,
)

# --- Bước 3: Gom nhóm biến thể theo token thích ứng ---
# Không dùng số token cố định theo category, vì cùng một category vẫn có
# nhóm phình rất to:
#   cat 4 "Oil, ..."   -> 59 dòng chung token "oil"
#   cat 1 "Cheese, ..." -> 79 dòng chung token "cheese"
#   cat 13 "Beef, ..."  -> 404 dòng chung token "beef"
# Cách làm: bắt đầu 1 token, nhóm nào còn quá MAX_GROUP_SIZE dòng thì
# tách sâu thêm 1 token, tối đa MAX_TOKEN_DEPTH.
# MAX_GROUP_SIZE=20 quá lỏng: "peppers" (14 dòng) và "mollusks" (12 dòng) không
# bị tách -> mất hết ớt, nghêu, sò, hàu chỉ còn 1 dòng đại diện mỗi nhóm.
MAX_GROUP_SIZE = 4
MAX_TOKEN_DEPTH = 4

# --- Bước 4: Nutrient ID cần lấy ---
NUTRIENT_MAP = {
    1008: "calories",  # Energy (KCAL)
    1003: "protein",   # Protein (G)
    1004: "fat",       # Total lipid (fat) (G)
    1005: "carbs",     # Carbohydrate, by difference (G)
}

# --- Bước 5: Ngưỡng validate ---
# Nới hơn kế hoạch gốc vì dữ liệu USDA có giá trị hợp lệ vượt ngưỡng tròn:
#   Lard / beef tallow / fish oil = 902 kcal  (đúng, không phải lỗi)
#   Oil, flaxseed  pro+fat+carb  = 100.09     (sai số làm tròn)
MAX_CALORIES = 910
MAX_MACRO_SUM = 105
ATWATER_TOLERANCE = 0.25
# Dưới mốc này, sai số tương đối Atwater vô nghĩa (chia cho số rất nhỏ).
ATWATER_MIN_CALORIES = 20

# --- Bước 6: Khối lượng riêng (g/ml) để sinh unit_conversions ở Giai đoạn 3 ---
DENSITY_OIL = 0.92
DENSITY_MILK = 1.03


def load_source() -> pd.DataFrame:
    """Bước 1: Đọc food.csv + food_category.csv, giữ lại category nguyên liệu thô."""
    food = pd.read_csv(SRC_DIR / "food.csv")
    categories = pd.read_csv(SRC_DIR / "food_category.csv")

    total = len(food)
    food = food[food["food_category_id"].isin(KEEP_CATEGORIES)].copy()

    # Cat 19: chỉ giữ chất tạo ngọt cơ bản, bỏ toàn bộ bánh kẹo/siro.
    is_sweets = food["food_category_id"] == 19
    sweets_ok = food["description"].str.contains(SWEETS_KEEP, regex=True, na=False)
    food = food[~is_sweets | sweets_ok].copy()

    cat_names = categories.set_index("id")["description"]
    food["category_name"] = food["food_category_id"].map(cat_names)

    print(f"[Bước 1] {total} dòng -> {len(food)} dòng sau khi giữ "
          f"{len(KEEP_CATEGORIES)} category nguyên liệu thô")
    return food


def exclude_processed(food: pd.DataFrame) -> pd.DataFrame:
    """Bước 2: Bỏ các dòng là món đã chế biến.

    HARD: loại vô điều kiện.
    SOFT: chỉ loại nếu dòng đó không có nhãn 'raw'.
    """
    before = len(food)
    desc = food["description"]

    hard = desc.str.contains(HARD_RE, regex=True, na=False)
    soft = desc.str.contains(SOFT_RE, regex=True, na=False)
    is_raw = desc.str.contains(RAW_RE, regex=True, na=False)

    # 'sauce' loại món sốt, trừ nước tương / nước mắm / dầu hào.
    sauce = (desc.str.contains(SAUCE_RE, regex=True, na=False)
             & ~desc.str.contains(SAUCE_KEEP_RE, regex=True, na=False))
    # 'mixed' loại món trộn, trừ 'mixed species' (tên loài của USDA).
    mixed = desc.str.contains(MIXED_DISH_RE, regex=True, na=False)

    brand = desc.str.contains(BRAND_RE, regex=True, na=False)
    industrial = desc.str.contains(INDUSTRIAL_RE, regex=True, na=False)

    drop = hard | sauce | brand | industrial | ((soft | mixed) & ~is_raw)
    food = food[~drop].copy()
    print(f"[Bước 2] {before} -> {len(food)} dòng "
          f"(hard: {int(hard.sum())}, sauce: {int(sauce.sum())}, "
          f"brand: {int(brand.sum())}, industrial: {int(industrial.sum())}, "
          f"soft/mixed: {int(((soft | mixed) & ~is_raw).sum())})")
    return food


def attach_nutrition(food: pd.DataFrame) -> pd.DataFrame:
    """Bước 3: Join food_nutrient.csv và pivot 4 chỉ số về dạng cột.

    Làm TRƯỚC bước gom nhóm để bước chọn đại diện có sẵn dữ liệu dinh dưỡng.
    """
    nutrients = pd.read_csv(
        SRC_DIR / "food_nutrient.csv",
        usecols=["fdc_id", "nutrient_id", "amount"],
    )
    nutrients = nutrients[nutrients["nutrient_id"].isin(NUTRIENT_MAP)]

    pivot = nutrients.pivot_table(
        index="fdc_id", columns="nutrient_id", values="amount", aggfunc="first"
    ).rename(columns=NUTRIENT_MAP)

    # Đảm bảo đủ 4 cột dù nutrient nào đó vắng mặt hoàn toàn
    for col in NUTRIENT_MAP.values():
        if col not in pivot.columns:
            pivot[col] = np.nan

    merged = food.merge(pivot, left_on="fdc_id", right_index=True, how="left")

    cols = list(NUTRIENT_MAP.values())
    missing = int(merged[cols].isna().any(axis=1).sum())
    merged[cols] = merged[cols].fillna(0)

    print(f"[Bước 3] Join dinh dưỡng cho {len(merged)} dòng "
          f"({missing} dòng thiếu ít nhất 1 chỉ số -> điền 0)")
    return merged


def assign_group_token(food: pd.DataFrame) -> pd.DataFrame:
    """Gán group_token bằng cách tách sâu dần các nhóm quá lớn.

    Bắt đầu ở độ sâu 1 token. Nhóm nào còn nhiều hơn MAX_GROUP_SIZE dòng và
    description còn token để tách thì tăng độ sâu lên 1, lặp tới MAX_TOKEN_DEPTH.
    """
    parts = food["description"].str.lower().str.split(",").map(
        lambda ps: [re.sub(r"\s+", " ", p).strip() for p in ps]
    )
    part_count = parts.str.len()
    depth = pd.Series(1, index=food.index)

    for _ in range(MAX_TOKEN_DEPTH - 1):
        token = pd.Series(
            [", ".join(p[:d]) for p, d in zip(parts, depth)],
            index=food.index,
        )
        size = token.groupby(token).transform("size")
        needs_split = (size > MAX_GROUP_SIZE) & (part_count > depth)
        if not needs_split.any():
            break
        depth = depth + needs_split.astype(int)

    food["group_token"] = [", ".join(p[:d]) for p, d in zip(parts, depth)]
    food["token_depth"] = depth
    return food


def deduplicate(food: pd.DataFrame) -> pd.DataFrame:
    """Bước 4: Gom nhóm biến thể, mỗi nhóm chọn 1 dòng đại diện.

    Ưu tiên: (1) có chữ 'raw', (2) description ngắn nhất.
    """
    food = assign_group_token(food)
    food["_is_raw"] = food["description"].str.contains(
        r"\braw\b", case=False, regex=True, na=False
    )
    food["_desc_len"] = food["description"].str.len()
    food["group_size"] = food.groupby("group_token")["fdc_id"].transform("size")

    # _is_raw giảm dần (True trước), rồi _desc_len tăng dần -> lấy dòng đầu nhóm
    ordered = food.sort_values(
        ["group_token", "_is_raw", "_desc_len"],
        ascending=[True, False, True],
    )
    picked = ordered.groupby("group_token", as_index=False).first()

    biggest = int(picked["group_size"].max())
    print(f"[Bước 4] {len(food)} dòng -> {len(picked)} nhóm nguyên liệu "
          f"(nhóm lớn nhất: {biggest} biến thể)")
    return picked


def clean_name(description: str) -> str:
    """Bỏ hậu tố ', raw' và khoảng trắng thừa khỏi tên gốc."""
    name = re.sub(r",\s*raw\s*$", "", str(description), flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", name).strip()


def validate(food: pd.DataFrame) -> pd.DataFrame:
    """Bước 5: Sanity check + đối chiếu hệ số Atwater. Chỉ GẮN CỜ, không xóa dòng."""
    cal = food["calories"]
    macro_sum = food["protein"] + food["fat"] + food["carbs"]

    out_of_range = (cal < 0) | (cal > MAX_CALORIES) | (macro_sum > MAX_MACRO_SUM)

    estimated = 4 * food["protein"] + 9 * food["fat"] + 4 * food["carbs"]
    # Chia cho NaN thay vì 0 để không sinh inf; nguyên liệu 0 kcal (muối) là hợp lệ.
    deviation = (estimated - cal).abs() / cal.replace(0, np.nan)
    atwater_bad = (deviation > ATWATER_TOLERANCE) & (cal >= ATWATER_MIN_CALORIES)

    food["atwater_estimate"] = estimated.round(2)
    food["review_needed"] = (out_of_range | atwater_bad).fillna(False)

    print(f"[Bước 5] Ngoài ngưỡng: {int(out_of_range.sum())} | "
          f"Lệch Atwater >{int(ATWATER_TOLERANCE * 100)}%: {int(atwater_bad.sum())} | "
          f"Tổng cần review: {int(food['review_needed'].sum())}/{len(food)}")
    return food


def assign_units(food: pd.DataFrame) -> pd.DataFrame:
    """Bước 6: base_unit='g' (USDA tính per 100 gram) + density cho nguyên liệu lỏng."""
    food["base_unit"] = "g"

    desc = food["description"].str.lower()
    is_oil = (food["food_category_id"] == 4) & desc.str.contains(
        r"\boil\b", regex=True, na=False
    )
    is_milk = (food["food_category_id"] == 1) & desc.str.startswith("milk")

    food["density"] = np.nan
    food.loc[is_oil, "density"] = DENSITY_OIL
    food.loc[is_milk, "density"] = DENSITY_MILK

    print(f"[Bước 6] base_unit='g' cho toàn bộ | density: "
          f"{int(is_oil.sum())} dầu ({DENSITY_OIL}), "
          f"{int(is_milk.sum())} sữa ({DENSITY_MILK})")
    return food


def export(food: pd.DataFrame) -> None:
    """Bước 7: Xuất CSV, thêm cột trống name_vi để điền ở Giai đoạn 2."""
    food["description"] = food["description"].map(clean_name)
    food["name_vi"] = ""
    # Cột lọc tay Giai đoạn 2: điền 1 = giữ, 0 = bỏ. Để trống coi như chưa xét.
    food["keep"] = ""

    columns = [
        "fdc_id", "description", "name_vi", "keep",
        "food_category_id", "category_name",
        "group_token", "token_depth", "group_size", "calories", "protein",
        "fat", "carbs", "atwater_estimate", "base_unit", "density",
        "review_needed",
    ]
    result = (food[columns]
              .sort_values(["food_category_id", "description"])
              .reset_index(drop=True))

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig để Excel mở không lỗi font tiếng Việt.
    # Lưu ý: file .sql sinh ở Giai đoạn 3 phải là utf-8 KHÔNG BOM.
    result.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")

    print(f"[Bước 7] Đã xuất {len(result)} dòng -> {OUT_FILE}")
    print("\nSố nguyên liệu theo nhóm:")
    for (cat_id, cat_name), count in result.groupby(
            ["food_category_id", "category_name"]).size().items():
        print(f"  {cat_id:>3}  {cat_name:<38} {count:>4}")


def main() -> int:
    if not SRC_DIR.exists():
        print(f"LỖI: Không tìm thấy thư mục dataset: {SRC_DIR}", file=sys.stderr)
        return 1

    for filename in ("food.csv", "food_category.csv", "food_nutrient.csv"):
        if not (SRC_DIR / filename).exists():
            print(f"LỖI: Thiếu file bắt buộc: {filename}", file=sys.stderr)
            return 1

    food = load_source()
    food = exclude_processed(food)
    food = attach_nutrition(food)
    food = deduplicate(food)
    food = validate(food)
    food = assign_units(food)
    export(food)
    return 0


if __name__ == "__main__":
    sys.exit(main())

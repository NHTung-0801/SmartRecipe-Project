"""Gộp các nhóm nguyên liệu bị USDA tách quá mảnh về một dòng đại diện.

Vì sao cần script riêng thay vì sửa tay trong Excel: Excel đã một lần làm hỏng
cấu trúc CSV (xem tools/repair_csv.py). Sửa bằng script thì có log, có backup,
và chạy lại được.

Mỗi luật gộp phải chỉ rõ fdc_id GIỮ LẠI, không để script tự đoán, vì chỉ số
dinh dưỡng giữa các biến thể chênh nhau nhiều (bò xay 70% nạc 332 kcal so với
90% nạc 176 kcal) — chọn sai là sai calo của mọi công thức dùng nó.

Sau khi gộp, dòng đại diện được gán lại group_token / token_depth / group_size
cho khớp nhóm mới, để tools/verify_dataset.py vẫn kiểm tra được.

Chạy:
    python tools/collapse_groups.py --dry-run
    python tools/collapse_groups.py --apply
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

# Mỗi phần tử: (tên tiếng Việt mới, fdc_id giữ lại, group_token mới,
#               token_depth mới, danh sách fdc_id bị loại)
#
# Thịt bò xay: giữ 174036 (80% nạc / 20% mỡ) vì đây là loại bán phổ thông nhất
# ở quầy thịt, nằm giữa dải 70–90% nên sai số calo về hai phía đều nhỏ nhất.
# group_token 'beef, ground' ở depth 2 vẫn dựng lại được từ description gốc
# "Beef, ground, 80% lean meat / 20% fat" nên verify_dataset.py không báo lỗi.
COLLAPSE_RULES = [
    (
        "Thịt bò xay",
        174036,
        "beef, ground",
        2,
        [168608, 168652, 171796, 174030],
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(CSV_FILE, encoding=ENCODING)
    before = len(df)
    drop_ids: list[int] = []

    for name_vi, keep_id, token, depth, remove_ids in COLLAPSE_RULES:
        ids = [keep_id, *remove_ids]
        found = df[df["fdc_id"].isin(ids)]
        if len(found) != len(ids):
            missing = set(ids) - set(found["fdc_id"])
            sys.exit(f"LỖI: không thấy fdc_id {sorted(missing)} trong CSV")

        print(f"Gộp {len(ids)} dòng -> {name_vi!r} (giữ fdc_id {keep_id})")
        for _, r in found.iterrows():
            mark = "GIỮ" if r["fdc_id"] == keep_id else "bỏ"
            print(f"  {mark:>4}  [{r.fdc_id}] {r.name_vi:<22} "
                  f"{r.calories:>6} kcal | P {r.protein:>5} | F {r.fat:>5}")

        idx = df.index[df["fdc_id"] == keep_id][0]
        df.at[idx, "name_vi"] = name_vi
        df.at[idx, "group_token"] = token
        df.at[idx, "token_depth"] = depth
        df.at[idx, "group_size"] = len(ids)
        drop_ids.extend(remove_ids)

    df = df[~df["fdc_id"].isin(drop_ids)].reset_index(drop=True)
    print(f"\n{before} dòng -> {len(df)} dòng (bỏ {len(drop_ids)})")

    dup = df[df["name_vi"].duplicated(keep=False)]
    if len(dup):
        print("\nCẢNH BÁO trùng name_vi sau khi gộp:")
        print(dup[["fdc_id", "description", "name_vi"]].to_string(index=False))

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
        return 0

    shutil.copy2(CSV_FILE, CSV_FILE.with_suffix(".csv.precollapse"))
    df.to_csv(CSV_FILE, index=False, encoding=ENCODING)
    print(f"\nBackup -> {CSV_FILE.with_suffix('.csv.precollapse')}")
    print(f"Đã ghi -> {CSV_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

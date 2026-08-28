"""Sinh lại các file dataset/vi_batch_XXX.txt từ CSV cuối cùng.

Vì sao cần: các file lô ban đầu là bản nháp gõ tay theo thứ tự CSV lúc đó.
Sau khi tools/collapse_groups.py gộp bớt dòng, số thứ tự trong file txt không
còn khớp vị trí trong CSV nữa, nên không apply lại được.

Script này coi CSV là nguồn chân lý và xuất lại file lô cho khớp, để:
  - bộ file lô trở thành bản lưu trữ đọc được, số thứ tự đúng;
  - chạy lại `translate_helper.py apply` cho từng lô là phép no-op, dùng
    làm kiểm tra vòng tròn (round-trip) rằng CSV và file txt nhất quán.

KHÔNG dùng file txt để seed database — nguồn seed là CSV.

Chạy:
    python tools/export_batches.py --dry-run
    python tools/export_batches.py --apply
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset"
CSV_FILE = DATASET_DIR / "ingredients_to_translate.csv"
ENCODING = "utf-8-sig"
BATCH_SIZE = 50


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(CSV_FILE, encoding=ENCODING)
    if df["name_vi"].isna().any():
        sys.exit("LỖI: còn dòng chưa có name_vi, chưa nên xuất file lô.")

    total = len(df)
    for start in range(1, total + 1, BATCH_SIZE):
        chunk = df.iloc[start - 1: start - 1 + BATCH_SIZE]
        path = DATASET_DIR / f"vi_batch_{start:03d}.txt"
        lines = [f"{i}. {vi}" for i, vi
                 in zip(range(start, start + len(chunk)), chunk["name_vi"])]
        body = "\n".join(lines) + "\n"

        print(f"{path.name:<20} {len(chunk):>3} dòng  "
              f"({lines[0]}  …  {lines[-1]})")
        if args.apply:
            # utf-8-sig để khớp cách translate_helper.py đọc lại (nó strip BOM).
            path.write_text(body, encoding="utf-8-sig")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì)")
    else:
        print(f"\nĐã xuất lại {(total + BATCH_SIZE - 1) // BATCH_SIZE} file lô "
              f"từ {total} dòng CSV.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

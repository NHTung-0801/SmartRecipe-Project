"""Hỗ trợ Giai đoạn 2: lọc tay + dịch tên nguyên liệu sang tiếng Việt.

Ba lệnh con:

  batch  - Xuất từng lô dòng chưa dịch ra text đánh số, dán thẳng vào chatbot.
           Chỉ lấy dòng có keep=1 (nếu cột keep tồn tại).

  apply  - Ghép bản dịch trở lại CSV theo SỐ THỨ TỰ của lô, có kiểm tra
           số dòng khớp. Không khớp -> báo lỗi, không ghi gì.

  status - Thống kê tiến độ: đã giữ / đã dịch / còn lại.

Vì sao ghép theo số thứ tự mà không theo tên: tên tiếng Anh có dấu phẩy và
ngoặc, chatbot rất hay đổi định dạng khi trả lời. Số thứ tự thì ổn định.

Cách dùng:
    python tools/translate_helper.py status
    python tools/translate_helper.py batch --start 1 --size 50
    python tools/translate_helper.py apply --start 1 --size 50 --file vi.txt
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
ENCODING = "utf-8-sig"


def load() -> pd.DataFrame:
    if not CSV_FILE.exists():
        sys.exit(f"LỖI: Chưa có {CSV_FILE}. Chạy tools/clean_ingredients.py trước.")
    df = pd.read_csv(CSV_FILE, encoding=ENCODING)
    if "name_vi" not in df.columns:
        df["name_vi"] = ""
    df["name_vi"] = df["name_vi"].fillna("").astype(str)
    return df


def keep_flag(df: pd.DataFrame) -> pd.Series | None:
    """Trả về Series 1/0/NaN của cột keep, hoặc None nếu chưa có cột.

    Ô trống là 'chưa xét', KHÔNG phải 'bỏ' -> giữ NaN, không fillna(0).
    """
    if "keep" not in df.columns:
        return None
    return pd.to_numeric(df["keep"], errors="coerce")


def selected(df: pd.DataFrame) -> pd.DataFrame:
    """Tập dòng cần dịch, thứ tự ỔN ĐỊNH.

    Chỉ lọc theo keep==1, KHÔNG loại dòng đã dịch. Nếu loại dòng đã dịch thì
    tập này co lại sau mỗi lần apply, khiến '--start 51' của lô 2 trỏ nhầm dòng.
    Giữ nguyên tập -> số thứ tự lô 1..50, 51..100 luôn cố định.
    """
    keep = keep_flag(df)
    if keep is None:
        return df
    return df[keep == 1]


def untranslated(df: pd.DataFrame) -> pd.DataFrame:
    """Các dòng thuộc tập cần dịch nhưng name_vi còn trống (chỉ để đếm)."""
    rows = selected(df)
    return rows[rows["name_vi"].str.strip() == ""]


def cmd_status(_: argparse.Namespace) -> int:
    df = load()
    total = len(df)
    translated = int((df["name_vi"].str.strip() != "").sum())

    print(f"Tổng số dòng            : {total}")
    keep = keep_flag(df)
    if keep is None:
        print("Không có cột 'keep' -> dịch toàn bộ (đã lọc bằng "
              "tools/suggest_keep.py).")
    else:
        print(f"Đã đánh dấu giữ (keep=1): {int((keep == 1).sum())}")
        print(f"Đã đánh dấu bỏ  (keep=0): {int((keep == 0).sum())}")
        print(f"Chưa xét (để trống)     : {int(keep.isna().sum())}")
    print(f"Đã dịch                 : {translated}")
    print(f"Còn phải dịch           : {len(untranslated(df))}")
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    df = load()
    rows = selected(df)
    if rows.empty:
        print("Chưa có dòng nào keep=1. Điền cột 'keep' = 1 trước đã.")
        return 0

    chunk = rows.iloc[args.start - 1: args.start - 1 + args.size]
    if chunk.empty:
        print(f"Không có dòng nào từ vị trí {args.start}. Tổng cần dịch: {len(rows)}")
        return 0

    # Không còn cột keep (đã lọc bằng suggest_keep.py) -> cả file là tập cần dịch.
    scope = "dòng keep=1" if keep_flag(df) is not None else "dòng cần dịch"
    done = int((chunk["name_vi"].str.strip() != "").sum())
    print(f"# Lô {args.start}..{args.start + len(chunk) - 1} / {len(rows)} {scope}")
    if done:
        print(f"# CẢNH BÁO: {done} dòng trong lô này ĐÃ có name_vi, apply sẽ ghi đè.")
    print("# Dán khối dưới đây cho chatbot, yêu cầu trả về ĐÚNG "
          f"{len(chunk)} dòng, giữ nguyên số thứ tự.\n")
    for i, desc in enumerate(chunk["description"], start=args.start):
        print(f"{i}. {desc}")
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    df = load()
    rows = selected(df)
    chunk = rows.iloc[args.start - 1: args.start - 1 + args.size]
    if chunk.empty:
        sys.exit(f"LỖI: Không có dòng nào từ vị trí {args.start}.")

    # utf-8-sig: bản dịch dán từ Notepad/PowerShell thường có BOM, nếu đọc bằng
    # utf-8 thường thì dòng đầu thành "\ufeff1. ..." và tiền tố số không bóc được.
    raw = Path(args.file).read_text(encoding="utf-8-sig").splitlines()
    names: list[str] = []
    for line in raw:
        line = line.strip().lstrip("\ufeff").strip()
        if not line or line.startswith("#"):
            continue
        # Bỏ tiền tố "12." / "12)" / "12 -" nếu chatbot có đánh số
        m = re.match(r"^\d+\s*[.)\-]\s*(.+)$", line)
        if m:
            line = m.group(1).strip()
        names.append(line)

    if len(names) != len(chunk):
        sys.exit(f"LỖI: Bản dịch có {len(names)} dòng nhưng lô cần "
                 f"{len(chunk)} dòng. Không ghi gì cả.")

    df.loc[chunk.index, "name_vi"] = names
    df.to_csv(CSV_FILE, index=False, encoding=ENCODING)

    print(f"Đã ghi {len(names)} bản dịch vào {CSV_FILE}")
    for idx, vi in zip(chunk.index, names):
        print(f"  {df.at[idx, 'description'][:55]:<55} -> {vi}")
    print(f"\nCòn lại chưa dịch: {len(untranslated(load()))}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Xem tiến độ lọc và dịch")

    p_batch = sub.add_parser("batch", help="Xuất một lô để dịch")
    p_batch.add_argument("--start", type=int, default=1)
    p_batch.add_argument("--size", type=int, default=50)

    p_apply = sub.add_parser("apply", help="Ghép bản dịch trở lại CSV")
    p_apply.add_argument("--start", type=int, required=True)
    p_apply.add_argument("--size", type=int, default=50)
    p_apply.add_argument("--file", required=True, help="File .txt chứa bản dịch")

    args = parser.parse_args()
    return {"status": cmd_status, "batch": cmd_batch, "apply": cmd_apply}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())

"""Đề xuất cột 'keep' cho dataset nguyên liệu, rồi XÓA hẳn các dòng keep=0.

Mặc định GIỮ (theo yêu cầu "đa số muốn giữ lại"). Chỉ loại khi khớp một luật
DROP cụ thể. Mỗi luật ghi lý do vào cột 'drop_reason' để rà lại được.

Chạy thử, không ghi gì:
    python tools/suggest_keep.py --dry-run

Ghi đè CSV, xóa hẳn dòng keep=0 (có backup .bak + file dropped riêng):
    python tools/suggest_keep.py --apply
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "dataset" / "ingredients_to_translate.csv"
DROPPED_FILE = ROOT / "dataset" / "dropped_ingredients.csv"
ENCODING = "utf-8-sig"


def rx(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# (lý do, set category áp dụng hoặc None = mọi category, regex)
# Luật đầu tiên khớp sẽ thắng.
DROP_RULES: list[tuple[str, set[int] | None, re.Pattern]] = [
    ("thit thu la", {5}, rx(
        r"^(emu|ostrich|squab|guinea hen|pheasant|quail|"
        r"ruffed grouse|canada goose|duck, wild)")),

    ("phan loai thit My qua chi tiet", {13}, rx(
        r"trimmed to|separable lean|composite of|retail cuts|"
        r"\b(choice|select|prime|all grades)\b|sandwich steaks")),
    ("phan loai thit My qua chi tiet", {10}, rx(
        r"separable lean|composite of|enhanced|\bcap steak\b|"
        r"petite tender|sirloin tip roast|shoulder breast")),

    ("gio ham kieu My", {10}, rx(
        r"cured, ham|breakfast strips|salt pork|blade roll|"
        r"pickled pork hocks|oriental style, dehydrated")),

    ("noi tang it dung", {5, 10, 13}, rx(
        r"\b(brain|lungs|pancreas|spleen|thymus|suet|leaf fat|backfat|"
        r"chitterlings|carcass)\b|mechanically separated|separable fat|"
        r"skin only|skin \(|skin, from")),

    # --- Sữa & phô mai ---
    ("pho mai hiem o VN", {1}, rx(
        r"cheese, (gjetost|caraway|cheshire|colby|brick|limburger|"
        r"port de salut|tilsit|fontina|edam|gouda|gruyere|muenster|"
        r"neufchatel|roquefort|romano|provolone|monterey|blue|brie|"
        r"camembert|swiss|queso|mexican|dry white|white, queso|"
        r"goat, hard|cottage)")),
    ("pho mai che bien san", {1}, rx(r"pasteurized process|american")),
    ("sua dac thu phuong Tay", {1}, rx(
        r"milk, (human|indian buffalo|sheep|goat|low sodium|producer|"
        r"dry|buttermilk|evaporated|chocolate|fluid, 1%|lowfat)|"
        r"eggnog|milk shakes|whey|dulce de leche|half and half|"
        r"sour cream, light|cream, fluid|butter oil")),
    ("sua chua co huong vi san", {1}, rx(
        r"yogurt.*(vanilla|strawberry|chocolate|fruit|peach|blueberry|"
        r"coconut|mango|lemon)|DANNON|OIKOS")),
    ("trung dang bot", {1}, rx(r"egg.*dried")),
    ("trung thu la", {1}, rx(r"egg, (goose|turkey|quail)")),

    # --- Dầu mỡ ---
    ("dau hiem o VN", {4}, rx(
        r"oil, (babassu|cupu assu|sheanut|ucuhuba|teaseed|tomatoseed|"
        r"nutmeg butter|apricot kernel|hazelnut|poppyseed|oat|"
        r"soybean lecithin|wheat germ|almond|walnut|grapeseed|"
        r"flaxseed|cocoa butter|corn and canola|corn, peanut)|"
        r"fat, goose|bacon grease|vegetable oil, palm kernel")),
    ("dau ca bo sung", {4}, rx(r"^fish oil")),

    # --- Gia vị ---
    ("gia vi phuong Tay it dung", {2}, rx(
        r"spices, (allspice|anise|caraway|cardamom|celery seed|chervil|"
        r"dill seed|dill weed|fenugreek|mace|marjoram|oregano|"
        r"poppy seed|poultry seasoning|pumpkin pie|saffron|sage|savory|"
        r"tarragon|thyme|rosemary|parsley|basil)|"
        r"^(spearmint|rosemary|dill weed|thyme|peppermint), |"
        r"seasoning mix")),

    # --- Trái cây ---
    ("trai cay hiem o VN", {9}, rx(
        r"^(abiyuch|acerola|carissa|cherimoya|crabapples|currants|"
        r"custard-apple|elderberries|feijoa|gooseberries|groundcherries|"
        r"horned melon|java-plum|mammy-apple|oheloberries|pitanga|"
        r"prickly pears|quinces|rose-apples|roselle|rowal|sapodilla|"
        r"sapote|baobab|goji|jujube|loquats|mulberries|nectarines|"
        r"grapes, muscadine|melons, casaba|persimmons, native|"
        r"blackberries|blueberries|cranberries|raspberries|"
        r"breadfruit|apricots|figs|plums|pears|cherries|clementines|"
        r"kumquats|rhubarb|dates)")),
    ("nuoc ep dong chai", {9}, rx(
        r"juice|smoothie|puree|concentrate|ODWALLA|REAL LEMON")),
    ("trai cay say/che bien", {9}, rx(
        r"dehydrated|dried|stewed|raisins|prunes|sulfured|peel")),
    ("giong trai cay My", {9}, rx(
        r"(apples|oranges|pears|grapefruit), raw, "
        r"(fuji|gala|golden|granny|red delicious|california|florida|"
        r"navels|bartlett|bosc|green anjou|red anjou|asian|"
        r"pink and red,|white,|without skin|with peel)")),

    # --- Rau củ ---
    ("rau la khong co o VN", {11}, rx(
        r"^(arrowhead|artichokes|arugula|borage|butterbur|cardoon|"
        r"celtuce|chicory|cornsalad|dandelion|dock|endive|epazote|eppaw|"
        r"fiddlehead|fireweed|jerusalem-artichokes|jute|lambsquarters|"
        r"nopales|pokeberry|purslane|radicchio|salsify|sesbania|"
        r"vinespinach|yautia|poi|grape leaves|hearts of palm|"
        r"beet greens|collards|kale|chard|broccoli raab|"
        r"brussels sprouts|kohlrabi|parsnips|rutabagas|"
        r"turnip|celeriac|burdock|alfalfa|cress|amaranth|"
        r"chrysanthemum|drumstick|mountain yam|new zealand|"
        r"winged bean|hyacinth|lima beans|broadbeans|"
        r"lettuce, (butterhead|cos|green leaf|red leaf|iceberg)|"
        r"squash, (summer|winter)|beets|borage|kanpyo)")),
    ("rau che bien san", {11}, rx(
        r"pickle|kimchi|catsup|relish|souffle|pancakes|mashed|sauteed|"
        r"dehydrated|powder|juice|succotash|salted|sun-dried|flour|"
        r"sprouted|radishes, hawaiian")),
    ("nam phuong Tay", {11}, rx(
        r"mushrooms?, (chanterelle|morel|maitake|portabella|"
        r"brown, italian)|exposed to ultraviolet")),
    ("rong bien it dung", {11}, rx(
        r"seaweed, (canadian|agar|irishmoss|spirulina|laver)")),
    ("ot kho phuong Tay", {11}, rx(
        r"peppers, (ancho|pasilla|hungarian|banana)")),
    ("giong khoai tay My", {11}, rx(
        r"potatoes, (red|russet|white|raw, skin)")),

    # --- Hạt ---
    ("hat hiem o VN", {12}, rx(
        r"nuts, (acorn|beechnuts|brazilnuts|butternuts|hickorynuts|"
        r"pilinuts|ginkgo|macadamia|pecans|pine nuts|almond paste|"
        r"walnuts, glazed|chestnuts, (european|japanese)|"
        r"hazelnuts|pistachio)|"
        r"seeds, (breadfruit|breadnut|cottonseed|safflower|sisymbrium|"
        r"hemp|chia|flaxseed|sesame flour|sunflower seed butter|"
        r"watermelon)")),
    ("bo hat che bien", {12}, rx(r"butter, plain|tahini|desiccated")),

    # --- Đậu ---
    ("dau hiem o VN", {16}, rx(
        r"beans, (cranberry|french|great northern|navy|pink|"
        r"small white|yellow|kidney, (california|royal))|"
        r"broadbeans|lupins|mothbeans|hyacinth|carob|"
        r"pigeon peas|chickpea flour|liquid from stewed")),
    ("san pham dau nanh phuong Tay", {16}, rx(
        r"soymilk|tofu yogurt|hummus|natto|okara|papad|tempeh|"
        r"peanut butter|peanut flour|soy flour|soy meal")),

    # --- Ngũ cốc ---
    ("ngu coc phuong Tay", {20}, rx(
        r"^(barley|buckwheat|bulgur|couscous|millet|rye|semolina|"
        r"sorghum|triticale|wild rice|arrowroot flour|"
        r"vital wheat gluten|oat bran|oat flour|oats)|"
        r"wheat, (hard|soft|durum|sprouted)")),
    ("mi/pasta phuong Tay", {20}, rx(
        r"macaroni|spaghetti|^pasta|noodles, (egg|flat|japanese)|"
        r"wheat flour, white, (tortilla|cake)|"
        r"cornmeal, (yellow|white, self-rising|degermed)|"
        r"corn flour, (masa|yellow)|wheat flours, bread, unenriched|"
        r"wheat flour, whole-grain, soft")),
    ("cam/mam ngu coc", {20}, rx(r"bran, crude|germ, crude|malt flour")),

    # --- Hải sản ---
    ("ca nuoc lanh khong co o VN", {15}, rx(
        r"fish, (burbot|butterfish|cisco|cusk|drum|gefiltefish|"
        r"haddock|halibut|herring|ling|lingcod|monkfish|"
        r"ocean perch|pout|roughy|sablefish|scup|shad|sheepshead|"
        r"smelt|spot|sturgeon|sucker|sunfish|turbot|whitefish|"
        r"whiting|wolffish|yellowtail|caviar|roe|surimi|"
        r"bass, striped|bluefish|flatfish|pollock|pompano|"
        r"rockfish|sea bass|seatrout|shark|swordfish|trout|"
        r"tilefish|croaker|perch, mixed|"
        r"salmon, (chum|chinook|coho|pink|sockeye|atlantic)|"
        r"mackerel, (king|spanish|pacific|salted))")),
    ("hai san la", {15}, rx(
        r"crustaceans, (crayfish|lobster|spiny lobster|"
        r"crab, (queen|dungeness|alaska))|"
        r"mollusks, (abalone|whelk|scallop|mussel)|"
        r"turtle|frog legs|jellyfish")),
]

# Ưu tiên CAO HƠN mọi luật DROP. Dùng cho nguyên liệu cốt lõi vô tình
# rơi vào một pattern DROP rộng (vd "Beef, ground" dính "separable lean").
KEEP_OVERRIDE = rx(
    r"beef, variety meats and by-products, "
    r"(liver|heart|kidneys|tongue|tripe)|"
    r"^beef, ground, (70|80|90)% lean|^beef, grass-fed, ground|"
    r"^beef, brisket, whole|^beef, shank crosscuts|"
    r"^beef, chuck for stew|^beef, rib, shortribs|"
    r"^beef, flank, steak, separable lean only|"
    r"^beef, tenderloin, steak, separable lean only|"
    r"^pork, fresh, ground|^pork, ground|^pork, fresh, belly|"
    r"^pork, fresh, spareribs|^pork, fresh, backribs|^pork loin, fresh|"
    r"^pork, fresh, loin, tenderloin|^pork, fresh, shoulder, whole|"
    r"^pork, fresh, leg \(ham\), whole|"
    r"pork, fresh, variety meats and by-products, "
    r"(liver|heart|kidneys|tongue|feet|tail|stomach|ears)|"
    r"^chicken, ground|^turkey, ground, 93|"
    r"^chicken, broilers or fryers, "
    r"(breast, meat and skin|thigh, meat and skin|drumstick|wing|"
    r"leg, meat only|meat only)$|"
    r"^chicken, broiler or fryers, breast, skinless|"
    r"^chicken, (liver|heart|gizzard)|"
    r"^duck, domesticated, liver|"
    r"^milk, whole|^milk, reduced fat|^milk, nonfat|"
    r"^yogurt, plain|^yogurt, greek, plain|"
    r"^cheese, mozzarella, whole milk|^cheese, cheddar \(|^cheese, cream|"
    r"^cheese, parmesan, grated|^cheese, ricotta|^cheese, feta|"
    r"^butter, salted|^cream, sour, cultured|"
    r"^egg, whole, raw|^egg, white, raw|^egg, yolk, raw|^egg, duck|"
    r"^oil, (canola|coconut|palm|rice bran|sunflower|mustard|avocado)|"
    r"^oil, vegetable, soybean|^lard|"
    r"^spices, (pepper, black|chili powder|curry|cinnamon|"
    r"cloves|coriander|cumin|fennel|garlic powder|ginger|"
    r"mustard seed|nutmeg|onion powder|paprika|turmeric|bay leaf)|"
    r"^spices, coriander leaf|^basil, fresh|^salt, table|"
    r"^vanilla extract|^vinegar, cider|"
    r"^apples, raw, with skin|^oranges, raw, all|^pineapple, raw|"
    r"^grapefruit, raw, pink and red and white|^avocados, raw|"
    r"^lemon juice$|^lime juice$|"
    r"^seaweed, (kelp|wakame)|"
    r"^mushrooms, (white|shiitake|enoki|oyster)$|"
    r"^beans, kidney, all types|^beans, kidney, red|"
    r"^cornmeal, whole-grain, white|^corn flour, whole-grain|"
    r"^wheat flour, white, all-purpose|^wheat flour, white, bread|"
    r"^wheat flour, whole-grain \(|^rice noodles|^rice flour|"
    r"^fish, (tuna|tilapia|catfish|carp|mackerel, atlantic|"
    r"anchovy|snapper|grouper|mahimahi|milkfish|eel|cod|mullet|"
    r"pike, walleye)|"
    r"^crustaceans, (shrimp|crab, blue)|"
    r"^mollusks, (squid|clam|oyster|octopus|cuttlefish|snail)",
)

# Bò nhập khẩu và các biến thể gà/gà tây kiểu Mỹ — thêm sau các luật trên.
DROP_RULES.extend([
    ("thit bo nhap khau", {13}, rx(
        r"^beef, (australian|new zealand)|corned beef|"
        r"grass-fed, (?!ground)")),
    ("bo phan ga it dung", {5}, rx(
        r"giblets|capons|cornish|rotisserie|"
        r"chicken, (roasting|stewing)|"
        r"back, meat only|neck, meat only|"
        r"\b(dark meat|light meat)\b|meat and skin and")),
    ("ga tay it dung o VN", {5}, rx(r"^turkey")),
    ("gan ngong hiem o VN", {5}, rx(r"^goose, liver")),

    # --- Trùng nghĩa / dư thừa: giữ 1-2 dòng đại diện mỗi loại ---
    ("trung nghia bo bam", {13}, rx(
        r"^beef, ground, (70|75|93|95|97)% lean")),
    ("trung nghia pho mai", {1}, rx(
        r"cheese, cheddar, sharp|cheese, low fat, cheddar|"
        r"cheese, low-sodium, cheddar|"
        r"cheese, mozzarella, (low moisture|low sodium|nonfat|part skim)|"
        r"cheese, parmesan, (dry grated|hard|low sodium|shredded)")),
    ("trung nghia nam meo", {11}, rx(
        r"^pepeao, dried|^jew's ear")),
    ("trung nghia bong cai", {11}, rx(
        r"^broccoli, (flower clusters|leaves|stalks)")),
    ("trung nghia ca chua", {11}, rx(
        r"^tomatoes, (orange|yellow)")),
    ("trung nghia bap cai", {11}, rx(
        r"^cabbage, (common|savoy)")),
    ("trung nghia cu cai", {11}, rx(
        r"^radishes, white icicle")),
    ("trung nghia gao/bot", {20}, rx(
        r"^rice, white, (medium|short)-grain")),
    ("trung nghia dau tuong", {16}, rx(
        r"soy sauce, reduced sodium|"
        r"soy sauce made from hydrolyzed")),
    ("rau it dung o VN", {11}, rx(
        r"^(arrowroot|tomatillos|pepper, banana|"
        r"mustard spinach|fennel, bulb|asparagus|"
        r"soybeans, green|pigeonpeas|beans, fava)")),
])


def build_keep(df: pd.DataFrame) -> pd.DataFrame:
    keep = pd.Series(1, index=df.index, dtype=int)
    reason = pd.Series("", index=df.index, dtype=object)

    desc = df["description"].astype(str)
    cat = df["food_category_id"]
    # Dùng .map + pattern.search thay cho .str.contains để tránh
    # UserWarning "pattern has match groups" của pandas.
    override = desc.map(lambda s: KEEP_OVERRIDE.search(s) is not None)

    for label, cats, pattern in DROP_RULES:
        hit = desc.map(lambda s, p=pattern: p.search(s) is not None)
        if cats is not None:
            hit &= cat.isin(cats)
        # Không đè lên dòng đã loại bởi luật trước, và bỏ qua dòng override.
        hit &= (keep == 1) & ~override
        keep[hit] = 0
        reason[hit] = label

    df = df.copy()
    df["keep"] = keep
    df["drop_reason"] = reason
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true",
                       help="Chỉ in thống kê, không ghi file")
    group.add_argument("--apply", action="store_true",
                       help="Ghi CSV mới, xóa hẳn dòng keep=0")
    args = parser.parse_args()

    if not CSV_FILE.exists():
        sys.exit(f"LỖI: Không thấy {CSV_FILE}")

    df = pd.read_csv(CSV_FILE, encoding=ENCODING)
    before = len(df)
    df = build_keep(df)

    kept = df[df["keep"] == 1]
    dropped = df[df["keep"] == 0]

    print(f"Tổng    : {before}")
    print(f"Giữ lại : {len(kept)}")
    print(f"Loại bỏ : {len(dropped)}\n")

    print("Loại theo lý do:")
    for label, count in dropped["drop_reason"].value_counts().items():
        print(f"  {label:<34} {count:>4}")

    print("\nGiữ lại theo nhóm:")
    for (cid, cname), count in kept.groupby(
            ["food_category_id", "category_name"]).size().items():
        print(f"  {cid:>3}  {cname:<38} {count:>4}")

    if args.dry_run:
        print("\n(dry-run: chưa ghi gì. Chạy --apply để ghi.)")
        return 0

    backup = CSV_FILE.with_suffix(".csv.bak")
    shutil.copy2(CSV_FILE, backup)

    dropped.drop(columns=["keep"]).to_csv(
        DROPPED_FILE, index=False, encoding=ENCODING)
    kept.drop(columns=["keep", "drop_reason"]).to_csv(
        CSV_FILE, index=False, encoding=ENCODING)

    print(f"\nBackup       -> {backup}")
    print(f"Dòng đã loại -> {DROPPED_FILE}")
    print(f"Còn lại      -> {CSV_FILE} ({len(kept)} dòng)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

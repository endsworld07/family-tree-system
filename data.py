from pathlib import Path
import json

from relationship import RELATION_LAYOUT


# ============================================
# 資料夾
# ============================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DATA_FILE = DATA_DIR / "family.json"


# ============================================
# 建立資料夾
# ============================================

DATA_DIR.mkdir(exist_ok=True)


# ============================================
# 預設資料
# ============================================

def default_family():

    family = {}

    for title in RELATION_LAYOUT.keys():

        family[title] = ""

    return family


# ============================================
# 建立 JSON
# ============================================

def initialize_data():

    if not DATA_FILE.exists():

        save_family(default_family())


# ============================================
# 讀取
# ============================================

def load_family():

    initialize_data()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

    except Exception:

        data = default_family()

        save_family(data)

    # 若 relationship.py 新增稱謂，自動補齊

    changed = False

    for title in RELATION_LAYOUT.keys():

        if title not in data:

            data[title] = ""

            changed = True

    if changed:

        save_family(data)

    return data


# ============================================
# 儲存
# ============================================

def save_family(family):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            family,
            f,
            ensure_ascii=False,
            indent=4
        )


# ============================================
# 清空
# ============================================

def reset_family():

    save_family(default_family())
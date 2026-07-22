# data.py

import json
from pathlib import Path
from relationship import RELATIONS

# -----------------------------
# JSON 檔案位置
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "family.json"


def default_family():
    """
    建立預設親屬資料
    """
    return {
        person["title"]: ""
        for person in RELATIONS
    }


def load_family():
    """
    讀取 family.json
    若不存在則建立
    """

    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():

        family = default_family()

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                family,
                f,
                ensure_ascii=False,
                indent=4
            )

        return family

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        family = json.load(f)

    # 新增 relationship.py 增加的新親屬
    changed = False

    for person in RELATIONS:

        if person["title"] not in family:
            family[person["title"]] = ""
            changed = True

    # 刪除 relationship.py 已不存在的親屬
    valid_titles = {
        person["title"]
        for person in RELATIONS
    }

    remove_keys = [
        key
        for key in family
        if key not in valid_titles
    ]

    for key in remove_keys:
        del family[key]
        changed = True

    if changed:

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                family,
                f,
                ensure_ascii=False,
                indent=4
            )

    return family


def save_family(family):
    """
    儲存 family.json
    """

    DATA_DIR.mkdir(exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            family,
            f,
            ensure_ascii=False,
            indent=4
        )
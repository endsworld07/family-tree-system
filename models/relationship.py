from __future__ import annotations

from dataclasses import dataclass

from models.person import Person


DISPLAY_TITLES = {
    # ==========================================
    # 申請人
    # ==========================================
    "SELF": "申請人",

    # ==========================================
    # 父母
    # ==========================================
    "FATHER": "父親",
    "MOTHER": "母親",

    # ==========================================
    # 祖先
    # ==========================================
    "GRANDFATHER": "祖父",
    "GRANDMOTHER": "祖母",

    "GREAT_GRANDFATHER": "曾祖父",
    "GREAT_GRANDMOTHER": "曾祖母",

    "HIGH_GRANDFATHER": "高祖父",
    "HIGH_GRANDMOTHER": "高祖母",

    "HEAVEN_GRANDFATHER": "天祖父",
    "HEAVEN_GRANDMOTHER": "天祖母",

    "TAI_GRANDFATHER": "太祖父",
    "TAI_GRANDMOTHER": "太祖母",

    "LIE_GRANDFATHER": "烈祖父",
    "LIE_GRANDMOTHER": "烈祖母",

    # ==========================================
    # 配偶
    # ==========================================
    "SPOUSE": "配偶",

    # ==========================================
    # 子孫
    # ==========================================
    "CHILD": "子女",
    "GRANDCHILD": "孫子女",

    # ==========================================
    # 伯叔
    # ==========================================
    "UNCLE": "伯叔父",
    "UNCLE_SPOUSE": "伯叔母",

    # ==========================================
    # 堂親
    # ==========================================
    "COUSIN_BROTHER": "堂兄弟",
    "COUSIN_SISTER": "堂姊妹",
}


@dataclass(slots=True)
class Relationship:
    """
    解析完成的親屬關係
    """

    person: Person

    title: str | None = None

    generation: int = 0

    order: int = 0

    source: str | None = None

    @property
    def display_title(self) -> str:
        return DISPLAY_TITLES.get(self.title, self.title or "")
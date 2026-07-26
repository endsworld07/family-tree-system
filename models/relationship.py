from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from models.person import Person


DISPLAY_TITLES = {
    # ==========================================================
    # 申請人
    # ==========================================================
    "SELF": "申請人",

    # ==========================================================
    # 父母
    # ==========================================================
    "FATHER": "父親",
    "MOTHER": "母親",

    # ==========================================================
    # 祖先
    # ==========================================================
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

    # ==========================================================
    # 配偶
    # ==========================================================
    "SPOUSE": "配偶",

    # ==========================================================
    # 子孫
    # ==========================================================
    "CHILD": "子女",
    "GRANDCHILD": "孫子女",

    # ==========================================================
    # 伯叔
    # ==========================================================
    "UNCLE": "伯叔父",
    "UNCLE_SPOUSE": "伯叔母",

    "GREAT_UNCLE": "曾伯叔父",
    "GREAT_UNCLE_SPOUSE": "曾伯叔母",

    "HIGH_UNCLE": "高伯叔父",
    "HIGH_UNCLE_SPOUSE": "高伯叔母",

    "HEAVEN_UNCLE": "天伯叔父",
    "HEAVEN_UNCLE_SPOUSE": "天伯叔母",

    "TAI_UNCLE": "太伯叔父",
    "TAI_UNCLE_SPOUSE": "太伯叔母",

    "LIE_UNCLE": "烈伯叔父",
    "LIE_UNCLE_SPOUSE": "烈伯叔母",

    # ==========================================================
    # 堂親
    # ==========================================================
    "COUSIN_BROTHER": "堂兄弟",
    "COUSIN_SISTER": "堂姊妹",
}


@dataclass(slots=True)
class Relationship:
    """
    一位人物的親屬關係資訊
    """

    # 基本資料
    person: Person
    title: str | None = None
    generation: int = 0
    order: int = 0
    source: str | None = None

    # 親屬關係
    father: "Relationship | None" = None
    mother: "Relationship | None" = None

    spouses: list["Relationship"] = field(default_factory=list)
    children: list["Relationship"] = field(default_factory=list)
    siblings: list["Relationship"] = field(default_factory=list)

    # 所屬家庭
    group: Any = None

    @property
    def display_title(self) -> str:
        return DISPLAY_TITLES.get(self.title, self.title or "")

    @property
    def has_spouse(self) -> bool:
        return bool(self.spouses)

    @property
    def has_children(self) -> bool:
        return bool(self.children)

    def add_spouse(self, spouse: "Relationship") -> None:
        if spouse is not self and spouse not in self.spouses:
            self.spouses.append(spouse)

    def add_child(self, child: "Relationship") -> None:
        if child not in self.children:
            self.children.append(child)

    def add_sibling(self, sibling: "Relationship") -> None:
        if sibling is not self and sibling not in self.siblings:
            self.siblings.append(sibling)
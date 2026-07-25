from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(slots=True)
class Person:
    """
    人物資料（V2）

    一個 Person 只代表一個人。
    親屬關係由 father、mother、spouses、children 建立。
    """

    # -------------------------
    # 基本資料
    # -------------------------

    id: str
    name: str
    gender: Literal["男", "女"]

    # -------------------------
    # 血緣
    # -------------------------

    father: str | None = None
    mother: str | None = None

    # -------------------------
    # 婚姻
    # -------------------------

    spouses: list[str] = field(default_factory=list)

    # -------------------------
    # 子女
    # -------------------------

    children: list[str] = field(default_factory=list)

    # -------------------------
    # 顯示資訊
    # -------------------------

    custom_title: str | None = None
    note: str | None = None

    # =========================
    # Property
    # =========================

    @property
    def is_male(self) -> bool:
        return self.gender == "男"

    @property
    def is_female(self) -> bool:
        return self.gender == "女"

    @property
    def has_spouse(self) -> bool:
        return len(self.spouses) > 0

    @property
    def spouse_count(self) -> int:
        return len(self.spouses)

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    @property
    def child_count(self) -> int:
        return len(self.children)
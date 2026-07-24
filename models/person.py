from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(slots=True)
class Person:
    """
    人物基本資料
    """

    id: str
    name: str
    gender: Literal["男", "女"]

    father: str | None = None
    mother: str | None = None

    custom_title: str | None = None
    note: str | None = None

    @property
    def is_male(self) -> bool:
        return self.gender == "男"

    @property
    def is_female(self) -> bool:
        return self.gender == "女"
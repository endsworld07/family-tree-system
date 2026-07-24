from __future__ import annotations

from dataclasses import dataclass

from models.person import Person


DISPLAY_TITLES = {
    "SELF": "本人",
    "FATHER": "父親",
    "MOTHER": "母親",
    "SPOUSE": "配偶",
    "CHILD": "子女",
    "SIBLING": "兄弟姊妹",
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

    @property
    def display_title(self) -> str:
        return DISPLAY_TITLES.get(self.title, self.title or "")
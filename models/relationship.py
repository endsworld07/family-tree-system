from __future__ import annotations

from dataclasses import dataclass

from models.person import Person


@dataclass(slots=True)
class Relationship:
    """
    解析完成的親屬關係
    """

    # 對應的人物
    person: Person

    # 稱謂（父親、母親、祖父、本人…）
    title: str | None = None

    # 世代
    generation: int = 0

    # 同世代排序
    order: int = 0
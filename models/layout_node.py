from __future__ import annotations

from dataclasses import dataclass

from models.relationship import Relationship


@dataclass(slots=True)
class LayoutNode:
    """
    親屬關係圖版面節點
    """

    relationship: Relationship

    # 左上角座標
    x: int = 0
    y: int = 0

    # 節點尺寸
    width: int = 120
    height: int = 60
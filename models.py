from dataclasses import dataclass, field
from typing import Optional


# ----------------------------------------
# 人物資料
# ----------------------------------------

@dataclass
class Person:
    """
    人物資料模型

    本類別只保存資料，不包含任何商業邏輯。
    """

    id: str
    name: str
    label: str = ""

    father: Optional[str] = None
    mother: Optional[str] = None

    spouses: list[str] = field(default_factory=list)


# ----------------------------------------
# 排版位置
# ----------------------------------------

@dataclass
class Position:
    """
    Layout Engine 計算後的位置。

    column：
        第幾欄（左右）

    row：
        第幾列（上下）

    本類別不保存任何 SVG 或畫面座標。
    """

    column: int
    row: int
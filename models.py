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

    # 此人為招贅者時，其子女的祖系主幹改由子女的母親往上追溯。
    is_matrilineal_main_line: bool = False

    # 是否列入本次起掘人數統計
    is_exhumation: bool = False

    # 顯示於關係圖的小字備註，例如：已移置他處
    non_exhumation_note: str = ""


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

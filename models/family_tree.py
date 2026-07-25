from __future__ import annotations

from dataclasses import dataclass

from models.family_group import FamilyGroup


@dataclass(slots=True)
class FamilyTree:
    """
    一棵完整的親屬關係樹。

    FamilyTree 是整個系統的根物件（Root Object），
    封裝所有 FamilyGroup 的關係，提供 LayoutEngine、
    ConnectionEngine 與 SvgRenderer 作為唯一的輸入。

    不負責任何排版、繪圖或親屬稱謂判斷。
    """

    # 最上層家庭（根節點）
    root: FamilyGroup

    # 申請人家庭
    applicant: FamilyGroup

    # 全部家庭
    groups: dict[str, FamilyGroup]

    @property
    def size(self) -> int:
        """家庭數量。"""
        return len(self.groups)


    @property
    def is_empty(self) -> bool:
        """是否沒有任何家庭。"""
        return not self.groups    
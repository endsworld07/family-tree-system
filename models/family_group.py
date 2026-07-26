from __future__ import annotations

from dataclasses import dataclass, field

from models.relationship import Relationship


@dataclass(slots=True)
class FamilyGroup:
    """
    一個家庭單位（Family Unit）。

    FamilyGroup 是整張親屬關係圖的基本單位。

    例如：

        祖父
        祖母

    或

        爸爸
        媽媽

    或

          本人
      妻子1   妻子2

    規則：
    ----------------------------
    - head 為本組主要人物（直系血親）
    - spouses 為所有配偶
    - Group 內不畫任何連線
    - 只有 FamilyGroup 與 FamilyGroup 之間才有連線
    - Layout 由 LayoutEngine 負責
    """

    # ==========================================================
    # Basic
    # ==========================================================

    # 唯一識別碼（通常使用 head.person.id）
    id: str

    # 本組主要人物
    head: Relationship

    # 所有配偶（0~N）
    spouses: list[Relationship] = field(default_factory=list)

    # ==========================================================
    # Tree
    # ==========================================================

    # 上一代家庭
    parent: FamilyGroup | None = None

    # 下一代家庭
    child_groups: list[FamilyGroup] = field(default_factory=list)

    # ==========================================================
    # Layout（由 LayoutEngine 計算）
    # ==========================================================

    x: float = 0.0
    y: float = 0.0

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def has_spouse(self) -> bool:
        """是否有配偶。"""
        return bool(self.spouses)

    @property
    def has_children(self) -> bool:
        """是否有下一代家庭。"""
        return bool(self.child_groups)

    # ==========================================================
    # Methods
    # ==========================================================

    def add_spouse(
        self,
        spouse: Relationship,
    ) -> None:
        """加入配偶。"""
        self.spouses.append(spouse)

    def add_child_group(
        self,
        child: FamilyGroup,
    ) -> None:
        """加入下一代家庭。"""
        self.child_groups.append(child)
        child.parent = self
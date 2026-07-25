from __future__ import annotations

from dataclasses import dataclass, field

from models.relationship import Relationship


@dataclass(slots=True)
class FamilyGroup:
    """
    代表一個家庭（Family Unit）。

    一個 FamilyGroup 以一位主要人物（head）為中心，
    包含其主要配偶、其他配偶、子女，以及與其他 FamilyGroup
    的父子關係。

    FamilyGroup 不負責任何版面配置（Layout）、
    SVG 繪製或親屬稱謂判斷。
    """

    # 唯一識別碼（通常使用 head.person.id）
    id: str

    # 家庭代表人
    head: Relationship

    # 主要配偶
    spouse: Relationship | None = None

    # 其他配偶（預留多配偶支援）
    other_spouses: list[Relationship] = field(default_factory=list)

    # 子女（Relationship）
    children: list[Relationship] = field(default_factory=list)

    # 上一代家庭
    parent: FamilyGroup | None = None

    # 下一代家庭
    child_groups: list[FamilyGroup] = field(default_factory=list)

    @property
    def has_spouse(self) -> bool:
        """是否有主要配偶。"""
        return self.spouse is not None

    @property
    def has_children(self) -> bool:
        """是否有子女家庭。"""
        return bool(self.child_groups)

    def add_child(self, child: Relationship) -> None:
        self.children.append(child)

    def add_child_group(self, child: FamilyGroup) -> None:
        self.child_groups.append(child)
        child.parent = self
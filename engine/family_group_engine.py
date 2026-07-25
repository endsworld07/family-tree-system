from __future__ import annotations

from models.family_group import FamilyGroup
from models.relationship import Relationship


class FamilyGroupEngine:
    """
    Government Family Tree

    將 RelationshipResolver 產生的 Relationship
    轉換成 FamilyGroup。
    """

    def __init__(
        self,
        relationships: list[Relationship],
    ):

        self.relationships = relationships

        self.groups: list[FamilyGroup] = []

    # =====================================================
    # Public
    # =====================================================

    def build(
        self,
    ) -> FamilyGroup | None:

        self.groups.clear()

        self._build_main_groups()

        self._attach_parents()

        self._attach_spouses()

        self._attach_children()

        if not self.groups:
            return None

        return self.groups[0]

    # =====================================================
    # Main Groups
    # =====================================================

    def _build_main_groups(
        self,
    ) -> None:

        main_titles = {
            "SELF",
            "FATHER",
            "GRANDFATHER",
            "GREAT_GRANDFATHER",
            "HIGH_GRANDFATHER",
            "HEAVEN_GRANDFATHER",
            "TAI_GRANDFATHER",
            "LIE_GRANDFATHER",
        }

        previous_group = None

        for relationship in self.relationships:

            if relationship.title not in main_titles:
                continue

            group = FamilyGroup(
                generation=relationship.generation,
                applicant=relationship,
            )

            if previous_group is not None:
                previous_group.next_group = group

            self.groups.append(group)

            previous_group = group
    # =====================================================
    # Parents
    # =====================================================

    def _attach_parents(
        self,
    ) -> None:

    # generation -> FamilyGroup
        group_map = {
            group.generation: group
            for group in self.groups
        }

        for relationship in self.relationships:

            title = relationship.title

            # 父系主幹
            if title in {
                "FATHER",
                "GRANDFATHER",
                "GREAT_GRANDFATHER",
                "HIGH_GRANDFATHER",
                "HEAVEN_GRANDFATHER",
                "TAI_GRANDFATHER",
                "LIE_GRANDFATHER",
            }:

                child_group = group_map.get(
                    relationship.generation + 1
                )

                if child_group:
                    child_group.father = relationship

            # 母系
            elif title in {
                "MOTHER",
                "GRANDMOTHER",
                "GREAT_GRANDMOTHER",
                "HIGH_GRANDMOTHER",
                "HEAVEN_GRANDMOTHER",
                "TAI_GRANDMOTHER",
                "LIE_GRANDMOTHER",
            }:

                child_group = group_map.get(
                    relationship.generation + 1
                )

                if child_group:
                    child_group.mother = relationship

    # =====================================================
    # Spouses
    # =====================================================

    def _attach_spouses(
        self,
    ) -> None:

        # generation -> FamilyGroup
        group_map = {
            group.generation: group
            for group in self.groups
        }

        for relationship in self.relationships:

            if relationship.title != "SPOUSE":
                continue

            group = group_map.get(relationship.generation)

            if group is None:
                continue

            # 第一位配偶放中央
            if group.spouse is None:
                group.spouse = relationship

            # 其餘配偶放側邊
            else:
                group.applicant_other_spouses.append(
                    relationship
                )

    # =====================================================
    # Children
    # =====================================================

    def _attach_children(
        self,
    ) -> None:

        # generation -> FamilyGroup
        group_map = {
            group.generation: group
            for group in self.groups
        }

        for relationship in self.relationships:

            if relationship.title != "CHILD":
                continue

            # 子女掛到申請人這一代
            parent_group = group_map.get(
                relationship.generation - 1
            )

            if parent_group is None:
                continue

            parent_group.children.append(
                relationship
            )

        # 保持固定排序
        for group in self.groups:

            group.children.sort(
                key=lambda r: (
                    r.order,
                    r.person.name,
                )
            )        
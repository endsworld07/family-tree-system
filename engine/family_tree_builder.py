from __future__ import annotations

from models.family_group import FamilyGroup
from models.family_tree import FamilyTree
from models.relationship import Relationship


class FamilyTreeBuilder:
    """
    將 Relationship 集合建立為 FamilyTree。

    Responsibilities
    ----------------
    1. 建立 FamilyGroup
    2. 建立 FamilyTree
    3. 建立家庭階層

    Not Responsibilities
    --------------------
    - Layout
    - SVG
    - Connection
    """

    HEAD_RELATIONS = {
        "SELF",

        "FATHER",
        "GRANDFATHER",
        "GREAT_GRANDFATHER",
        "HIGH_GRANDFATHER",
        "HEAVEN_GRANDFATHER",
        "TAI_GRANDFATHER",
        "LIE_GRANDFATHER",

        "UNCLE",

        "CHILD",
    }

    def __init__(
        self,
        relationships: list[Relationship],
    ) -> None:

        self.relationships = relationships

        self.relationship_map: dict[str, Relationship] = {}

        self.groups: list[FamilyGroup] = []

        self.group_map: dict[str, FamilyGroup] = {}

        self.tree: FamilyTree | None = None

    # ==========================================================
    # Public
    # ==========================================================

    def build(self) -> FamilyTree:
        """
        建立完整 FamilyTree。
        """

        self.relationship_map.clear()

        self.groups.clear()
        self.group_map.clear()

        self._create_relationship_map()

        self._create_groups()

        self._attach_spouses()

        self._attach_children()

        self._build_child_groups()

        self._build_family_tree()

        if self.tree is None:
            raise RuntimeError("FamilyTree build failed.")

        return self.tree

    # ==========================================================
    # Create
    # ==========================================================

    def _create_relationship_map(
        self,
    ) -> None:
        """
        建立 Relationship 快速索引。
        """

        self.relationship_map.clear()

        for relationship in self.relationships:

            person_id = relationship.person.id

            if person_id in self.relationship_map:

                raise ValueError(
                    f"Duplicate person id: {person_id}"
                )

            self.relationship_map[person_id] = relationship

    def _create_groups(
        self,
    ) -> None:
        """
        建立所有 FamilyGroup。

        只有家庭代表人(Head)才建立 FamilyGroup，
        配偶將於 _attach_spouses() 加入。
        """

        self.groups.clear()

        self.group_map.clear()

        for relationship in self.relationships:

            if not self._is_head_relationship(
                relationship,
            ):
                continue

            group = FamilyGroup(
                id=relationship.person.id,
                head=relationship,
            )

            self.groups.append(group)

            self.group_map[group.id] = group

    # ==========================================================
    # Attach
    # ==========================================================

    def _attach_spouses(
        self,
    ) -> None:
        """
        將配偶加入 FamilyGroup。

        一個 FamilyGroup：
            head
            spouse
            other_spouses
        """

        for group in self.groups:

            person = group.head.person

            for spouse_id in person.spouses:

                spouse_group = self._find_group(spouse_id)

                if spouse_group is not None:
                    continue

                spouse = self._find_relationship(
                    spouse_id,
                )

                if spouse is None:
                    continue

                if group.spouse is None:

                    group.spouse = spouse

                else:

                    group.other_spouses.append(
                        spouse,
                    )

    def _attach_children(
        self,
    ) -> None:
        """
        將子女加入 FamilyGroup。
        """

        for group in self.groups:

            person = group.head.person

            for child_id in person.children:

                child = self._find_relationship(
                    child_id,
                )

                if child is None:
                    continue

                group.children.append(
                    child,
                )

    # ==========================================================
    # Build Tree
    # ==========================================================

    def _build_child_groups(
        self,
    ) -> None:
        """
        建立 FamilyGroup 之間的父子階層。

        規則：
        1. 依 Person.father 建立父子 Group 關係。
        2. 若沒有 father，再使用 mother。
        """

        for group in self.groups:

            person = group.head.person

            parent_group = None

            if person.father:
                parent_group = self._find_group(person.father)

            elif person.mother:
                parent_group = self._find_group(person.mother)

            if parent_group is None:
                continue

            parent_group.add_child_group(group)

    def _build_family_tree(
        self,
    ) -> None:
        """
        建立 FamilyTree。
        """

        root = self._find_root()

        applicant = self._find_applicant()

        self._validate(
            root,
            applicant,
        )

        self.tree = FamilyTree(
            root=root,
            applicant=applicant,
            groups=self.group_map,
        )

    # ==========================================================
    # Find
    # ==========================================================

    def _find_group(
        self,
        person_id: str,
    ) -> FamilyGroup | None:

        return self.group_map.get(
            person_id,
        )

    def _find_relationship(
        self,
        person_id: str,
    ) -> Relationship | None:

        return self.relationship_map.get(
            person_id,
        )

    # ==========================================================
    # Helper
    # ==========================================================

    def _is_head_relationship(
        self,
        relationship: Relationship,
    ) -> bool:

        return (
            relationship.title
            in self.HEAD_RELATIONS
        )

    # ==========================================================
    # Validate
    # ==========================================================

    def _find_root(
        self,
    ) -> FamilyGroup:

        roots = [
            group
            for group in self.groups
            if group.parent is None
        ]

        if not roots:
            raise ValueError(
                "FamilyTree has no root."
            )

        if len(roots) == 1:
            return roots[0]

        # 多個 Root 時，選擇世代最高者
        roots.sort(
            key=lambda g: g.head.generation
        )

        return roots[0]

    def _find_applicant(
        self,
    ) -> FamilyGroup:

        for group in self.groups:

            if group.head.title == "SELF":
                return group

        raise ValueError(
            "Applicant not found."
        )

    def _validate(
        self,
        root: FamilyGroup,
        applicant: FamilyGroup,
    ) -> None:

        if root is None:
            raise ValueError(
                "Root FamilyGroup is None."
            )

        if applicant is None:
            raise ValueError(
                "Applicant FamilyGroup is None."
            )

        if not self.group_map:
            raise ValueError(
                "FamilyGroup is empty."
            )                                
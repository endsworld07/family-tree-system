from __future__ import annotations

from models.family_tree import FamilyTree
from models.family_group import FamilyGroup
from models.relationship import Relationship


class FamilyTreeBuilder:
    """
    將 Relationship 集合建立為 FamilyTree。
    """

    def __init__(self, relationships: list[Relationship]):
        self.relationships = relationships

        self.relationship_map: dict[str, Relationship] = {}

        self.groups: dict[str, FamilyGroup] = {}

        self.tree: FamilyTree | None = None

    def build(self) -> FamilyTree:
        """
        建立完整 FamilyTree。
        """

        self.relationship_map.clear()
        self.groups.clear()

        self._create_relationship_map()

        self._create_groups()

        self._attach_spouses()

        self._attach_children()

        self._build_child_groups()

        self._build_family_tree()

        return self.tree

    def _create_relationship_map(self) -> None:
        """
        建立 Relationship 的快速查詢索引。
        """

        self.relationship_map.clear()

        for relationship in self.relationships:

            person_id = relationship.person.id

            if person_id in self.relationship_map:
                raise ValueError(
                    f"Duplicate person id: {person_id}"
                )

            self.relationship_map[person_id] = relationship

    def _create_groups(self) -> None:
        ...

    def _attach_spouses(self) -> None:
        ...

    def _attach_children(self) -> None:
        ...

    def _build_child_groups(self) -> None:
        ...

    def _build_family_tree(self) -> None:
        ...

    def _find_root(self) -> FamilyGroup:
        ...

    def _find_applicant(self) -> FamilyGroup:
        ...

    def _validate(
        self,
        root: FamilyGroup,
        applicant: FamilyGroup,
    ) -> None:
        ...
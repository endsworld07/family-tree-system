from __future__ import annotations

from dataclasses import dataclass, field

from models.relationship import Relationship


@dataclass(slots=True)
class GraphNode:
    """
    Relationship 的圖形節點。

    GraphNode 不負責：

        - Layout
        - SVG
        - FamilyGroup

    只描述 Relationship 之間的連線。
    """

    relationship: Relationship

    parent: GraphNode | None = None

    children: list[GraphNode] = field(default_factory=list)

    spouses: list[GraphNode] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.relationship.person.id

    @property
    def title(self) -> str | None:
        return self.relationship.title

    @property
    def person(self):
        return self.relationship.person

    def add_child(
        self,
        child: GraphNode,
    ) -> None:

        self.children.append(child)

        child.parent = self

    def add_spouse(
        self,
        spouse: GraphNode,
    ) -> None:

        if spouse not in self.spouses:

            self.spouses.append(spouse)

        if self not in spouse.spouses:

            spouse.spouses.append(self)

    # ==========================================================
    # Create
    # ==========================================================

    def _create_nodes(
        self,
    ) -> None:

        for relationship in self.relationships:

            person_id = relationship.person.id

            if person_id in self.node_map:

                raise ValueError(
                    f"Duplicate person id: {person_id}"
                )

            self.node_map[person_id] = GraphNode(
                relationship=relationship,
            )

    # ==========================================================
    # Find
    # ==========================================================

    def _find_node(
        self,
        person_id: str,
    ) -> GraphNode | None:

        return self.node_map.get(
            person_id,
        )
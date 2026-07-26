from __future__ import annotations

from dataclasses import dataclass

from models.graph_node import GraphNode


@dataclass(slots=True)
class Graph:
    """
    完整親屬圖(Graph)。

    Graph 是 RelationshipResolver 與
    FamilyTreeBuilder 之間的中介模型。
    """

    root: GraphNode

    applicant: GraphNode

    nodes: dict[str, GraphNode]

    @property
    def size(self) -> int:

        return len(self.nodes)

    @property
    def is_empty(self) -> bool:

        return not self.nodes
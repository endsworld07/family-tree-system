from __future__ import annotations

from models.graph import Graph
from models.graph_node import GraphNode
from models.relationship import Relationship


class RelationshipGraphBuilder:
    """
    建立 Relationship Graph。

    Responsibilities
    ----------------
    1. 建立 GraphNode
    2. 建立 Parent Edge
    3. 建立 Spouse Edge
    4. 找出 Root
    5. 找出 Applicant

    不負責：
        - Layout
        - SVG
        - FamilyGroup
    """

    def __init__(
        self,
        relationships: list[Relationship],
    ) -> None:

        self.relationships = relationships

        self.node_map: dict[str, GraphNode] = {}

        self.graph: Graph | None = None

    # ==========================================================
    # Public
    # ==========================================================

    def build(self) -> Graph:

        self.node_map.clear()

        self._create_nodes()

        self._build_parent_edges()

        self._build_spouse_edges()

        root = self._find_root()

        applicant = self._find_applicant()

        self.graph = Graph(
            root=root,
            applicant=applicant,
            nodes=self.node_map,
        )

        return self.graph
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from models import Person
from layout_engine import LayoutResult


# ---------------------------------------------------------
# Connection
# ---------------------------------------------------------

@dataclass
class Connection:
    """單一連線"""

    source: str
    target: str
    type: str


# ---------------------------------------------------------
# Family Group
# ---------------------------------------------------------

@dataclass
class FamilyGroup:
    """同一父母的家庭群組"""

    father: Optional[str]
    mother: Optional[str]
    children: List[str]


# ---------------------------------------------------------
# Connection Result
# ---------------------------------------------------------

@dataclass
class ConnectionResult:
    connections: List[Connection] = field(default_factory=list)
    parent_connections: List[Connection] = field(default_factory=list)
    family_groups: List[FamilyGroup] = field(default_factory=list)


# ---------------------------------------------------------
# Connection Engine
# ---------------------------------------------------------

class ConnectionEngine:
    """
    依照關係與排版位置，建立 SVG 要用的連線資料。

    原則：
    - 保留 parent connections
    - 不畫 spouse connections
    - family_groups 交給 SvgRenderer 畫共同主幹 / 90° 路徑
    """

    def __init__(
        self,
        people: Dict[str, Person],
        relationships: dict,
        layout_result: LayoutResult,
    ):
        self.people = people
        self.relationships = relationships
        self.layout_result = layout_result
        self.result = ConnectionResult()

        self._parent_map = relationships.get("parents", {})
        self._children_map = relationships.get("children", {})
        self._siblings_map = relationships.get("siblings", {})
        self._spouses_map = relationships.get("spouses", {})
        self._family_groups = relationships.get("family_groups", [])

    def build(self) -> ConnectionResult:
        self.result = ConnectionResult()

        self._build_parent_connections()
        self._build_family_groups()

        return self.result

    # ---------------------------------------------------------
    # Parent
    # ---------------------------------------------------------

    def _build_parent_connections(self) -> None:
        """
        建立父 / 母 到子女的連線。

        這裡只保留資料，實際畫法交給 SvgRenderer。
        """
        for child_id, (father_id, mother_id) in self._parent_map.items():
            if (
                father_id
                and father_id in self.layout_result.positions
                and child_id in self.layout_result.positions
            ):
                self._add_connection(
                    father_id,
                    child_id,
                    "parent",
                )

            if (
                mother_id
                and mother_id in self.layout_result.positions
                and child_id in self.layout_result.positions
            ):
                self._add_connection(
                    mother_id,
                    child_id,
                    "parent",
                )

    # ---------------------------------------------------------
    # Family Groups
    # ---------------------------------------------------------

    def _build_family_groups(self) -> None:
        """
        將 family_groups 整理進 result，供 SvgRenderer 畫共同主幹。

        不在這裡畫夫妻線。
        """
        for group in self._family_groups:
            father = group.get("father")
            mother = group.get("mother")
            children = [
                child
                for child in group.get("children", [])
                if child in self.layout_result.positions
            ]

            if not children:
                continue

            self.result.family_groups.append(
                FamilyGroup(
                    father=father,
                    mother=mother,
                    children=children,
                )
            )

    # ---------------------------------------------------------
    # Add Connection
    # ---------------------------------------------------------

    def _add_connection(
        self,
        source: str,
        target: str,
        conn_type: str,
    ) -> None:
        connection = Connection(
            source=source,
            target=target,
            type=conn_type,
        )

        self.result.connections.append(connection)

        if conn_type == "parent":
            self.result.parent_connections.append(connection)
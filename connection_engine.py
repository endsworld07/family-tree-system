from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from models import Person, Position
from layout_engine import LayoutResult


@dataclass
class Connection:
    """單一連線。"""

    source: str
    target: str
    type: str  # parent / spouse


@dataclass
class ConnectionResult:
    """ConnectionEngine 的輸出。"""

    connections: List[Connection] = field(default_factory=list)
    parent_connections: List[Connection] = field(default_factory=list)
    spouse_connections: List[Connection] = field(default_factory=list)


class ConnectionEngine:
    """依照關係與排版位置，建立 SVG 要用的連線資料。"""

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

        self._parent_map: Dict[str, Tuple[Optional[str], Optional[str]]] = relationships.get("parents", {})
        self._spouses_map: Dict[str, List[str]] = relationships.get("spouses", {})

    def build(self) -> ConnectionResult:
        self.result = ConnectionResult()
        self._build_parent_connections()
        self._build_spouse_connections()
        return self.result

    def _build_parent_connections(self) -> None:
        """建立父/母到子女的連線。"""
        for child_id, (father_id, mother_id) in self._parent_map.items():
            if father_id and father_id in self.layout_result.positions:
                self._add_connection(
                    source=father_id,
                    target=child_id,
                    conn_type="parent",
                )

            if mother_id and mother_id in self.layout_result.positions:
                self._add_connection(
                    source=mother_id,
                    target=child_id,
                    conn_type="parent",
                )

    def _build_spouse_connections(self) -> None:
        """建立配偶連線；同一對配偶只畫一次。"""
        seen: Set[Tuple[str, str]] = set()

        for person_id, spouses in self._spouses_map.items():
            for spouse_id in spouses:
                if person_id == spouse_id:
                    continue

                pair_key = tuple(sorted((person_id, spouse_id)))
                if pair_key in seen:
                    continue

                if person_id not in self.layout_result.positions:
                    continue
                if spouse_id not in self.layout_result.positions:
                    continue

                seen.add(pair_key)
                self._add_connection(
                    source=person_id,
                    target=spouse_id,
                    conn_type="spouse",
                )

    def _add_connection(self, source: str, target: str, conn_type: str) -> None:
        connection = Connection(
            source=source,
            target=target,
            type=conn_type,
        )

        self.result.connections.append(connection)

        if conn_type == "parent":
            self.result.parent_connections.append(connection)
        elif conn_type == "spouse":
            self.result.spouse_connections.append(connection)

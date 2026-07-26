from __future__ import annotations

from dataclasses import dataclass

from models.family_tree import FamilyTree


@dataclass(slots=True)
class Connection:
    """
    一條連接線。

    (x1, y1) -------- (x2, y2)
    """

    x1: float
    y1: float

    x2: float
    y2: float

    kind: str

class ConnectionEngine:
    """
    建立 FamilyTree 的連接線。

    Responsibilities
    ----------------
    1. 建立父子線
    2. 建立夫妻線

    Not Responsibilities
    --------------------
    - Layout
    - SVG
    """

    def __init__(
        self,
        tree: FamilyTree,
    ) -> None:

        self.tree = tree

        self.connections: list[Connection] = []

    # ======================================================
    # Public
    # ======================================================

    def build(
        self,
    ) -> list[Connection]:

        self.connections.clear()

        self._build_parent_lines()

        self._build_spouse_lines()

        return self.connections  
    
    # ======================================================
    # 父子線
    # ======================================================   

    def _build_parent_lines(
        self,
    ) -> None:

        for group in self.tree.groups.values():

            if group.parent is None:
                continue

            self.connections.append(

                Connection(
                    x1=group.parent.x,
                    y1=group.parent.y,

                    x2=group.x,
                    y2=group.y,

                    kind="parent",
                )

            )

    # ======================================================
    # 夫妻線
    # ====================================================== 
    def _build_spouse_lines(
        self,
    ) -> None:

        for group in self.tree.groups.values():

            if not group.has_spouse:
                continue

            self.connections.append(

                Connection(
                    x1=group.x,
                    y1=group.y,

                    x2=group.x,
                    y2=group.y,

                    kind="spouse",
                )

            )  
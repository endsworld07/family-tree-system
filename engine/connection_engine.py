#==========================================================
# ConnectionEngine 3.0
# Part 1（正式版）
# Data Model
#==========================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from layout_engine import LayoutGroup, LayoutResult


#==========================================================
# Connection Type
#==========================================================

class ConnectionType(Enum):

    # 主幹
    MAIN = "main"

    # 主幹分支（祖父母→伯父母、父母、叔父母）
    BRANCH = "branch"

    # 主幹到旁系
    SIDE = "side"

    # 單一直線
    LINE = "line"

    # 折線
    POLYLINE = "polyline"


#==========================================================
# Point
#==========================================================

@dataclass(slots=True)
class Point:

    x: float
    y: float


#==========================================================
# Connection
#==========================================================

@dataclass(slots=True)
class Connection:

    # 唯一ID
    id: str

    # Connection種類
    type: ConnectionType

    # 折線所有節點
    points: List[Point] = field(default_factory=list)

    # 起點Group
    start_group: Optional[LayoutGroup] = None

    # 終點Group
    end_group: Optional[LayoutGroup] = None

    # SVG樣式
    stroke: str = "#000000"

    stroke_width: float = 2.0

    dashed: bool = False

    css_class: str = ""

    # 備註
    remark: str = ""


#==========================================================
# Connection Result
#==========================================================

@dataclass(slots=True)
class ConnectionResult:

    # 全部Connection
    connections: List[Connection] = field(default_factory=list)

    # 主幹
    main_connections: List[Connection] = field(default_factory=list)

    # 分支
    branch_connections: List[Connection] = field(default_factory=list)

    # 旁系
    side_connections: List[Connection] = field(default_factory=list)

    # 快速索引
    connection_index: Dict[str, Connection] = field(default_factory=dict)

    # 統計
    connection_count: int = 0

    main_count: int = 0

    branch_count: int = 0

    side_count: int = 0


#==========================================================
# Connection Engine
#==========================================================

class ConnectionEngine:

    #------------------------------------------------------

    def __init__(self):

        self.layout: Optional[LayoutResult] = None

        self.result = ConnectionResult()

        # Branch 與 Parent Group 的距離
        self.branch_offset_y = 30

    #------------------------------------------------------

    def build(
        self,
        layout: LayoutResult
    ) -> ConnectionResult:

        self.layout = layout

        self.result = ConnectionResult()

        # Part 2
        self._build_main_connections()

        # Part 3
        self._build_branch_connections()

        # Part 4
        self._build_side_connections()

        # Part 5
        self._finalize()

        return self.result

#==========================================================
# ConnectionEngine 3.0
# Part 2（正式版）
# Build Main Connections
#==========================================================

    def _build_main_connections(self):

        if self.layout is None:
            return

        groups = self.layout.main_groups

        if len(groups) < 2:
            return

        for parent, child in zip(groups[:-1], groups[1:]):

            connection = Connection(

                id=f"main_{parent.id}_{child.id}",

                type=ConnectionType.MAIN,

                start_group=parent,

                end_group=child,

                points=[

                    Point(
                        x=parent.bottom_center[0],
                        y=parent.bottom_center[1]
                    ),

                    Point(
                        x=child.top_center[0],
                        y=child.top_center[1]
                    )

                ],

                stroke="#000000",

                stroke_width=2.0,

                dashed=False,

                css_class="main-line"

            )

            self.result.connections.append(connection)

            self.result.main_connections.append(connection)
#==========================================================
# ConnectionEngine 3.1
# Part 3（正式版）
# Build Branch Connections
#==========================================================

    def _build_branch_connections(self):

        if self.layout is None:
            return

        #--------------------------------------------------
        # 每個 Main Group 都可能有 Branch
        #--------------------------------------------------

        for parent in self.layout.main_groups:

            side_groups = parent.side_groups

            if not side_groups:
                continue

            #--------------------------------------------------
            # Branch Y
            #
            # 位於 Parent Group 下方
            #--------------------------------------------------

            branch_y = (
                parent.bottom
                + self.branch_offset_y
            )

            #--------------------------------------------------
            # Branch 左端
            #--------------------------------------------------

            start_x = min(
                group.center_x
                for group in side_groups
            )

            #--------------------------------------------------
            # Branch 右端
            #--------------------------------------------------

            end_x = max(
                group.center_x
                for group in side_groups
            )

            #--------------------------------------------------
            # Parent 中心必須包含在 Branch 範圍內
            #--------------------------------------------------

            parent_center_x = parent.center_x

            start_x = min(start_x, parent_center_x)

            end_x = max(end_x, parent_center_x)

            #--------------------------------------------------
            # 建立 Branch
            #--------------------------------------------------

            connection = Connection(

                id=f"branch_{parent.id}",

                type=ConnectionType.BRANCH,

                start_group=parent,

                end_group=None,

                points=[

                    Point(
                        x=start_x,
                        y=branch_y
                    ),

                    Point(
                        x=end_x,
                        y=branch_y
                    )

                ],

                stroke="#000000",

                stroke_width=2.0,

                dashed=False,

                css_class="branch-line"

            )

            self.result.connections.append(connection)

            self.result.branch_connections.append(connection)

#==========================================================
# ConnectionEngine 3.1
# Part 4（正式版）
# Build Side Connections
#==========================================================

    def _build_side_connections(self):

        if self.layout is None:
            return

        #--------------------------------------------------
        # 每一個 Main Group
        #--------------------------------------------------

        for parent in self.layout.main_groups:

            side_groups = parent.side_groups

            if not side_groups:
                continue

            #--------------------------------------------------
            # Branch Y
            #
            # 必須與 Part3 完全一致
            #--------------------------------------------------

            branch_y = (
                parent.bottom
                + self.branch_offset_y
            )

            #--------------------------------------------------
            # 每一個 Side Group
            #--------------------------------------------------

            for group in side_groups:

                connection = Connection(

                    id=f"side_{parent.id}_{group.id}",

                    type=ConnectionType.SIDE,

                    start_group=parent,

                    end_group=group,

                    points=[

                        Point(
                            x=group.center_x,
                            y=branch_y
                        ),

                        Point(
                            x=group.top_center[0],
                            y=group.top_center[1]
                        )

                    ],

                    stroke="#000000",

                    stroke_width=2.0,

                    dashed=False,

                    css_class="side-line"

                )

                self.result.connections.append(connection)

                self.result.side_connections.append(connection)

#==========================================================
# ConnectionEngine 3.1
# Part 5（正式版）
# Finalize
#==========================================================

    def _finalize(self):

        if self.layout is None:
            return self.result

        #--------------------------------------------------
        # 去除重複 Connection
        #--------------------------------------------------

        unique_connections = {}

        for connection in self.result.connections:
            unique_connections[connection.id] = connection

        self.result.connections = list(
            unique_connections.values()
        )

        #--------------------------------------------------
        # 繪製順序
        #
        # MAIN
        #   ↓
        # BRANCH
        #   ↓
        # SIDE
        #--------------------------------------------------

        priority = {

            ConnectionType.MAIN: 0,

            ConnectionType.BRANCH: 1,

            ConnectionType.SIDE: 2,

            ConnectionType.LINE: 3,

            ConnectionType.POLYLINE: 4

        }

        self.result.connections.sort(

            key=lambda connection: (

                priority.get(
                    connection.type,
                    999
                ),

                connection.points[0].y
                if connection.points
                else 0,

                connection.points[0].x
                if connection.points
                else 0

            )

        )

        #--------------------------------------------------
        # 分類
        #--------------------------------------------------

        self.result.main_connections = [

            connection

            for connection in self.result.connections

            if connection.type == ConnectionType.MAIN

        ]

        self.result.branch_connections = [

            connection

            for connection in self.result.connections

            if connection.type == ConnectionType.BRANCH

        ]

        self.result.side_connections = [

            connection

            for connection in self.result.connections

            if connection.type == ConnectionType.SIDE

        ]

        #--------------------------------------------------
        # 建立 Connection Index
        #--------------------------------------------------

        self.result.connection_index.clear()

        for connection in self.result.connections:

            self.result.connection_index[
                connection.id
            ] = connection

        #--------------------------------------------------
        # 統計
        #--------------------------------------------------

        self.result.main_count = len(
            self.result.main_connections
        )

        self.result.branch_count = len(
            self.result.branch_connections
        )

        self.result.side_count = len(
            self.result.side_connections
        )

        self.result.connection_count = len(
            self.result.connections
        )

        #--------------------------------------------------
        # 主幹完整性檢查
        #--------------------------------------------------

        expected = max(
            len(self.layout.main_groups) - 1,
            0
        )

        if self.result.main_count != expected:

            raise RuntimeError(

                "Main Connection Count Error\n"

                f"Expected : {expected}\n"

                f"Actual   : {self.result.main_count}"

            )

        #--------------------------------------------------
        # 完成
        #--------------------------------------------------

        return self.result
#==========================================================
# ConnectionEngine 2.0
# Part 1（正式版）
# Data Model
#==========================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from layout_engine import LayoutGroup, LayoutMember, LayoutResult


#==========================================================
# Connection Type
#==========================================================

class ConnectionType(Enum):

    MAIN = "main"          # 主幹
    SIDE = "side"          # 旁系
    SPOUSE = "spouse"      # 夫妻
    GROUP = "group"        # Group 內部
    VERTICAL = "vertical"  # 垂直線
    HORIZONTAL = "horizontal"  # 水平線


#==========================================================
# Point
#==========================================================

@dataclass
class Point:

    x: float
    y: float


#==========================================================
# Connection
#==========================================================

@dataclass
class Connection:

    id: str

    type: ConnectionType

    start: Point
    end: Point

    start_group: Optional[LayoutGroup] = None
    end_group: Optional[LayoutGroup] = None

    start_member: Optional[LayoutMember] = None
    end_member: Optional[LayoutMember] = None

    label: str = ""

    color: str = "#000000"

    width: float = 2

    dashed: bool = False


#==========================================================
# Connection Result
#==========================================================

@dataclass
class ConnectionResult:

    connections: List[Connection] = field(default_factory=list)

    main_connections: List[Connection] = field(default_factory=list)

    side_connections: List[Connection] = field(default_factory=list)

    spouse_connections: List[Connection] = field(default_factory=list)

    connection_index: dict = field(default_factory=dict)

    connection_count: int = 0


#==========================================================
# Connection Engine
#==========================================================

class ConnectionEngine:

    #======================================================

    def __init__(self):

        self.layout: Optional[LayoutResult] = None

        self.result = ConnectionResult()

    #======================================================

    def build(self, layout: LayoutResult):

        self.layout = layout

        self.result = ConnectionResult()

        self._build_main_connections()

        self._build_side_connections()

        self._build_spouse_connections()

        self._finalize()

        return self.result

    #======================================================
    # Part 2
    #======================================================

    def _build_main_connections(self):
        pass

    #======================================================
    # Part 3
    #======================================================

    def _build_side_connections(self):
        pass

    #======================================================
    # Part 4
    #======================================================

    def _build_spouse_connections(self):
        pass

    #======================================================
    # Part 5
    #======================================================

    def _finalize(self):
        pass
#==========================================================
# LayoutEngine 3.0
# Government Family Relationship Layout
# Part 1
#==========================================================

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


#==========================================================
# Group Role
#==========================================================

class GroupRole(Enum):

    MAIN = "main"

    SIDE = "side"


#==========================================================
# Member
#==========================================================

@dataclass(slots=True)
class LayoutMember:

    id: str

    title: str

    name: str

    generation: int = 0

    width: int = 120

    height: int = 60

    x: float = 0

    y: float = 0


#==========================================================
# Group
#==========================================================

@dataclass(slots=True)
class LayoutGroup:

    id: str

    title: str

    role: GroupRole

    generation: int = 0

    members: List[LayoutMember] = field(default_factory=list)

    parent: Optional["LayoutGroup"] = None

    child: Optional["LayoutGroup"] = None

    side_groups: List["LayoutGroup"] = field(default_factory=list)

    x: float = 0

    y: float = 0

    width: float = 120

    height: float = 60

    level: int = 0


#==========================================================
# Layout Result
#==========================================================

@dataclass(slots=True)
class LayoutResult:

    groups: List[LayoutGroup] = field(default_factory=list)

    main_groups: List[LayoutGroup] = field(default_factory=list)

    group_index: Dict[str, LayoutGroup] = field(default_factory=dict)

    member_index: Dict[str, LayoutMember] = field(default_factory=dict)

    root: Optional[LayoutGroup] = None

    width: int = 0

    height: int = 0

    left: float = 0

    top: float = 0

    right: float = 0

    bottom: float = 0

    group_count: int = 0

    member_count: int = 0

    main_group_count: int = 0

    side_group_count: int = 0

    version: str = "LayoutEngine 3.0"

#==========================================================
# LayoutEngine 3.0
# Part 2
# Layout Engine
#==========================================================

class LayoutEngine:

    #------------------------------------------------------
    # Node Size
    #------------------------------------------------------

    NODE_WIDTH = 120

    NODE_HEIGHT = 60

    MEMBER_GAP = 10

    #------------------------------------------------------
    # Layout
    #------------------------------------------------------

    START_X = 500

    START_Y = 60

    MAIN_GAP_Y = 180

    SIDE_GAP_X = 220

    CANVAS_PADDING = 50

    #------------------------------------------------------

    def __init__(self):

        self.relationships = []

        self.groups: List[LayoutGroup] = []

        self.main_groups: List[LayoutGroup] = []

        self.group_map: Dict[str, LayoutGroup] = {}

        self.result = LayoutResult()

    #------------------------------------------------------
    # Public
    #------------------------------------------------------

    def build(
        self,
        relationships
    ) -> LayoutResult:

        self.relationships = relationships

        self.groups.clear()

        self.main_groups.clear()

        self.group_map.clear()

        self.result = LayoutResult()

        self._build_group_tree()

        self._layout_groups()

        self._layout_members()

        self._build_result()

        self._finalize_layout()

        return self.result

    #------------------------------------------------------
    # Helper
    #------------------------------------------------------

    def _new_group(

        self,

        group_id: str,

        title: str,

        role: GroupRole,

        generation: int,

    ) -> LayoutGroup:

        group = LayoutGroup(

            id=group_id,

            title=title,

            role=role,

            generation=generation,

        )

        self.groups.append(group)

        self.group_map[group_id] = group

        return group

    #------------------------------------------------------

    def _get_group(

        self,

        group_id: str,

    ) -> Optional[LayoutGroup]:

        return self.group_map.get(group_id)
    
#==========================================================
# LayoutEngine 3.0
# Part 2（Government Edition）
# Layout Engine
#==========================================================

class LayoutEngine:

    #------------------------------------------------------
    # Node Size
    #------------------------------------------------------

    NODE_WIDTH = 120
    NODE_HEIGHT = 60

    MEMBER_GAP = 10

    #------------------------------------------------------
    # Layout
    #------------------------------------------------------

    START_X = 500
    START_Y = 60

    MAIN_GAP_Y = 180
    SIDE_GAP_X = 220

    CANVAS_PADDING = 50

    #------------------------------------------------------

    def __init__(self):

        self.groups: List[LayoutGroup] = []

        self.main_groups: List[LayoutGroup] = []

        self.group_map: Dict[str, LayoutGroup] = {}

        self.result = LayoutResult()

    #======================================================
    # Public
    #======================================================

    def build(
        self,
        groups: List[LayoutGroup]
    ) -> LayoutResult:
        """
        groups 必須由 FamilyGroupBuilder 建立。

        LayoutEngine 不負責：
            - 判斷親屬
            - 建立夫妻
            - 建立父母
            - 建立主幹

        LayoutEngine 只負責：

            Group
                ↓

            X、Y

                ↓

            LayoutResult
        """

        self.groups = list(groups)

        self.main_groups = [

            group

            for group in self.groups

            if group.role == GroupRole.MAIN

        ]

        self.group_map = {

            group.id: group

            for group in self.groups

        }

        self.result = LayoutResult()

        self._layout_groups()

        self._layout_members()

        self._build_result()

        self._finalize_layout()

        return self.result

    #======================================================
    # Helper
    #======================================================

    def get_group(
        self,
        group_id: str
    ) -> Optional[LayoutGroup]:

        return self.group_map.get(group_id)

#==========================================================
# LayoutEngine 3.0
# Part 4
# Fixed Main Line Layout
#==========================================================

    #======================================================
    # Main Line
    #======================================================

    def _layout_main_line(self):

        """
        Government Fixed Main Line

        烈祖
          │
        太祖
          │
        高祖
          │
        曾祖
          │
        祖父母
          │
        父母
          │
        申請人
        """

        if not self.main_groups:
            return

        self.main_groups.sort(
            key=lambda group: group.generation
        )

        current_y = self.START_Y

        previous_group = None

        for group in self.main_groups:

            group.x = self.START_X

            group.y = current_y

            if previous_group is not None:

                previous_group.child = group

                group.parent = previous_group

            previous_group = group

            current_y += self.MAIN_GAP_Y


    #======================================================
    # Update Layout
    #======================================================

    def _layout_groups(self):

        """
        Government Layout

        1. 排主幹
        2. 排旁系
        """

        self._layout_main_line()

        self._layout_side_groups()

#==========================================================
# LayoutEngine 3.0
# Part 5
# Government Fixed Order
#==========================================================

    GOVERNMENT_ORDER = {

        "烈祖父母": 1,

        "太祖父母": 2,

        "高祖父母": 3,

        "曾祖父母": 4,

        "祖父母": 5,

        "父母": 6,

        "申請人": 7,

    }

    #------------------------------------------------------

    def _group_order(
        self,
        group: LayoutGroup
    ) -> int:

        return self.GOVERNMENT_ORDER.get(
            group.title,
            999
        )

    #------------------------------------------------------

    def _layout_main_line(self):

        """
        政府固定主幹

        烈祖父母

        太祖父母

        高祖父母

        曾祖父母

        祖父母

        父母

        申請人
        """

        ordered = sorted(

            self.main_groups,

            key=self._group_order

        )

        current_y = self.START_Y

        previous = None

        for group in ordered:

            group.x = self.START_X

            group.y = current_y

            if previous:

                previous.child = group

                group.parent = previous

            previous = group

            current_y += self.MAIN_GAP_Y

        self.main_groups = ordered

#==========================================================
# LayoutEngine 3.0
# Part 6
# Government Side Layout
#==========================================================

    SIDE_VERTICAL_GAP = 90

    #------------------------------------------------------

    def _layout_side_groups(self):

        """
        Government Side Layout

        主幹固定置中

                主幹

        左側 side_groups

        右側 side_groups

        左右完全依照輸入順序
        """

        for main_group in self.main_groups:

            left_index = 0
            right_index = 0

            for index, side_group in enumerate(main_group.side_groups):

                #------------------------------------------
                # 左側
                #------------------------------------------

                if index % 2 == 0:

                    side_group.x = (
                        main_group.x
                        - self.SIDE_GAP_X
                    )

                    side_group.y = (
                        main_group.y
                        + left_index * self.SIDE_VERTICAL_GAP
                    )

                    left_index += 1

                #------------------------------------------
                # 右側
                #------------------------------------------

                else:

                    side_group.x = (
                        main_group.x
                        + self.SIDE_GAP_X
                    )

                    side_group.y = (
                        main_group.y
                        + right_index * self.SIDE_VERTICAL_GAP
                    )

                    right_index += 1

#==========================================================
# LayoutEngine 3.0
# Part 7
# Layout Member
#==========================================================

    MEMBER_VERTICAL_GAP = 70

    #------------------------------------------------------

    def _layout_members(self):

        """
        每個 Group 內的人員排列。

        規則：

        夫妻：
            上下排列

        單人：
            置中

        LayoutEngine 不判斷親屬，
        只依 members 的順序排版。
        """

        for group in self.groups:

            if not group.members:
                continue

            member_x = group.x

            member_y = group.y

            for member in group.members:

                member.width = self.NODE_WIDTH

                member.height = self.NODE_HEIGHT

                member.x = member_x

                member.y = member_y

                member_y += (
                    self.NODE_HEIGHT
                    + self.MEMBER_GAP
                )

            group.width = self.NODE_WIDTH

            group.height = max(
                self.NODE_HEIGHT,
                len(group.members)
                * self.NODE_HEIGHT
                + (len(group.members) - 1)
                * self.MEMBER_GAP
            )
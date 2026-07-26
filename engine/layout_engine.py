#==========================================================
# LayoutEngine 2.0
# Part 1（正式版）
# Data Model
#==========================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


#==========================================================
# Group Role
#==========================================================

class GroupRole(Enum):
    MAIN = "main"          # 主幹（祖先、父母、申請人）
    SIDE = "side"          # 旁系（伯叔、兄弟姐妹、堂兄弟姐妹）


#==========================================================
# Member
# 一個人
#==========================================================

@dataclass
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
# 一個家庭單位
#
# 例如：
#
# 父母 Group
#     父
#     母
#
# 伯父母 Group
#     伯父
#     伯母
#
# 申請人 Group
#     本人
#     配偶
#==========================================================

@dataclass
class LayoutGroup:

    id: str

    title: str

    role: GroupRole

    generation: int = 0

    members: List[LayoutMember] = field(default_factory=list)

    # ---------- Main Tree ----------
    parent: Optional["LayoutGroup"] = None
    child: Optional["LayoutGroup"] = None

    # ---------- Side Tree ----------
    side_groups: List["LayoutGroup"] = field(default_factory=list)

    # ---------- Layout ----------
    x: float = 0
    y: float = 0

    width: float = 0
    height: float = 0

    level: int = 0

    #======================================================

    def add_member(self, member: LayoutMember):

        self.members.append(member)

    #======================================================

    def add_side_group(self, group: "LayoutGroup"):

        group.parent = self

        self.side_groups.append(group)

    #======================================================

    def set_child(self, group: "LayoutGroup"):

        self.child = group

        group.parent = self


#==========================================================
# Layout Result
#==========================================================

@dataclass
class LayoutResult:

    groups: List[LayoutGroup] = field(default_factory=list)

    main_groups: List[LayoutGroup] = field(default_factory=list)

    group_index: dict = field(default_factory=dict)

    member_index: dict = field(default_factory=dict)

    width: int = 0
    height: int = 0

    left: float = 0
    top: float = 0
    right: float = 0
    bottom: float = 0

    root: Optional[LayoutGroup] = None

    version: str = ""

    group_count: int = 0
    member_count: int = 0
    main_group_count: int = 0
    side_group_count: int = 0


#==========================================================
# Layout Engine
#==========================================================

class LayoutEngine:

    NODE_WIDTH = 120
    NODE_HEIGHT = 60

    MEMBER_GAP = 18

    GROUP_GAP_Y = 120

    SIDE_GAP_X = 220

    START_X = 1000

    START_Y = 120

    #======================================================

    def __init__(self):

        self.groups: List[LayoutGroup] = []

        self.main_groups: List[LayoutGroup] = []

        self.result = LayoutResult()

    #======================================================

    def build(self, relationship_engine):

        self.groups.clear()

        self.main_groups.clear()

        self.result = LayoutResult()

        self._build_group_tree(relationship_engine)

        self._layout_groups()

        self._layout_members()

        self._build_result()

        return self.result

    #==========================================================
    # LayoutEngine 2.0
    # Part 2（正式版）
    # Build Group Tree
    #==========================================================

    def _build_group_tree(self, relationship_engine):

        #--------------------------------------------------
        # 建立所有 Group
        #--------------------------------------------------

        group_map = {}

        for person in relationship_engine.nodes.values():

            #--------------------------------------------------
            # 每個 Person 都應已經具有 group_id
            # RelationshipEngine 負責決定：
            #
            # 父母 -> 同一個 group_id
            # 伯父母 -> 同一個 group_id
            # 本人+配偶 -> 同一個 group_id
            # 兄弟 -> 各自 group_id
            # 堂兄弟 -> 各自 group_id
            #--------------------------------------------------

            group_id = person.group_id

            if group_id not in group_map:

                role = (
                    GroupRole.MAIN
                    if getattr(person, "is_main_line", False)
                    else GroupRole.SIDE
                )

                group = LayoutGroup(
                    id=group_id,
                    title=person.title,
                    role=role,
                    generation=person.generation,
                )

                group_map[group_id] = group

                self.groups.append(group)

            member = LayoutMember(
                id=person.id,
                title=person.title,
                name=person.name,
                generation=person.generation,
            )

            group_map[group_id].add_member(member)

        #--------------------------------------------------
        # 主幹排序
        #--------------------------------------------------

        self.main_groups = sorted(
            [
                g
                for g in self.groups
                if g.role == GroupRole.MAIN
            ],
            key=lambda g: g.generation
        )

        #--------------------------------------------------
        # 建立主幹
        #--------------------------------------------------

        for index in range(len(self.main_groups) - 1):

            current_group = self.main_groups[index]
            next_group = self.main_groups[index + 1]

            current_group.set_child(next_group)

        #--------------------------------------------------
        # 建立旁系
        #--------------------------------------------------

        for group in self.groups:

            if group.role != GroupRole.SIDE:
                continue

            first_member = group.members[0]

            parent_group_id = getattr(first_member, "parent_group_id", None)

            if parent_group_id is None:
                continue

            if parent_group_id not in group_map:
                continue

            group_map[parent_group_id].add_side_group(group)

        #--------------------------------------------------
        # SideGroup 排序
        #
        # 完全依照 RelationshipEngine 建立順序
        # 不依稱謂
        # 不依年齡
        #--------------------------------------------------

        for group in self.groups:

            if len(group.side_groups) <= 1:
                continue

            group.side_groups.sort(
                key=lambda g: getattr(
                    g.members[0],
                    "input_order",
                    0
                    )
                )

    #==========================================================
    # LayoutEngine 2.0
    # Part 3（正式版）
    # Layout Main Groups & Side Groups
    #==========================================================

    def _layout_groups(self):

        #--------------------------------------------------
        # 主幹排列
        #--------------------------------------------------

        current_y = self.START_Y

        for level, group in enumerate(self.main_groups):

            group.level = level

            group.x = self.START_X
            group.y = current_y

            current_y += self.GROUP_GAP_Y

        #--------------------------------------------------
        # Side Group 排列
        #
        # 規則：
        #
        # 左1 → 右1 → 左2 → 右2 → 左3 → 右3
        #
        # 完全依 input_order
        #--------------------------------------------------

        for parent in self.main_groups:

            if not parent.side_groups:
                continue

            left_index = 1
            right_index = 1

            for index, group in enumerate(parent.side_groups):

                #------------------------------
                # 奇數放左
                #------------------------------
                if index % 2 == 0:

                    group.x = (
                        parent.x
                        - self.SIDE_GAP_X * left_index
                    )

                    left_index += 1

                #------------------------------
                # 偶數放右
                #------------------------------
                else:

                    group.x = (
                        parent.x
                        + self.SIDE_GAP_X * right_index
                    )

                    right_index += 1

                group.y = parent.y

                group.level = parent.level

        #--------------------------------------------------
        # 計算 Group 大小
        #--------------------------------------------------

        for group in self.groups:

            member_count = len(group.members)

            if member_count == 0:

                group.width = self.NODE_WIDTH
                group.height = self.NODE_HEIGHT

                continue

            #------------------------------------------
            # 一對夫妻上下排列
            #------------------------------------------

            if member_count == 2:

                group.width = self.NODE_WIDTH

                group.height = (
                    self.NODE_HEIGHT * 2
                    + self.MEMBER_GAP
                )

            #------------------------------------------
            # 單人
            #------------------------------------------

            else:

                group.width = self.NODE_WIDTH

                group.height = self.NODE_HEIGHT

        #--------------------------------------------------
        # 更新 LayoutResult 尺寸
        #--------------------------------------------------

        if not self.groups:

            self.result.width = 0
            self.result.height = 0
            return

        max_right = max(
            g.x + g.width
            for g in self.groups
        )

        max_bottom = max(
            g.y + g.height
            for g in self.groups
        )

        min_left = min(
            g.x
            for g in self.groups
        )

        self.result.width = int(max_right - min_left + self.START_X)

        self.result.height = int(max_bottom + self.GROUP_GAP_Y)

    #==========================================================
    # LayoutEngine 2.0
    # Part 4（正式版）
    # Layout Members
    #==========================================================

    def _layout_members(self):

        for group in self.groups:

            member_count = len(group.members)

            if member_count == 0:
                continue

            #--------------------------------------------------
            # 單人 Group
            #
            # 兄弟
            # 姐妹
            # 堂兄弟
            # 堂姐妹
            #--------------------------------------------------

            if member_count == 1:

                member = group.members[0]

                member.x = group.x
                member.y = group.y

                continue

            #--------------------------------------------------
            # 夫妻 Group
            #
            # 男在上
            # 女在下
            #
            # 如果資料只有一人
            # 則仍維持目前位置
            #--------------------------------------------------

            if member_count == 2:

                husband = None
                wife = None

                for member in group.members:

                    title = member.title

                    #------------------------------------------
                    # 男性稱謂
                    #------------------------------------------

                    if title in {

                        "烈祖父",
                        "太祖父",
                        "天祖父",
                        "高祖父",
                        "曾祖父",
                        "祖父",
                        "父",
                        "伯父",
                        "叔父",
                        "姑丈",
                        "姨丈",
                        "舅父",
                        "兄弟",
                        "堂兄弟",
                        "申請人"

                    }:

                        husband = member

                    else:

                        wife = member

                #------------------------------------------
                # 若資料不足
                #------------------------------------------

                if husband is None:

                    husband = group.members[0]

                if wife is None:

                    wife = group.members[1]

                husband.x = group.x
                husband.y = group.y

                wife.x = group.x
                wife.y = (
                    group.y
                    + self.NODE_HEIGHT
                    + self.MEMBER_GAP
                )

                continue

            #--------------------------------------------------
            # 三人以上（預留）
            #--------------------------------------------------

            current_y = group.y

            for member in group.members:

                member.x = group.x
                member.y = current_y

                current_y += (
                    self.NODE_HEIGHT
                    + self.MEMBER_GAP
                )

            group.height = (
                member_count * self.NODE_HEIGHT
                + (member_count - 1) * self.MEMBER_GAP
            )

    #==========================================================
    # LayoutEngine 2.0
    # Part 5（正式版）
    # Build Layout Result
    #==========================================================

    def _build_result(self):

        #--------------------------------------------------
        # 清空結果
        #--------------------------------------------------

        self.result.groups.clear()

        #--------------------------------------------------
        # 收集所有 Group
        #--------------------------------------------------

        self.result.groups.extend(self.groups)

        #--------------------------------------------------
        # 計算整體範圍
        #--------------------------------------------------

        if not self.groups:

            self.result.width = 0
            self.result.height = 0
            return

        min_x = min(group.x for group in self.groups)
        min_y = min(group.y for group in self.groups)

        max_x = max(group.x + group.width for group in self.groups)
        max_y = max(group.y + group.height for group in self.groups)

        #--------------------------------------------------
        # 若座標有負值，全部平移
        #--------------------------------------------------

        offset_x = 0
        offset_y = 0

        if min_x < 0:
            offset_x = abs(min_x) + 50

        if min_y < 0:
            offset_y = abs(min_y) + 50

        if offset_x or offset_y:

            for group in self.groups:

                group.x += offset_x
                group.y += offset_y

                for member in group.members:

                    member.x += offset_x
                    member.y += offset_y

        #--------------------------------------------------
        # 重新計算畫布大小
        #--------------------------------------------------

        max_x = max(group.x + group.width for group in self.groups)
        max_y = max(group.y + group.height for group in self.groups)

        self.result.width = int(max_x + 50)
        self.result.height = int(max_y + 50)

        #--------------------------------------------------
        # 主幹排序（由上而下）
        #--------------------------------------------------

        self.main_groups.sort(
            key=lambda g: (
                g.generation,
                g.y
            )
        )

        #--------------------------------------------------
        # Side Group 排序（左→右）
        #--------------------------------------------------

        for group in self.main_groups:

            group.side_groups.sort(
                key=lambda g: g.x
            )

        #--------------------------------------------------
        # 所有 Group 排序
        # 方便 SvgRenderer 依序輸出
        #--------------------------------------------------

        self.result.groups.sort(
            key=lambda g: (
                g.level,
                g.x,
                g.y
            )
        )

        return self.result

    #==========================================================
    # LayoutEngine 2.0
    # Part 6（正式版）
    # Finalize Layout
    #==========================================================

    def _finalize_layout(self):

        #--------------------------------------------------
        # 建立索引
        #--------------------------------------------------

        self.result.group_index = {}
        self.result.member_index = {}

        for group in self.result.groups:

            self.result.group_index[group.id] = group

            for member in group.members:

                self.result.member_index[member.id] = member

        #--------------------------------------------------
        # Main Groups
        #--------------------------------------------------

        self.result.main_groups = list(self.main_groups)

        #--------------------------------------------------
        # Group 排序
        #
        # 依：
        #   1. 世代
        #   2. Y
        #   3. X
        #--------------------------------------------------

        self.result.groups.sort(
            key=lambda g: (
                g.generation,
                g.y,
                g.x
            )
        )

        #--------------------------------------------------
        # Main Group 檢查
        #--------------------------------------------------

        previous = None

        for group in self.main_groups:

            if previous is not None:

                if previous.child != group:

                    raise RuntimeError(
                        f"Main Line Broken : {previous.title}"
                    )

            previous = group

        #--------------------------------------------------
        # Side Group 排序
        #
        # 左 -> 右
        #--------------------------------------------------

        for group in self.main_groups:

            group.side_groups.sort(
                key=lambda g: g.x
            )

        #--------------------------------------------------
        # Bounding Box
        #--------------------------------------------------

        if self.result.groups:

            left = min(g.x for g in self.result.groups)
            top = min(g.y for g in self.result.groups)

            right = max(
                g.x + g.width
                for g in self.result.groups
            )

            bottom = max(
                g.y + g.height
                for g in self.result.groups
            )

            self.result.left = left
            self.result.top = top
            self.result.right = right
            self.result.bottom = bottom

        else:

            self.result.left = 0
            self.result.top = 0
            self.result.right = 0
            self.result.bottom = 0

        #--------------------------------------------------
        # Main Line Root
        #--------------------------------------------------

        self.result.root = (
            self.main_groups[0]
            if self.main_groups
            else None
        )

        #--------------------------------------------------
        # 統計
        #--------------------------------------------------

        self.result.group_count = len(self.result.groups)

        self.result.member_count = sum(
            len(g.members)
            for g in self.result.groups
        )

        self.result.main_group_count = len(
            self.main_groups
        )

        self.result.side_group_count = sum(
            len(g.side_groups)
            for g in self.main_groups
        )

        #--------------------------------------------------
        # Layout Version
        #--------------------------------------------------

        self.result.version = "LayoutEngine 2.0"

        #--------------------------------------------------
        # 完成
        #--------------------------------------------------

        return self.result
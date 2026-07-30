from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from models import Person
from layout_engine import LayoutResult
from connection_engine import ConnectionResult, Connection


@dataclass
class SvgRenderResult:
    svg: str = ""
    width: int = 0
    height: int = 0


class SvgRenderer:
    NODE_WIDTH = 120
    NODE_HEIGHT = 60
    COLUMN_GAP = 180
    ROW_GAP = 60
    PADDING_X = 60
    PADDING_Y = 60
    ELBOW_MARGIN = 24

    def __init__(self):
        self.layout_result: Optional[LayoutResult] = None
        self.connection_result: Optional[ConnectionResult] = None
        self.people: Dict[str, Person] = {}
        self.result = SvgRenderResult()
        self._elements: List[str] = []
        self._origin_x = 0
        self._origin_y = 0

    def render(self, people: Dict[str, Person], layout_result: LayoutResult,
               connection_result: ConnectionResult) -> SvgRenderResult:
        self.people = people
        self.layout_result = layout_result
        self.connection_result = connection_result
        self.result = SvgRenderResult()
        self._elements = []
        self._prepare_canvas()
        self._begin_svg()
        self._draw_connections()
        self._draw_nodes()
        self._end_svg()
        return self.result

    def _prepare_canvas(self) -> None:
        if self.layout_result is None or not self.layout_result.positions:
            return
        columns = [position.column for position in self.layout_result.positions.values()]
        rows = [position.row for position in self.layout_result.positions.values()]
        min_col, max_col = min(columns), max(columns)
        min_row, max_row = min(rows), max(rows)
        self._origin_x = self.PADDING_X - min_col * self.COLUMN_GAP
        self._origin_y = self.PADDING_Y - min_row * self.ROW_GAP
        self.result.width = (max_col - min_col + 1) * self.COLUMN_GAP + self.PADDING_X * 2
        self.result.height = (max_row - min_row + 1) * self.ROW_GAP + self.PADDING_Y * 2

    def _begin_svg(self) -> None:
        self._elements.extend([
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.result.width}" height="{self.result.height}" viewBox="0 0 {self.result.width} {self.result.height}">',
            '<style>text{font-family:"Microsoft JhengHei","PMingLiU",sans-serif;fill:#000}.person-box{fill:#fff;stroke:#000;stroke-width:.6}.person-box.inactive{fill:#eeeeee;stroke:#999}.person-box.applicant{fill:#fff3a3;stroke:#c78300;stroke-width:.9}.inactive-text{fill:#777}.connection-line,.connection-bar{stroke:#000;stroke-width:2;fill:none;stroke-linecap:square;stroke-linejoin:miter}.name-text{font-size:14px;text-anchor:middle;dominant-baseline:middle}.label-text{font-size:13px;text-anchor:middle;dominant-baseline:middle}.note-text{font-size:9px;text-anchor:middle;dominant-baseline:middle}</style>',
        ])

    def _end_svg(self) -> None:
        self._elements.append('</svg>')
        self.result.svg = '\n'.join(self._elements)

    def _draw_connections(self) -> None:
        if self.connection_result is None:
            return
        grouped_children = set()
        for group in self.connection_result.family_groups:
            grouped_children.update(group.children)
            path = self._family_group_path(group)
            if path:
                self._elements.append(path)
        # A malformed/incomplete family group can still use the old parent fallback.
        for connection in self.connection_result.parent_connections:
            if connection.target not in grouped_children:
                path = self._parent_path(connection)
                if path:
                    self._elements.append(path)

    def _person_center(self, person_id: str) -> Optional[Tuple[int, int]]:
        if self.layout_result is None or person_id not in self.layout_result.positions:
            return None
        position = self.layout_result.positions[person_id]
        return self._origin_x + position.column * self.COLUMN_GAP, self._origin_y + position.row * self.ROW_GAP

    def _person_box_top(self, person_id: str) -> Optional[Tuple[int, int]]:
        center = self._person_center(person_id)
        return None if center is None else (center[0], center[1] - self.NODE_HEIGHT // 2)

    def _person_box_bottom(self, person_id: str) -> Optional[Tuple[int, int]]:
        center = self._person_center(person_id)
        return None if center is None else (center[0], center[1] + self.NODE_HEIGHT // 2)

    def _parent_path(self, connection: Connection) -> str:
        source = self._person_box_bottom(connection.source)
        target = self._person_box_top(connection.target)
        if source is None or target is None:
            return ''
        sx, sy = self._line_start_after_spouse(connection.source, connection.target, source)
        tx, ty = target
        junction_y = min(ty - self.ELBOW_MARGIN, sy + self.ELBOW_MARGIN)
        return f'<path class="connection-line" d="M {sx} {sy} L {sx} {junction_y} L {tx} {junction_y} L {tx} {ty}" />'

    def _family_group_path(self, group) -> str:
        children = [child for child in group.children if self._person_box_top(child) is not None]
        # The person recorded as the mother is the spouse whose branch owns
        # these children.  Fall back to the father for one-parent data.
        anchor_id = group.mother if self._person_box_bottom(group.mother) is not None else group.father
        anchor = self._person_box_bottom(anchor_id) if anchor_id else None
        if anchor is None or not children:
            return ''
        targets = [self._person_box_top(child) for child in children]
        targets = [target for target in targets if target is not None]
        # A family is drawn once: parent -> one horizontal bar -> every child.
        ax, ay = self._line_start_after_spouse(anchor_id, children[0], anchor)
        junction_y = min(target[1] for target in targets) - self.ELBOW_MARGIN
        if junction_y <= ay:
            # A compact layout can leave less than one elbow margin between a
            # parent and child.  Keep the connection instead of dropping it.
            # The midpoint still produces a clean vertical / right-angle path.
            junction_y = (ay + min(target[1] for target in targets)) / 2
            if junction_y <= ay:
                return ''
        left_x = min(target[0] for target in targets)
        right_x = max(target[0] for target in targets)
        parts = [f'<path class="connection-bar" d="M {ax} {ay} L {ax} {junction_y}" />']
        if left_x != right_x:
            parts.append(f'<path class="connection-bar" d="M {left_x} {junction_y} L {right_x} {junction_y}" />')
        for child_x, child_top_y in targets:
            if child_x != ax or child_top_y != junction_y:
                parts.append(f'<path class="connection-bar" d="M {child_x} {junction_y} L {child_x} {child_top_y}" />')
        return ''.join(parts)

    def _line_start_after_spouse(self, source_id: str, target_id: str,
                                 source_bottom: Tuple[int, int]) -> Tuple[int, int]:
        """Do not draw a parent line through the spouse placed below it."""
        if self.layout_result is None:
            return source_bottom
        source_pos = self.layout_result.positions.get(source_id)
        target_pos = self.layout_result.positions.get(target_id)
        if source_pos is None or target_pos is None:
            return source_bottom
        x, y = source_bottom
        # Only the source person's own spouse may sit in the path.  Looking at
        # every spouse in the same column can incorrectly suppress a valid
        # parent-child line in a neighbouring family branch.
        spouse_ids = set(self.people.get(source_id, Person(id="", name="")).spouses)
        spouse_ids.update(
            person_id for person_id, person in self.people.items()
            if source_id in person.spouses
        )
        for spouse_id in spouse_ids:
            spouse_pos = self.layout_result.positions.get(spouse_id)
            if spouse_pos is None:
                continue
            if spouse_pos.column == source_pos.column and source_pos.row < spouse_pos.row < target_pos.row:
                spouse_bottom = self._person_box_bottom(spouse_id)
                if spouse_bottom is not None:
                    y = max(y, spouse_bottom[1])
        return x, y

    def _draw_nodes(self) -> None:
        if self.layout_result is None:
            return
        for person_id, position in self.layout_result.positions.items():
            person = self.people.get(person_id)
            if person is None:
                continue
            x = self._origin_x + position.column * self.COLUMN_GAP - self.NODE_WIDTH // 2
            y = self._origin_y + position.row * self.ROW_GAP - self.NODE_HEIGHT // 2
            self._elements.append(self._draw_person_box(x, y, person))

    def _draw_person_box(self, x: int, y: int, person: Person) -> str:
        name, label = self._escape(person.name), self._escape(person.label or '')
        note = self._escape(person.non_exhumation_note.strip()) if not person.is_exhumation else ''
        is_applicant = person.label.strip() == "申請人"
        state_class = " applicant" if is_applicant else ("" if person.is_exhumation else " inactive")
        text_class = "" if is_applicant or person.is_exhumation else " inactive-text"
        center_x = x + self.NODE_WIDTH / 2
        if note:
            return f'<g><rect class="person-box{state_class}" x="{x}" y="{y}" width="{self.NODE_WIDTH}" height="{self.NODE_HEIGHT}" rx="0" ry="0" /><text class="name-text{text_class}" x="{center_x}" y="{y + 18}">{name}</text><text class="label-text{text_class}" x="{center_x}" y="{y + 35}">{label}</text><text class="note-text{text_class}" x="{center_x}" y="{y + 51}">{note}</text></g>'
        return f'<g><rect class="person-box{state_class}" x="{x}" y="{y}" width="{self.NODE_WIDTH}" height="{self.NODE_HEIGHT}" rx="0" ry="0" /><text class="name-text{text_class}" x="{center_x}" y="{y + 24}">{name}</text><text class="label-text{text_class}" x="{center_x}" y="{y + 42}">{label}</text></g>'

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

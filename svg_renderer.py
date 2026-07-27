from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from models import Person, Position
from layout_engine import LayoutResult
from connection_engine import ConnectionResult, Connection


@dataclass
class SvgRenderResult:
    svg: str = ""
    width: int = 0
    height: int = 0


class SvgRenderer:
    """
    將 LayoutResult.positions 與 ConnectionResult.connections
    轉成 SVG。
    """

    NODE_WIDTH = 120
    NODE_HEIGHT = 60

    COLUMN_GAP = 180
    ROW_GAP = 90

    PADDING_X = 60
    PADDING_Y = 60

    def __init__(self):
        self.layout_result: Optional[LayoutResult] = None
        self.connection_result: Optional[ConnectionResult] = None
        self.people: Dict[str, Person] = {}
        self.result = SvgRenderResult()

        self._elements: List[str] = []
        self._origin_x: int = 0
        self._origin_y: int = 0

    def render(
        self,
        people: Dict[str, Person],
        layout_result: LayoutResult,
        connection_result: ConnectionResult,
    ) -> SvgRenderResult:
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

    # --------------------------------------------------
    # Canvas
    # --------------------------------------------------
    def _prepare_canvas(self) -> None:
        if self.layout_result is None or not self.layout_result.positions:
            self._origin_x = 0
            self._origin_y = 0
            self.result.width = 0
            self.result.height = 0
            return

        columns = [pos.column for pos in self.layout_result.positions.values()]
        rows = [pos.row for pos in self.layout_result.positions.values()]

        min_col = min(columns)
        max_col = max(columns)
        min_row = min(rows)
        max_row = max(rows)

        self._origin_x = self.PADDING_X - min_col * self.COLUMN_GAP
        self._origin_y = self.PADDING_Y - min_row * self.ROW_GAP

        self.result.width = int((max_col - min_col + 1) * self.COLUMN_GAP + self.PADDING_X * 2)
        self.result.height = int((max_row - min_row + 1) * self.ROW_GAP + self.PADDING_Y * 2)

    def _begin_svg(self) -> None:
        self._elements.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{self.result.width}" '
            f'height="{self.result.height}" '
            f'viewBox="0 0 {self.result.width} {self.result.height}">'
        )
        self._elements.append(self._style())

    def _end_svg(self) -> None:
        self._elements.append("</svg>")
        self.result.svg = "\n".join(self._elements)

    def _style(self) -> str:
        return """
<style>
text {
    font-family: "Microsoft JhengHei", "PMingLiU", sans-serif;
    fill: #000;
}

.person-box {
    fill: #fff;
    stroke: #000;
    stroke-width: 1.5;
}

.connection-line {
    stroke: #000;
    stroke-width: 2;
    fill: none;
    stroke-linecap: square;
    stroke-linejoin: miter;
}

.name-text {
    font-size: 14px;
    text-anchor: middle;
    dominant-baseline: middle;
}

.label-text {
    font-size: 13px;
    text-anchor: middle;
    dominant-baseline: middle;
}
</style>
""".strip()

    # --------------------------------------------------
    # Draw Connections
    # --------------------------------------------------
    def _draw_connections(self) -> None:
        if self.layout_result is None or self.connection_result is None:
            return

        for conn in self.connection_result.connections:
            points = self._connection_points(conn)
            if len(points) < 2:
                continue

            d = self._polyline_points(points)
            self._elements.append(
                f'<polyline class="connection-line" points="{d}" />'
            )

    def _connection_points(self, conn: Connection) -> List[tuple[int, int]]:
        if self.layout_result is None:
            return []

        src = self.layout_result.positions.get(conn.source)
        tgt = self.layout_result.positions.get(conn.target)

        if src is None or tgt is None:
            return []

        sx = self._origin_x + src.column * self.COLUMN_GAP
        sy = self._origin_y + src.row * self.ROW_GAP
        tx = self._origin_x + tgt.column * self.COLUMN_GAP
        ty = self._origin_y + tgt.row * self.ROW_GAP

        # 簡單做法：先以直線連接
        # 後續若要更像你的圖，可以再改成折線
        return [(sx, sy), (tx, ty)]

    def _polyline_points(self, points: List[tuple[int, int]]) -> str:
        return " ".join(f"{x},{y}" for x, y in points)

    # --------------------------------------------------
    # Draw Nodes
    # --------------------------------------------------
    def _draw_nodes(self) -> None:
        if self.layout_result is None:
            return

        for person_id, pos in self.layout_result.positions.items():
            person = self.people.get(person_id)
            if person is None:
                continue

            x = self._origin_x + pos.column * self.COLUMN_GAP - self.NODE_WIDTH // 2
            y = self._origin_y + pos.row * self.ROW_GAP - self.NODE_HEIGHT // 2

            self._elements.append(self._draw_person_box(x, y, person))

    def _draw_person_box(self, x: int, y: int, person: Person) -> str:
        name = self._escape(person.name)
        label = self._escape(person.label or "")

        name_y = y + 24
        label_y = y + 42

        return (
            f'<g>'
            f'<rect class="person-box" x="{x}" y="{y}" width="{self.NODE_WIDTH}" height="{self.NODE_HEIGHT}" rx="0" ry="0" />'
            f'<text class="name-text" x="{x + self.NODE_WIDTH / 2}" y="{name_y}">{name}</text>'
            f'<text class="label-text" x="{x + self.NODE_WIDTH / 2}" y="{label_y}">{label}</text>'
            f'</g>'
        )

    def _escape(self, text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )
#==========================================================
# SvgRenderer 1.0
# Part 1
# Government Family Tree
#==========================================================

from dataclasses import dataclass
from typing import List, Optional

from layout_engine import LayoutResult
from connection_engine import ConnectionResult


#==========================================================
# SVG Render Result
#==========================================================

@dataclass
class SvgRenderResult:

    svg: str = ""

    width: int = 0

    height: int = 0


#==========================================================
# Svg Renderer
#==========================================================

class SvgRenderer:

    def __init__(self):

        self.layout: Optional[LayoutResult] = None

        self.connections: Optional[ConnectionResult] = None

        self.result = SvgRenderResult()

        self.elements: List[str] = []

    #------------------------------------------------------
    # Build
    #------------------------------------------------------

    def build(
        self,
        layout: LayoutResult,
        connections: ConnectionResult
    ) -> SvgRenderResult:

        self.layout = layout

        self.connections = connections

        self.result = SvgRenderResult()

        self.elements = []

        self._begin_svg()

        self._draw_groups()

        self._draw_connections()

        self._draw_text()

        self._end_svg()

        return self.result

#------------------------------------------------------
# SVG Start
#------------------------------------------------------

    def _begin_svg(self):

        if self.layout is None:
            return

        self.result.width = self.layout.width
        self.result.height = self.layout.height

        self.elements.append(

            f'<svg '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'width="{self.result.width}" '
            f'height="{self.result.height}" '
            f'viewBox="0 0 {self.result.width} {self.result.height}">'

        )

        self._draw_style()

#------------------------------------------------------
# Draw Groups
#------------------------------------------------------

    def _draw_groups(self):

        if self.layout is None:
            return

        for group in self.layout.groups:

            svg = (
                f'<rect '
                f'x="{group.x}" '
                f'y="{group.y}" '
                f'width="{group.width}" '
                f'height="{group.height}" '
                f'fill="white" '
                f'stroke="black" '
                f'stroke-width="1"/>'
            )

            self.elements.append(svg)

#------------------------------------------------------
# Draw Connections
#------------------------------------------------------

    def _draw_connections(self):

        if self.connections is None:
            return

        for connection in self.connections.connections:

            if len(connection.points) < 2:
                continue

            #----------------------------------------------
            # 建立 SVG Polyline 座標
            #----------------------------------------------

            point_text = " ".join(

                f"{point.x},{point.y}"

                for point in connection.points

            )

            svg = (

                f'<polyline '

                f'points="{point_text}" '

                f'fill="none" '

                f'stroke="{connection.stroke}" '

                f'stroke-width="{connection.stroke_width}" '

                f'stroke-linecap="square" '

                f'stroke-linejoin="miter" '

                f'class="{connection.css_class}"'

            )

            if connection.dashed:

                svg += ' stroke-dasharray="5,5"'

            svg += '/>'

            self.elements.append(svg)

#------------------------------------------------------
# Draw Text
#------------------------------------------------------

    def _draw_text(self):

        if self.layout is None:
            return

        FONT_SIZE = 14

        for group in self.layout.groups:

            for member in group.members:

                #------------------------------------------
                # 個人外框
                #------------------------------------------

                self.elements.append(

                    f'<rect '
                    f'x="{member.x}" '
                    f'y="{member.y}" '
                    f'width="{member.width}" '
                    f'height="{member.height}" '
                    f'fill="white" '
                    f'stroke="black" '
                    f'stroke-width="1"/>'

                )

                #------------------------------------------
                # 稱謂
                #------------------------------------------

                title_y = (
                    member.y
                    + member.height / 2
                    - 8
                )

                self.elements.append(

                    f'<text '
                    f'x="{member.x + member.width / 2}" '
                    f'y="{title_y}" '
                    f'font-size="{FONT_SIZE}" '
                    f'text-anchor="middle" '
                    f'dominant-baseline="middle">'
                    f'{member.title}'
                    f'</text>'

                )

                #------------------------------------------
                # 姓名
                #------------------------------------------

                if member.name:

                    name_y = (
                        member.y
                        + member.height / 2
                        + 12
                    )

                    self.elements.append(

                        f'<text '
                        f'x="{member.x + member.width / 2}" '
                        f'y="{name_y}" '
                        f'font-size="{FONT_SIZE}" '
                        f'text-anchor="middle" '
                        f'dominant-baseline="middle">'
                        f'{member.name}'
                        f'</text>'

                    )
#------------------------------------------------------
# SVG Style
#------------------------------------------------------

    def _draw_style(self):

        self.elements.append("""

<style>

text{

    font-family:
        "Microsoft JhengHei",
        "PMingLiU",
        sans-serif;

    fill:#000;

    user-select:none;

}

.title{

    font-size:14px;

    font-weight:bold;

}

.name{

    font-size:13px;

}

.main-line,
.branch-line,
.side-line{

    fill:none;

    stroke:#000;

    stroke-linecap:square;

    stroke-linejoin:miter;

}

</style>

""")

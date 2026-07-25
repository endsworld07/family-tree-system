class SvgRenderer:
    """
    將 FamilyGroup 轉成 SVG
    """

    NODE_WIDTH = 120
    NODE_HEIGHT = 60

    def render(self, nodes, family_groups):

        lines = []

        for group in family_groups:
            lines.extend(self.draw_family(group))

        return "\n".join(lines)

    def draw_family(self, group):

        lines = []

        # ===========================
        # 母親 → 申請人
        # ===========================

        if group.main_spouse and group.next_person:

            x = self.center(group.main_spouse)[0]

            lines.append(
                self.vertical(
                    x,
                    self.bottom_center(group.main_spouse)[1],
                    self.top_center(group.next_person)[1],
                )
            )

        # ===========================
        # 配偶 → 第一位子女
        # （注意：不是申請人→配偶）
        # ===========================

        if group.other_spouses and group.children:

            spouse = group.other_spouses[0]
            first_child = group.children[0]

            x = self.center(spouse)[0]

            lines.append(
                self.vertical(
                    x,
                    self.bottom_center(spouse)[1],
                    self.top_center(first_child)[1],
                )
            )

        return lines

    def horizontal(self, x1, x2, y):
        return self.line(x1, y, x2, y)

    def vertical(self, x, y1, y2):
        return self.line(x, y1, x, y2)

    def line(self, x1, y1, x2, y2):

        return (
            f'<line '
            f'x1="{x1}" '
            f'y1="{y1}" '
            f'x2="{x2}" '
            f'y2="{y2}" '
            f'stroke="black" '
            f'stroke-width="2" />'
        )

    def center(self, node):
        return (
            node.x + self.NODE_WIDTH // 2,
            node.y + self.NODE_HEIGHT // 2,
        )

    def top_center(self, node):
        return (
            node.x + self.NODE_WIDTH // 2,
            node.y,
        )

    def bottom_center(self, node):
        return (
            node.x + self.NODE_WIDTH // 2,
            node.y + self.NODE_HEIGHT,
        )

    def left_center(self, node):
        return (
            node.x,
            node.y + self.NODE_HEIGHT // 2,
        )

    def right_center(self, node):
        return (
            node.x + self.NODE_WIDTH,
            node.y + self.NODE_HEIGHT // 2,
        )
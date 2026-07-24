from engine.layout_config import POSITIONS
from models.layout_node import LayoutNode


class LayoutEngine:

    CHILD_SPACING = 120

    def layout(self, relationships):

        nodes = []

        child_index = 0

        for relationship in relationships:

            x, y = POSITIONS.get(
                relationship.title,
                (0, 0),
            )

            if relationship.title == "CHILD":
                x = x + child_index * self.CHILD_SPACING
                child_index += 1

            node = LayoutNode(
                relationship=relationship,
                x=x,
                y=y,
            )

            nodes.append(node)

        return nodes
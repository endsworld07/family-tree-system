from __future__ import annotations

from dataclasses import dataclass

from models.layout_node import LayoutNode


@dataclass(slots=True)
class Connection:
    """
    親屬關係連線
    """

    from_node: LayoutNode
    to_node: LayoutNode
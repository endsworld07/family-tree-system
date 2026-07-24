from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Marriage:
    """
    婚姻關係
    """

    husband: str
    wife: str

    note: str | None = None
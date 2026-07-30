from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from models import Person, Position


@dataclass
class LayoutItem:
    person_id: str
    column: int
    row: int
    x: int = 0
    y: int = 0


@dataclass
class LayoutResult:
    positions: Dict[str, Position] = field(default_factory=dict)
    items: Dict[str, LayoutItem] = field(default_factory=dict)
    columns: Dict[int, List[str]] = field(default_factory=dict)
    rows: Dict[int, List[str]] = field(default_factory=dict)
    main_line: List[str] = field(default_factory=list)
    family_groups: List[dict] = field(default_factory=list)
    spouse_lookup: set[str] = field(default_factory=set)
    family_centers: Dict[Tuple[Optional[str], Optional[str]], int] = field(default_factory=dict)


class LayoutEngine:
    NODE_WIDTH = 120
    NODE_HEIGHT = 60
    COLUMN_GAP = 180
    ROW_GAP = 60
    NODE_MARGIN = 15

    def __init__(self, people: Dict[str, Person], relationships: dict, applicant_id: str):
        self.people = people
        self.relationships = relationships
        self.applicant_id = applicant_id
        self.result = LayoutResult()
        self._parents: Dict[str, Tuple[Optional[str], Optional[str]]] = relationships.get("parents", {})
        self._spouses: Dict[str, List[str]] = relationships.get("spouses", {})
        self._family_groups_raw: List[dict] = relationships.get("family_groups", [])
        self._family_groups: Dict[Tuple[Optional[str], Optional[str]], List[str]] = {}
        for group in self._family_groups_raw:
            key = (group.get("father"), group.get("mother"))
            if key == (None, None):
                continue
            children = self._family_groups.setdefault(key, [])
            for child_id in group.get("children", []):
                if child_id not in children:
                    children.append(child_id)
        self._placed: set[str] = set()
        self._occupied: set[Tuple[int, int]] = set()
        self._spouse_lookup: set[str] = set()
        self._main_line: List[str] = []
        self._family_centers: Dict[Tuple[Optional[str], Optional[str]], int] = {}

    def build(self) -> LayoutResult:
        self.result = LayoutResult()
        self._placed.clear()
        self._occupied.clear()
        self._spouse_lookup.clear()
        self._main_line = []
        self._family_centers = {}
        if self.applicant_id not in self.people:
            return self.result

        self._build_main_chain()
        self._build_sibling_rows()
        self._build_spouses()
        self._build_descendant_rows()
        # Descendants may themselves have spouses, so expand them after they
        # have received a position as well.
        self._build_spouses()
        self._finalize_positions()
        self.result.main_line = list(self._main_line)
        self.result.family_groups = list(self._family_groups_raw)
        self.result.spouse_lookup = set(self._spouse_lookup)
        self.result.family_centers = dict(self._family_centers)
        return self.result

    def _build_main_chain(self) -> None:
        """Place the paternal chain on a compact, single vertical axis."""
        chain: List[str] = []
        current = self.applicant_id
        visited = set()
        while current and current not in visited:
            visited.add(current)
            chain.append(current)
            father, _ = self._parents.get(current, (None, None))
            current = father
        chain.reverse()
        self._main_line = chain
        for index, person_id in enumerate(chain):
            # One row for the person, one for the spouse, then one blank row
            # before the next blood generation.
            self._place(person_id, 0, index * 3)

    def _build_sibling_rows(self) -> None:
        """Put every main-line person and their siblings on exactly one row."""
        for main_person_id in self._main_line:
            base = self.result.positions.get(main_person_id)
            if base is None:
                continue
            key = self._parents.get(main_person_id, (None, None))
            children = self._family_groups.get(key, [])
            siblings = [
                child_id for child_id in children
                if child_id != main_person_id and child_id in self.people and child_id not in self._placed
            ]
            left_count = len(siblings) // 2
            for index, sibling_id in enumerate(siblings[:left_count], start=1):
                self._place(sibling_id, base.column - (left_count - index + 1), base.row)
            for index, sibling_id in enumerate(siblings[left_count:], start=1):
                self._place(sibling_id, base.column + index, base.row)
            self._family_centers[key] = base.column

    def _build_descendant_rows(self) -> None:
        """Add children for the main branch and visible collateral branches."""
        for (father_id, mother_id), group_children in self._family_groups.items():
            father_pos = self.result.positions.get(father_id)
            mother_pos = self.result.positions.get(mother_id)
            if father_pos is None and mother_pos is None:
                continue

            # The mother shown in the child's record is the connection parent.
            anchor_pos = mother_pos or father_pos
            assert anchor_pos is not None
            parent_row = max(
                pos.row for pos in (father_pos, mother_pos) if pos is not None
            )
            child_row = parent_row + 2
            # A collateral parent can be placed before its child-bearing
            # spouse.  That spouse is added during the next spouse pass.  In
            # that case reserve the spouse row now, otherwise the later spouse
            # would be inserted directly between the parent and child and hide
            # their parent-child connection.
            missing_spouse_id = (
                mother_id if father_pos is not None and mother_pos is None else
                father_id if mother_pos is not None and father_pos is None else
                None
            )
            if missing_spouse_id in self.people:
                child_row += 1
            children = [
                child_id for child_id in group_children
                if child_id in self.people and child_id not in self._placed
            ]
            if not children:
                self._family_centers[(father_id, mother_id)] = anchor_pos.column
                continue

            offsets = self._centered_offsets(len(children))
            for child_id, offset in zip(children, offsets):
                self._place_child_outward(
                    child_id,
                    anchor_pos.column + offset,
                    child_row,
                    anchor_pos.column,
                )
            self._family_centers[(father_id, mother_id)] = anchor_pos.column

    @staticmethod
    def _centered_offsets(count: int) -> List[int]:
        if count % 2:
            return list(range(-(count // 2), count // 2 + 1))
        return list(range(-(count // 2), 0)) + list(range(1, count // 2 + 1))

    def _build_spouses(self) -> None:
        """Place the child-bearing spouse below; put additional spouses beside it."""
        # Use a queue because a spouse can be declared on either person's record.
        # This also makes a one-way value such as "王媽媽 -> 王老爸" sufficient.
        pending = list(self.result.positions)
        handled: set[str] = set()
        while pending:
            person_id = pending.pop(0)
            if person_id in handled:
                continue
            handled.add(person_id)
            base = self.result.positions.get(person_id)
            if base is None:
                continue
            spouse_ids = self._ordered_spouse_ids(person_id)
            spouse_row = base.row + 1
            spouse_columns = self._spouse_columns(base.column, len(spouse_ids))

            # Keep a collateral person and its spouse group together.  If the
            # group would collide with the central family's spouses, move the
            # collateral person outward before placing any of its spouses.
            while (
                spouse_ids
                and not self._spouse_slots_available(spouse_ids, spouse_columns, spouse_row)
                and self._move_person_outward(person_id)
            ):
                base = self.result.positions[person_id]
                spouse_row = base.row + 1
                spouse_columns = self._spouse_columns(base.column, len(spouse_ids))

            for spouse_id, spouse_column in zip(spouse_ids, spouse_columns):
                if spouse_id not in self.people or spouse_id in self._placed:
                    continue
                self._spouse_lookup.add(spouse_id)
                self._place_near(spouse_id, spouse_column, spouse_row, base.column)
                pending.append(spouse_id)

    @staticmethod
    def _spouse_columns(base_column: int, count: int) -> List[float]:
        if count == 1:
            return [base_column]
        if count == 2:
            # Keep a two-spouse family together while leaving one normal box
            # margin between the two spouse boxes.
            offset = (LayoutEngine.NODE_WIDTH + LayoutEngine.NODE_MARGIN) / (2 * LayoutEngine.COLUMN_GAP)
            return [base_column - offset, base_column + offset]
        # Three or more spouses retain a centre seat and expand evenly.
        return [base_column + offset for offset in LayoutEngine._centered_offsets(count)]

    def _ordered_spouse_ids(self, person_id: str) -> List[str]:
        """Prioritise the spouse named as mother/father of this person's child."""
        spouse_ids = self._spouse_ids_for(person_id)
        primary_id: Optional[str] = None
        for _, (father_id, mother_id) in self._parents.items():
            if father_id == person_id and mother_id in spouse_ids:
                primary_id = mother_id
                break
            if mother_id == person_id and father_id in spouse_ids:
                primary_id = father_id
                break
        if primary_id is None:
            return spouse_ids
        return [primary_id] + [spouse_id for spouse_id in spouse_ids if spouse_id != primary_id]

    def _spouse_ids_for(self, person_id: str) -> List[str]:
        """Return both direct and reverse spouse declarations, preserving input order."""
        spouse_ids: List[str] = []
        for spouse_id in self._spouses.get(person_id, []):
            if spouse_id not in spouse_ids:
                spouse_ids.append(spouse_id)
        for other_id, other_spouses in self._spouses.items():
            if person_id in other_spouses and other_id not in spouse_ids:
                spouse_ids.append(other_id)
        return spouse_ids

    def _place_near(self, person_id: str, column: int, row: int, origin_column: int) -> None:
        if self._is_slot_available(column, row):
            self._place(person_id, column, row)
            return
        # For a collateral branch, collisions always move farther away from
        # the central trunk rather than back across it.
        direction = 1 if origin_column >= 0 else -1
        for distance in range(1, len(self.people) + 2):
            candidate_column = column + direction * distance
            if self._is_slot_available(candidate_column, row):
                self._place(person_id, candidate_column, row)
                return

    def _spouse_slots_available(
        self,
        spouse_ids: List[str],
        spouse_columns: List[float],
        row: int,
    ) -> bool:
        return all(
            spouse_id in self._placed or self._is_slot_available(column, row)
            for spouse_id, column in zip(spouse_ids, spouse_columns)
        )

    def _move_person_outward(self, person_id: str) -> bool:
        """Move a collateral person outward so its spouse remains directly below it."""
        position = self.result.positions.get(person_id)
        if position is None or position.column == 0:
            return False
        direction = 1 if position.column > 0 else -1
        for distance in range(1, len(self.people) + 2):
            candidate_column = position.column + direction * distance
            if not self._is_slot_available(candidate_column, position.row):
                continue
            self._occupied.remove((position.column, position.row))
            position.column = candidate_column
            self._occupied.add((candidate_column, position.row))
            return True
        return False

    def _place_child_outward(self, person_id: str, column: int, row: int, origin_column: int) -> None:
        self._place_near(person_id, column, row, origin_column)

    def _place(self, person_id: str, column: int, row: int) -> None:
        if person_id not in self.people or not self._is_slot_available(column, row):
            return
        self.result.positions[person_id] = Position(column=column, row=row)
        self._placed.add(person_id)
        self._occupied.add((column, row))

    def _is_slot_available(self, column: float, row: int) -> bool:
        """Avoid overlapping boxes even when their fractional columns differ."""
        required_gap = (self.NODE_WIDTH + self.NODE_MARGIN) / self.COLUMN_GAP
        for occupied_column, occupied_row in self._occupied:
            if occupied_row == row and abs(occupied_column - column) < required_gap - 1e-9:
                return False
        return True

    def _finalize_positions(self) -> None:
        for person_id, pos in self.result.positions.items():
            self.result.items[person_id] = LayoutItem(person_id, pos.column, pos.row, pos.column, pos.row)
            self.result.columns.setdefault(pos.column, []).append(person_id)
            self.result.rows.setdefault(pos.row, []).append(person_id)

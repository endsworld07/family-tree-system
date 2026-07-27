# layout_engine.py

from models import Position


class LayoutEngine:
    """
    Government Family Relationship System

    Layout Engine

    職責：
        依照 RelationshipEngine 建立排版模型。

    不負責：
        - 親屬推論
        - SVG
        - HTML
        - 座標換算
    """

    def __init__(self, people, relationships, applicant):

        self.people = people
        self.relationships = relationships
        self.applicant = applicant

        # 最終位置
        self.positions = {}

        # 主幹
        self.main_line = []

    # ----------------------------------------------------

    def build(self):

        self.positions.clear()
        self.main_line.clear()

        self._build_main_line()

        return self.positions

    # ----------------------------------------------------
    # 建立申請人直系主幹
    # ----------------------------------------------------

    def _build_main_line(self):

        current = self.applicant

        chain = []

        while current:

            person = self.people[current]

            chain.append(current)

            if not person.father:
                break

            current = person.father

        chain.reverse()

        row = 0

        for person_id in chain:

            person = self.people[person_id]

            self.main_line.append(person_id)

            self.positions[person_id] = Position(
                column=0,
                row=row,
            )

            row += 2

            if person.mother:

                self.positions[person.mother] = Position(
                    column=0,
                    row=row,
                )

                row += 2
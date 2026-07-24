from __future__ import annotations

from models.person import Person
from models.relationship import Relationship


class RelationshipResolver:
    """
    親屬關係解析器（V1）
    第一版只解析申請人
    """

    def __init__(
        self,
        people: list[Person],
        applicant: str,
    ) -> None:

        self.people = people
        self.applicant = applicant

        # 依姓名建立索引
        self.persons = {
            person.name: person
            for person in people
        }

    def resolve(self) -> list[Relationship]:
        """
        解析親屬關係
        """

        applicant = self._get_applicant()

        return [
            Relationship(
                person=applicant,
                title="SELF",
                generation=0,
                order=1,
            )
        ]

    def _get_applicant(self) -> Person:
        """
        取得申請人
        """

        person = self.persons.get(self.applicant)

        if person is None:
            raise ValueError(f"找不到申請人：{self.applicant}")

        return person
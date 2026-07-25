from __future__ import annotations

from models.person import Person


class PersonIndex:
    """
    Person Index

    提供 Person 快速查詢。

    職責：
    - 建立 id -> Person 索引
    - 依 id 取得 Person
    - 取得全部 Person

    不負責：
    - 親屬判斷
    - 稱謂解析
    - 家庭建立
    """

    def __init__(self, people: list[Person]) -> None:
        self._persons = {
            person.id: person
            for person in people
        }

    def get(self, person_id: str | None) -> Person | None:
        """
        依 ID 取得 Person
        """

        if not person_id:
            return None

        return self._persons.get(person_id)

    def all(self) -> list[Person]:
        """
        取得全部人物
        """

        return list(self._persons.values())

    def exists(self, person_id: str | None) -> bool:
        """
        判斷人物是否存在
        """

        if not person_id:
            return False

        return person_id in self._persons
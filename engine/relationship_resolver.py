from __future__ import annotations

from models.person import Person
from models.relationship import Relationship


class RelationshipResolver:
    """
    Government Family Tree
    Relationship Resolver

    職責：

    - 解析申請人
    - 解析父系祖先
    - 解析配偶
    - 解析子女
    - 解析伯叔
    - 解析堂兄弟姊妹

    不負責：

    - 排版(Layout)
    - 家族分群(FamilyGroup)
    - SVG
    """

    ANCESTOR_RELATIONS = [
        ("FATHER", "MOTHER"),
        ("GRANDFATHER", "GRANDMOTHER"),
        ("GREAT_GRANDFATHER", "GREAT_GRANDMOTHER"),
        ("HIGH_GRANDFATHER", "HIGH_GRANDMOTHER"),
        ("HEAVEN_GRANDFATHER", "HEAVEN_GRANDMOTHER"),
        ("TAI_GRANDFATHER", "TAI_GRANDMOTHER"),
        ("LIE_GRANDFATHER", "LIE_GRANDMOTHER"),
    ]

    def __init__(
        self,
        people: list[Person],
        applicant: str,
    ):

        self.people = people
        self.applicant = applicant

        self.person_map = {
            person.id: person
            for person in people
        }

        self.relationships: list[Relationship] = []

        # Person.id -> Relationship
        self.relationship_map: dict[str, Relationship] = {}

    # =====================================================
    # Public
    # =====================================================

    def resolve(self) -> list[Relationship]:

        self.relationships.clear()
        self.relationship_map.clear()

        applicant = self._get_applicant()

        # 申請人
        self._build_self(applicant)

        # 父系祖先
        self._build_ancestors(applicant)

        # 配偶
        self._build_spouses(applicant)

        # 子女
        self._build_children(applicant)

        # 伯叔
        self._build_uncles(applicant)

        # 堂兄弟姊妹
        self._build_cousins(applicant)

        self._sort_relationships()

        return self.relationships

    # =====================================================
    # Self
    # =====================================================

    def _build_self(
        self,
        applicant: Person,
    ) -> None:

        self._append_relationship(
            applicant,
            title="SELF",
            generation=0,
            order=0,
        )

    # =====================================================
    # Ancestors
    # =====================================================

    def _build_ancestors(
        self,
        applicant: Person,
    ) -> None:

        current = applicant

        generation = -1

        for father_title, mother_title in self.ANCESTOR_RELATIONS:

            father = self._find_person(current.father)

            mother = self._find_person(current.mother)

            if father:

                self._append_relationship(
                    father,
                    title=father_title,
                    generation=generation,
                    order=0,
                )

            if mother:

                self._append_relationship(
                    mother,
                    title=mother_title,
                    generation=generation,
                    order=1,
                )

            # 父系主幹繼續往上找
            if father is None:
                break

            current = father
            generation -= 1

    # =====================================================
    # Spouses
    # =====================================================

    def _build_spouses(
        self,
        applicant: Person,
    ) -> None:

        spouses = self._find_spouses(applicant.id)

        order = 0

        for spouse in spouses:

            self._append_relationship(
                spouse,
                title="SPOUSE",
                generation=0,
                order=order,
            )

            order += 1

    # =====================================================
    # Children
    # =====================================================

    def _build_children(
        self,
        applicant: Person,
    ) -> None:

        children = self._find_children(applicant.id)

        order = 0

        for child in children:

            self._append_relationship(
                child,
                title="CHILD",
                generation=1,
                order=order,
            )

            order += 1

    # =====================================================
    # Uncles
    # =====================================================

    def _build_uncles(
        self,
        applicant: Person,
    ) -> None:

        father = self._find_person(applicant.father)

        if father is None:
            return

        grandfather = self._find_person(father.father)

        if grandfather is None:
            return

        order = 0

        for person in self.people:

            if person.id == father.id:
                continue

            if person.father != grandfather.id:
                continue

            self._append_relationship(
                person,
                title="UNCLE",
                generation=-1,
                order=order,
            )

            spouse_order = 0

            for spouse in self._find_spouses(person.id):

                self._append_relationship(
                    spouse,
                    title="UNCLE_SPOUSE",
                    generation=-1,
                    order=100 + order + spouse_order,
                )

                spouse_order += 1

            order += 1

    # =====================================================
    # Cousins
    # =====================================================

    def _build_cousins(
        self,
        applicant: Person,
    ) -> None:

        father = self._find_person(applicant.father)

        if father is None:
            return

        grandfather = self._find_person(father.father)

        if grandfather is None:
            return

        order = 0

        for uncle in self.people:

            if uncle.id == father.id:
                continue

            if uncle.father != grandfather.id:
                continue

            children = self._find_children(uncle.id)

            for child in children:

                title = (
                    "COUSIN_BROTHER"
                    if child.gender == "男"
                    else "COUSIN_SISTER"
                )

                self._append_relationship(
                    child,
                    title=title,
                    generation=0,
                    order=order,
                )

                order += 1  

    # =====================================================
    # Helper
    # =====================================================

    def _append_relationship(
        self,
        person: Person,
        title: str,
        generation: int,
        order: int,
        source: str | None = None,
    ) -> None:

        if person.id in self.relationship_map:
            return

        relationship = Relationship(
            person=person,
            title=title,
            generation=generation,
            order=order,
            source=source,
        )

        self.relationship_map[person.id] = relationship
        self.relationships.append(relationship)

    # -----------------------------------------------------

    def _sort_relationships(self) -> None:

        self.relationships.sort(
            key=lambda relationship: (
                relationship.generation,
                relationship.order,
                relationship.person.name,
            )
        )

    # -----------------------------------------------------

    def _get_applicant(self) -> Person:

        person = self.person_map.get(self.applicant)

        if person is None:
            raise ValueError("找不到申請人")

        return person

    # -----------------------------------------------------

    def _find_person(
        self,
        person_id: str | None,
    ) -> Person | None:

        if not person_id:
            return None

        return self.person_map.get(person_id)

    # -----------------------------------------------------
    
    def _find_spouses(
        self,
        person_id: str,
    ) -> list[Person]:
        """
        取得指定人物的所有配偶。
        """

        person = self._find_person(person_id)

        if person is None:
            return []

        spouses: list[Person] = []

        for spouse_id in person.spouses:

            spouse = self._find_person(spouse_id)

            if spouse is not None:
                spouses.append(spouse)

        return spouses
    
    # -----------------------------------------------------

    def _find_children(
        self,
        parent_id: str,
    ) -> list[Person]:
        """
        取得指定人物的所有子女。
        """

        parent = self._find_person(parent_id)

        if parent is None:
            return []

        children: list[Person] = []

        for child_id in parent.children:

            child = self._find_person(child_id)

            if child is not None:
                children.append(child)

        children.sort(
            key=lambda person: person.birth_order
        )

        return children
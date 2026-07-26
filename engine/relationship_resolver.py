#==========================================================
# Part 1
# 檔名：RelationshipEngine.py
#==========================================================

from __future__ import annotations

from collections import defaultdict

from models.person import Person
from models.relationship import Relationship
from engine.kinship_title_resolver import KinshipTitleResolver


class RelationshipEngine:
    """
    親屬關係建立器

    功能：
        Person -> Relationship

    負責：

        1. 建立所有 Relationship
        2. 建立父母關係
        3. 建立配偶關係
        4. 建立子女關係
        5. 建立兄弟姐妹關係
        6. 建立世代(generation)
        7. 呼叫 KinshipTitleResolver 建立稱謂

    不負責：

        Layout
        SVG
        Connection
        FamilyGroup
    """

    def __init__(
        self,
        people: list[Person],
    ) -> None:

        # 原始人物資料
        self.people = people

        # 第一位固定為申請人
        self.applicant: Person | None = (
            people[0] if people else None
        )

        # id -> Person
        self.person_map: dict[str, Person] = {
            person.id: person
            for person in people
        }

        # id -> Relationship
        self.relationships: dict[str, Relationship] = {}

        # generation -> Relationship List
        self.generations: dict[int, list[Relationship]] = (
            defaultdict(list)
        )

    #======================================================
    # Public
    #======================================================

    def build(self) -> list[Relationship]:

        self._build_relationships()

        self._build_parents()

        self._build_spouses()

        self._build_children()

        self._build_siblings()

        self._build_generations()

        self._resolve_titles()

        return list(
            self.relationships.values()
        )

    #==========================================================
    # Part 2
    # Relationship Base
    #==========================================================

    def _build_relationships(self) -> None:
        """
        建立所有 Relationship
        """

        self.relationships.clear()

        for person in self.people:

            relationship = Relationship(
                person=person,
            )

            self.relationships[
                person.id
            ] = relationship

    #======================================================

    def _get(
        self,
        person_id: str | None,
    ) -> Relationship | None:
        """
        取得 Relationship
        """

        if person_id is None:
            return None

        return self.relationships.get(
            person_id
        )

    #======================================================

    def _get_applicant(
        self,
    ) -> Relationship | None:
        """
        取得申請人 Relationship
        """

        if self.applicant is None:
            return None

        return self._get(
            self.applicant.id
        )

    #==========================================================
    # Part 3
    # Parent Relationship
    #==========================================================

    def _build_parents(self) -> None:
        """
        建立父母關係
        """

        for relationship in self.relationships.values():

            person = relationship.person

            #------------------------------
            # Father
            #------------------------------

            relationship.father = self._get(
                person.father
            )

            #------------------------------
            # Mother
            #------------------------------

            relationship.mother = self._get(
                person.mother
            )

    #==========================================================
    # Part 4
    # Spouse Relationship
    #==========================================================

    def _build_spouses(self) -> None:
        """
        建立配偶關係

        規則：

            A <-> B

        配偶關係為雙向建立。
        """

        for relationship in self.relationships.values():

            person = relationship.person

            for spouse_id in person.spouses:

                spouse = self._get(
                    spouse_id
                )

                if spouse is None:
                    continue

                relationship.add_spouse(
                    spouse
                )

                spouse.add_spouse(
                    relationship
                )

    #==========================================================
    # Part 5
    # Children Relationship
    #==========================================================

    def _build_children(self) -> None:
        """
        建立父母與子女關係

        規則：

            1. 依 Person.children 建立子女
            2. 父親自動加入子女
            3. 母親自動加入子女
            4. 不重覆加入
        """

        for relationship in self.relationships.values():

            person = relationship.person

            #------------------------------
            # Person.children
            #------------------------------

            for child_id in person.children:

                child = self._get(
                    child_id
                )

                if child is None:
                    continue

                relationship.add_child(
                    child
                )

            #------------------------------
            # Father -> Child
            #------------------------------

            if relationship.father is not None:

                relationship.father.add_child(
                    relationship
                )

            #------------------------------
            # Mother -> Child
            #------------------------------

            if relationship.mother is not None:

                relationship.mother.add_child(
                    relationship
                )

#==========================================================
# Part 6
# Sibling Relationship
#==========================================================

    def _build_siblings(self) -> None:
        """
        建立兄弟姐妹關係

        規則：

            同父且同母 == 兄弟姐妹

        不推測：

            同父異母
            同母異父
        """

        relationships = list(
            self.relationships.values()
        )

        count = len(
            relationships
        )

        for i in range(count):

            left = relationships[i]

            left_person = left.person

            #------------------------------
            # 必須有完整父母資訊
            #------------------------------

            if (
                not left_person.father
                or
                not left_person.mother
            ):
                continue

            for j in range(i + 1, count):

                right = relationships[j]

                right_person = right.person

                if (
                    not right_person.father
                    or
                    not right_person.mother
                ):
                    continue

                #------------------------------
                # 同父同母
                #------------------------------

                if (
                    left_person.father == right_person.father
                    and
                    left_person.mother == right_person.mother
                ):

                    left.add_sibling(
                        right
                    )

                    right.add_sibling(
                        left
                    )

    #==========================================================
    # Part 7
    # Generation & Title
    #==========================================================

    def _build_generations(self) -> None:
        """
        建立世代(generation)

        generation 定義：

            申請人        = 0

            父母          = +1
            祖父母        = +2
            曾祖父母      = +3
            ...

            子女          = -1

        配偶：
            與本人相同 generation
        """

        self.generations.clear()

        applicant = self._get_applicant()

        if applicant is None:
            return

        visited: set[str] = set()

        self._assign_generation(
            relationship=applicant,
            generation=0,
            visited=visited,
        )

        for relationship in self.relationships.values():

            self.generations[
                relationship.generation
            ].append(
                relationship
            )

    #======================================================

    def _assign_generation(
        self,
        relationship: Relationship,
        generation: int,
        visited: set[str],
    ) -> None:
        """
        DFS 建立世代
        """

        person_id = relationship.person.id

        if person_id in visited:
            return

        visited.add(person_id)

        relationship.generation = generation

        #------------------------------
        # Father
        #------------------------------

        if relationship.father:

            self._assign_generation(
                relationship=relationship.father,
                generation=generation + 1,
                visited=visited,
            )

        #------------------------------
        # Mother
        #------------------------------

        if relationship.mother:

            self._assign_generation(
                relationship=relationship.mother,
                generation=generation + 1,
                visited=visited,
            )

        #------------------------------
        # Spouse
        #------------------------------

        for spouse in relationship.spouses:

            self._assign_generation(
                relationship=spouse,
                generation=generation,
                visited=visited,
            )

        #------------------------------
        # Children
        #------------------------------

        for child in relationship.children:

            self._assign_generation(
                relationship=child,
                generation=generation - 1,
                visited=visited,
            )

    #======================================================
    # Title
    #======================================================

    def _resolve_titles(self) -> None:
        """
        建立所有親屬稱謂
        """

        applicant = self._get_applicant()

        if applicant is None:
            return

        resolver = KinshipTitleResolver(
            relationships=self.relationships,
            applicant=applicant,
        )

        resolver.build()
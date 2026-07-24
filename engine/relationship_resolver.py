from models.relationship import Relationship


class RelationshipResolver:

    def __init__(self, people, marriages, applicant):
        self.people = people
        self.marriages = marriages
        self.applicant = applicant

        self.person_index = {
            person.name: person
            for person in people
        }

    def _get_applicant(self):
        if self.applicant not in self.person_index:
            raise ValueError(f"找不到申請人：{self.applicant}")

        return self.person_index[self.applicant]

    def _get_spouse(self, applicant):
        for marriage in self.marriages:

            if marriage.husband == applicant.name:
                return self.person_index.get(marriage.wife)

            if marriage.wife == applicant.name:
                return self.person_index.get(marriage.husband)

        return None

    def _get_children(self, applicant):
        children = []

        for person in self.people:
            if (
                person.father == applicant.name
                or person.mother == applicant.name
            ):
                children.append(person)

        return children    

    def _get_siblings(self, applicant):
        siblings = []

        for person in self.people:

            if person.name == applicant.name:
                continue
            # 沒有父母資料，不判斷兄弟姊妹
            if applicant.father is None or applicant.mother is None:
                continue
            if (
                person.father == applicant.father
                and person.mother == applicant.mother
            ):
                siblings.append(person)

        return siblings

    def resolve(self):
        applicant = self._get_applicant()

        result = []

        # 父親
        if applicant.father:
            father = self.person_index[applicant.father]
            result.append(
                Relationship(
                    person=father,
                    title="FATHER",
                    generation=-1,
                    order=1,
                )
            )

        # 母親
        if applicant.mother:
            mother = self.person_index[applicant.mother]
            result.append(
                Relationship(
                    person=mother,
                    title="MOTHER",
                    generation=-1,
                    order=2,
                )
            )

        # 申請人
        result.append(
            Relationship(
                person=applicant,
                title="SELF",
                generation=0,
                order=1,
                )
            )

        # 配偶
        spouse = self._get_spouse(applicant)

        if spouse:
            result.append(
                Relationship(
                person=spouse,
                title="SPOUSE",
                generation=0,
                order=2,
                )
            )

        # 子女
        children = self._get_children(applicant)

        for child in children:
            result.append(
                Relationship(
                person=child,
                title="CHILD",
                generation=1,
                order=1,
                )
            )

        # 兄弟姊妹
        siblings = self._get_siblings(applicant)

        for index, sibling in enumerate(siblings, start=1):
            result.append(
                Relationship(
                person=sibling,
                title="SIBLING",
                generation=0,
                order=index,
                )
            )



        return result    
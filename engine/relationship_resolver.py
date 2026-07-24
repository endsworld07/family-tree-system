from models.relationship import Relationship


class RelationshipResolver:

    def __init__(self, people, applicant):
        self.people = people
        self.applicant = applicant
        self.person_index = {
            person.name: person
            for person in people
        }

    def _get_applicant(self):
        if self.applicant not in self.person_index:
            raise ValueError(f"找不到申請人：{self.applicant}")

        return self.person_index[self.applicant]

    def resolve(self):
        applicant = self._get_applicant()

        result = []

        # 父親
        if applicant.father:
            father = self.person_index[applicant.father]
            result.append(
                Relationship(
                    person=father,
                    title="父親",
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
                    title="母親",
                    generation=-1,
                    order=2,
                )
            )

        # 本人
        result.append(
            Relationship(
                person=applicant,
                title="本人",
                generation=0,
                order=1,
            )
        )

        return result
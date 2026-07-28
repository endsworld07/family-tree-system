from collections import defaultdict


class RelationshipEngine:
    """建立人物關係"""

    def __init__(self, people: dict):
        self.people = people

    def _person_id_for(self, value):
        """Accept either the stored id or the name entered in the form."""
        if not value:
            return None
        if value in self.people:
            return value
        for person in self.people.values():
            if person.name == value:
                return person.id
        return None

    # ---------------------------------------------------------
    # 建立所有關係
    # ---------------------------------------------------------

    def build(self):

        relationships = {
            "parents": self._build_parents(),
            "children": self._build_children(),
            "siblings": self._build_siblings(),
            "spouses": self._build_spouses(),
            "family_groups": self._build_family_groups(),
        }

        return relationships

    # ---------------------------------------------------------
    # 父母
    # ---------------------------------------------------------

    def _build_parents(self):

        parents = {}

        for person in self.people.values():

            parents[person.id] = (
                self._person_id_for(person.father),
                self._person_id_for(person.mother),
            )

        return parents

    # ---------------------------------------------------------
    # 子女
    # ---------------------------------------------------------

    def _build_children(self):

        children = defaultdict(list)

        for person in self.people.values():

            father_id = self._person_id_for(person.father)
            mother_id = self._person_id_for(person.mother)
            if father_id:
                children[father_id].append(person.id)

            if mother_id:
                children[mother_id].append(person.id)

        return dict(children)

    # ---------------------------------------------------------
    # 配偶
    # ---------------------------------------------------------

    def _build_spouses(self):

        spouses = {person.id: [] for person in self.people.values()}

        def link(first_id, second_id):
            if not first_id or not second_id or first_id == second_id:
                return
            if second_id not in spouses[first_id]:
                spouses[first_id].append(second_id)
            if first_id not in spouses[second_id]:
                spouses[second_id].append(first_id)

        for person in self.people.values():
            for spouse in person.spouses:
                link(person.id, self._person_id_for(spouse))

        # A child's father and mother identify the same couple even when only
        # one side of the spouse field was filled in.
        for person in self.people.values():
            link(
                self._person_id_for(person.father),
                self._person_id_for(person.mother),
            )

        return spouses

    # ---------------------------------------------------------
    # 兄弟姐妹
    # ---------------------------------------------------------

    def _build_siblings(self):

        siblings = {}

        for person in self.people.values():

            group = []

            for other in self.people.values():

                if person.id == other.id:
                    continue

                if (
                    self._person_id_for(person.father) == self._person_id_for(other.father)
                    and self._person_id_for(person.mother) == self._person_id_for(other.mother)
                    and self._person_id_for(person.father)
                    and self._person_id_for(person.mother)
                ):
                    group.append(other.id)

            siblings[person.id] = group

        return siblings

    # ---------------------------------------------------------
    # Family Groups（LayoutEngine 使用）
    # ---------------------------------------------------------

    def _build_family_groups(self):

        groups = {}

        for person in self.people.values():

            key = (
                self._person_id_for(person.father),
                self._person_id_for(person.mother),
            )

            if key == (None, None):
                continue

            if key not in groups:

                groups[key] = {
                    "father": key[0],
                    "mother": key[1],
                    "children": [],
                }

            groups[key]["children"].append(person.id)

        return list(groups.values())

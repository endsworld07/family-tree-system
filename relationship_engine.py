# relationship_engine.py

from collections import defaultdict


class RelationshipEngine:
    """建立人物關係"""

    def __init__(self, people: dict):
        """
        people:
            {
                "P001": Person(...),
                "P002": Person(...),
                ...
            }
        """
        self.people = people

    def build(self):
        """建立所有人物關係"""

        relationships = {
            "parents": self._build_parents(),
            "children": self._build_children(),
            "siblings": self._build_siblings(),
            "spouses": self._build_spouses(),
        }

        return relationships

    # -------------------------
    # 父母
    # -------------------------

    def _build_parents(self):

        parents = {}

        for person in self.people.values():

            parents[person.id] = {
                "father": person.father,
                "mother": person.mother,
            }

        return parents

    # -------------------------
    # 子女
    # -------------------------

    def _build_children(self):

        children = defaultdict(list)

        for person in self.people.values():

            if person.father:
                children[person.father].append(person.id)

            if person.mother:
                children[person.mother].append(person.id)

        return dict(children)

    # -------------------------
    # 配偶
    # -------------------------

    def _build_spouses(self):

        spouses = {}

        for person in self.people.values():
            spouses[person.id] = list(person.spouses)

        return spouses

    # -------------------------
    # 兄弟姐妹
    # -------------------------

    def _build_siblings(self):

        siblings = {}

        for person in self.people.values():

            group = []

            for other in self.people.values():

                if person.id == other.id:
                    continue

                if (
                    person.father == other.father
                    and person.mother == other.mother
                    and person.father is not None
                    and person.mother is not None
                ):
                    group.append(other.id)

            siblings[person.id] = group

        return siblings
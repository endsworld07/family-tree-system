from engine.connection_engine import ConnectionEngine
from engine.layout_engine import LayoutEngine
from models.person import Person
from models.relationship import Relationship


def test_connection_engine():

    applicant = Person(
        id="P001",
        name="王小明",
        gender="男",
    )

    father = Person(
        id="P002",
        name="爸爸",
        gender="男",
    )

    mother = Person(
        id="P003",
        name="媽媽",
        gender="女",
    )

    spouse = Person(
        id="P004",
        name="王小美",
        gender="女",
    )

    child = Person(
        id="P005",
        name="王大寶",
        gender="男",
    )

    relationships = [
        Relationship(father, "FATHER", -1, 1),
        Relationship(mother, "MOTHER", -1, 2),
        Relationship(applicant, "SELF", 0, 1),
        Relationship(spouse, "SPOUSE", 0, 2),
        Relationship(child, "CHILD", 1, 1),
    ]

    nodes = LayoutEngine().layout(relationships)

    connections = ConnectionEngine().build(nodes)

    pairs = {
        (
            c.from_node.relationship.title,
            c.to_node.relationship.title,
        )
        for c in connections
    }

    assert ("FATHER", "SELF") in pairs
    assert ("MOTHER", "SELF") in pairs
    assert ("SELF", "SPOUSE") in pairs
    assert ("SELF", "CHILD") in pairs

    assert len(connections) == 4
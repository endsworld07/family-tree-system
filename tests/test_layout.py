from engine.layout_engine import LayoutEngine
from engine.relationship_resolver import RelationshipResolver
from models.person import Person
from models.marriage import Marriage


def test_layout():

    people = [
        Person(id="1", name="爸爸", gender="男"),
        Person(id="2", name="媽媽", gender="女"),

        Person(
            id="3",
            name="王小明",
            gender="男",
            father="爸爸",
            mother="媽媽",
        ),

        Person(
            id="4",
            name="王小美",
            gender="女",
        ),

        Person(
            id="5",
            name="王大寶",
            gender="男",
            father="王小明",
            mother="王小美",
        ),
    ]

    marriages = [
        Marriage(
            husband="王小明",
            wife="王小美",
        )
    ]

    resolver = RelationshipResolver(
        people=people,
        marriages=marriages,
        applicant="王小明",
    )

    relationships = resolver.resolve()

    engine = LayoutEngine()

    nodes = engine.layout(relationships)

    assert len(nodes) == len(relationships)

    titles = {}

    for node in nodes:
        titles[node.relationship.title] = (node.x, node.y)

    assert titles["SELF"] == (300, 300)
    assert titles["FATHER"] == (300, 100)
    assert titles["MOTHER"] == (500, 100)
    assert titles["SPOUSE"] == (500, 300)
    assert titles["CHILD"] == (300, 500)
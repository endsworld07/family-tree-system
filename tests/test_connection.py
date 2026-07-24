from engine.connection_engine import ConnectionEngine
from engine.relationship_resolver import RelationshipResolver
from models.marriage import Marriage
from models.person import Person
from engine.layout_engine import LayoutEngine


def test_connection():

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
        Person(id="4", name="王小美", gender="女"),
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

    layout = LayoutEngine()

    nodes = layout.layout(relationships)

    engine = ConnectionEngine()

    connections = engine.build(nodes)

    assert len(connections) == 4
    assert connections[0].from_node.relationship.title == "FATHER"
    assert connections[0].to_node.relationship.title == "SELF"
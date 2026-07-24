from engine.relationship_resolver import RelationshipResolver
from models.marriage import Marriage
from models.person import Person


def test_children():

    people = [
        Person(
            id="1",
            name="王小明",
            gender="男",
        ),
        Person(
            id="2",
            name="王小美",
            gender="女",
        ),
        Person(
            id="3",
            name="王大寶",
            gender="男",
            father="王小明",
            mother="王小美",
        ),
        Person(
            id="4",
            name="王小寶",
            gender="女",
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

    result = resolver.resolve()

    titles = [r.title for r in result]

    assert "SELF" in titles
    assert "SPOUSE" in titles
    assert titles.count("CHILD") == 2
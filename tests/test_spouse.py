from engine.relationship_resolver import RelationshipResolver
from models.marriage import Marriage
from models.person import Person


def test_spouse():

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

    assert len(result) == 2

    titles = {r.title for r in result}

    assert "SELF" in titles
    assert "SPOUSE" in titles
from engine.relationship_resolver import RelationshipResolver
from models.person import Person


def test_parents():

    people = [
        Person(
            id="1",
            name="王爸爸",
            gender="男",
        ),
        Person(
            id="2",
            name="王媽媽",
            gender="女",
        ),
        Person(
            id="3",
            name="王小明",
            gender="男",
            father="王爸爸",
            mother="王媽媽",
        ),
    ]

    resolver = RelationshipResolver(
        people=people,
        marriages=[],
        applicant="王小明",
    )

    result = resolver.resolve()

    assert len(result) == 3

    titles = {r.title for r in result}

    assert "FATHER" in titles
    assert "MOTHER" in titles
    assert "SELF" in titles
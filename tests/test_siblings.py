from engine.relationship_resolver import RelationshipResolver
from models.person import Person


def test_siblings():

    people = [
        Person(
            id="1",
            name="爸爸",
            gender="男",
        ),
        Person(
            id="2",
            name="媽媽",
            gender="女",
        ),
        Person(
            id="3",
            name="王小明",
            gender="男",
            father="爸爸",
            mother="媽媽",
        ),
        Person(
            id="4",
            name="王大哥",
            gender="男",
            father="爸爸",
            mother="媽媽",
        ),
        Person(
            id="5",
            name="王妹妹",
            gender="女",
            father="爸爸",
            mother="媽媽",
        ),
    ]

    resolver = RelationshipResolver(
        people=people,
        marriages=[],
        applicant="王小明",
    )

    result = resolver.resolve()

    titles = [r.title for r in result]

    assert titles.count("SIBLING") == 2
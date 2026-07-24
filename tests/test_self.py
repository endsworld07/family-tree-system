from engine.relationship_resolver import RelationshipResolver
from models.person import Person


def test_self():

    people = [
        Person(
            id="1",
            name="王小明",
            gender="男",
        )
    ]

    resolver = RelationshipResolver(
        people=people,
        applicant="王小明",
    )

    result = resolver.resolve()

    assert len(result) == 1

    relation = result[0]

    assert relation.person.name == "王小明"
    assert relation.title == "本人"
    assert relation.generation == 0
    assert relation.order == 1
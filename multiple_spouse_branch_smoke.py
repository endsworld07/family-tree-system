import sys
sys.path.insert(0, "/Users/liuyuepeng/Downloads")

from models import Person
from relationship_engine import RelationshipEngine
from layout_engine import LayoutEngine
from connection_engine import ConnectionEngine
from svg_renderer import SvgRenderer

people = {
    "gp": Person("gp", "祖父"),
    "gm": Person("gm", "祖母"),
    "f": Person("f", "父親", father="gp", mother="gm"),
    "uncle": Person("uncle", "伯父", father="gp", mother="gm", spouses=["first", "mother"]),
    "first": Person("first", "大媽"),
    "mother": Person("mother", "伯母"),
    "applicant": Person("applicant", "申請人", father="f", mother="fm"),
    "fm": Person("fm", "母親"),
    "cousin": Person("cousin", "堂弟", father="uncle", mother="mother"),
}
relations = RelationshipEngine(people).build()
layout = LayoutEngine(people, relations, "applicant").build()
uncle = layout.positions["uncle"]
first = layout.positions["first"]
mother = layout.positions["mother"]
cousin = layout.positions["cousin"]
assert first.row == mother.row == uncle.row + 1
print("spouses", uncle, first, mother)
assert cousin.row == uncle.row + 3
assert cousin.column > uncle.column, "collateral descendant should extend outward"
svg = SvgRenderer().render(people, layout, ConnectionEngine(people, relations, layout).build()).svg
assert "伯母" in svg and "大媽" in svg and "堂弟" in svg
print({person_id: (pos.column, pos.row) for person_id, pos in layout.positions.items()})
print("multiple-spouse branch smoke test OK")

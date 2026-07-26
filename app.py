from flask import Flask, render_template

from engine.data_loader import DataLoader
from engine.relationship_resolver import RelationshipResolver
from engine.family_tree_builder import FamilyTreeBuilder
from engine.layout_engine import LayoutEngine
from engine.connection_engine import ConnectionEngine
# from engine.svg_renderer import SvgRenderer

app = Flask(__name__)


@app.route("/")
def index():

    # =========================
    # 載入資料
    # =========================

    loader = DataLoader()
    people, applicant = loader.load("data/family.json")

    # =========================
    # 親屬解析
    # =========================

    resolver = RelationshipResolver(
        people=people,
        applicant=applicant,
    )

    relationships = resolver.resolve()

    # =========================
    # 建立 FamilyTree
    # =========================

    builder = FamilyTreeBuilder(relationships)

    tree = builder.build()

    # =========================
    # Layout
    # =========================

    layout = LayoutEngine(tree)
    layout.layout()

    print("\n========== Layout ==========\n")

    for group in tree.groups.values():
        print(
            f"{group.head.title:20}"
            f"x={group.x:<6}"
            f"y={group.y:<6}"
        )

    print("\n========== FamilyTree ==========\n")

    for group in tree.groups.values():
        print(
            f"{group.head.title:20}"
            f"{group.head.person.name:10}"
            f" parent="
            f"{group.parent.head.title if group.parent else 'None'}"
        )

    print("\n========== Child Groups ==========\n")

    for group in tree.groups.values():
        print(
            group.head.title,
            "->",
            [child.head.title for child in group.child_groups]
        )

    # =========================
    # Connections（下一階段）
    # =========================

    connection_engine = ConnectionEngine(tree)
    connections = connection_engine.build()

    print("\n========== Connections ==========\n")

    for line in connections:

        print(
            line.kind,
            (line.x1, line.y1),
            "->",
            (line.x2, line.y2),
        )

    # =========================
    # SVG（下一階段）
    # =========================

    # renderer = SvgRenderer(layout)
    # svg = renderer.render()

    return render_template(
        "index.html",
        tree=tree,
        # svg=svg,
    )


if __name__ == "__main__":
    app.run(debug=True)
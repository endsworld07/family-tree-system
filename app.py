from flask import Flask, render_template

from engine.data_loader import DataLoader
from engine.relationship_resolver import RelationshipResolver
from engine.family_tree_builder import FamilyTreeBuilder
# from engine.layout_engine import LayoutEngine
# from engine.connection_engine import ConnectionEngine
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
    # Layout（下一階段）
    # =========================

    # layout = LayoutEngine(tree)
    # layout.layout()

    # =========================
    # Connections（下一階段）
    # =========================

    # connection_engine = ConnectionEngine(layout)

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
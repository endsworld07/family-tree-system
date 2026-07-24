from flask import Flask, render_template

from engine.data_loader import DataLoader
from engine.relationship_resolver import RelationshipResolver
from engine.layout_engine import LayoutEngine
from engine.connection_engine import ConnectionEngine

app = Flask(__name__)


@app.route("/")
def index():

    # 載入資料
    loader = DataLoader()
    people, marriages, applicant = loader.load("data/family.json")

    # 親屬解析
    resolver = RelationshipResolver(
        people=people,
        marriages=marriages,
        applicant=applicant,
    )

    relationships = resolver.resolve()

    # 版面配置
    layout = LayoutEngine()
    nodes = layout.layout(relationships)

    # 建立連線
    connection_engine = ConnectionEngine()
    connections = connection_engine.build(nodes)

    return render_template(
        "index.html",
        nodes=nodes,
        connections=connections,
    )


if __name__ == "__main__":
    app.run(debug=True)
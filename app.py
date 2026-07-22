from flask import Flask, render_template, request, redirect, url_for

from relationship import RELATIONS
from data import load_family, save_family

app = Flask(__name__)


@app.route("/")
def index():

    family = load_family()

    return render_template(
        "index.html",
        relations=RELATIONS,
        family=family
    )


@app.route("/save", methods=["POST"])
def save():

    family = load_family()

    for person in RELATIONS:

        title = person["title"]

        family[title] = request.form.get(
            title,
            ""
        ).strip()

    save_family(family)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
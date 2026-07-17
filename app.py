from flask import Flask, render_template, request, redirect

app = Flask(__name__)

family = []

titles = [
    "烈祖父","烈祖母",
    "烈伯父","烈伯母",

    "天祖父","天祖母",
    "天伯父","天伯母",

    "高祖父","高祖母",
    "高伯父","高伯母",

    "曾祖父","曾祖母",
    "曾伯父","曾伯母",

    "祖父","祖母",

    "父親","母親",

    "申請人"
]


@app.route("/")
def home():

    return render_template(
        "index.html",
        family=family,
        titles=titles
    )


@app.route("/add", methods=["POST"])
def add():

    name=request.form["name"]

    title=request.form["title"]

    family.append({
        "name":name,
        "title":title
    })

    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):

    if index < len(family):
        family.pop(index)

    return redirect("/")


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=7860,
        debug=True
    )
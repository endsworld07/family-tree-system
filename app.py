from flask import Flask, render_template, request, redirect, url_for
from relationship import RELATION_LAYOUT

app = Flask(__name__)
app.config["SECRET_KEY"] = "family-tree"

# =========================
# 資料
# =========================

applicant = ""

titles = list(RELATION_LAYOUT.keys())

# 每一個稱謂固定一個姓名
family = {title: "" for title in titles}


# =========================
# 首頁
# =========================

@app.route("/")
def index():

    return render_template(
        "index.html",
        applicant=applicant,
        family=family,
        layout=RELATION_LAYOUT,
    )


# =========================
# 儲存申請人
# =========================

@app.route("/save_applicant", methods=["POST"])
def save_applicant():

    global applicant

    applicant = request.form.get("applicant", "").strip()

    return redirect(url_for("index"))


# =========================
# 更新親屬姓名
# =========================

@app.route("/save_family", methods=["POST"])
def save_family():

    relation = request.form.get("relation", "")
    name = request.form.get("name", "").strip()

    if relation in family:
        family[relation] = name

    return redirect(url_for("index"))


# =========================
# 清空
# =========================

@app.route("/clear")
def clear():

    global applicant

    applicant = ""

    for key in family:
        family[key] = ""

    return redirect(url_for("index"))


# =========================

if __name__ == "__main__":
    app.run(debug=True)
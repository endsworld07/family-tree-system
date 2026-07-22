from flask import Flask, render_template, request, redirect, url_for

from relationship import RELATION_LAYOUT
from data import load_family, save_family

app = Flask(__name__)


@app.route("/")
def index():

    family = load_family()

    applicant = family.get("applicant", "")
    id_number = family.get("id_number", "")
    birthday = family.get("birthday", "")
    gender = family.get("gender", "")
    address = family.get("address", "")
    phone = family.get("phone", "")
    purpose = family.get("purpose", "")

    family_count = sum(
        1
        for title in RELATION_LAYOUT.keys()
        if family.get(title, "").strip()
    )

    return render_template(
        "index.html",
        layout=RELATION_LAYOUT,
        family=family,
        applicant=applicant,
        id_number=id_number,
        birthday=birthday,
        gender=gender,
        address=address,
        phone=phone,
        purpose=purpose,
        family_count=family_count,
    )


@app.route("/save", methods=["POST"])
def save():

    family = load_family()

    # -------------------------
    # 申請人資料
    # -------------------------

    family["applicant"] = request.form.get("applicant", "").strip()
    family["id_number"] = request.form.get("id_number", "").strip()
    family["birthday"] = request.form.get("birthday", "").strip()
    family["gender"] = request.form.get("gender", "").strip()
    family["address"] = request.form.get("address", "").strip()
    family["phone"] = request.form.get("phone", "").strip()
    family["purpose"] = request.form.get("purpose", "").strip()

    # -------------------------
    # 親屬資料
    # -------------------------

    for title in RELATION_LAYOUT.keys():
        family[title] = request.form.get(title, "").strip()

    save_family(family)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
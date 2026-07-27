from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from flask import Flask, redirect, render_template, request, url_for

from connection_engine import ConnectionEngine
from data_loader import DataLoader
from layout_engine import LayoutEngine
from models import Person
from relationship_engine import RelationshipEngine
from svg_renderer import SvgRenderer

app = Flask(__name__)

DATA_FILE = Path("family.json")


# ---------------------------------------------------------
# 讀取資料
# ---------------------------------------------------------

def load_people() -> tuple[Dict[str, Person], str]:
    if not DATA_FILE.exists():
        return {}, ""

    loader = DataLoader(str(DATA_FILE))
    data = loader.load()

    return data["people"], data["applicant"]


# ---------------------------------------------------------
# 儲存資料
# ---------------------------------------------------------

def save_people(
    people: Dict[str, Person],
    applicant_id: str,
) -> None:

    payload = {
        "applicant": applicant_id,
        "people": [],
    }

    for person in people.values():

        payload["people"].append(
            {
                "id": person.id,
                "name": person.name,
                "label": person.label,
                "father": person.father,
                "mother": person.mother,
                "spouses": list(person.spouses),
            }
        )

    DATA_FILE.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ---------------------------------------------------------
# 產生 SVG
# ---------------------------------------------------------

def build_svg(
    people: Dict[str, Person],
    applicant_id: str,
) -> str:

    if (
        not people
        or not applicant_id
        or applicant_id not in people
    ):
        return ""

    relationship_engine = RelationshipEngine(people)
    relationships = relationship_engine.build()

    layout_engine = LayoutEngine(
        people,
        relationships,
        applicant_id,
    )

    layout_result = layout_engine.build()

    connection_engine = ConnectionEngine(
        people,
        relationships,
        layout_result,
    )

    connection_result = connection_engine.build()

    renderer = SvgRenderer()

    svg_result = renderer.render(
        people,
        layout_result,
        connection_result,
    )

    return svg_result.svg


# ---------------------------------------------------------
# 下一個人物 ID
# ---------------------------------------------------------

def next_person_id(
    people: Dict[str, Person],
) -> str:

    max_number = 0

    for pid in people.keys():

        if pid.startswith("P") and pid[1:].isdigit():

            max_number = max(
                max_number,
                int(pid[1:]),
            )

    return f"P{max_number + 1:03d}"


# ---------------------------------------------------------
# 依姓名取得人物
# 找不到就建立
# ---------------------------------------------------------

def get_or_create_person(
    people: Dict[str, Person],
    name: str,
) -> str | None:

    name = name.strip()

    if not name:
        return None

    # 已存在
    for pid, person in people.items():

        if person.name == name:
            return pid

    # 建立新人物
    new_id = next_person_id(people)

    people[new_id] = Person(
        id=new_id,
        name=name,
        label="",
        father=None,
        mother=None,
        spouses=[],
    )

    return new_id


# ---------------------------------------------------------
# 首頁
# ---------------------------------------------------------

@app.get("/")
def index():

    people, applicant_id = load_people()

    svg = ""

    if applicant_id:
        svg = build_svg(
            people,
            applicant_id,
        )

    return render_template(
        "index.html",
        people=people,
        applicant_id=applicant_id,
        svg=svg,
    )



@app.post("/person/add")
def person_add():

    people, applicant_id = load_people()

    name = request.form.get("name", "").strip()
    label = request.form.get("label", "").strip()

    father_name = request.form.get("father", "").strip()
    mother_name = request.form.get("mother", "").strip()
    spouse_name = request.form.get("spouse", "").strip()

    if not name:
        return redirect(url_for("index"))

    # 已存在的人物直接返回
    for person in people.values():
        if person.name == name:
            return redirect(url_for("index"))

    # 建立或取得父母、配偶
    father_id = get_or_create_person(
        people,
        father_name,
    )

    mother_id = get_or_create_person(
        people,
        mother_name,
    )

    spouse_id = get_or_create_person(
        people,
        spouse_name,
    )

    person_id = next_person_id(people)

    people[person_id] = Person(
        id=person_id,
        name=name,
        label=label,
        father=father_id,
        mother=mother_id,
        spouses=[],
    )

    if spouse_id:
        people[person_id].spouses.append(spouse_id)

        if person_id not in people[spouse_id].spouses:
            people[spouse_id].spouses.append(person_id)

    if not applicant_id:
        applicant_id = person_id

    save_people(people, applicant_id)

    print(">>> person_edit()")

    return redirect(url_for("index"))

# ---------------------------------------------------------
# 編輯頁面
# ---------------------------------------------------------

@app.get("/person/edit/<person_id>")
def person_edit(person_id: str):

    people, applicant_id = load_people()

    if person_id not in people:
        return redirect(url_for("index"))

    svg = ""

    if applicant_id:
        svg = build_svg(
            people,
            applicant_id,
        )
    print(">>> person_edit()")
    return render_template(
        "index.html",
        people=people,
        applicant_id=applicant_id,
        svg=svg,
        editing=people[person_id],
    )


# ---------------------------------------------------------
# 更新人物
# ---------------------------------------------------------

@app.post("/person/update/<person_id>")
def person_update(person_id: str):

    people, applicant_id = load_people()

    if person_id not in people:
        return redirect(url_for("index"))

    person = people[person_id]

    name = request.form.get("name", "").strip()
    label = request.form.get("label", "").strip()

    father_name = request.form.get("father", "").strip()
    mother_name = request.form.get("mother", "").strip()
    spouse_name = request.form.get("spouse", "").strip()

    if name:
        person.name = name

    person.label = label

    father_id = get_or_create_person(
        people,
        father_name,
    )

    mother_id = get_or_create_person(
        people,
        mother_name,
    )

    spouse_id = get_or_create_person(
        people,
        spouse_name,
    )

    # 避免自己指向自己
    if father_id == person_id:
        father_id = None

    if mother_id == person_id:
        mother_id = None

    if spouse_id == person_id:
        spouse_id = None

    person.father = father_id
    person.mother = mother_id

    # 清除舊配偶的雙向關係
    for other in people.values():
        if person_id in other.spouses:
            other.spouses.remove(person_id)

    person.spouses = []

    # 建立新的雙向配偶
    if spouse_id:

        person.spouses.append(
            spouse_id
        )

        if person_id not in people[spouse_id].spouses:
            people[spouse_id].spouses.append(
                person_id
            )

    save_people(
        people,
        applicant_id,
    )

    return redirect(
        url_for("index")
    )

# ---------------------------------------------------------
# 刪除人物
# ---------------------------------------------------------

@app.post("/person/delete/<person_id>")
def person_delete(person_id: str):

    people, applicant_id = load_people()

    if person_id not in people:
        return redirect(url_for("index"))

    # 清除所有人物對此人物的關聯
    for other in people.values():

        if other.father == person_id:
            other.father = None

        if other.mother == person_id:
            other.mother = None

        if person_id in other.spouses:
            other.spouses.remove(person_id)

    # 刪除人物
    del people[person_id]

    # 若刪除的是申請人
    if applicant_id == person_id:

        if people:
            applicant_id = next(iter(people.keys()))
        else:
            applicant_id = ""

    save_people(
        people,
        applicant_id,
    )

    return redirect(
        url_for("index")
    )


# ---------------------------------------------------------
# 設定申請人
# ---------------------------------------------------------

@app.post("/set-applicant/<person_id>")
def set_applicant(person_id: str):

    people, applicant_id = load_people()

    if person_id not in people:
        return redirect(url_for("index"))

    applicant_id = person_id

    save_people(
        people,
        applicant_id,
    )

    return redirect(
        url_for("index")
    )


# ---------------------------------------------------------
# 重新產生 SVG
# ---------------------------------------------------------

@app.post("/generate")
def generate():

    people, applicant_id = load_people()

    svg = ""

    if applicant_id:
        svg = build_svg(
            people,
            applicant_id,
        )

    return render_template(
        "index.html",
        people=people,
        applicant_id=applicant_id,
        svg=svg,
    )


# ---------------------------------------------------------
# 主程式
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
    )
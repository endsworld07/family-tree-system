# data_loader.py

import json
from pathlib import Path

from models import Person


class DataLoader:
    """讀取 family.json 並建立 Person 物件"""

    def __init__(self, filename: str = "family.json"):
        self.filename = Path(filename)

    def load(self):
        """載入人物資料"""

        with self.filename.open("r", encoding="utf-8") as f:
            data = json.load(f)

        people = {}

        for item in data.get("people", []):

            person = Person(
                id=item["id"],
                name=item["name"],
                label=item.get("label", ""),
                father=item.get("father"),
                mother=item.get("mother"),
                spouses=item.get("spouses", []),
                is_matrilineal_main_line=item.get("is_matrilineal_main_line", False),
                is_arrival_ancestor=item.get("is_arrival_ancestor", False),
                is_exhumation=item.get("is_exhumation", False),
                non_exhumation_note=item.get("non_exhumation_note", ""),
            )

            people[person.id] = person

        return {
            "applicant": data["applicant"],
            "people": people,
        }

import json

from models.person import Person


class DataLoader:
    """載入 family.json，建立 Person 資料。"""

    def load(self, filename: str) -> tuple[list[Person], str]:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        people: list[Person] = []

        for item in data["people"]:
            people.append(
                Person(
                    id=item["id"],
                    name=item["name"],
                    gender=item["gender"],
                    father=item.get("father"),
                    mother=item.get("mother"),
                    spouses=item.get("spouses", []),
                    children=item.get("children", []),
                    custom_title=item.get("custom_title"),
                    note=item.get("note"),
                )
            )

        applicant = data["applicant"]

        return people, applicant
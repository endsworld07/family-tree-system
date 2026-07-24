import json

from models.person import Person
from models.marriage import Marriage


class DataLoader:

    def load(self, filename):

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        people = []

        for item in data["people"]:
            people.append(
                Person(
                    id=item["id"],
                    name=item["name"],
                    gender=item["gender"],
                    father=item.get("father"),
                    mother=item.get("mother"),
                    custom_title=item.get("custom_title"),
                    note=item.get("note"),
                )
            )

        marriages = []

        for item in data["marriages"]:
            marriages.append(
                Marriage(
                    husband=item["husband"],
                    wife=item["wife"],
                    note=item.get("note"),
                )
            )

        applicant = data["applicant"]

        return people, marriages, applicant
from engine.data_loader import DataLoader


def test_data_loader():

    loader = DataLoader()

    people, marriages, applicant = loader.load("data/family.json")

    assert applicant == "王小明"

    assert isinstance(people, list)
    assert isinstance(marriages, list)
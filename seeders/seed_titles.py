from app.models import Titles
from app import db


data = [
    {"name_en": "U", "name_my": "ဦး",},
    {"name_en": "Ko", "name_my": "ကို",},
    {"name_en": "Daw", "name_my": "ဒေါ်",},
    {"name_en": "Ma", "name_my": "မ"},
]


def seed(user=None):
    for each in data:
        each["created_by"] = user
        each["changed_by"] = user
        found = db.session.query(Titles).filter_by(name_en=each.get("name_en")).first()
        if not found:
            record = Titles(**each)
            db.session.add(record)
            db.session.commit()

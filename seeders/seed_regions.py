from app import db
from app.models import Regions


data = [{"name_en": "Mandalay Region", "name_my": "မန္တလေးတိုင်းဒေသကြီး"}]


def seed(user=None):
    for each in data:
        each["created_by"] = user
        each["changed_by"] = user
        found = db.session.query(Regions).filter_by(name_en=each.get("name_en")).first()
        if not found:
            record = Regions(**each)
            db.session.add(record)
            db.session.commit()

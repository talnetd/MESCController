from app import db
from app.models import OperatorType

data = [{"name": "Provider"}, {"name": "Retailer"}]


def seed(user=None):
    for each in data:
        each["created_by"] = user
        each["changed_by"] = user
        found = (
            db.session.query(OperatorType)
            .filter_by(name=each.get("name"))
            .first()
        )
        if not found:
            record = OperatorType(**each)
            db.session.add(record)
            db.session.commit()


if __name__ == "__main__":
    from .lib import get_user

    user = get_user()
    seed(user)

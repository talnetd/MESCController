from . import seed_regions
from . import seed_titles
from . import seed_townships
from app import db
from flask_appbuilder.security.sqla.models import User


def main():
    user = db.session.query(User).filter_by(username="seeder").first()
    if not user:
        user = User(
            username="seeder",
            email="seeder@localhost",
            first_name="Data",
            last_name="Seeder",
            active=True,
        )
        db.session.add(user)
        db.session.commit()
    seed_titles.seed(user)
    seed_regions.seed(user)
    seed_townships.seed(user)

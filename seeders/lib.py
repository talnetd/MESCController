from app import db
from flask_appbuilder.security.sqla.models import User


def get_user():
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

    db.session.expunge(user)
    return user

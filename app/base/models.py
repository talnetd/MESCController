# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import (
    Binary,
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
)
from app import db, login_manager

from app.base.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == "password":
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


# NOTE: disabled temporary. by lmk on 2020-08-12
# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get("username")
#     user = User.query.filter_by(username=username).first()
#     return user if user else None


class Meterboxes(db.Model):

    __tablename__ = "meterboxes"

    id = Column(Integer, primary_key=True)
    box_number = Column(String(512))


class Bills(db.Model):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    reading_date = Column(DateTime)
    due_date = Column(DateTime)
    meterbox_id = Column(Integer)
    previous_reading = Column(Integer)
    current_reading = Column(Integer)
    diff_reading = Column(Integer)
    sub_total = Column(Float)
    maintenance_fee = Column(Float)
    horsepower_fee = Column(Float)
    grand_total = Column(Float)
    remark = Column(Text)


class BillsDetails(db.Model):

    __tablename__ = "bills_detail"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer)
    line_item = Column(String(512))
    unit_price = Column(Float)
    quantity = Column(Integer)
    line_total = Column(Float)


class PaymentInfoCard(db.Model):

    __tablename__ = "payment_info_card"

    id = Column(Integer, primary_key=True)
    card_holder_name = Column(String(512))
    card_number = Column(String(512))
    card_expiry_month = Column(String(512))
    card_expiry_year = Column(String(512))
    cvv_cvc = Column(String(512))


class PaymentInfoGeneric(db.Model):

    __tablename__ = "payment_info_generic"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))
    setting = Column(Text)


class PaymentMethods(db.Model):

    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))


class Providers(db.Model):

    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    provider_code = Column(String(512))
    name = Column(String(512))


class Retailers(db.Model):

    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))


class UserPaymentSettings(db.Model):

    __tablename__ = "user_payment_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    payment_info_type = Column(String(512))
    payment_info_id = Column(Integer)
    is_primary = Column(Boolean)


class Transactions(db.Model):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime)
    payer_type = Column(String(512))
    payer_id = Column(Integer)
    bill_id = Column(Integer)
    payment_setting_id = Column(Integer)
    grand_total = Column(Float)
    remark = Column(Text)

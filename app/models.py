from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class Meterboxes(Model):

    __tablename__ = "meterboxes"

    id = Column(Integer, primary_key=True)
    box_number = Column(String(512))


class Bills(Model):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    reading_date = Column(DateTime)
    due_date = Column(DateTime)
    meterbox_id = Column(Integer, ForeignKey("meterboxes.id"))
    previous_reading = Column(Integer)
    current_reading = Column(Integer)
    diff_reading = Column(Integer)
    sub_total = Column(Float)
    maintenance_fee = Column(Float)
    horsepower_fee = Column(Float)
    grand_total = Column(Float)
    remark = Column(Text)
    meterbox = relationship("Meterboxes")


class BillsDetails(Model):

    __tablename__ = "bills_detail"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    line_item = Column(String(512))
    unit_price = Column(Float)
    quantity = Column(Integer)
    line_total = Column(Float)
    bill = relationship("Bills")


class PaymentInfoCard(Model):

    __tablename__ = "payment_info_card"

    id = Column(Integer, primary_key=True)
    card_holder_name = Column(String(512))
    card_number = Column(String(512))
    card_expiry_month = Column(String(512))
    card_expiry_year = Column(String(512))
    cvv_cvc = Column(String(512))


class PaymentInfoGeneric(Model):

    __tablename__ = "payment_info_generic"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))
    setting = Column(Text)


class PaymentMethods(Model):

    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))


class Providers(Model):

    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    provider_code = Column(String(512))
    name = Column(String(512))


class Retailers(Model):

    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))


class UserPaymentSettings(Model):

    __tablename__ = "user_payment_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    payment_info_type = Column(String(512))
    payment_info_id = Column(Integer)
    is_primary = Column(Boolean)
    user = relationship("User")


class Transactions(Model):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime)
    payer_type = Column(String(512))
    payer_id = Column(Integer)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    payment_setting_id = Column(Integer, ForeignKey("user_payment_settings.id"))
    grand_total = Column(Float)
    remark = Column(Text)
    bill = relationship("Bills")
    payment_setting = relationship("UserPaymentSettings")

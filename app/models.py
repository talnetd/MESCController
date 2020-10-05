from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
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
from flask_babel import get_locale
from flask_babel import lazy_gettext as _
from sqlalchemy.orm import relationship

from . import db


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class Regions(AuditMixin, Model):

    __tablename__ = "regions"
    id = Column(Integer, primary_key=True)
    name_en = Column(String(128))
    name_my = Column(String(256))

    def __str__(self):
        current_locale = get_locale()
        attr_name = f"name_{current_locale}"
        if hasattr(self, attr_name):
            return getattr(self, attr_name)


class Townships(AuditMixin, Model):

    __tablename__ = "townships"
    id = Column(Integer, primary_key=True)
    name_en = Column(String(128))
    name_my = Column(String(256))
    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("Regions")

    def __str__(self):
        current_locale = get_locale()
        attr_name = f"name_{current_locale}"
        if hasattr(self, attr_name):
            return getattr(self, attr_name)


class PricingPolicy(AuditMixin, Model):

    __tablename__ = "pricing_policy"
    id = Column(Integer, primary_key=True)
    from_unit = Column(Integer)
    to_unit = Column(Integer, nullable=True)
    unit_price = Column(Float)

    def __str__(self):
        label = _("Ks {} ({} units and over)")
        message = label.format(self.unit_price, self.from_unit)
        if self.to_unit:
            label = _("Ks {} (from {} unit(s) to {} units)")
            message = label.format(self.unit_price, self.from_unit, self.to_unit)
        return message


class Titles(AuditMixin, Model):

    __tablename__ = "titles"
    id = Column(Integer, primary_key=True)
    name_en = Column(String(16))
    name_my = Column(String(32))

    def __str__(self):
        current_locale = get_locale()
        attr_name = f"name_{current_locale}"
        if hasattr(self, attr_name):
            return getattr(self, attr_name)


class Customers(AuditMixin, Model):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey("titles.id"))
    name_en = Column(String(256))
    name_my = Column(String(512))
    nrc_number = Column(String(256))
    township_id = Column(Integer, ForeignKey("townships.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    address = Column(String(2048))
    phones = Column(String(512))
    title = relationship("Titles")
    township = relationship("Townships")
    region = relationship("Regions")

    def __str__(self):
        current_locale = get_locale()
        attr_name = f"name_{current_locale}"
        result = ""
        if hasattr(self, attr_name):
            result = getattr(self, attr_name) or ""
        if result:
            result += " "
        result += f"({self.address} - {self.township} - {self.region})"
        return result


class Meterboxes(AuditMixin, Model):

    __tablename__ = "meterboxes"

    id = Column(Integer, primary_key=True)
    box_number = Column(String(512))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customers")

    def __str__(self):
        return f"{self.box_number} - {self.customer}"


class Bills(AuditMixin, Model):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    account_no = Column(String(32), nullable=True)
    reading_date = Column(DateTime)
    due_date = Column(DateTime)
    meterbox_id = Column(Integer, ForeignKey("meterboxes.id"))
    ref_code = Column(String(128), nullable=True)
    previous_reading = Column(Integer)
    current_reading = Column(Integer)
    diff_reading = Column(Integer)
    sub_total = Column(Float)
    maintenance_fee = Column(Float)
    horsepower_fee = Column(Float)
    grand_total = Column(Float)
    remark = Column(Text)
    meterbox = relationship("Meterboxes")
    is_billed = Column(Boolean, default=False)

    @classmethod
    def find_by_ref_code(cls, ref_code):
        return db.session.query(cls).filter_by(ref_code=ref_code).first()


class BillsDetails(AuditMixin, Model):

    __tablename__ = "bills_detail"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    line_item = Column(String(512))
    unit_price = Column(Float)
    quantity = Column(Integer)
    line_total = Column(Float)
    bill = relationship("Bills")


class PaymentInfoCard(AuditMixin, Model):

    __tablename__ = "payment_info_card"

    id = Column(Integer, primary_key=True)
    card_holder_name = Column(String(512))
    card_number = Column(String(512))
    card_expiry_month = Column(String(512))
    card_expiry_year = Column(String(512))
    cvv_cvc = Column(String(512))


class PaymentInfoGeneric(AuditMixin, Model):

    __tablename__ = "payment_info_generic"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))
    setting = Column(Text)


class PaymentMethods(AuditMixin, Model):

    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))


class Providers(AuditMixin, Model):

    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    provider_code = Column(String(512))
    name = Column(String(512))


class Retailers(AuditMixin, Model):

    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True)
    name = Column(String(512))


class UserPaymentSettings(AuditMixin, Model):

    __tablename__ = "user_payment_settings"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    payment_info_type = Column(String(512))
    payment_info_id = Column(Integer)
    is_primary = Column(Boolean)
    customer = relationship("Customers")


class Transactions(AuditMixin, Model):

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

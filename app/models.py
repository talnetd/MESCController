from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder.security.sqla.models import User
from flask_babel import get_locale
from flask_babel import lazy_gettext as _
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from . import db

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class UserExtension(User):
    __tablename__ = "ab_user"
    ref_code = Column(String(256))
    commission_fee = Column(Float)

    @property
    def is_provider(self):
        return any([each.name.lower() == "provider" for each in self.roles])

    @property
    def is_retailer(self):
        return any([each.name.lower() == "retailer" for each in self.roles])

    @classmethod
    def get_user(cls, user_id):
        return db.session.query(cls).filter_by(id=user_id).first()


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
            message = label.format(
                self.unit_price, self.from_unit, self.to_unit
            )
        return message


class Titles(AuditMixin, Model):

    __tablename__ = "titles"
    id = Column(Integer, primary_key=True)
    name_en = Column(String(16))
    name_my = Column(String(32))

    def __str__(self):
        # NOTE:
        # disabled getting value using dynamic locale.
        # current_locale = get_locale()
        # attr_name = f"name_{current_locale}"
        # if hasattr(self, attr_name):
        #     return getattr(self, attr_name)
        return self.name_en or self.name_my


class Customers(AuditMixin, Model):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=True)
    name_en = Column(String(256))
    name_my = Column(String(512))
    # NOTE: username is meter_user_name
    username = Column(String(512))
    nrc_number = Column(String(256))
    township_id = Column(Integer, ForeignKey("townships.id"), nullable=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    # NOTE:
    # address is meter_user_address
    address = Column(String(2048))
    phones = Column(String(512))
    title = relationship("Titles")
    township = relationship("Townships")
    region = relationship("Regions")

    def __str__(self):
        return f"{self.username} - {self.address}"


class Meterboxes(AuditMixin, Model):

    __tablename__ = "meterboxes"

    id = Column(Integer, primary_key=True)
    # NOTE
    # box_number is meter_number
    box_number = Column(String(512))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customers")
    bills = relationship("Bills", back_populates="meterbox", uselist=False)

    def __str__(self):
        return f"{self.box_number} - {self.customer}"


class OperatorType(AuditMixin, Model):

    __tablename__ = "operator_type"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))

    def __str__(self):
        return f"{self.name}"


class CommissionPolicy(AuditMixin, Model):

    __tablename__ = "commission_policy"

    id = Column(Integer, primary_key=True)
    # NOTE: operator_type will be: "provider", "retailer"
    operator_type_id = Column(
        Integer, ForeignKey("operator_type.id"), unique=True
    )
    operator_type = relationship("OperatorType")
    max_charge = Column(Float)
    global_commission_fee = Column(Float)

    @classmethod
    def get_policy_by_role(cls, role):
        operator_type = (
            db.session.query(OperatorType)
            .filter(OperatorType.name.ilike(f"{role}%"))
            .first()
        )
        if not operator_type:
            return
        return (
            db.session.query(cls)
            .filter_by(operator_type_id=operator_type.id)
            .first()
        )


class Bills(AuditMixin, Model):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    # NOTE: account_no is ledger_code
    account_no = Column(String(32), nullable=True)
    # NOTE: reading_date is meter_reading_date
    reading_date = Column(DateTime)
    # NOTE: due_date is meter_due_date
    due_date = Column(DateTime)
    meterbox_id = Column(Integer, ForeignKey("meterboxes.id"))
    # NOTE:
    # ref_code is unituue_id
    ref_code = Column(String(128), nullable=True)
    # NOTE: previous_reading is previous_unit
    previous_reading = Column(Integer)
    # NOTE: current_reading is current_unit
    current_reading = Column(Integer)
    # NOTE: diff_reading is used_unit
    diff_reading = Column(Integer)
    # NOTE: sub_total is the sum of BillDetails
    sub_total = Column(Float)
    # NOTE: maintenance_fee is service_charge
    maintenance_fee = Column(Float)
    # NOTE: horsepower is horse_power
    horsepower = Column(Float)
    # NOTE: horsepower_fee is horse_power_charge
    horsepower_fee = Column(Float)
    ref_multiply = Column(Float)
    ref_addition = Column(Float)
    # NOTE: ref_terrif_code is terrifcode
    ref_terrif_code = Column(String(32))
    ref_rate = Column(Float)
    grand_total = Column(Float)
    # NOTE: ref_total_charge is total_charge as a reference.
    ref_total_charge = Column(Float)
    remark = Column(Text)
    meterbox = relationship("Meterboxes")
    is_billed = Column(Boolean, default=False)
    exemption = Column(Float)

    @classmethod
    def find_by_ref_code(cls, ref_code):
        return db.session.query(cls).filter_by(ref_code=ref_code).first()

    @classmethod
    def find_by_meter_number_and_ref_code(cls, meter_number, ref_code):
        meterbox = (
            db.session.query(Meterboxes)
            .filter_by(box_number=meter_number)
            .first()
        )
        if meterbox:
            bill = (
                db.session.query(cls)
                .filter_by(ref_code=ref_code, meterbox=meterbox)
                .first()
            )
            return bill

    def __str__(self):
        return f"{self.account_no} - {self.ref_code}"


class BillsDetails(AuditMixin, Model):

    __tablename__ = "bills_detail"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    line_item = Column(String(512))
    unit_price = Column(Float)
    pricing_policy_id = Column(
        Integer, ForeignKey("pricing_policy.id"), nullable=True
    )
    quantity = Column(Integer)
    line_total = Column(Float)
    bill = relationship("Bills")
    pricing_policy = relationship("PricingPolicy")


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
    payment_setting_id = Column(
        Integer, ForeignKey("user_payment_settings.id")
    )
    grand_total = Column(Float)
    remark = Column(Text)
    bill = relationship("Bills")
    payment_setting = relationship("UserPaymentSettings")

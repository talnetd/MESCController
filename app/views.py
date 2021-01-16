import csv
from io import StringIO

from flask import g, make_response, render_template
from flask_appbuilder import ModelView
from flask_appbuilder.api import expose
from flask_appbuilder.baseviews import get_filter_args
from flask_appbuilder.models.sqla.filters import (FilterEqual,
                                                  FilterEqualFunction,
                                                  FilterInFunction)
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.widgets import ListWidget
from flask_babel import lazy_gettext as _

from . import appbuilder, db, models
from .api_views import BillModelApi, BillsAPI, CreditAPI
from .form_views import ViewCheckBillStatus
"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""
"""
    Application wide 404 error handler
"""


def get_user():
    user_ext = models.UserExtension.get_user(g.user.id)
    if user_ext.has_role("admin"):
        return [each.id for each in db.session.query(models.User).all()]
    else:
        return [g.user.id]


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            base_template=appbuilder.base_template,
            appbuilder=appbuilder,
        ),
        404,
    )


class MescBaseModelView(ModelView):
    add_exclude_columns = [
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    edit_exclude_columns = [
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    formatters_columns = {
        "created_on": lambda x: x.strftime("%d %b %Y %I:%M:%S %p"),
        "changed_on": lambda x: x.strftime("%d %b %Y %I:%M:%S %p"),
    }


class RegionsView(MescBaseModelView):
    datamodel = SQLAInterface(models.Regions)
    list_columns = [
        "id",
        "name_en",
        "name_my",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {
        "name_en": _("Name (En)"),
        "name_my": _("Name (My)"),
    }
    list_title = _("List Regions/States")
    add_title = _("Add Region/State")
    edit_title = _("Edit Region/State")
    show_title = _("Region/State Info")


class TownshipsView(MescBaseModelView):
    datamodel = SQLAInterface(models.Townships)
    list_columns = [
        "id",
        "name_en",
        "name_my",
        "region",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {
        "name_en": _("Name (En)"),
        "name_my": _("Name (My)"),
        "region": _("Region/State"),
    }
    list_title = _("List Townships")
    add_title = _("Add Township")
    edit_title = _("Edit Township")
    show_title = _("Township Info")


class TitlesView(MescBaseModelView):
    datamodel = SQLAInterface(models.Titles)
    list_columns = [
        "id",
        "name_en",
        "name_my",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {
        "name_en": _("Name (En)"),
        "name_my": _("Name (My)"),
    }
    list_title = _("List Titles")
    add_title = _("Add Title")
    edit_title = _("Edit Title")
    show_title = _("Title Info")


class CustomersView(MescBaseModelView):
    datamodel = SQLAInterface(models.Customers)
    list_columns = [
        "id",
        "username",
        "address",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {
        "username": _("Username"),
        "nrc_number": _("N.R.C"),
        "address": _("Address"),
        "region": _("Region"),
        "township": _("Township"),
        "phones": _("Phones"),
    }
    show_fieldsets = [
        (_("Naming"), {
            "fields": ["username"]
        }),
        (_("Additional"), {
            "fields": ["nrc_number"]
        }),
        (
            _("Contact"),
            {
                "fields": ["address", "region", "township", "phones"]
            },
        ),
    ]
    add_fieldsets = [
        (_("Naming"), {
            "fields": ["username"]
        }),
        (_("Additional"), {
            "fields": ["nrc_number"]
        }),
        (
            _("Contact"),
            {
                "fields": ["address", "region", "township", "phones"]
            },
        ),
    ]
    edit_fieldsets = [
        (_("Naming"), {
            "fields": ["username"]
        }),
        (_("Additional"), {
            "fields": ["nrc_number"]
        }),
        (
            _("Contact"),
            {
                "fields": ["address", "region", "township", "phones"]
            },
        ),
    ]
    list_title = _("List Customers")
    add_title = _("Add Customer")
    edit_title = _("Edit Customer")
    show_title = _("Customer Info")


class MeterboxView(MescBaseModelView):
    datamodel = SQLAInterface(models.Meterboxes)
    list_columns = [
        "id",
        "box_number",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {"box_number": _("Box Number")}
    list_title = _("List Meterboxes")
    add_title = _("Add Meterbox")
    edit_title = _("Edit Meterbox")
    show_title = _("Meterbox Info")
    search_columns = ["id", "box_number"]


class BillDetailView(MescBaseModelView):
    datamodel = SQLAInterface(models.BillsDetails)
    list_columns = [
        "id",
        "bill",
        "line_item",
        "unit_price",
        "quantity",
        "line_total",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {
        "bill": _("Bill"),
        "line_item": _("Line Item"),
        "unit_price": _("Unit Price"),
        "quantity": _("Quantity"),
        "line_total": _("Line Total"),
    }
    list_title = _("List Bill Details")
    add_title = _("Add Bill Detail")
    edit_title = _("Edit Bill Detail")
    show_title = _("Bill Detail Info")


class BillView(MescBaseModelView):
    datamodel = SQLAInterface(models.Bills)
    list_columns = [
        "id",
        "account_no",
        "ref_code",
        "reading_date",
        "due_date",
        "meterbox",
        "previous_reading",
        "current_reading",
        "diff_reading",
        "ref_total_charge",
        "created_on",
        "created_by",
        "changed_on",
        "changed_by",
    ]
    label_columns = {
        "account_no": _("Account No."),
        "ref_code": _("Reference Code"),
        "reading_date": _("Reading Date"),
        "due_date": _("Due Date"),
        "previous_reading": _("Previous Reading"),
        "current_reading": _("Current Reading"),
        "diff_reading": _("Reading Difference"),
        "sub_total": _("Subtotal"),
        "maintenance_fee": _("Maintenance Fee"),
        "horsepower_fee": _("Horsepower Fee"),
        "ref_total_charge": _("Total Charge"),
        "remark": _("Remark"),
        "meterbox": _("Meterbox Number"),
    }
    list_title = _("List Bills")
    add_title = _("Add Bill")
    edit_title = _("Edit Bill")
    show_title = _("Bill Info")
    related_views = [BillDetailView]
    search_columns = [
        "id",
        "account_no",
        "ref_code",
        "reading_date",
        "due_date",
    ]


class PaymentInfoCardView(MescBaseModelView):
    datamodel = SQLAInterface(models.PaymentInfoCard)
    list_columns = []
    label_columns = {}
    list_title = _("List Payment Info Cards")
    add_title = _("Add Payment Info Card")
    edit_title = _("Edit Payment Info Card")
    show_title = _("Payment Info Card")


class PaymentInfoGenericView(MescBaseModelView):
    datamodel = SQLAInterface(models.PaymentInfoGeneric)
    list_columns = []
    label_columns = {}
    list_title = _("List Payment Info Generic")
    add_title = _("Add Payment Info Generic")
    edit_title = _("Edit Payment Info Generic")
    show_title = _("Payment Info Generic")


class PaymentMethodsView(MescBaseModelView):
    datamodel = SQLAInterface(models.PaymentMethods)
    list_columns = []
    label_columns = {}
    list_title = _("List Payment Methods")
    add_title = _("Add Payment Method")
    edit_title = _("Edit Payment Method")
    show_title = _("Payment Method Info")


class UserPaymentSettingsView(MescBaseModelView):
    datamodel = SQLAInterface(models.UserPaymentSettings)
    list_columns = []
    label_columns = {}
    list_title = _("List User Payment Settings")
    add_title = _("Add User Payment Setting")
    edit_title = _("Edit User Payment Setting")
    show_title = _("User Payment Setting Info")


class Transactions(MescBaseModelView):
    datamodel = SQLAInterface(models.Transactions)
    list_columns = ["id", "transaction_date", "payer_type", "payer_id", "bill"]
    label_columns = {
        "transaction_date": _("Transaction Date"),
        "payer_type": _("Agent Type"),
        "payer_id": _("Agent"),
        "bill": _("Bill"),
    }
    list_title = _("List Transactions")
    add_title = _("Add Transaction")
    edit_title = _("Edit Transaction")
    show_title = _("Transaction Info")


class CommissionPolicy(MescBaseModelView):
    datamodel = SQLAInterface(models.CommissionPolicy)
    list_columns = [
        "id",
        "operator_type",
        "max_charge",
        "global_commission_fee",
    ]
    label_columns = {
        "operator_type": _("Type"),
        "max_charge": _("Max Charge"),
        "global_commission_fee": _("Commission Fee"),
    }
    list_title = _("List Commission Policies")
    add_title = _("Add Commission Policy")
    edit_title = _("Edit Commission Policy")
    show_title = _("Commission Policy Info")


class CreditTransactionsView(MescBaseModelView):
    datamodel = SQLAInterface(models.CreditTransactions)
    list_columns = [
        "id", "transaction_date", "user", "amount", "remark", "created_by"
    ]
    label_columns = {
        "transaction_date": _("Credit On"),
        "user": _("Credit To"),
        "created_by": _("By")
    }
    base_filters = [["user_id", FilterInFunction, get_user]]

    def post_add(self, item):
        try:
            balance = db.session.query(
                models.CreditBalance).filter_by(user=item.user).first()
            if not balance:
                balance = models.CreditBalance()
                balance.user = item.user
                balance.amount = item.amount
            else:
                balance.amount += item.amount

            db.session.add(balance)
            db.session.commit()
        except:
            db.session.rollback()

    def post_delete(self, item):
        try:
            balance = db.session.query(
                models.CreditBalance).filter_by(user_id=item.user_id).first()
            if balance:
                balance.amount -= item.amount
                db.session.add(balance)
                db.session.commit()
        except:
            db.session.rollback()


class CreditBalanceView(MescBaseModelView):
    datamodel = SQLAInterface(models.CreditBalance)
    list_columns = [
        "id", "user", "amount", "created_by", "created_on", "changed_by",
        "changed_on"
    ]
    base_filters = [["user_id", FilterInFunction, get_user]]


class DownloadBillsByPartnerWidget(ListWidget):
    template = 'components/download_bills_by_partner.html'


class ReportBillsCollectedByPartnersView(MescBaseModelView):
    base_permissions = ['can_list', 'can_csv']
    datamodel = SQLAInterface(models.ReportBillsCollectedByPartners)
    base_filters = [["changed_by_fk", FilterInFunction, get_user]]
    base_order = ("id", "asc")
    list_columns = [
        "collected_date",
        "collected_bills",
        "amount",
        # "first_name",
        # "last_name",
        "username",
        "ref_code",
        "role",
    ]

    list_widget = DownloadBillsByPartnerWidget

    @expose('/csv', methods=['GET'])
    def download_csv(self):
        get_filter_args(self._filters)
        order_column, order_direction = self.base_order
        count, lst = self.datamodel.query(self._filters, order_column,
                                          order_direction)

        sio = StringIO()
        csv_writer = csv.DictWriter(sio, fieldnames=self.list_columns)
        csv_writer.writeheader()
        for item in self.datamodel.get_values(lst, self.list_columns):
            csv_writer.writerow(item)
        response = make_response(sio.getvalue())
        cd = 'attachment; filename=mycsv.csv'
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'text/csv'
        return response


# disabled by lmk on 2020-12-18
# db.create_all()

appbuilder.add_view(
    RegionsView,
    "Regions",
    label=_("Regions/States"),
    icon="fa-folder-open-o",
    category="Manage",
    category_label=_("Manage"),
)
appbuilder.add_view(
    TownshipsView,
    "Townships",
    label=_("Townships"),
    icon="fa-folder-open-o",
    category="Manage",
)
# appbuilder.add_separator("Manage")
appbuilder.add_view(
    TitlesView,
    "Titles",
    label=_("Titles"),
    icon="fa-folder-open-o",
    category="Manage",
)
appbuilder.add_view(
    CustomersView,
    "Customers",
    label=_("Customers"),
    icon="fa-folder-open-o",
    category="Manage",
)
# appbuilder.add_separator("Manage")
appbuilder.add_view(
    MeterboxView,
    "Meterboxes",
    label=_("Meterboxes"),
    icon="fa-folder-open-o",
    category="Manage",
)
appbuilder.add_view(
    Transactions,
    "submenu_transactions",
    label=_("Transactions"),
    icon="fa-folder-open-o",
    category="Manage",
)
appbuilder.add_view(
    CommissionPolicy,
    "submenu_commission_policy",
    label=_("Commission Policy"),
    icon="fa-folder-open-o",
    category="Manage",
)
appbuilder.add_separator("Manage")

appbuilder.add_view(CreditBalanceView,
                    "submenu_credit_balance",
                    label=_("Credit Balance"),
                    icon="fa-folder-open-o",
                    category="Manage")
appbuilder.add_view(CreditTransactionsView,
                    "submenu_credit_transactions",
                    label=_("Credit Transaction"),
                    icon="fa-folder-open-o",
                    category="Manage")

appbuilder.add_view(
    BillView,
    "submenu_bills",
    label=_("Bills"),
    icon="fa-folder-open-o",
    category="Bill",
    category_label=_("Bill"),
)
appbuilder.add_view(
    BillDetailView,
    "submenu_bill_details",
    label=_("Bill Details"),
    icon="fa-folder-open-o",
    category="Bill",
)
appbuilder.add_view(
    PaymentInfoCardView,
    "submenu_payment_info_card",
    label=_("Payment Info - Card"),
    icon="fa-folder-open-o",
    category="Payment",
    category_label=_("Payment"),
)
appbuilder.add_view(
    PaymentInfoGenericView,
    "submenu_payment_info_generic",
    label=_("Payment Info - Generic"),
    icon="fa-folder-open-o",
    category="Payment",
)
appbuilder.add_view(
    PaymentMethodsView,
    "submenu_payment_methods",
    label=_("Payment Methods"),
    icon="fa-folder-open-o",
    category="Payment",
)
appbuilder.add_view(
    UserPaymentSettingsView,
    "submenu_payment_settings",
    label=_("Payment Settings"),
    icon="fa-folder-open-o",
    category="Payment",
)
appbuilder.add_view(
    ViewCheckBillStatus,
    "public_submenu_check_bill_status",
    label=_("Bill Status"),
    icon="fa-folder-open-o",
    category="public_menu_check",
    category_label=_("Check"),
)
appbuilder.add_view(ReportBillsCollectedByPartnersView,
                    "submenu_bills_collected",
                    label=_("Bills Collected by Partners"),
                    icon="fa-table",
                    category="Report")
appbuilder.add_separator("Report")
appbuilder.add_api(BillsAPI)
appbuilder.add_api(BillModelApi)
appbuilder.add_api(CreditAPI)

# appbuilder.security_cleanup()

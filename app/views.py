from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_babel import lazy_gettext as _

from . import appbuilder, db
from . import models


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


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


class MeterboxView(ModelView):
    datamodel = SQLAInterface(models.Meterboxes)


class BillView(ModelView):
    datamodel = SQLAInterface(models.Bills)


class BillDetailView(ModelView):
    datamodel = SQLAInterface(models.BillsDetails)


class PaymentInfoCardView(ModelView):
    datamodel = SQLAInterface(models.PaymentInfoCard)


class PaymentInfoGenericView(ModelView):
    datamodel = SQLAInterface(models.PaymentInfoGeneric)


class PaymentMethodsView(ModelView):
    datamodel = SQLAInterface(models.PaymentMethods)


class ProvidersView(ModelView):
    datamodel = SQLAInterface(models.Providers)


class RetailersView(ModelView):
    datamodel = SQLAInterface(models.Providers)


class UserPaymentSettingsView(ModelView):
    datamodel = SQLAInterface(models.UserPaymentSettings)


class Transactions(ModelView):
    datamodel = SQLAInterface(models.Transactions)


db.create_all()


appbuilder.add_view(
    MeterboxView,
    "Meterboxes",
    label=_("Meterboxes"),
    icon="fa-folder-open-o",
    category="Manage",
    category_label=_("Manage"),
)
appbuilder.add_view(
    BillView,
    "Bills",
    label=_("Bills"),
    icon="fa-folder-open-o",
    category="Bill",
    category_label=_("Bill"),
)
appbuilder.add_view(
    BillDetailView,
    "Bill Details",
    label=_("Bill Details"),
    icon="fa-folder-open-o",
    category="Bill",
)
appbuilder.add_view(
    PaymentInfoCardView,
    "Payment Info - Card",
    label=_("Payment Info - Card"),
    icon="fa-folder-open-o",
    category="Payment",
    category_label=_("Payment"),
)
appbuilder.add_view(
    PaymentInfoGenericView,
    "Payment Info - Generic",
    label=_("Payment Info - Generic"),
    icon="fa-folder-open-o",
    category="Payment",
)
appbuilder.add_view(
    PaymentMethodsView,
    "Payment Methods",
    label=_("Payment Methods"),
    icon="fa-folder-open-o",
    category="Payment",
)
appbuilder.add_view(
    ProvidersView,
    "Providers",
    label=_("Providers"),
    icon="fa-folder-open-o",
    category="Manage",
)
appbuilder.add_view(
    RetailersView,
    "Retailers",
    label=_("Retailers"),
    icon="fa-folder-open-o",
    category="Manage",
)
appbuilder.add_view(
    UserPaymentSettingsView,
    "Payment Settings",
    label=_("Payment Settings"),
    icon="fa-folder-open-o",
    category="Payment",
)
appbuilder.add_view(
    Transactions,
    "Transactions",
    label=_("Transactions"),
    icon="fa-folder-open-o",
    category="Manage",
)

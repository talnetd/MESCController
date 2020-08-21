# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint, url_for
from flask_admin.contrib.sqla import ModelView
from app import admin, db
from app.base import models


blueprint = Blueprint(
    "base_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)


admin.add_view(ModelView(models.User, db.session, category="System"))
admin.add_view(ModelView(models.Meterboxes, db.session, category="Manage"))
admin.add_view(ModelView(models.Bills, db.session, category="Billing"))
admin.add_view(ModelView(models.BillsDetails, db.session, category="Billing"))
admin.add_view(ModelView(models.PaymentInfoCard, db.session, category="Payment"))
admin.add_view(ModelView(models.PaymentInfoGeneric, db.session, category="Payment"))
admin.add_view(ModelView(models.PaymentMethods, db.session, category="Payment"))
admin.add_view(ModelView(models.Providers, db.session, category="Manage"))
admin.add_view(ModelView(models.Retailers, db.session, category="Manage"))
admin.add_view(ModelView(models.UserPaymentSettings, db.session, category="Payment"))
admin.add_view(ModelView(models.Transactions, db.session, category="Manage"))

from flask import flash
from flask_appbuilder import PublicFormView
from flask_babel import lazy_gettext as _
from app import db

from .forms import FormCheckBillStatus
from .models import Bills


class FormViewCheckBillStatus(PublicFormView):
    form = FormCheckBillStatus
    form_title = _("Check Bill Status")
    route_base = "/check/bill_status"
    form_template = "forms/check_bill_status.html"

    def form_post(self, form):
        # post process form
        ref_code = form.data.get("ref_code")
        record = Bills.find_by_ref_code(ref_code)
        if record:
            if record.is_billed:
                flash(
                    _(f"Congrats! You already have paid Meter Bill for {ref_code}."),
                    "info",
                )
            else:
                due_date = record.due_date
                message = f"Meter Bill for {ref_code} is NOT paid yet."
                if due_date:
                    message += f"<br/><br/>DUE DATE IS {due_date.strftime('%d %b %Y')}."
                flash(_(message), "warning")
        else:
            flash(_(f"Sorry. We could not find Meter Bill for {ref_code}."), "danger")

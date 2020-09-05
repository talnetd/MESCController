from flask import flash, request, redirect
from flask_appbuilder import PublicFormView, expose
from flask_babel import lazy_gettext as _

from .forms import FormCheckBillStatus, FormCheckBillStatusV2
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
                    _("Congrats! You already have paid Meter Bill for {}.").format(
                        ref_code
                    ),
                    "info",
                )
            else:
                due_date = record.due_date
                message = "Meter Bill for {} is NOT paid yet."
                if due_date:
                    message += "<br/><br/>DUE DATE IS {}."
                flash(
                    _(message).format(ref_code, due_date.strftime("%d %b %Y")),
                    "warning",
                )
        else:
            flash(
                _("Sorry. We could not find Meter Bill for {}.").format(ref_code),
                "danger",
            )


class ViewCheckBillStatus(PublicFormView):
    route_base = "/check"
    default_view = "bill_status"

    @expose("/bill_status/", methods=["GET", "POST"])
    def bill_status(self):
        form = FormCheckBillStatusV2()
        if request.method == "POST":
            ref_code = request.form.get("ref_code")
            record = Bills.find_by_ref_code(ref_code)
            if record:
                if record.is_billed:
                    flash(
                        _("Congrats! You already have paid Meter Bill for {}.").format(
                            ref_code
                        ),
                        "info",
                    )
                else:
                    due_date = record.due_date
                    message = "Meter Bill for {} is NOT paid yet."
                    if due_date:
                        message += "<br/><br/>DUE DATE IS {}."
                    flash(
                        _(message).format(ref_code, due_date.strftime("%d %b %Y")),
                        "warning",
                    )
            else:
                flash(
                    _("Sorry. We could not find Meter Bill for {}.").format(ref_code),
                    "danger",
                )

        return self.render_template("forms/check_bill_status_v2.html", form=form)

from wtforms import StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_babel import lazy_gettext as _


class FormCheckBillStatus(DynamicForm):
    ref_code = StringField(
        _("Reference Code"),
        description=_("Enter reference code to check Bill Status."),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
    )

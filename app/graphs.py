# import calendar

from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_sum
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _

from . import appbuilder
from .models import ReportDailyBillCollected


def pretty_collected_date(value):
    return value.strftime("%d-%b-%Y")


def pretty_month_year(value):
    return value.strftime("%B-%Y")


def pretty_year(value):
    return str(value.year)


class BillListReportChart(GroupByChartView):
    datamodel = SQLAInterface(ReportDailyBillCollected)
    chart_title = "Total Collected Bills"
    chart_type = "ColumnChart"
    label_columns = {"collected_date": "Collected On"}
    search_columns = ["collected_date", "total"]
    definitions = [{
        "group": "collected_date",
        "label": "Daily",
        "formatter": pretty_collected_date,
        "series": [(aggregate_sum, "total")],
    }, {
        "group": "month_year",
        "label": "Monthly",
        "formatter": pretty_month_year,
        "series": [(aggregate_sum, "total")],
    }, {
        "group": "year",
        "label": "Yearly",
        "formatter": pretty_year,
        "series": [(aggregate_sum, "total")],
    }]


appbuilder.add_view(BillListReportChart,
                    "submenu_bill_chart",
                    label=_("Bill Collection Chart"),
                    icon="fa-dashboard",
                    category="Report")

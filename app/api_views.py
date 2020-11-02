import logging
from http import HTTPStatus

import requests
from flask import g, request
from flask_appbuilder.api import BaseApi, ModelRestApi, expose, safe
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import protect

from app import db
from app.models import Bills

logger = logging.getLogger()


def get_user():
    return g.user


class BillsAPI(BaseApi):

    resource_name = "bills"

    # @expose("/check/public", methods=["GET"])
    # @safe
    def check_bill_status(self):
        """Check bill status. (PUBLIC API)
        ---
        get:
          summary: Check Meter Bill Status using Reference Code. This is PUBLIC API.
          responses:
            200:
              description: status of Meter Bill
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      data:
                        type: object
                        properties:
                          is_billed:
                            type: boolean

        """
        resp_data = dict()
        if request.method == "GET":
            billed = False
            ref_code = request.args.get("ref_code")
            found = Bills.find_by_ref_code(ref_code)
            if found:
                billed = found.is_billed or False
            resp_data["is_billed"] = billed
            return self.response(HTTPStatus.OK, data=resp_data)

    @expose("/check")
    @protect()
    @safe
    def check_private(self):
        """Check bill status in details. (PROTECTED API)
        ---
        get:
          summary: Check Meter Bill Status using Reference Code. This is PROTECTED API.
          parameters:
            - in: query
              name: ref_code
              schema:
                type: string
              description: Reference Code for Meter Bill
          responses:
            200:
              description: status of Meter Bill
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      data:
                        type: object
                        properties:
                          is_billed:
                            type: boolean
                          previous_reading:
                            type: integer
                          current_reading:
                            type: integer
                          diff_reading:
                            type: integer
                          maintenance_fee:
                            type: number
                          horsepower:
                            type: number
                          horsepower_fee:
                            type: number
                          multiply:
                            type: number
                          addition:
                            type: number
                          terrif_code:
                            type: string
                          total_charge:
                            type: number
                          user:
                            type: object
                            properties:
                              username:
                                type: string
                              address:
                                type: string
        """
        resp_data = dict()
        if request.method == "GET":
            billed = False
            ref_code = request.args.get("ref_code")
            found = Bills.find_by_ref_code(ref_code)
            if found:
                billed = found.is_billed or False
                resp_data["previous_reading"] = found.previous_reading
                resp_data["current_reading"] = found.current_reading
                resp_data["diff_reading"] = found.diff_reading
                resp_data["maintenance_fee"] = found.maintenance_fee
                resp_data["horsepower"] = found.horsepower
                resp_data["horsepower_fee"] = found.horsepower_fee
                resp_data["multiply"] = found.ref_multiply
                resp_data["addition"] = found.ref_addition
                resp_data["terrif_code"] = found.ref_terrif_code
                resp_data["total_charge"] = found.ref_total_charge

                user_data = dict(
                    username=found.meterbox.customer.username,
                    address=found.meterbox.customer.address,
                )
                resp_data.update(user=user_data)

            resp_data["is_billed"] = billed
            return self.response(HTTPStatus.OK, data=resp_data)

    def execute_callback(self, url, data, ref_code=None):
        try:
            resp = requests.post(url, data=data)
            if not resp.ok:
                logger.warning(
                    f"An error occurred when executing callback for {ref_code}."
                )
                logger.error(resp.text)
            else:
                logger.info(
                    f"Successfully executed callback URL for {ref_code}"
                )
                logger.info(resp.text)
        except Exception as exc:
            logger.warning("Could not execute callback API.")
            logger.error(exc)

    @expose("/pay", methods=["POST"])
    @protect()
    @safe
    def pay_meter_bill(self):
        """Pay Meter Bill
        ---
        post:
          summary: Pay Meter Bill using Reference Code.
          requestBody:
            description: A JSON object containing Reference Code
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    ref_code:
                      type: string
                    callback_url:
                      type: string
                    callback_data:
                      type: object

          responses:
            200:
              description: Paid successfully.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
            409:
              description: Bill already paid
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
            404:
              description: Bill not found.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        message = ""
        status = HTTPStatus.BAD_REQUEST
        if request.method == "POST":
            # Sample: using form data.
            # print(request.form)
            # ref_code = request.form.get("ref_code")

            # Sample: using application/json
            json_data = request.get_json() or dict()
            ref_code = json_data.get("ref_code")
            cb_url = json_data.get("callback_url")
            cb_data = json_data.get("callback_data")

            found = Bills.find_by_ref_code(ref_code)
            if found:
                if not found.is_billed:
                    found.is_billed = True
                    db.session.add(found)
                    db.session.commit()

                    self.execute_callback(cb_url, cb_data, ref_code=ref_code)

                    status = HTTPStatus.OK
                    message = "Meter Bill has been paid successfully."
                else:
                    status = HTTPStatus.CONFLICT
                    message = (
                        f"Meter Bill has been already paid for {ref_code}."
                    )
            else:
                status = HTTPStatus.NOT_FOUND
                message = f"Meter Bill not found for {ref_code}."

        return self.response(status, message=message)


class BillModelApi(ModelRestApi):
    exclude_route_methods = ("put", "post", "delete")
    resource_name = "bill"
    datamodel = SQLAInterface(Bills)
    page_size = 20
    base_filters = [["changed_by", FilterEqualFunction, get_user]]
    list_columns = [
        "id",
        "account_no",
        "reading_date",
        "due_date",
        "meterbox_id",
        "ref_code",
        "previous_reading",
        "current_reading",
        "diff_reading",
        "sub_total",
        "maintenance_fee",
        "horsepower",
        "horsepower_fee",
        "ref_multiply",
        "ref_addition",
        "ref_terrif_code",
        "ref_rate",
        "grand_total",
        "ref_total_charge",
        "remark",
        "meterbox",
        "is_billed",
        "created_by",
        "changed_by",
    ]

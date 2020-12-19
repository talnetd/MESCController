import logging
from http import HTTPStatus

import requests
from flask import g, request
from flask_appbuilder.api import BaseApi, ModelRestApi, expose, safe
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import permission_name, protect

from app import db
from app.models import Bills, BillsDetails, CommissionPolicy, UserExtension, CreditBalance, CreditTransactions

logger = logging.getLogger()


def get_user():
    return g.user


class CreditAPI(BaseApi):
    resource_name = "credit"
    base_permissions = [
        "can_get",
        "can_put",
        "can_post",
        "can_delete",
        "can_info",
    ]

    @expose("/")
    @protect()
    @safe
    @permission_name("get")
    def get_info(self):
        """Get Retailer Balance.
        ---
        get:
          summary: Get Credit Balance and Credit Transactions of each retailer 
          responses:
            200:
              description: Balance and Transaction List
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      data:
                        type: object

        """
        user = get_user()
        balance = db.session.query(CreditBalance).filter_by(user=user).first()
        resp = dict()
        if balance:
            resp = balance.to_json()
        transactions = db.session.query(CreditTransactions).filter_by(
            user=user).all()
        if transactions:
            resp["transactions"] = [each.to_json() for each in transactions]
        return self.response(HTTPStatus.OK, data=resp)


class BillsAPI(BaseApi):

    resource_name = "bills"
    base_permissions = [
        "can_get",
        "can_put",
        "can_post",
        "can_delete",
        "can_info",
    ]

    # @expose("/check/public", methods=["GET"])
    # @safe
    def check_bill_status(self):
        """Check bill status. (PUBLIC API)
        ---
        get:
          summary: Check Meter Bill Status using Reference Code. This is PUBLIC API.
          parameters:
            - in: query
              name: ref_code
              schema:
                type: string
              description: Reference Code for Meter Bill
            - in: query
              name: meter_number
              schema:
                type: string
              description: Meterbox Number for the Bill
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
            meter_number = request.args.get("meter_number")
            found = Bills.find_by_meter_number_and_ref_code(
                meter_number, ref_code)
            if found:
                billed = found.is_billed or False
            resp_data["is_billed"] = billed
            return self.response(HTTPStatus.OK, data=resp_data)

    @expose("/check")
    @protect()
    @safe
    @permission_name("get")
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
            - in: query
              name: meter_number
              schema:
                type: string
              description: Meterbox Number for the Bill
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
                          id:
                            type: integer
                          meterbox_id:
                            type: integer
                          due_date:
                            type: string
                          reading_date:
                            type: string
                          ref_code:
                            type: string
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
                          rate:
                            type: number
                          exemption:
                            type: number
                          user:
                            type: object
                            properties:
                              username:
                                type: string
                              address:
                                type: string
                          meterbox:
                            type: object
                            properties:
                              box_number:
                                type: string
                          bill_details:
                            type: array
                            items:
                              type: object
                              properties:
                                bill_id:
                                  type: integer
                                  description: id of Bills
                                id:
                                  type: integer
                                  description: Primary Key of BillDetails
                                line_item:
                                  type: string
                                line_total:
                                  type: number
                                pricing_policy_id:
                                  type: integer
                                quantity:
                                  type: integer
                                unit_price:
                                  type: number
        """
        resp_data = dict()
        if request.method == "GET":
            ref_code = request.args.get("ref_code")
            meter_number = request.args.get("meter_number")
            found = Bills.find_by_meter_number_and_ref_code(
                meter_number, ref_code)
            if found:
                resp_data = found.to_json()
                tmp_ref_fields = [
                    "ref_multiply",
                    "ref_addition",
                    "ref_terrif_code",
                    "ref_total_charge",
                    "ref_rate",
                ]
                for each in tmp_ref_fields:
                    tmp_data = resp_data.pop(each)
                    tmp_field = each.replace("ref_", "")
                    resp_data[tmp_field] = tmp_data

                resp_data["is_billed"] = resp_data.get("is_billed") or False
                resp_data.pop("sub_total")
                resp_data.pop("grand_total")

                # calculate total_charge
                # formula: total_charge + (global_commission_fee or each_commission_fee)
                ###
                # user_ext = UserExtension.get_user(g.user.id)
                # each_commission_fee = user_ext.commission_fee
                # role = "N/A"
                # global_commission_fee = 0
                # if user_ext.is_provider:
                #     role = "provider"
                # elif user_ext.is_retailer:
                #     role = "retailer"
                # commission_policy_record = CommissionPolicy.get_policy_by_role(
                #     role
                # )
                # if commission_policy_record:
                #     global_commission_fee = (
                #         commission_policy_record.global_commission_fee
                #     )
                # if each_commission_fee:
                #     resp_data["total_charge"] += each_commission_fee
                # else:
                #     resp_data["total_charge"] += global_commission_fee

                user_data = dict(
                    username=found.meterbox.customer.username,
                    address=found.meterbox.customer.address,
                )
                meterbox_data = dict(box_number=found.meterbox.box_number)

                resp_data.update(user=user_data)
                resp_data.update(meterbox=meterbox_data)

                bill_details = (db.session.query(BillsDetails).filter_by(
                    bill_id=found.id).all())
                resp_data["bill_details"] = [
                    each.to_json() for each in bill_details
                ]
            else:
                message = f"Bill not found for {ref_code}."
                return self.response(HTTPStatus.NOT_FOUND, message=message)

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
                    f"Successfully executed callback URL for {ref_code}")
                logger.info(resp.text)
        except Exception as exc:
            logger.warning("Could not execute callback API.")
            logger.error(exc)

    @expose("/pay", methods=["POST"])
    @protect()
    @safe
    @permission_name("post")
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
                    meter_number:
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
            meter_number = json_data.get("meter_number")
            cb_url = json_data.get("callback_url")
            cb_data = json_data.get("callback_data")

            found = Bills.find_by_meter_number_and_ref_code(
                meter_number, ref_code)
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
                        f"Meter Bill has been already paid for {ref_code}.")
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
        "created_by.username",
        "created_by.first_name",
        "created_by.last_name",
        "created_by.active",
        "changed_by.username",
        "changed_by.first_name",
        "changed_by.last_name",
        "changed_by.active",
    ]

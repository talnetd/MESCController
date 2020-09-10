from http import HTTPStatus
from flask import request
from flask_appbuilder.api import BaseApi, expose, safe
from flask_appbuilder.security.decorators import protect

from app import db
from app.models import Bills


class BillsAPI(BaseApi):

    resource_name = "bills"

    @expose("/check", methods=["GET"])
    @safe
    def check_bill_status(self):
        """Check bill status
        ---
        get:
          summary: Check Meter Bill Status using Reference Code.
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
            # print(request.form)
            ref_code = request.form.get("ref_code")
            found = Bills.find_by_ref_code(ref_code)
            if found:
                if not found.is_billed:
                    found.is_billed = True
                    db.session.add(found)
                    db.session.commit()

                    status = HTTPStatus.OK
                    message = f"Meter Bill has been paid successfully."
                else:
                    status = HTTPStatus.CONFLICT
                    message = f"Meter Bill has been already paid for {ref_code}."
            else:
                status = HTTPStatus.NOT_FOUND
                message = f"Meter Bill not found for {ref_code}."

            return self.response(status, message=message)

import click
import xlrd
from app import db
from app.models import Bills, BillsDetails, Customers, Meterboxes
from dateutil.parser import parse
from flask_appbuilder.security.sqla.models import User
from tqdm import tqdm


def create_user(
    username="importer",
    email="importer@localhost",
    first_name="Date",
    last_name="Importer",
):
    user = None
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            active=True,
        )
        db.session.add(user)
        db.session.commit()
    db.session.expunge(user)
    return user


class RowImporter:
    def __init__(self, row, user):
        self.row = row
        self.user = user
        self.db_session = db.create_scoped_session()

    def prepare_customer(self):
        username = self.row.get("meter_user_name")
        address = self.row.get("meter_user_address")
        customer = (
            self.db_session.query(Customers)
            .filter_by(username=username, address=address)
            .first()
        )
        if not customer:
            customer = Customers(username=username, address=address)
            customer.created_by = self.user
            customer.changed_by = self.user
            self.db_session.add(customer)
            self.db_session.flush()
        return customer

    def prepare_meterbox(self, customer):
        box_number = self.row.get("meter_number")
        meterbox = (
            self.db_session.query(Meterboxes)
            .filter_by(box_number=box_number, customer=customer)
            .first()
        )
        if not meterbox:
            meterbox = Meterboxes(box_number=box_number, customer=customer)
            meterbox.created_by = self.user
            meterbox.changed_by = self.user
            self.db_session.add(meterbox)
            self.db_session.flush()
        return meterbox

    def prepare_bill(self, meterbox):
        ref_code = self.row.get("unituue_id")
        account_no = self.row.get("ledger_code")
        bill = (
            self.db_session.query(Bills)
            .filter_by(
                account_no=account_no, ref_code=ref_code, meterbox=meterbox
            )
            .first()
        )
        if not bill:
            bill = Bills(
                account_no=account_no,
                reading_date=parse(self.row.get("meter_reading_date")),
                due_date=parse(self.row.get("meter_due_date")),
                meterbox=meterbox,
                ref_code=ref_code,
                previous_reading=self.row.get("previous_unit"),
                current_reading=self.row.get("current_unit"),
                diff_reading=self.row.get("used_unit"),
                sub_total=0,
                maintenance_fee=self.row.get("service_charge"),
                horsepower=self.row.get("horse_power") or 0,
                horsepower_fee=self.row.get("horse_power_charge") or 0,
                ref_total_charge=self.row.get("total_charge"),
                ref_multiply=self.row.get("multiply") or 0,
                ref_addition=self.row.get("addition") or 0,
                ref_terrif_code=self.row.get("terrifcode"),
                ref_rate=self.row.get("rate"),
            )
            bill.created_by = self.user
            bill.changed_by = self.user
            self.db_session.add(bill)
            self.db_session.flush()
        return bill

    def prepare_bill_details(self, bill):
        total_bill_details = (
            self.db_session.query(BillsDetails).filter_by(bill=bill).count()
        )
        if total_bill_details < 1:
            for i in range(1, 8):
                line_total = int(self.row.get(f"charge{i}") or 0)
                quantity = int(self.row.get(f"unit{i}") or 0)
                unit_price = 0
                if quantity and line_total:
                    unit_price = line_total / quantity
                bill_detail = BillsDetails(
                    bill=bill,
                    line_item=f"charge{i}",
                    unit_price=unit_price,
                    quantity=quantity,
                    line_total=line_total,
                )
                bill_detail.created_by = self.user
                bill_detail.changed_by = self.user
                self.db_session.add(bill_detail)
                self.db_session.flush()

    def load(self):
        try:
            customer = self.prepare_customer()
            meterbox = self.prepare_meterbox(customer)
            bill = self.prepare_bill(meterbox)
            self.prepare_bill_details(bill)

            self.db_session.commit()
        except Exception as exc:
            click.echo(exc)
            self.db_session.rollback()
        finally:
            self.db_session.close()


class XlsToDb:
    path = None
    fieldnames = None
    pbar = None

    def _prepare(self):
        self.user = create_user()
        wb = xlrd.open_workbook(self.path)
        extract_value = lambda x: [each.value for each in x]  # noqa
        for sheet in wb.sheets():
            rows = sheet.get_rows()
            self.pbar = tqdm(total=sheet.nrows - 1)
            for e, row in enumerate(rows):
                if e == 0:
                    self.fieldnames = extract_value(row)
                    continue
                values = extract_value(row)
                row_prepared = dict(zip(self.fieldnames, values))
                yield row_prepared

    def load(self, path):
        self.path = path
        rows = self._prepare()
        for row in rows:
            row_importer = RowImporter(row, self.user)
            row_importer.load()
            self.pbar.update()


@click.command()
@click.argument("path", type=click.Path(exists=True))
def main(path):
    xls2db = XlsToDb()
    xls2db.load(path)


if __name__ == "__main__":
    main()

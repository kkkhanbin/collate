import math

from flask import render_template, redirect
import uuid

from pprint import pprint

from routes import routes_bp
from forms import DocumentsUpload
from parsers import ExcelParser
from data import connection

TITLE = 'Collate'

INV_COLS = [
    "EINVOICEID",
    "PRICEWITHTAX",
    "PRICEWITHOUTTAX",
    "QUANTITY",
    "UNITPRICE",
    "UNITNOMENCLATURE",
    "UNITCODE",
    "NDSRATE",
    "DESCRIPTION"
]
PO_COLS = [
    "PURCHASEORDERNUMBER",
    "LINENUMBER",
    "LINEAMOUNT",
    "ORDEREDPURCHASEQUANTITY",
    "PURCHASEPRICE",
    "PURCHASEUNITSYMBOL",
    "TNVEDCODE",
    "SALESTAXITEMGROUPCODE",
    "PURCHASEORDERLINESTATUS",
    "LINEDESCRIPTION"
]


def get_values(values: list, headers: list, required_headers: list) -> list:
    response = []
    for req in required_headers:
        value = values[headers.index(req)]
        if type(value) != str:
            if math.isnan(value):
                value = 0.0
        response.append(value)
    return response


def send_data(cc, data: list, header: list, tablename: str, pair_id: str) -> None:
    for field in data:
        df = ExcelParser.parse(field)

        cols = df.columns.tolist()
        values = df.values.tolist()
        values = list(map(lambda row: get_values(row, cols, header), values))
        values = [[str(pair_id)] + value for value in values]

        cc.executemany(f"INSERT INTO {tablename}(id, {", ".join(header)}) VALUES(?{", ?" * len(header)})", values)


@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    form = DocumentsUpload()

    if form.validate_on_submit():
        cc = connection.cursor()
        pair_id = uuid.uuid1()
        
        send_data(cc, form.invoice.data, INV_COLS, "Invoices", pair_id)
        send_data(cc, form.purchase_order.data, PO_COLS, "PurchaseOrders", pair_id)

        cc.close()

        return redirect(f"/results?id={pair_id}")

    return render_template("/index.html", form=form, title=TITLE)

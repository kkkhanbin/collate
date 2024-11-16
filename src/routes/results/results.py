from pprint import pprint

from flask import render_template, request

from routes import routes_bp
from forms import DocumentsUpload
from parsers import ExcelParser
from data import connection, AI
from compare import Compare


INV_COLS = [
    "UNITCODE",
    "QUANTITY",
    "UNITPRICE",
    "EINVOICEID",
    "UNITNOMENCLATURE",
    "NDSRATE",
    "PRICEWITHTAX",
    "PRICEWITHOUTTAX",
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

TITLE = 'Результат валидации'
PROMPT = '''
{related}
Если данные отстутствуют, значит ответ не требуется.
Это тип данных список, написанный на языке программирования Python. Список хранит в себе другие списки. 
Каждый внутренний список хранит в себе названия товаров или услуг. Твоя задача - определить могут ли названия из кортежа быть одним и тем же товаром или услугой.
Если все наименования совпали, то выведи сообщение длиной в максимально кратко, в несколько слов с описанием того, что все совпало.
Если где-то обнаружились несовпадения, выведи ответ в виде короткого сообщения (примерно 150 символов) с описанием ошибки на на словах
'''


@routes_bp.route('/results', methods=['GET'])
def results():
    cc = connection.cursor()

    pair_id = request.args["id"]
    
    cc.execute(f"SELECT {", ".join(INV_COLS)} FROM Invoices WHERE id='{pair_id}'")
    invoices = cc.fetchall()

    cc.execute(f"SELECT {', '.join(PO_COLS)} FROM PurchaseOrders WHERE id='{pair_id}'")
    pos = cc.fetchall()

    cc.close()

    cmp = Compare(invoices, pos)
    resp = cmp.process()

    inv_header = ["EINVOICEID", "DESCRIPTION", "PRICEWITHOUTTAX", "PRICEWITHTAX", "QUANTITY", "UNITPRICE"]
    po_header = ["PURCHASEORDERNUMBER", "LINENUMBER", "LINEAMOUNT", "SALESTAXITEMGROUPCODE", "LINEDESCRIPTION", "ORDEREDPURCHASEQUANTITY", "PURCHASEPRICE"]
    report_data = cmp.prepare_report_data(resp, inv_header, po_header)
    cmp.make_report(report_data, pair_id)

    rest_len = len(resp["rest"]["invs"])
    is_error = any(map(bool, resp["errors"]))

    descriptions = []
    for pair in resp["related"]:
        row = [pair[0][cmp.get_i(cmp.INV_NAME, "DESCRIPTION")]]
        for po in pair[1]:
            row.append(po[cmp.get_i(cmp.PO_NAME, "LINEDESCRIPTION")])
        descriptions.append(row)

    client = AI()
    ai_resp = client.ask(PROMPT.format(related=descriptions))
    ai_desc_status = ai_resp.json()["choices"][0]["message"]["content"]

    is_ai_needed = bool(descriptions)

    if rest_len == 0 and not is_error:
        status = 1
    elif (rest_len > 0 and len(resp["related"]) > 0) or (rest_len == 0 and is_error):
        status = 0
    else:
        status = -1
    
    return render_template(
        "results/results.html",
        title=TITLE,
        response=resp,
        status=status,
        pair_id=pair_id,
        data=report_data,
        ai_desc_status=ai_desc_status,
        is_ai_needed=is_ai_needed
    )

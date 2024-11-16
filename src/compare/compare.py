import itertools
from pprint import pprint
import os

import pandas as pd

from .validators.price.price import PriceValidator
from .validators.unit_nomenclature.unit_nomenclature import UnitNomenclatureValidator
from .validators.nds.nds import NDSValidator


class Compare:
    VALIDATORS = [PriceValidator, UnitNomenclatureValidator, NDSValidator]

    REPORTS_DIR_PATH = "src/static/reports"
    REPORT_FILENAME = "report.xlsx"

    INV_NAME = "invoice document id"
    PO_NAME = "po document id"
    
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

    def __init__(self, invoices: list, pos: list) -> None:
        self.invoices = invoices
        self.pos = sorted(pos, key=lambda po: po[self.get_i(self.PO_NAME, "ORDEREDPURCHASEQUANTITY")], reverse=True)
        self.related = []
        self.create_inv_groups()

    def create_inv_groups(self):
        self.inv_groups = {}
        for invoice in self.invoices:
            key = invoice[self.get_i(self.INV_NAME, "UNITPRICE")]
            if key in self.inv_groups:
                self.inv_groups[key].append(invoice)
            else:
                self.inv_groups[key] = [invoice]

        for unitprice in self.inv_groups:
            self.inv_groups[unitprice] = \
                sorted(self.inv_groups[unitprice], key=lambda invoice: 
                       invoice[self.get_i(self.INV_NAME, "QUANTITY")], reverse=True)
    
    @classmethod
    def prepare_report_data(cls, resp: dict, inv_header, po_header) -> list:
        sheets = []

        # Сопоставлено
        data, header = [], inv_header + ["-"] + po_header + ["Ошибка"]
        cnt = 1
        for i in range(len(resp["related"])):
            rlt = resp["related"][i]
            inv, pos = rlt[0], rlt[1]
            error = resp["errors"][i]

            first = True
            for po in pos:
                row = []
                cnt += 1

                if first:
                    row += [inv[cls.get_i(cls.INV_NAME, col_name)] for col_name in inv_header]
                else:
                    row += ["⤷"] + ["->" for _ in range(len(inv_header) - 1)]
                row += ["-"]
                row += [po[cls.get_i(cls.PO_NAME, col_name)] for col_name in po_header]

                if first:
                    err_msg = "\n".join(error)
                    err_msg = err_msg if err_msg else "-"
                    row += [err_msg]
                    first = False
                else:
                    row += ["-"]

                data.append(row)
        
        sheets.append((data, header, "Сопоставленные строки"))

        # Не сопоставленные ЭСФ
        data = []

        rest = resp["rest"]["invs"]
        for inv in rest:
            data.append([inv[cls.get_i(cls.INV_NAME, col_name)] for col_name in inv_header])

        sheets.append((data, inv_header, 'Несопоставленные строки ЭСФ'))

        # Не сопоставленные Заказы
        data = []

        rest = resp["rest"]["pos"]
        for po in rest:
            data.append([po[cls.get_i(cls.PO_NAME, col_name)] for col_name in po_header])

        sheets.append((data, po_header, 'Несопоставленные строки PO'))

        return sheets
                
    @classmethod
    def make_report(cls, sheets: list, pair_id: str) -> None:
        path = cls.REPORTS_DIR_PATH + f"/{pair_id}"
        if not os.path.exists(path):
            os.mkdir(path)

        with pd.ExcelWriter(f"{path}/{cls.REPORT_FILENAME}", engine='xlsxwriter') as writer:
            for sheet in sheets:
                data, header, sheet_name = sheet
                if not data:
                    data = [["" for _ in range(len(header))]]
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, header=header)

    def process(self) -> tuple:
        related = []
        rest = {
            "invs": [],
            "pos": []
        }
        
        errors = []
        for unitprice in self.inv_groups: 
            inv_group = self.inv_groups[unitprice]
            max_match_amount, resp = -1, None

            combs = itertools.permutations(inv_group, len(inv_group))
            for comb in combs:
                cur_resp = self.process_inv_group(comb, self.pos.copy())
                if len(cur_resp["related"]) > max_match_amount:
                    resp = cur_resp
                    max_match_amount = len(cur_resp["related"])

            related += resp["related"]
            rest["invs"] += resp["rest"]["invs"]
            rest["pos"] += resp["rest"]["pos"]

            errors_group = [[] for _ in range(len(resp["related"]))]
            for i in range(len(resp["related"])):
                for validator in self.VALIDATORS:   
                    _, error = validator.process([resp["related"][i]])
                    errors_group[i] += error
            errors += errors_group
            
        return dict(related=related, rest=rest, errors=errors)

    def process_inv_group(self, inv_group: list, pos: list) -> dict:
        resp = {
            "related": [],
            "rest": {
                "invs": [],
                "pos": []
            }
        }

        for inv in inv_group:
            unitprice = inv[self.get_i(self.INV_NAME, "UNITPRICE")]
            nds_rate = inv[self.get_i(self.INV_NAME, "NDSRATE")]
            unitprice += unitprice * nds_rate / 100
            unitprice = round(unitprice)

            inv_q = inv[self.get_i(self.INV_NAME, "QUANTITY")]
            taken_po_indices = []

            pos = list(filter(lambda po: po[self.get_i(self.PO_NAME, "PURCHASEPRICE")] == unitprice or \
                    po[self.get_i(self.PO_NAME, "PURCHASEORDERLINESTATUS")] not in ["Received", "Backorder"] != unitprice, pos))

            for j in range(len(pos)):
                po = pos[j]

                if inv_q == 0:
                    break

                if j in taken_po_indices:
                    continue

                po = pos[j]
                po_q = po[self.get_i(self.PO_NAME, "ORDEREDPURCHASEQUANTITY")]

                if po_q > inv_q:
                    continue

                taken_po_indices.append(j)
                inv_q -= po_q

            if inv_q != 0:
                resp["rest"]["invs"].append(inv)
            else:
                pair = [inv, []]
                cnt = 0
                for i in taken_po_indices:
                    pair[1].append(pos[i - cnt])
                    del pos[i - cnt]
                    cnt += 1
                resp["related"].append(pair)
        
        resp["rest"]["pos"] += pos

        return resp

    @classmethod
    def get_i(cls, doc: str, col_name: str) -> int:
        if doc == cls.INV_NAME:
            return cls.INV_COLS.index(col_name)
        return cls.PO_COLS.index(col_name)

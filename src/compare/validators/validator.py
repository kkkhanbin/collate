class Validator:
    INV_NAME = "invoice document id"
    PO_NAME = "po document id"
    
    INV_COLS =[
        "UNITCODE",
        "QUANTITY",
        "UNITPRICE",
        "EINVOICEID",
        "UNITNOMENCLATURE",
        "NDSRATE",
        "PRICEWITHTAX",
        "PRICEWITHOUTTAX"
    ]
    PO_COLS = [
        "PURCHASEORDERNUMBER",
        "LINENUMBER",
        "LINEAMOUNT",
        "ORDEREDPURCHASEQUANTITY",
        "PURCHASEPRICE",
        "PURCHASEUNITSYMBOL",
        "TNVEDCODE",
        "SALESTAXITEMGROUPCODE"
    ]

    @classmethod
    def process(cls, related: list) -> tuple:
        pass

    @classmethod
    def get_i(cls, doc: str, col_name: str) -> int:
        if doc == cls.INV_NAME:
            return cls.INV_COLS.index(col_name)
        return cls.PO_COLS.index(col_name)

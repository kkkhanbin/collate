from ..validator import Validator

NDS_RATES = {
    "РПТРУ": 12,
    "РПТРУУК": 12,
    "РПТРУБзНДС": 0,
    "РПТРУБНДСЭ": 0,
    "РПСоцЗнБзН": 8,
    "РПТРУБзНСД": 0,
    "РПТРУБНСДЭ": 0,
    "РПИмпорт": 0,
    "РПОбИмпорт": 0,
    "РПЗап.части импорт": 0,
    "РПСомОбяз": 12,
    "РПОплСомОб": 12
}


class NDSValidator(Validator):
    INVALID_MESSAGE = "Параметр SALESTAXITEMGROUPCODE строки (строк) под номером (номерами) \
{lines} в Заказе (Заказах) на покупку с ID {ids} \
не совпадает с параметром NDSRATE строки в ЭСФ с ID {inv_id}"

    @classmethod
    def process(cls, related: list) -> tuple:
        verdict, errors = True, []

        for inv_group in related:
            inv, pos = inv_group
            nds_rate = inv[cls.get_i(cls.INV_NAME, "NDSRATE")]
            for po in pos:
                po_nds = NDS_RATES[po[cls.get_i(cls.PO_NAME, "SALESTAXITEMGROUPCODE")]]

                if po_nds != nds_rate:
                    kwargs = dict(
                        inv_id = inv[cls.get_i(cls.INV_NAME, "EINVOICEID")],
                        lines = ", ".join(list(map(lambda po: str(po[cls.get_i(cls.PO_NAME, "LINENUMBER")]), pos))),
                        ids = ", ".join(set(map(lambda po: str(po[cls.get_i(cls.PO_NAME, "PURCHASEORDERNUMBER")]), pos)))
                    )
                    verdict = False

                    errors.append(cls.INVALID_MESSAGE.format(**kwargs))
        if verdict is True:
            return verdict, []
        return verdict, errors

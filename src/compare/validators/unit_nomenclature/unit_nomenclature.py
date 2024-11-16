from ..validator import Validator

MEASUREMENT_UNITS = {
    166: "кг",
    797: "100 шт",
    246: "1000 квт*ч",
    130: "1000 л",
    114: "1000 м3",
    798: "1000 шт",
    163: "г",
    306: "г д/и",
    162: "кар",
    845: "кг 90% с/в",
    841: "кг h2o2",
    852: "кг k2o",
    859: "кг koh",
    861: "кг n",
    863: "кг naoh",
    865: "кг p2o5",
    867: "кг u",
    305: "ки",
    112: "л",
    831: "л 100% спирта",
    6: "м",
    55: "м2",
    113: "м3",
    715: "пар",
    185: "т грп",
    796: "шт",
    168: "т",
    5114: "услуга"
}


class UnitNomenclatureValidator(Validator):
    INVALID_MESSAGE = "Несовпадение номенклатуры у строк под номером (номерами) \
{lines} в Заказе (Заказах) на покупку с ID {ids} \
с номенклатурой в ЭСФ с ID {inv_id}"

    @classmethod
    def process(cls, related: list) -> tuple:
        verdict, errors = True, []

        for inv_group in related:
            inv, pos = inv_group
            inv_unit = MEASUREMENT_UNITS[inv[cls.get_i(cls.INV_NAME, "UNITNOMENCLATURE")]].lower()
            for po in pos:
                if po[cls.get_i(cls.PO_NAME, "PURCHASEUNITSYMBOL")].lower() != inv_unit:

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

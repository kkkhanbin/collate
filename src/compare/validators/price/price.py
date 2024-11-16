from ..validator import Validator


class PriceValidator(Validator):
    INVALID_COMMON_PRICE_MESSAGE = "Общая стоимость строк под номером (номерами) \
{lines} в Заказе (Заказах) на покупку с ID {ids} \
не совпадает с общей стоимостью товара в ЭСФ с ID {inv_id}"
    INVALID_LINE_AMOUNT_MESSAGE = "Параметр LINEAMOUNT не совпадает с произведением QUANTITY и UNITPRICE у \
Заказа на покупку с ID {id} на строке {line}"

    ROUND_DIGITS = None

    @classmethod
    def process(cls, related: list) -> tuple:
        verdict, errors = True, []

        for inv_group in related:
            inv, pos = inv_group

            price_with_tax = round(inv[cls.get_i(cls.INV_NAME, "PRICEWITHTAX")], cls.ROUND_DIGITS)
            price_without_tax = round(inv[cls.get_i(cls.INV_NAME, "PRICEWITHOUTTAX")], cls.ROUND_DIGITS)

            sum_of_pos_multiplied = round(sum(map(lambda po: po[cls.get_i(
                cls.PO_NAME, "PURCHASEPRICE")] * po[cls.get_i(cls.PO_NAME, "ORDEREDPURCHASEQUANTITY")], pos)), cls.ROUND_DIGITS)
            sum_of_pos_line_amount = round(sum(map(lambda po: po[cls.get_i(
                cls.PO_NAME, "LINEAMOUNT")], pos)), cls.ROUND_DIGITS)
            
            errors_group = []

            if (sum_of_pos_line_amount != price_with_tax) & \
                    (sum_of_pos_line_amount != price_without_tax) & \
                    (sum_of_pos_multiplied != price_with_tax) & \
                    (sum_of_pos_multiplied != price_without_tax):
                kwargs = dict(
                    inv_id = inv[cls.get_i(cls.INV_NAME, "EINVOICEID")],
                    lines = ", ".join(list(map(lambda po: str(po[cls.get_i(cls.PO_NAME, "LINENUMBER")]), pos))),
                    ids = ", ".join(set(map(lambda po: str(po[cls.get_i(cls.PO_NAME, "PURCHASEORDERNUMBER")]), pos)))
                )
                verdict = False
                errors_group.append(cls.INVALID_COMMON_PRICE_MESSAGE.format(**kwargs))
            
            for po in pos:
                quantity = po[cls.get_i(cls.PO_NAME, "ORDEREDPURCHASEQUANTITY")]
                unitprice = po[cls.get_i(cls.PO_NAME, "PURCHASEPRICE")]
                line_amount = po[cls.get_i(cls.PO_NAME, "LINEAMOUNT")]

                if round(quantity * unitprice, cls.ROUND_DIGITS) != round(line_amount, cls.ROUND_DIGITS):
                    kwargs = dict(
                        id = po[cls.get_i(cls.PO_NAME, "PURCHASEORDERNUMBER")],
                        line = po[cls.get_i(cls.PO_NAME, "LINENUMBER")]
                    )
                    verdict = False
                    errors_group.append(cls.INVALID_LINE_AMOUNT_MESSAGE.format(**kwargs))
            
            errors += errors_group

        if verdict is True:
            return verdict, []
        return verdict, errors

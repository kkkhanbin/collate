from flask_wtf.file import FileAllowed
from wtforms import SubmitField, MultipleFileField

from forms.form import Form


class DocumentsUpload(Form):
    invoice = MultipleFileField(
        'Выбрать документы "ЭСФ"', 
        validators=[FileAllowed(["xlsx"], "Разрешено использовать формат файла xlsx")],
    )
    purchase_order = MultipleFileField(
        'Выбрать документы "Заказ на Покупку"', 
        validators=[FileAllowed(["xlsx"], "Разрешено использовать формат файла xlsx")])
    submit = SubmitField("Отправить на сверку")

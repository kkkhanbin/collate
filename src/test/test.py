import os
import sys
sys.path.append(os.path.abspath('../..'))

from dotenv import load_dotenv
load_dotenv('../.env')

from src.parsers import ExcelParser
from src.data import connection

FILEPATH = "input.xlsx"
SHEET_NAME = "Invoice"

parser = ExcelParser(FILEPATH)
dataframe = parser.parse(sheet_name=SHEET_NAME)

for row in dataframe.values:
    print(row)

print(", ".join(dataframe.columns))

cc = connection.cursor()


# cc.executemany('''
# INSERT INTO Invoices_test ()
# ''')
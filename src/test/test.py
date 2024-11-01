import os
import sys
sys.path.append(os.path.abspath('../..'))

from dotenv import load_dotenv
load_dotenv('../.env')

from src.parsers import ExcelParser
from src.data import connection

# Parsing xlsx file
FILEPATH = "input.xlsx"
SHEET_NAME = "Invoice"

parser = ExcelParser(FILEPATH)
df = parser.parse(sheet_name=SHEET_NAME)

# Sending data to the DB
cc = connection.cursor()
columns = ", ".join(df.columns)
cc.executemany(f"INSERT INTO Invoices_test({columns}) VALUES(?, ?, ?, ?)", [value for value in df.values])
cc.close()

import pandas as pd

from src.config import default


class ExcelParser:
    def __init__(self, path: str):
        self.path = path

    def parse(self, sheet_name: str = None) -> pd.DataFrame:
        dataframe = pd.read_excel(self.path, header=0, sheet_name=default(sheet_name))

        return dataframe

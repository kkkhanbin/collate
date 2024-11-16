import pandas as pd


class ExcelParser:
    @classmethod
    def parse(self, data) -> pd.DataFrame:
        dataframe = pd.read_excel(data)
        return dataframe

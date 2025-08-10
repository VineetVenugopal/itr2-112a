from record.record_builder import RecordBuilder


import pandas as pd


from functools import cache

from record.record import Record


class KFinExcelToRecordConverter:
    """
    TODO: This is incomplete.
    """

    C1 = 'Fund'
    C2 = 'Fund Name'
    C3 = 'Folio Number'
    C4 = 'Scheme Name'
    C5 = 'Purchase.Trxn.Type'
    C6 = 'Purchase.Date'
    C7 = 'Purchase.Current Units'
    C8 = 'Purchase.Source Scheme units'
    C9 = 'Purchase.Original Purchase Cost'
    C10 = 'Purchase.Original Cost Amount	'
    C11 = 'Purchase.Grandfathered NAV as on 31/01/2018'
    C12 = 'Purchase.GrandFathered NAV Cost Value'
    C13 = 'Purchase.IT Applicable NAV'
    C14 = 'Purchase.IT Applicable Cost Value'
    C15 = 'Redemption.Trxn.Type'
    C16 = 'Redemption.Date'
    C17 = 'Redemption.Units'
    C18 = 'Redemption.Amount'
    C19 = 'Redemption.Price'
    C20 = 'Redemption.Tax Perc'
    C21 = 'Redemption.Tax'
    C22 = 'Short Term'
    C23 = 'Indexed Cost'
    C24 = 'Long Term With Index'
    C25 = 'Long Term Without Index'

    columns = [
        C1, C2, C3, C4, C5, C6,
        C7, C8, C9, C10, C11, C12, C13, C14,
        C15, C16, C17, C18, C19, C20, C21,
        C22, C23, C24, C25
    ]

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _convert_to_record(self, row_dict: dict) -> Record:
        record = Record(row_dict)

        builder = RecordBuilder()
        builder.purchase_date(pd.to_datetime(row_dict[self.C6]).date()) \
            .transfer_date(pd.to_datetime(row_dict[self.C16]).date()) \
            .isin_code(row_dict[self.C1]) \
            .name(row_dict[self.C2]) \
            .no_of_shares(row_dict[self.C7]) \
            .sale_price_per_share(row_dict[self.C19]) \
            .expenditure_wholly_exclusively(0).build()


        return record

    @cache
    def convert(self):
        for _, row in self.df.iterrows():
            record = self._convert_to_record(row.to_dict())
            self.records.append(record)
        return self.records

    @staticmethod
    def read_excel(filename: str, **kwargs) -> pd.DataFrame:
        df = pd.read_excel(filename, sheet_name='Sheet1', skiprows=40)
        print(df.head())
        df.columns = KFinExcelToRecordConverter.columns
        print(df.columns)


K_FIN_EXCEL_FILE = r'KFintech_FY_24-25_CG_Stmt.xlsx'
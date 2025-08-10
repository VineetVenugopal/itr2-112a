import json
from record import write_to_csv_file
from record.record_builder import RecordBuilder


import pandas as pd


import math
from functools import cache

from record.record import Record


class IciciDirectExcelToRecordConverter:

    C1 = "Serial No."
    C2 = "Category"
    C3 = "Sub-category"
    C4 = "AMC"
    C5 = "Scheme Name"
    C6 = "Matched qty"
    C7 = "Purchase Transaction Type"
    C8 = "Purchase NAV Date"
    C9 = "Purchase NAV"
    C10 = "Purchase Value"
    C11 = "Purchase Grandfathered Value"
    C12 = "Purchase Indexed Value"
    C13 = "Purchase Channel"
    C14 = "Redemption Transaction Type"
    C15 = "Redemption NAV Date"
    C16_red_nav = "Redemption NAV"
    C17 = "Redemption Value"
    C18 = "Redemption Channel"
    C19_stcg = "Short Term Gain"
    C20 = "NAV (per unit) on 31-Jan-2018"
    C21 = "Purchase NAV considered"
    C22 = "Long Term Gain Absolute"
    C23 = "Long Term Gain Indexed"
    C24 = "AMFI Code"
    C25 = "ISIN Code"

    columns = [C1, C2, C3, C4, C5, C6,
               C7, C8, C9, C10, C11, C12,
               C13, C14, C15, C16_red_nav, C17, C18,
               C19_stcg, C20, C21, C22, C23, C24,
               C25]

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.records = []

    def _convert_to_record(self, row_dict: dict) -> Record:
        builder = RecordBuilder()

        record = builder.purchase_date(pd.to_datetime(row_dict[self.C8]).date()) \
            .transfer_date(pd.to_datetime(row_dict[self.C15]).date()) \
            .isin_code(row_dict[self.C25]) \
            .name(row_dict[self.C5]) \
            .no_of_shares(row_dict[self.C6]) \
            .purchase_nav(row_dict[self.C9]) \
            .sale_price_per_share(row_dict[self.C16_red_nav]) \
            .nav_as_of_31Jan2018(row_dict[self.C20]) \
            .expenditure_wholly_exclusively(0).build()
        return record

    @property
    def filters(self):
        """List of filters to apply on the rows."""
        return [self._check_stcg_zero]

    @cache
    def convert(self):
        counter = 0

        dropped_rows = []
        for _, row in self.df.iterrows():
            try:
                counter += 1
                row['__1_index__'] = counter

                if not all([fn(row) for fn in self.filters]):
                    dropped_rows.append(counter)
                    print(f"Dropped row {counter}")
                    continue # Skip rows that do not meet the criteria

                record = self._convert_to_record(row.to_dict())
                self.records.append(record)
            except Exception as e:
                print(row)
                raise e
        return self.records, dropped_rows

    def _check_stcg_zero(self, row_dict: dict) -> bool:
        """Check if STCG is zero."""

        stcg = row_dict[self.C19_stcg]
        return stcg is None or math.isclose(stcg, 0)

    @staticmethod
    def read_excel(filename: str, sheet_name) -> pd.DataFrame:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        print(df.head())

        print(df[IciciDirectExcelToRecordConverter.C19_stcg])
        # df.columns = KFinExcelToRecordConverter.columns
        print(df.columns)
        return df


def execute():
    ICICISEC_EXCEL_FILE = r'ICICI_DIRECT_FY24-25_CG-MF.xlsx'
    df = IciciDirectExcelToRecordConverter.read_excel(ICICISEC_EXCEL_FILE, 'Transactions_formatted')
    converter = IciciDirectExcelToRecordConverter(df)
    records, dropped_rows = converter.convert()
    write_to_csv_file('icici_sec_itr_output.csv', records)

    with open('icici_sec_itr_dropped.json', 'w') as f:
        json.dump(dropped_rows, f, indent=4)

    # for record in records:
    #     print(record.to_string())
    print(sum([x[Record.C14] for x in records]))



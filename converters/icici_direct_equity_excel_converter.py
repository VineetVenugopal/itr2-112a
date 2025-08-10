
from functools import cache
import json
import pandas as pd

from record import write_to_csv_file
from record.record import Record
from record.record_builder import RecordBuilder


class IciciDirectEquityLTCGExcelConverter:

    C1 = "Stock Symbol"
    C2 = "ISIN"
    C3 = "Qty"
    C4 = "Sale Date"
    C5 = "Sale Rate"
    C6 = "Sale Value"
    C7 = "Sale Expenses"
    C8 = "Purchase Date"
    C9 = "Purchase Rate"
    C10 = "Price as on 31st Jan 2018"
    C11 = "Purchase Price Considered"
    C12 = "Purchase Value"
    C13 = "Purchase Expenses"
    C14 = "Profit/Loss(-)"

    columns = [C1, C2, C3, C4, C5, C6,
               C7, C8, C9, C10, C11, C12,
               C13, C14]

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.records = []

    def _convert_to_record(self, row_dict: dict) -> Record:
        builder = RecordBuilder()

        total_expenses = row_dict[self.C7] + row_dict[self.C13]
        
        record = builder.purchase_date(pd.to_datetime(row_dict[self.C8]).date()) \
            .transfer_date(pd.to_datetime(row_dict[self.C4]).date()) \
            .isin_code(row_dict[self.C2]) \
            .name(row_dict[self.C1]) \
            .no_of_shares(row_dict[self.C3]) \
            .purchase_nav(row_dict[self.C9]) \
            .sale_price_per_share(row_dict[self.C5]) \
            .nav_as_of_31Jan2018(row_dict[self.C10]) \
            .expenditure_wholly_exclusively(total_expenses).build()
        return record

    @property
    def filters(self):
        """List of filters to apply on the rows."""
        return []

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


def execute():
    file_name = r'files/ICICI_DIRECT_EQ_CAPITALGAIN_24-25_ORIGLNAL.xlsx'    
    df = pd.read_excel(file_name, sheet_name='Formatted_LTCG')

    # for i, col in enumerate(df.columns):
    #     print(f'C{i+1} = "{col}"')

    converter = IciciDirectEquityLTCGExcelConverter(df)
    records, dropped_rows = converter.convert()
    print(f"Total records: {len(records)}")
    write_to_csv_file('icici_sec_eq_ltcg_itr_output.csv', records)

    print(sum([
        r[Record.C14] for r in records 
    ]))
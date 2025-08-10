from datetime import date

from converters import ModuleExecutors
from record import write_to_csv_file
from record.record_builder import RecordBuilder


"""
# USAGE 

def trial():
    builder = RecordBuilder()
    record = (builder.purchase_date(date(2018, 5, 1))
              .transfer_date(date(2019, 3, 1))
              .isin_code("INF740K01029")
              .name("DSP Flexi Cap Fund - Regular Plan - IDCW")
              .no_of_shares(26.506)
              .sale_price_per_share(62.623)
              .nav_as_of_31Jan2018(62.623)
              .expenditure_wholly_exclusively(0)
              .build())

    write_to_csv_file(records=[record])
"""


if __name__ == "__main__":
    ModuleExecutors.execute(ModuleExecutors.ICICI_DIRECT_EQUITY_LTCG_EXCEL)
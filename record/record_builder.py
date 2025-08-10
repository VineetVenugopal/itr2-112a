from record.record import Record


from datetime import date


class RecordBuilder:
    """
    A builder class to construct a Record for Schedule 112A.
    This class provides methods to set various fields of the record.
    It encapsulates the logic to calculate derived fields based on the inputs.

    Usage:

    ```python
    from datetime import date
    from record.record_builder import RecordBuilder
    from record import write_to_csv_file

    builder = RecordBuilder()
    
    record = (builder.purchase_date(date(2018, 5, 1))
              .transfer_date(date(2019, 3, 1))
              .isin_code("INF740K01029")
              .name("DSP Flexi Cap Fund - Regular Plan - IDCW")
              .no_of_shares(26.506)
              .purchase_nav(62.623)
              .sale_price_per_share(62.623)
              .nav_as_of_31Jan2018(62.623)
              .expenditure_wholly_exclusively(0)
              .build())

    write_to_csv_file(records=[record])
    ```
    """

    def __init__(self):
        self.record = Record()
        self._purchase_nav = 0
        self._nav_asof_31Jan_2018 = 0.0


    def purchase_nav(self, nav: float):
        """Set the purchase NAV."""
        self._purchase_nav = nav
        return self

    def purchase_date(self, d: date):
        self.record['___purchase_date___'] = d
        if d > date(2018, 1, 31):
            val = 'AE'
        else:
            val = 'BE'
        self.record[Record.C1_a] = val
        return self

    def transfer_date(self, d: date):
        self.record['___transfer_date___'] = d
        if d > date(2024, 7, 23):
            val = 'AE'
        else:
            val = 'BE'
        self.record[Record.C1_b] = val
        return self

    def isin_code(self, code: str):
        val = code if not self.record.purchased_after_epoch else 'INNOTREQUIRD'

        self.record[Record.C2] = val
        return self

    def name(self, name: str):
        name = name if not self.record.purchased_after_epoch else 'CONSOLIDATED'
        self.record[Record.C3] = name
        return self

    def no_of_shares(self, no: float):
        self.record[Record.C4] = float(no)
        return self

    def sale_price_per_share(self, price: float):
        """"Sale price in the context of shares. NAV in the context of MFs."""
        self.record[Record.C5] = float(price)
        return self

    def nav_as_of_31Jan2018(self, value: float):
        """
        nav in the context of MFs. Sale price in the context of shares.
        """
        if not isinstance(value, float):
            raise ValueError("NAV as of 31-Jan-2018 must be a float.")
        self._nav_asof_31Jan_2018 = value
        if self.record.purchased_after_epoch:
            self.record[Record.C10] = ''
        else:
            self.record[Record.C10] = float(value)
        return self

    def expenditure_wholly_exclusively(self, expenditure: float):
        self.record[Record.C12] = expenditure
        return self

    def _calculate_total_fair_market_value(self):
        """Calculate the total fair market value based on purchase date."""
        qty = self.record.get(Record.C4, 0.0)
        fmv = self._nav_asof_31Jan_2018
        
        if self.record.purchased_after_epoch:
            return ''
        else:
            return qty * fmv

    def _getf(self, col:str):
        """Helper function to get value from record."""
        return self.record.get(col, 0.0) if col in self.record else 0.0

    def _calculate_cost_of_acquisition(self):
        """Calculate the cost of acquisition based on purchase date."""
        qty = self._getf(Record.C4)
        if self.record.purchased_after_epoch:
            return self._purchase_nav * qty
        else:
            return self._calculate_total_fair_market_value()
        # return self._purchase_nav * self._getf(Record.C4)

    def build(self):
        self.record[Record.C8] = round(self._calculate_cost_of_acquisition(), 4)
        self.record[Record.C6] = round(self._getf(Record.C4) * self._getf(Record.C5), 4)

        self.record[Record.C11] = self._calculate_total_fair_market_value()

        if self.record.purchased_after_epoch:
            pass
        else:
            self.record[Record.C9] = round(min(self._getf(Record.C6), self._getf(Record.C11)), 4)

        self.record[Record.C7] = round(max(self._getf(Record.C8), self._getf(Record.C9)))
        self.record[Record.C13] = round(self._getf(Record.C7) + self._getf(Record.C12))

        theoretical_ltcg = round(self._getf(Record.C6) - self._getf(Record.C13))
        if not self.record.purchased_after_epoch and theoretical_ltcg < 0:
            effective_ltcg = theoretical_ltcg
        else:
            effective_ltcg = theoretical_ltcg

        self.record[Record.C14] = effective_ltcg

        return self.record
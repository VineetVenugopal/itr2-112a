import json


class Record(dict):
    C1_a = "Share/Unit acquired(1a)"
    C1_b = "Share/Unit Transferred(1b)"
    C2 = "ISIN Code(2)"
    C3 = "Name of the Share/Unit(3)"
    C4 = "No. of Shares/Units(4)"
    C5 = "Sale-price per Share/Unit(5)"
    C6 = "Full Value of Consideration(Total Sale Value)(6) = 4 * 5"
    C7 = "Cost of acquisition without indexation(7)"
    C8 = "Cost of acquisition(8)"
    C9 = "If the long term capital asset was acquired before 01.02.2018(9)"
    C10 = "Fair Market Value per share/unit as on 31st January,2018(10)"
    # Important note: As of 30-Jul-2025, the fair market value per share/unit header name provided in the template is wrong. 
    # Provided header is "Fair Market Value per share/unit as on 31st January 2018(10)"
    # Reference: https://freefincal.com/how-to-upload-equity-mf-share-ltcg-transactions-in-itr2-itr3-schedule-112a/#:~:text=If%20you%20have%20several%20LTCG%20entries%20%28regardless%20of,these%20are%20labelled%20as%20%281a%29%2C%20%282%29%2C%20%E2%80%A6%20%2814%29.
    # and https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Ffreefincal.com%2Fwp-content%2Fuploads%2F2023%2F06%2FSchedule-112A-Instructions.xlsx&wdOrigin=BROWSELINK

    C11 = "Total Fair Market Value of capital asset as per section 55(2)(ac)(11) = 4 * 10"
    C12 = "Expenditure wholly and exclusively in connection with transfer(12)"
    C13 = "Total deductions(13) = 7 + 12"
    C14 = "Balance(14) = 6 - 13"

    columns = [
        C1_a, C1_b, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14
    ]

    @property
    def purchased_after_epoch(self) -> bool:
        """Check if the purchase date is after 31st January 2018."""
        c1_a = self.get(self.C1_a)
        if not c1_a:
            raise Exception("Purchase date (C1_a) is not set in the record.")
        return c1_a == 'AE'

    def to_string(self):
        return json.dumps(self, indent=4, default=str)
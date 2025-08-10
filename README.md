# itr2-112a

## Introduction

For those trying to file income tax returns (ITR-2) themselves, reporting long term capital gains (LTCG) in Schedule 112A is painstaking (atleast as of AY 2025-26). 

Uploading the mutual funds and shares capital gains reports from various platform to generate the CSV for bulk upload is a lot of manual effort. Adding to that, there are some serious usability issues with the bulk upload feature. For one the [template provided](_template.csv) has some typos that make it unusable by default.

This python utility tries to solve this problem for those who file ITRs themselves. 

## Directory Structure
This utility is structured to allow easy modification and extension.
The main components of the utility are organized into directories:

```
.
├── record
│   ├── __init__.py
│   └── record_builder.py
└── main.py
```
The `record` directory contains the logic to build the records for Schedule 112A. It is here that the ITR2-112a logic is encapsulated. There is room for improvement/bugfixes. 

The `converters` directory contains the logic to convert the input files from various platforms to the required format. These converters are NOT to be used blindly. Create or modify the converters as per your requirements. Treat these converters as examples to create your own converters.

The `main.py` file is the entry point. It calls one of the converters to read the input files, build the records and write the output to a CSV file.

## Usage

```python
from datetime import date
from record.record_builder import RecordBuilder, Record
from record import write_to_csv_file

builder = RecordBuilder()

record: Record = builder.purchase_date(date(2018, 5, 1))
            .transfer_date(date(2019, 3, 1))
            .isin_code("INF740K01029")
            .name("DSP Flexi Cap Fund - Regular Plan - IDCW")
            .no_of_shares(26.506)
            .purchase_nav(62.623)
            .sale_price_per_share(62.623)
            .nav_as_of_31Jan2018(62.623)
            .expenditure_wholly_exclusively(0)
            .build()

write_to_csv_file(records=[record], filename='result.csv')
```

### Converters
The `converters` module might use `pandas` to read from excel files. For that, install dependency with the below command:

```bash
pip install -r requirements.txt
```

Example on how the converters have been wired up:
```python
from converters import ModuleExecutors

ModuleExecutors.execute(ModuleExecutors.ICICI_DIRECT_EQUITY_LTCG_EXCEL)
```

## Sources
[Freefincal](https://freefincal.com/how-to-upload-equity-mf-share-ltcg-transactions-in-itr2-itr3-schedule-112a/#:~:text=If%20you%20have%20several%20LTCG%20entries%20%28regardless%20of,these%20are%20labelled%20as%20%281a%29%2C%20%282%29%2C%20%E2%80%A6%20%2814%29.)
has provided a detailed guide on how to upload equity and mutual fund share LTCG transactions in ITR2/ITR3 Schedule 112A. You can find the guide [here](https://freefincal.com/how-to-upload-equity-mf-share-ltcg-transactions-in-itr2-itr3-schedule-112a/).

The order of columns in the CSV file is important. The utility will generate the CSV file with the correct order of columns as per the requirements of Schedule 112A as described in the [Freefincal guide](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Ffreefincal.com%2Fwp-content%2Fuploads%2F2023%2F06%2FSchedule-112A-Instructions.xlsx&wdOrigin=BROWSELINK).

## Contributions
This utility is open source and contributions are welcome.
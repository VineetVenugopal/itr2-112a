# itr2-112a

## Introduction
Hi there, 

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
First install dependencies using pip:

```bash
pip install -r requirements.txt
```

To run the utility, you can use the following command:

```bash
python main.py
```

## Sources
[Freefincal](https://freefincal.com/how-to-upload-equity-mf-share-ltcg-transactions-in-itr2-itr3-schedule-112a/#:~:text=If%20you%20have%20several%20LTCG%20entries%20%28regardless%20of,these%20are%20labelled%20as%20%281a%29%2C%20%282%29%2C%20%E2%80%A6%20%2814%29.)
has provided a detailed guide on how to upload equity and mutual fund share LTCG transactions in ITR2/ITR3 Schedule 112A. You can find the guide [here](https://freefincal.com/how-to-upload-equity-mf-share-ltcg-transactions-in-itr2-itr3-schedule-112a/).

The order of columns in the CSV file is important. The utility will generate the CSV file with the correct order of columns as per the requirements of Schedule 112A as described in the [Freefincal guide](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Ffreefincal.com%2Fwp-content%2Fuploads%2F2023%2F06%2FSchedule-112A-Instructions.xlsx&wdOrigin=BROWSELINK).

## Contributions
This utility is open source and contributions are welcome.
from record.record import Record


import csv


def write_to_csv_file(filename = 'result.csv', records = None):

    with open(filename, 'w', newline='') as csvfile:

        header = ['"{}"'.format(c) for c in Record.columns]
        csvfile.write(','.join(header) + '\n')
        # Doing this because there is a comma in one of the headers. The csv writer will not handle it correctly.

        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_NONE, escapechar='\\')


        # spamwriter.writerow([f'"{c}"' for c in Record.columns])

        if records is not None:
            for record in records:
                spamwriter.writerow([record.get(col, '') for col in Record.columns])
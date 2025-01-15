import json
import csv
import openpyxl

def clean_json_string(json_string):
    """
    Removes triple quotes from the beginning and end of a JSON string.

    Args:
        json_string: The JSON string with triple quotes.

    Returns:
        The cleaned JSON string without triple quotes.
    """
    if json_string.startswith("\"\"\"") and json_string.endswith("\"\"\""):
        return json_string[3:-3]
    else:
        return json_string

def json_to_csv(json_data, csv_file):
    """
    Converts JSON data to CSV format.

    Args:
        json_data: The JSON data to be converted.
        csv_file: The path to the output CSV file.
    """
    json_data = json.loads(json_data)
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['shop', 'item', 'quantity', 'price', 'currency' ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for receipt in json_data.get('receipts', []):
            for item in receipt.get('items', []):
                writer.writerow({
                    'shop': receipt.get('shop', ''),
                    'item': item.get('item', ''),
                    'quantity': item.get('quantity', 1),
                    'price': item.get('price', 0),
                    'currency': receipt.get('currency', ''),
                    # 'total': receipt.get('total', 0)
                })

def json_to_xls(json_data, xls_file):
    """
    Converts JSON data to XLSX format.

    Args:
        json_data: The JSON data to be converted.
        xls_file: The path to the output XLSX file.
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    json_data = json.loads(json_data)
    sheet.append(['shop', 'item', 'quantity', 'price', 'currency'])

    for receipt in json_data.get('receipts', []):
        for item in receipt.get('items', []):
            sheet.append([
                receipt.get('shop', ''),
                item.get('item', ''),
                item.get('quantity', 1),
                item.get('price', 0),
                receipt.get('currency', ''),
                # receipt.get('total', 0)
            ])

    workbook.save(xls_file)

# Example usage

import base64

def get_table_download_link(df_buffer, filename):
    """
    Generates a download link for a Pandas DataFrame.

    Args:
        df_buffer: A Pandas DataFrame buffer containing the data.
        filename: The desired filename for the downloaded file.

    Returns:
        A string containing the HTML code for the download link.
    """

    csv = df_buffer.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"data:application/octet-stream;base64,{b64}"
    return f'<a href="{href}" download="{filename}">Download CSV</a>'
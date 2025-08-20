import gspread, sys
from datetime import datetime

def parse_date(displayed_date):
    return datetime.strptime(displayed_date, "%d.%m.%Y").strftime("%Y-%m-%d")

def get_google_sheet_id(file_name):
    return next((line.strip() for line in open(file_name) if line.strip()), None)

def open_sheet(gsheet, spreadsheet_id, sheet_name):
    spreadsheet = gsheet.open_by_key(spreadsheet_id)
    for s in spreadsheet.worksheets():
        if sheet_name == s.title:
            return s
    print(f'Error opening sheet "{sheet_name}" in table "{spreadsheet_id}"')
    exit()

def update_google_sheet(sheet, table):
    table = [row for row in sheet.get_all_values() if row[0]]
    return table

def clear_and_append(sheet, table):
    column_a = sheet.col_values(1) or []
    target_date = table[0][0]
    rows_to_delete = [i + 1 for i, value in enumerate(column_a) if value == target_date]
    for i in reversed(rows_to_delete):
        sheet.delete_rows(i)
    sheet.add_rows(len(table))
    sheet.append_rows(table, value_input_option="USER_ENTERED")


def extend_formula(sheet, column_letter, formula_template):
    last_row = len(sheet.col_values(1))
    updates = []

    for i in range(1, last_row + 1):
        formula = formula_template.format(i=i)
        updates.append([formula])
    sheet.update(updates, f"{column_letter}1:{column_letter}{last_row}", value_input_option="USER_ENTERED")


displayed_date = sys.argv[1]
date_object = parse_date(displayed_date)
Gsheet = gspread.service_account(filename='sheet_ids/credentials.json')

CurrentStatid = get_google_sheet_id('sheet_ids/stat-gsheet-id')
CopyC32teasersid = get_google_sheet_id('sheet_ids/CopyTeasers-gsheet-id')
C32teasersid = get_google_sheet_id('sheet_ids/Teasers-gsheet-id')
sheet = open_sheet(Gsheet, CurrentStatid, 'For C32 teasers')
sheet.update_cell(1, 8, displayed_date)
table = update_google_sheet(open_sheet(Gsheet, CurrentStatid, 'output'), [])
sheet = open_sheet(Gsheet, CopyC32teasersid, 'Лист1')
clear_and_append(sheet, table)

for row in table:
    if len(row) > 2:
        row[2] = ''

sheet = open_sheet(Gsheet, C32teasersid, 'Лист1')
clear_and_append(sheet, table)
extend_formula(sheet, 'G', '=СЦЕПИТЬ(ТЕКСТ(A{i};"dd.mm.yyyy")&D{i})')

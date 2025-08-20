import gspread
import sys
from PharseStatKadam import KadamOutput
from PhasreStatTor import TorOutput
# При добавлении новой сети, импортируем вывод данных сюда и объеднияем в OutputData
def get_google_sheet_id(file_name):
    return next((line.strip() for line in open(file_name) if line.strip()), None)

def open_sheet(gsheet, spreadsheet_id, sheet_name):
    spreadsheet = gsheet.open_by_key(spreadsheet_id)
    for s in spreadsheet.worksheets():
        if sheet_name == s.title:
            return s
    print(f'Error opening sheet "{sheet_name}" in table "{spreadsheet_id}"')
    exit()

def clear_and_append(sheet, table):
    column_a = sheet.col_values(1) or []
    target_date = table[0][0]
    exchange = sys.argv[2] if len(sys.argv) > 2 else exit("Не введен курс доллара")
    rows_to_delete = [i + 1 for i, value in enumerate(column_a) if value == target_date]
    for i in reversed(rows_to_delete):
        sheet.delete_rows(i)
    sheet.add_rows(len(table))
    sheet.append_rows(table, value_input_option="USER_ENTERED")
    last_row = len(sheet.col_values(1))
    for i in range(last_row - len(table) + 1, last_row + 1):
        sheet.update([[exchange]],                f"K{i}", value_input_option="USER_ENTERED")
        sheet.update([[f"=G{i}*K{i}"]],           f"H{i}", value_input_option="USER_ENTERED")
        sheet.update([[f"=ОКРУГЛ(G{i}/F{i};2)"]], f"I{i}", value_input_option="USER_ENTERED")
        sheet.update([[f"=F{i}/E{i}"]],           f"J{i}", value_input_option="USER_ENTERED")


if __name__ == "__main__":
    Gsheet = gspread.service_account(filename='sheet_ids/credentials.json')
    OutputData = TorOutput + KadamOutput
    CurrentStatid = get_google_sheet_id('sheet_ids/stat-gsheet-id')
    sheet = open_sheet(Gsheet, CurrentStatid, 'Stat')
    clear_and_append(sheet, OutputData)


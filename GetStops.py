from tg_bot import ChatAnalyzer
import gspread
from Creds import TOKEN, CHAT_ID
def get_google_sheet_id(file_name):
    return next((line.strip() for line in open(file_name) if line.strip()), None)
def open_sheet(gsheet, spreadsheet_id, sheet_name):
    spreadsheet = gsheet.open_by_key(spreadsheet_id)
    for s in spreadsheet.worksheets():
        if sheet_name == s.title:
            return s
    print(f'Error opening sheet "{sheet_name}" in table "{spreadsheet_id}"')
    exit()
analyzer = ChatAnalyzer(TOKEN, CHAT_ID)
stoplist = analyzer.process_messages()
Gsheet = gspread.service_account(filename='sheet_ids/credentials.json')
Amberdataid = get_google_sheet_id('sheet_ids/Amberdata-gsheet-id')
sheet = open_sheet(Gsheet, Amberdataid, 'stop-list')
stops = set(sum(sheet.get_all_values(), []))  # Преобразуем в множество для быстрого поиска
new_stops = [word for word in stoplist if word not in stops]
if new_stops:
    sheet.append_rows([[word] for word in new_stops]) # еще нужно родлить формулы в столбце С и вставить значение
    print(f"Остановленны кампании: {new_stops}")
else:
    print("Все кампании уже есть в списке.")
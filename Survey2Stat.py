import requests, json, sys
from datetime import datetime
from Creds import mybid_key, kadam_key, rv_key
user_id = "168548"

if len(sys.argv) < 2:
    print('Usage: PharseStatKadam.py <Date (01.02.2025)>')
    exit()

date_object = datetime.strptime(sys.argv[1], "%d.%m.%Y")
Date = date_object.strftime("%Y-%m-%d")
AmHeaders ={
    'X-Auth-Token': mybid_key,
    'Content-Type': 'application/json'
}
AmParams = {
    'date_from': Date,
    'date_to': Date
}
RvHeaders ={
    'Authorization': rv_key,
    'Content-Type': 'application/json'
}
RvParams ={
    'dateFrom': Date,
    'dateTo': Date
}
KadamHeaders = {
    'Authorization': kadam_key,
    'Content-Type': 'application/json'
}
KadamParamsCampaignsGet = {
    'app_id': user_id,
    'client_id': user_id,
    'include_archive': 0,
}

RvGetStat = requests.get('http://api.rivertraffic.com/advertiser/statistics/campaign', headers=RvHeaders, params=RvParams)
AmGetStat = requests.get('http://api.mybid.io/gateway/v1/api/campaigns', headers=AmHeaders)
KadamGetCampaigns = requests.get('http://api.kadam.net/ads.campaigns.get', headers=KadamHeaders, params=KadamParamsCampaignsGet)

KadamStatusCampaigns = json.loads(KadamGetCampaigns.text)
RvStat = json.loads(RvGetStat.text)
AmStatusCampaigns = json.loads(AmGetStat.text)
Amids = [item['id'] for item in AmStatusCampaigns['data']]
Kadamids = [item['id'] for item in KadamStatusCampaigns['response']['items']]
formatted_ids = ', '.join(Kadamids)
KadamMapNamesIds = {item['id']: item['name'] for item in KadamStatusCampaigns['response']['items']}
AmMapNamesIds = {item['id']: item['name'] for item in AmStatusCampaigns['data']}
mapTypesIds = {item['id']: item['ad_format'] for item in KadamStatusCampaigns['response']['items']}
KadamParamsStatCampaign = {
        'app_id': user_id,
        'client_id': user_id,
        'campaigns': formatted_ids,
        'group': 'campaign',
        'date_from': Date,
        'date_to': Date
}
AmParamsStatCampaign= {
    "campaigns": [23484, 23480],
    "ad_types": ["popunder", "inpage"],
    "countries": ["DE", "FR"],
    "os_types": ["mobile", "computer"],
    "os_families": ["android", "ios"],
    "date_from": "2025-02-03",
    "date_to": "2025-02-03",
    "group_by": "country"
}
AmStatCampaigns = requests.get('http://api.mybid.io/gateway/v1/api/statistic', headers=AmHeaders, params=AmParamsStatCampaign)
Am = json.loads(AmStatCampaigns.text)
print(Am)
KadamStatCampaigns = requests.get('http://api.kadam.net/ads.stats.campaign.get', headers=KadamHeaders, params=KadamParamsStatCampaign)
TodayStat = json.loads(KadamStatCampaigns.text)
campaignsKadam = [
        {
            "Date": sys.argv[1],
            "id": item['id'],
            "Display": item['views'],
            "Clicks": item['clicks'],
            "Cost":item['moneyOut']
        }

        for item in TodayStat['response']['items']
    ]

#собираем данные с двух запросов и фильтруем ненужные
filters = ["Survey_2"]
filtered_campaigns = []
for campaign in campaignsKadam:
    campaign_id = str(campaign['id'])
    campaign['Campaign ID'] = KadamMapNamesIds.get(campaign_id, "Unknown")
    campaign['Network'] = "kd"
    if any(filter_word in campaign['Campaign ID'] for filter_word in filters) and campaign['Cost'] > 0: # условия на кампании из запроса
        filtered_campaigns.append(campaign)
    del campaign['id']  # Удаляем id, он больше не нужен
#маппинг по типу кампаний
type_mapping = {
    '10': "teaser",
    '20': "banner",
    '30': "push",
    '40': "Clickunder",
    '60': "context"
}
for item in filtered_campaigns:
    item['Type'] = type_mapping.get(item.get('Type', None), "Unknown")  # Replace type with type name


# задаем порядок столбцов, приводим к формату гугл таблиц
OutputData = []
# for entry in filtered_campaigns:
#     OutputData.append([
#         entry['Date'],
#         entry['Network'],
#         entry['Campaign ID'],
#         entry['Display'],
#         entry['Clicks'],
#         entry['Cost']
#     ])
#
#
# googleSheetId = os.getenv('CopyTeasers-gsheet-id')  # обновление файла stops.csv из гугла
# if not googleSheetId:
#     with open('CopyTeasers-gsheet-id') as f:
#         for line in f:
#             googleSheetId = line.strip()
#             if googleSheetId:
#                 break
#         f.close()
# Gsheet = gspread.service_account(filename='credentials.json')
# document = Gsheet.open_by_key(googleSheetId)
# sheet = None
# sheetName = 'Survey 2'
# for s in document.worksheets():
#     # выбираем первый лист; можно выбрать по имени
#     if sheetName == s.title:
#         sheet = s
#         break
# if not sheet:
#     print('Error opening sheet "{}" in table "{}"'.format(sheetName, googleSheetId))
#     exit()
# table = sheet.get_all_values()
#
# # удаляем кампании за выбранный день, чтобы избежаить переполнения
# for data_row in OutputData:
#     date_to_check = data_row[0]
#
#     rows_to_delete = []
#     for i, row in enumerate(table):
#         if row[0] == date_to_check:
#             rows_to_delete.append(i + 1)
#
#     # Удаляем строки с конца, чтобы избежать смещения индексов
#     for row_index in reversed(rows_to_delete):
#         sheet.delete_rows(row_index)
#
# for data_row in OutputData:
#     sheet.append_row(data_row)
import requests, json, sys
from datetime import datetime
from Creds import secret_key_kd, user_id_kd

displayed_date = sys.argv[1]
date_object = datetime.strptime(sys.argv[1], "%d.%m.%Y")
Date = date_object.strftime("%Y-%m-%d")

headers = {
    'Authorization': secret_key_kd,
    'Content-Type': 'application/json'
}

paramsCampaignsGet = {
    'app_id': user_id_kd,
    'client_id': user_id_kd,
    'include_archive': 0,
}

KadamGetCampaigns = requests.get('http://api.kadam.net/ads.campaigns.get', headers=headers, params=paramsCampaignsGet)

StatusCampaigns = json.loads(KadamGetCampaigns.text)
ids = [item['id'] for item in StatusCampaigns['response']['items']]
formatted_ids = ', '.join(ids)
mapNamesIds = {item['id']: item['name'] for item in StatusCampaigns['response']['items']}
mapTypesIds = {item['id']: item['ad_format'] for item in StatusCampaigns['response']['items']}
paramsStatCampaign = {
        'app_id': user_id_kd,
        'client_id': user_id_kd,
        'campaigns': formatted_ids,
        'group': 'campaign',
        'date_from': Date,
        'date_to': Date
}
KadamStatCampaigns = requests.get('http://api.kadam.net/ads.stats.campaign.get', headers=headers, params=paramsStatCampaign)
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
filters = ["лднр", "през", "днб","цгии","проч", "мат"]
filtered_campaigns = []
for campaign in campaignsKadam:
    campaign_id = str(campaign['id'])
    campaign['Campaign ID'] = mapNamesIds.get(campaign_id, "Unknown")
    campaign['Type'] = mapTypesIds.get(campaign_id, "Unknown")
    campaign['Network'] = "Kadam"
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
KadamOutput = []
for entry in filtered_campaigns:
    KadamOutput.append([
        entry['Date'],
        entry['Network'],
        entry['Type'],
        entry['Campaign ID'],
        int(entry['Display']),
        int(entry['Clicks']),
        entry['Cost']
    ])
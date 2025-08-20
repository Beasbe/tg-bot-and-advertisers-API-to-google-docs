import requests, json, sys
from datetime import datetime
from Creds import secret_key_ev

displayed_date = sys.argv[1]
date_object = datetime.strptime(sys.argv[1], "%d.%m.%Y")
Date = date_object.strftime("%Y-%m-%d")

headers = {
    'X-Api-Key': secret_key_ev,
    'Content-Type': 'application/json'
}

params = {

    'day': Date,
    'format': 'popunder'
}

EvadavGetCampaigns = requests.get('https://evadavapi.com/api/v2.2/advertiser/stats/date', headers=headers, params=params)

Stats = json.loads(EvadavGetCampaigns.text)
impressions = list(Stats['data']['stat'].values())[0]['impressions'] # Просмотры за определнный день формата кликандер



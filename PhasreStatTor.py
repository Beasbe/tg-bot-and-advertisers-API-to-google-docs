import requests, json, sys
from datetime import datetime
from Creds import Token_tor
displayesd_date = sys.argv[1]
date_object = datetime.strptime(sys.argv[1], "%d.%m.%Y")
Date = date_object.strftime("%Y-%m-%d")
TorParams = {
    'token': Token_tor,
    'adv_id': 11,
    'group': 'creative',
    'date_start': Date,
    'date_end': Date
}
TorStatRequest = requests.get('https://api.tor.energy/api/adv', params=TorParams)
TorStat = json.loads(TorStatRequest.text)
TorStatData = TorStat.get('data',[])
TorOutput = []
# Обработка данных
for item in TorStatData:
    creative_id = item['creative_id']
    roundedcost = round(item['cost'], 2)
    item['Network'] = "TOR"
    campaignid, type_ = creative_id.split('-')
    if type_ == "banner":
        type_ = "teaser"
    TorOutput.append([
        displayesd_date,
        item['Network'],
        type_,
        campaignid,
        int(item['impressions']),
        int(item['clicks']),
        roundedcost
    ])

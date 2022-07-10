import requests
import json
import pandas as pd
from requests.structures import CaseInsensitiveDict

# Getting access token
url = "https://api.dubaipulse.gov.ae/oauth/client_credential/accesstoken?grant_type=client_credentials"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
data = "client_id=123456"
resp = requests.post(url, headers=headers, data=data)
access_token = json.loads(resp.text)['access_token']

# Getting incidents data
url = "https://api.dubaipulse.gov.ae/open/dubai-police/dp_traffic_incidents-open-api?order_by=acci_time%20desc"
headers = CaseInsensitiveDict()
headers["Authorization"] = "Bearer " + access_token
resp = requests.get(url, headers=headers)
traffic_incidents = json.loads(resp.text)['results']

traffic_incidents = pd.DataFrame(traffic_incidents)

print(traffic_incidents.head())
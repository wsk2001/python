from requests import Request, Session
import json
import pprint
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'

parameters = {
    'slug' : 'tether', 
    'time_period' : 'daily',
    'time_start' : '2022-05-20',
    'convert' : 'USD'
    
    
}

headers = {
    'Accepts' : 'applications/json',
    'X-CMC_PRO_API_KEY': '408f9e2f-96b8-45fb-ae03-0cd552fda446'
}

session = Session()
session.headers.update(headers)

response = session.get(url, params = parameters)
pprint.pprint(json.loads(response.text))
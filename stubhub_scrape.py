import requests
import base64
import json
import pandas as pd
import datetime

# Enter user's API key, secret, and Stubhub login
app_token = input('Enter app token: ')
consumer_key = input('Enter consumer key: ')
consumer_secret = input('Enter consumer secret: ')
stubhub_username = input('Enter Stubhub username (email): ')
stubhub_password = input('Enter Stubhub password: ')

# Generating basic authorization token
combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo.encode('utf-8'))

# Parameters for API call
headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Authorization':'Basic '+basic_authorization_token.decode('utf-8'),}
body = {
        'grant_type':'password',
        'username':stubhub_username,
        'password':stubhub_password,
        'scope':'PRODUCTION'}

# Making the call
url = 'https://api.stubhub.com/login'
r = requests.post(url, headers=headers, data=body)
token_respoonse = r.json()
access_token = token_respoonse['access_token']
user_GUID = r.headers['X-StubHub-User-GUID']

## Searching for event IDs 
# Enter event name 
info_url= 'https://api.stubhub.com/search/catalog/events/v3/'
name = input('Enter Show name: ')
data = {'name': name, 'rows': 500}
headers['Authorization'] = 'Bearer ' + access_token
headers['Accept'] = 'application/json'
headers['Accept-Encoding'] = 'application/json'

performer_info = requests.get(info_url, headers=headers, params=data)
performer = performer_info.json()

performer_events = performer['events']

eventid_list = []
eventinfo = []
for i in performer_events:
    eventid_list.append(i['webURI'].split("/")[2])
    eventinfo.append(i['eventDateLocal'])

eventid_list = list(map(int, eventid_list))
performance_info = dict(zip(eventid_list, eventinfo))


headers['Authorization'] = 'Bearer ' + access_token
headers['Accept'] = 'application/json'
headers['Accept-Encoding'] = 'application/json'
inventory_url = 'https://api.stubhub.com/search/inventory/v2'

def get_event(eventid):
    data = {'eventid': eventid, 'rows':500}
    inventory = requests.get(inventory_url, headers=headers, params=data)
    return inventory.json()

# Concatenate output of all events
events = [get_event(eventid) for eventid in eventid_list]

listing_df = pd.DataFrame.from_dict(events)


listing_df_new = listing_df.set_index('eventId').listing.apply(pd.Series).stack().reset_index(level=-1, drop=True).reset_index()
listing_df_new = listing_df_new[0].apply(pd.Series).join(listing_df_new['eventId'])
listing_df_new['eventId'] = listing_df_new['eventId'].astype(int)
listing_df_new['performance'] = listing_df_new['eventId'].map(performance_info)


columns = ['deliveryMethodList', 'deliveryTypeList', 'dirtyTicketInd', 'isGA', 'listingAttributeCategoryList', 'listingAttributeList', 'listingId',
           'sellerOwnInd', 'splitOption', 'splitVector', 'ticketSplit', 'zoneId', 'sectionId', 'faceValue', 'sellerSectionName', 'listingPrice']
listing_df_new.drop(columns, axis=1, inplace=True)
listing_df_new['currentPrice'] = listing_df_new.apply(lambda x: x['currentPrice']['amount'], axis=1)
listing_df_new['performance'] = listing_df_new['performance'].str[:-8].str.replace('T', ' ').apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M'))

# Change file name
listing_df_new.to_csv('####.csv', index=False)

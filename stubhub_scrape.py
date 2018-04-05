import requests
import base64
import json
import pandas as pd
import datetime
import getpass

# Enter user's API key, secret, and Stubhub login
app_token = input('Enter app token: ')
consumer_key = input('Enter consumer key: ')
consumer_secret = input('Enter consumer secret: ')
stubhub_username = input('Enter Stubhub username (email): ')
stubhub_password = getpass.getpass('Enter Stubhub password: ')

#app_token = ''
#consumer_key = ''
#consumer_secret = ''
#stubhub_username = ''
#stubhub_password = ''

# Generating basic authorization token
combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo.encode('utf-8'))

# POST Parameters for API call
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

## Searching for eventids for a specific show
# Enter event name 
info_url= 'https://api.stubhub.com/search/catalog/events/v3/'
name = input('Enter Show name: ')
data = {'name': name, 'rows': 500}
headers['Authorization'] = 'Bearer ' + access_token
headers['Accept'] = 'application/json'
headers['Accept-Encoding'] = 'application/json'

# GET request 
performer_info = requests.get(info_url, headers=headers, params=data)
performer = performer_info.json()

# Getting event/performance info from json results
performer_events = performer['events']

# Appending eventid and event/performance date to a list
eventid_list = []
eventinfo = []
for i in performer_events:
    eventid_list.append(i['webURI'].split("/")[2])
    eventinfo.append(i['eventDateLocal'])

# Converting eventid objects to integers
eventid_list = list(map(int, eventid_list))
# Creating a dictionary of eventids and event/performance date with eventid as the key
performance_info = dict(zip(eventid_list, eventinfo))

## Searching inventory for an event/performance
headers['Authorization'] = 'Bearer ' + access_token
headers['Accept'] = 'application/json'
headers['Accept-Encoding'] = 'application/json'
inventory_url = 'https://api.stubhub.com/search/inventory/v2'

# Function to GET request
def get_event(eventid):
    data = {'eventid': eventid, 'rows':500}
    inventory = requests.get(inventory_url, headers=headers, params=data)
    return inventory.json()

# Looping through each eventid and concatenate output of all events
events = [get_event(eventid) for eventid in eventid_list]
# Changing to dataframe
listing_df = pd.DataFrame.from_dict(events)

# Converting the list in the "listing" column to rows
listing_df_new = listing_df.set_index('eventId').listing.apply(pd.Series).stack().reset_index(level=-1, drop=True).reset_index()
# Converting dictionary in "0" column to a dataframe
listing_df_new = listing_df_new[0].apply(pd.Series).join(listing_df_new['eventId'])
# Converting eventId to integer
listing_df_new['eventId'] = listing_df_new['eventId'].astype(int)
# Matching eventIds to add performance date to dataframe
listing_df_new['performance'] = listing_df_new['eventId'].map(performance_info)

# Dropping unnecessary columns
columns = ['businessGuid', 'deliveryMethodList', 'deliveryTypeList', 'dirtyTicketInd', 'isGA', 'listingAttributeCategoryList', 'listingAttributeList', 
           'sellerOwnInd', 'splitOption', 'splitVector', 'ticketSplit', 'zoneId', 'sectionId', 'faceValue', 'sellerSectionName']
listing_df_new.drop(columns, axis=1, inplace=True)

# Getting ticket prices out of "currentPrice" column and "listingPrice" column
listing_df_new['currentPrice'] = listing_df_new.apply(lambda x: x['currentPrice']['amount'], axis=1)
listing_df_new['listingPrice'] = listing_df_new.apply(lambda x: x['listingPrice']['amount'], axis=1)

# Converting "performance" column to dataetime
listing_df_new['performance'] = listing_df_new['performance'].str[:-8].str.replace('T', ' ').apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M'))
# Adding the date when the report was pulled
listing_df_new['datePulled'] = pd.to_datetime('today')

# Adding empty score column (only for Harry Potter)
if name == "harry potter and the cursed child new york":
    listing_df_new.insert(loc=5, column='score', value=0)
else:
    pass

# Adding vendor name
listing_df_new['vendor'] = 'StubHub'

# Export to csv (change file name: i.e. bandsvisit, comefromaway, harrypotter)
filename = input('Enter filename: ')
listing_df_new.to_csv(filename + '.csv', mode='a', index=False, header=None)
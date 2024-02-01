import requests
from config import vc_key
import csv
import pandas as pd

# https://www.visualcrossing.com/usage

def get_api_url(type, content_type, args):

    api_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/'

    while len(args) < 4:
        args.append('')
        
    type_urls = {
        'forecast': f'weatherdata/forecast?locations={args[0]},{args[1]}&forecastDays=5&includeAstronomy=true&aggregateHours=24&unitGroup=us&shortColumnNames=false&contentType={content_type}&key={vc_key}',
        'timeline': f'timeline/{args[0]},{args[1]}/{str(args[2].date())}?key={vc_key}',
        'history':f'weatherdata/history?&aggregateHours=24&startDateTime={str(args[2].date())}T{str(args[2].time())}&unitGroup=uk&contentType={content_type}&location={args[0]},{args[1]}&key={vc_key}',
        'history_summary':f'weatherdata/historysummary?aggregateHours=24&minYear={args[2]}&maxYear={args[2]}&chronoUnit=months&breakBy=self&dailySummaries=false&contentType=json&unitGroup=us&locationMode=single&key={vc_key}&locations={args[0]},{args[1]}'

    }

    return api_url + type_urls[type]

def call_data(api_url, type):
    response = requests.get(api_url)

    response.raise_for_status()  # raises exception when not a 2xx respons

    if response.status_code != 204:
        if type == 'json':
            return response.json()
        elif type == 'csv':
            return response.content.decode('utf-8')
    else:
        print(response.status_code)

def read_csv(data, idx):
    # this works if the data is one row
    csv_reader = csv.DictReader(data.splitlines(), delimiter=',')

    # Iterate over rows
    for row in csv_reader:
        weather_data = pd.DataFrame(row, index = [idx])
        
    return weather_data

def add_weather_data(df):
    # add weather data from visual crossing for data that has lat, long, data, time
    type = 'csv'
    df_weather = []
    for index, row in df.iterrows():
        # skip data that has no data in these fields
        crash = row[['Latitude','Longitude', 'Crash Date', 'Crash Time']]
        if not (crash == 'NO DATA').any():
            # get the history data url
            api_url = get_api_url('history',type, list(crash ))
            # request the api to get the data
            data = call_data(api_url, type)
            # read the returned csv, convert it to dictionary with csv_reader and return a pd dataframe
            # join the 
            df_weather.append(pd.concat([pd.DataFrame(row).T,read_csv(data, index)], axis = 1))

    return pd.concat(df_weather)

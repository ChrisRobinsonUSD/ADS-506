from datetime import date
from pandas.tseries import offsets
import datetime, pandas as pd, json, requests, ast

def get_weather_info(y_from,y_to):
    for y in range(y_from,y_to+1):
        d_from = pd.to_datetime(f'{y}-1-1').strftime("%Y-%m-%d")
        d_to = (pd.to_datetime(f'{y+1}-1-1') + datetime.timedelta(days = -1)).strftime("%Y-%m-%d")
        api_key = 'XXXXXXXXXXXXXXXXXXXX'
        URL_full = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/delhi%2C%20india/{d_from}/{d_to}?unitGroup=us&key={api_key}"
        
        try: 
            response = requests.get(URL_full)
            JSONCode = json.loads(response.text)
            with open(f'{y}.json', 'w', encoding='utf-8') as f:
                json.dump(JSONCode, f, ensure_ascii=False, indent=4)

        except:pass

def combine_json_to_df(y_from,y_to):
    df = pd.DataFrame()
    for y in range(y_from,y_to+1):
        print(y)
        with open(f'{y}.json') as json_file:
            JSONCode = json.load(json_file)
        
        WeatherInfo = str(JSONCode.get('days'))
        BreakDown = ast.literal_eval(WeatherInfo)
        
        for row in range(len(BreakDown)):
            last_row = len(df) + 1
            df.loc[last_row,'datetime'] = BreakDown[row].get('datetime')
            df.loc[last_row,'tempmax'] = BreakDown[row].get('tempmax')
            df.loc[last_row,'tempmin'] = BreakDown[row].get('tempmin')
            df.loc[last_row,'temp'] = BreakDown[row].get('temp')
            df.loc[last_row,'humidity'] = BreakDown[row].get('humidity')
            df.loc[last_row,'precip'] = BreakDown[row].get('precip')
            df.loc[last_row,'windspeed'] = BreakDown[row].get('windspeed')
            df.loc[last_row,'pressure'] = BreakDown[row].get('pressure')
            df.loc[last_row,'visibility'] = BreakDown[row].get('visibility')
            df.loc[last_row,'conditions'] = BreakDown[row].get('conditions')
            df.loc[last_row,'cloudcover'] = BreakDown[row].get('cloudcover')
            
    df.to_csv('allww.csv')


y_from = 1973
y_to = 2021

get_weather_info(y_from,y_to)
combine_json_to_df(y_from,y_to)


if __name__ == '__main__':
    y_from = 1973
    y_to = 2021

    get_weather_info(y_from,y_to)
    combine_json_to_df(y_from,y_to)
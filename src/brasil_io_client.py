import requests
import pandas as pd
from datetime import datetime, date
import numpy as np

DATA_URL = 'https://brasil.io/api/dataset/covid19/caso/data?city=Campinas'
COVID_DATA_CITY = '/home/leonardo/Projects/covid19/data/covidbr-city.csv'


def get_data(city, state, country='Brazil'):
    mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d").date()
    url = DATA_URL
    df = pd.read_csv(COVID_DATA_CITY, sep=';', parse_dates=['Date'], date_parser=mydateparser)
    while url is not None:
        resp = requests.get(url=DATA_URL, verify=False)
        data = resp.json()
        for item in data.get('results'):
            dt_str = item.get('date')
            dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
            found = False
            for d in df['Date']:
                if d.year == dt.year and d.month == dt.month and d.day == dt.day:
                    found = True
                    break
            if not found:
                confirmed = item.get('confirmed')
                deaths = item.get('deaths')

                d = {'Date': [dt], 'Confirmed': [confirmed], 'Deaths': [deaths], 'City': [city], 'State': [state],
                     'Country': country, 'Investigation': np.nan, 'Discarded': np.nan}
                aux = pd.DataFrame(d)
                df = df.append(aux)
        url = data.get('next')
    df.to_csv(COVID_DATA_CITY, sep=';', index=False)
    print('Saved new {}'.format(COVID_DATA_CITY))


def main():
    get_data(city='Campinas', state='SP')


if __name__ == '__main__':
    main()
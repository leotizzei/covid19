import requests
import pandas as pd
from datetime import datetime, date
import numpy as np

DATA_URL = 'https://brasil.io/api/dataset/covid19/caso/data'
COVID_DATA_CITY = '/home/leonardo/Projects/covid19/data/covidbr-city.csv'


def get_data(cities, country='Brazil'):
    mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d").date()
    url = DATA_URL
    df = pd.read_csv(COVID_DATA_CITY, sep=';', parse_dates=['Date'], date_parser=mydateparser)
    while url is not None:
        print('Getting data from: {}'.format(DATA_URL))
        resp = requests.get(url=url, verify=False)
        data = resp.json()
        for city, state in cities:
            print('City={} State={}'.format(city, state))
            for item in data.get('results'):
                if item.get('city') == city and item.get('state') == state:
                    dt_str = item.get('date')
                    dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
                    found = False
                    subdf = df[(df['City'] == city) & (df['State'] == state)]
                    for d in subdf['Date']:
                        if d.year == dt.year and d.month == dt.month and d.day == dt.day:
                            found = True
                            break
                    if not found:
                        confirmed = item.get('confirmed')
                        deaths = item.get('deaths')
                        assert isinstance(dt, date)
                        d = {'Date': [dt], 'Confirmed': [confirmed], 'Deaths': [deaths], 'City': [city], 'State': [state],
                             'Country': country, 'Investigation': np.nan, 'Discarded': np.nan}
                        aux = pd.DataFrame(d)
                        df = df.append(aux)
        url = data.get('next')
    df.to_csv(COVID_DATA_CITY, sep=';', index=False, date_format='%Y-%m-%d')
    print('Saved new {}'.format(COVID_DATA_CITY))


def main():
    cities_states = [('Campinas', 'SP'), ('São Paulo', 'SP'), ('Brasília', 'DF'), ('Maceió', 'AL')]
    get_data(cities=cities_states)


if __name__ == '__main__':
    main()
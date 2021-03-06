import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt

UPPER_BOUND_CASES = 999999999
LOWER_BOUND_CASES = 100
RATE_LOWER_BOUND_CASES = 100
DEATH_LIMIT=99999999
SELECTED_COUNTRIES = ['Brazil', 'Germany', 'US', 'Italy', 'Korea, South', 'Spain', 'United Kingdom']
MOST_TESTING_COUNTRIES = ['Iceland', 'Norway', 'Switzerland', 'United Arab Emirates', 'Israel', 'Estonia', 'Slovenia',
                          'Brunei']
# SELECTED_COUNTRIES = ['Brazil','Italy', 'South Korea', 'US', 'Spain']
# SELECTED_COUNTRIES = ['Brazil', 'Argentina', 'Chile', 'Venezuela']
SLASH_COUNTRY = 'Country/Region'
UNDERSCORE_COUNTRY = 'Country_Region'
PROVINCE_COL = 'Province/State'
UNDERSCORE_LAST_UPDATE = 'Last_Update'
WITHOUT_UNDERSCORE_LAST_UPDATE = 'Last Update'
CONFIRMED_CSV_FILE = '/Users/ltizzei/Projects/covid19/data/time_series_covid19_confirmed_global.csv'
DEATHS_CSV_FILE = '/Users/ltizzei/Projects/covid19/data/time_series_covid19_deaths_global.csv'
COVID_DATA_CITY = '/Users/ltizzei/Projects/covid19/data/covidbr-city.csv'
COUNTRY_COLUMN = 'Country/Region'
CONFIRMED_COLUMN = 'Confirmed'
DEATH_COLUMN = 'Deaths'


def plot_total_deaths(df):
    """

    :param df: pd.DataFrame
    :return:
    """

    countries = df[COUNTRY_COLUMN].unique()
    countries = [c for c in countries if c in SELECTED_COUNTRIES]
    num_days = list()

    country_list = list()
    num_deaths = list()
    for country in countries:
        subdf = df[df[COUNTRY_COLUMN] == country]
        subdf = subdf[subdf['Deaths'] >= 1]
        dates = subdf['date'].to_list()
        sorted_dates = sorted(dates)
        if len(sorted_dates) > 0:
            first = sorted_dates[0]
            for dt in dates:
                td = dt - first
                num_days.append(td.days)

        country_list.extend([country] * subdf.shape[0])
        num_deaths.extend(subdf['Deaths'].to_list())
    df_days = pd.DataFrame(data={'country': country_list, 'num_days': num_days,
                                 'num_deaths': num_deaths})

    g = sns.lineplot(x='num_days', y='num_deaths', hue='country', data=df_days)
    g.set(xlabel='days after 1st case', ylabel='total deaths')
    g.set_yscale("log")
    # plt.show()
    plt.tight_layout()
    plt.savefig('covid19-deaths.png', dpi=300)


def plot_total_cases(df, countries):
    """

    :param df: pd.DataFrame
    :return:
    """

    # countries = df[COUNTRY_COLUMN].unique()
    # countries = [c for c in countries if c in SELECTED_COUNTRIES]
    num_days = list()
    num_cases = list()
    country_list = list()
    num_deaths = list()
    for country in countries:

        subdf = df[df[COUNTRY_COLUMN]==country]
        subdf = subdf[(subdf[CONFIRMED_COLUMN]<=UPPER_BOUND_CASES) & (subdf[CONFIRMED_COLUMN]>=LOWER_BOUND_CASES)]
        dates = subdf['date'].to_list()
        sorted_dates = sorted(dates)
        if len(sorted_dates) > 0:
            first = sorted_dates[0]
            for dt in dates:
                td = dt - first
                num_days.append(td.days)
            num_cases.extend(subdf[CONFIRMED_COLUMN].to_list())
            country_list.extend([country] * subdf.shape[0])

    df_days = pd.DataFrame(data={CONFIRMED_COLUMN: num_cases, COUNTRY_COLUMN: country_list, 'num_days': num_days})
    g = sns.lineplot(x='num_days', y=CONFIRMED_COLUMN, hue=COUNTRY_COLUMN, data=df_days)
    g.set(xlabel='number of days', ylabel='total cases')
    g.set_yscale("log")
    plt.tight_layout()
    # plt.show()
    plt.savefig('covid19-cases.png', dpi=300)
    print('Saved covid19-cases.png')
    plt.close()


# def parse_csv(csv_dir):
#     """
#
#     :param csv_dir:
#     :return:
#     """
#     dfs = list()
#
#     for f in [c for c in os.listdir(csv_dir) if c.endswith('.csv')]:
#
#         print(f)
#
#         path = os.path.join(csv_dir, f)
#
#         aux = pd.read_csv(path)
#
#         for country in SELECTED_COUNTRIES:
#             # handling distinct column names
#             if SLASH_COUNTRY in aux.columns:
#                 aux[COUNTRY_COLUMN] = aux[SLASH_COUNTRY]
#                 aux.drop(columns=[SLASH_COUNTRY], inplace=True)
#             if WITHOUT_UNDERSCORE_LAST_UPDATE in aux.columns:
#                 aux[UNDERSCORE_LAST_UPDATE] = aux[WITHOUT_UNDERSCORE_LAST_UPDATE]
#                 aux.drop(columns=[WITHOUT_UNDERSCORE_LAST_UPDATE], inplace=True)
#             # handling distinct names for South Korea
#             aux[COUNTRY_COLUMN] = aux[COUNTRY_COLUMN].replace('Korea, South', 'South Korea')
#
#             sub = aux[aux[COUNTRY_COLUMN] == country]
#             if sub.shape[0] > 0:
#                 last_updates = sub[UNDERSCORE_LAST_UPDATE].to_list()
#                 df_group = sub.groupby(by=COUNTRY_COLUMN).sum()
#
#                 dt_str = last_updates[0]
#                 try:
#                     dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
#                 except ValueError:
#                     index = dt_str.find('/')
#                     if index > 0:
#                         month = int(dt_str[:index])
#                         new_dt_str = '{:02d}{}'.format(month, dt_str[index:])
#                         try:
#                             dt = datetime.strptime(new_dt_str, '%m/%d/%y %H:%M')
#                         except ValueError:
#                             dt = datetime.strptime(new_dt_str, '%m/%d/%Y %H:%M')
#                     else:
#                         dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
#                 s = [dt] * df_group.shape[0]
#                 country = list(df_group.index)
#                 temp_df = pd.DataFrame({'date': s, DEATH_COLUMN: df_group['Deaths'], CONFIRMED_COLUMN: df_group[CONFIRMED_COLUMN],
#                                     'Recovered': df_group['Recovered'], COUNTRY_COLUMN: country})
#                 dfs.append(temp_df)
#     df = pd.concat(dfs)
#     return df


def parse_csv_confirmed(csv_confirmed, selected_countries):
    """

    Parameters
    ----------
    csv_confirmed: str
    selected_countries: List[str]

    Returns
    -------

    """
    assert os.path.isfile(csv_confirmed), "Error! {}".format(csv_confirmed)
    csv_confirmed.endswith('.csv')

    aux = pd.read_csv(csv_confirmed)
    confirmed_list = list()
    country_list = list()
    date_list = list()
    for country in selected_countries:
        if country == 'United Kingdom':
            sub = aux[(aux[COUNTRY_COLUMN] == country) & (aux[PROVINCE_COL].isnull())]
        else:
            sub = aux[aux[COUNTRY_COLUMN] == country]  # type: pd.DataFrame
        for i in range(4, len(sub.columns)):
            column_name = sub.columns[i]
            index = column_name.find('/')
            if index > 0:
                month = int(column_name[:index])
                new_dt_str = '{:02d}{}'.format(month, column_name[index:])
                try:
                    dt = datetime.strptime(new_dt_str, '%m/%d/%y').date()
                except ValueError:
                    dt = datetime.strptime(new_dt_str, '%m/%d/%Y').date()
                print(country, column_name)
                row = sub.loc[:, column_name]
                date_list.append(dt)
                confirmed = row.to_list().pop()
                confirmed_list.append(confirmed)
                country_list.append(country)
    df = pd.DataFrame({'date': date_list, CONFIRMED_COLUMN: confirmed_list, COUNTRY_COLUMN: country_list})
    return df


def plot_br_cities(df, city):
    """

    Parameters
    ----------
    df: pd.DataFrame
    city: str

    Returns
    -------

    """
    subdf = df[df['City'] == city]
    fig = plt.figure(num=None, figsize=(15, 6), dpi=300, facecolor='w', edgecolor='k')
    sns.set_style("whitegrid")
    g = sns.lineplot(x='Date', y='Confirmed', data=subdf, marker='o')
    g = sns.lineplot(x='Date', y='Deaths', data=subdf, marker='*')
    g.set(xlabel='Date', ylabel='')
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = 'covid19-br-{}.png'.format(city)
    plt.savefig(filename, dpi=300)
    plt.close()
    print('Saved {}'.format(filename))


def plot_br(confirmed_df, deaths_df):
    """

    Parameters
    ----------
    confirmed_df: pd.DataFrame
    deaths_df: pd.DataFrame

    Returns
    -------

    """
    fig = plt.figure(num=None, figsize=(15, 6), dpi=300, facecolor='w', edgecolor='k')
    sns.set_style("whitegrid")
    subdf_confirmed = confirmed_df[confirmed_df[COUNTRY_COLUMN] == 'Brazil']
    subdf_deaths = deaths_df[deaths_df[COUNTRY_COLUMN] == 'Brazil']
    g = sns.lineplot(x='date', y='Confirmed', data=subdf_confirmed, marker='o')
    g = sns.lineplot(x='date', y='Deaths', data=subdf_deaths, marker='*')
    g.set(xlabel='date', ylabel='')
    g.set_yscale("log")
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = 'covid19-br.png'
    plt.savefig(filename, dpi=300)
    plt.close()
    print('Saved {}'.format(filename))


def parse_csv_deaths(csv_deaths, selected_countries):
    """

    Parameters
    ----------
    csv_deaths: str
    selected_countries: List[str]

    Returns
    -------

    """
    assert os.path.isfile(csv_deaths)
    csv_deaths.endswith('.csv')

    aux = pd.read_csv(csv_deaths)
    death_list = list()
    country_list = list()
    date_list = list()
    for country in selected_countries:

        if country == 'United Kingdom':
            sub = aux[(aux[COUNTRY_COLUMN] == country) & (aux[PROVINCE_COL].isnull())]
        else:
            sub = aux[aux[COUNTRY_COLUMN] == country]  # type: pd.DataFrame
        for i in range(4, len(sub.columns)):
            column_name = sub.columns[i]
            index = column_name.find('/')
            if index > 0:
                month = int(column_name[:index])
                new_dt_str = '{:02d}{}'.format(month, column_name[index:])
                try:
                    dt = datetime.strptime(new_dt_str, '%m/%d/%y').date()
                except ValueError:
                    dt = datetime.strptime(new_dt_str, '%m/%d/%Y').date()
                print(country, column_name)
                row = sub.loc[:, column_name]
                date_list.append(dt)
                deaths = row.to_list().pop()
                death_list.append(deaths)
                country_list.append(country)
    df = pd.DataFrame({'date': date_list, DEATH_COLUMN: death_list, COUNTRY_COLUMN: country_list})
    return df


def plot_cases_rate(df, countries, col_name, lower_bound):
    """

    Parameters
    ----------
    df: pd.DataFrame
    countries: List[str]
    col_name: str
    lower_bound: int

    Returns
    -------

    """
    sns.set_style("whitegrid")
    rate = list()
    country_list = list()
    num_days = list()
    avg_of_days = 5
    for country in countries:

        subdf = df[df[COUNTRY_COLUMN] == country]
        subdf = subdf[subdf[col_name] >= lower_bound]
        if subdf.shape[0] > 0:
            dates = subdf['date'].to_list()
            sorted_dates = sorted(dates)

            first = sorted_dates[0]

            subdf = subdf.sort_values(by=['date'])

            temp_rate = list()
            for i in range(1, subdf.shape[0]):
                prev_row = subdf.iloc[i-1, :]
                row = subdf.iloc[i, :]
                prev = prev_row[col_name]
                cur = row[col_name]
                new_cases = cur - prev
                if new_cases < 0:
                    new_cases = 0
                if i > 0:
                    dt = row['date']
                    delta = dt - first  # type: timedelta
                    days = delta.days
                    if days % avg_of_days == 0:
                        avg_rate = np.mean(temp_rate)
                        temp_rate = list()
                        rate.append(avg_rate)
                        country_list.append(country)
                        num_days.append(days)
                    else:
                        temp_rate.append(new_cases)

    df_rate = pd.DataFrame(data={'growth_rate': rate, 'country': country_list, 'num_days': num_days})
    g = sns.lineplot(x='num_days', y='growth_rate', hue='country', data=df_rate)
    y_label = 'avg-{}-of-{}-days-'.format(col_name, avg_of_days)
    g.set(xlabel='number of days', ylabel=y_label)
    # g.set_yscale("log")
    plt.tight_layout()
    filename = 'covid19-growth-rate-{}.png'.format(col_name)
    plt.savefig(filename, dpi=300)
    plt.close()
    print('Saved {}'.format(filename))


def plot_city_growth_rate(df, city='Campinas'):
    """

    Parameters
    ----------
    df: pd.DataFrame
    city: str

    Returns
    -------

    """
    fig = plt.figure(num=None, figsize=(15, 6), dpi=300, facecolor='w', edgecolor='k')
    sns.set_style("whitegrid")
    subdf = df[df.City == city]
    subdf = subdf.sort_values(by=['Date'])
    rate_list = list()
    num_days = list()
    prev = None
    first_day = None
    temp_rate = list()
    for index, rows in subdf.iterrows():

        cur = rows['Confirmed']
        dt = rows['Date']
        if prev is not None:
            delta = dt - first_day
            num_day = delta.days
            rate = cur - prev
            if num_day % 5 == 0:
                num_days.append(num_day)
                rate_avg = np.mean(temp_rate)
                rate_list.append(rate_avg)
                temp_rate = list()
            else:
                temp_rate.append(rate)

        else:
            first_day = dt
        prev = cur

    df_rate = pd.DataFrame(data={'growth_rate': rate_list, 'num_days': num_days})
    g = sns.barplot(x='num_days', y='growth_rate', data=df_rate)
    g.set(xlabel='number of days', ylabel='growth rate')
    plt.tight_layout()
    filename = 'covid19-city-growth-rate.png'
    plt.savefig(filename, dpi=300)
    plt.close()
    print('Saved {}'.format(filename))



def plot_lethality(confirmed_df, deaths_df):
    """

    Parameters
    ----------
    confirmed_df: pd.DataFrame
    deaths_df: pd.DataFrame

    Returns
    -------

    """
    unique_countries = confirmed_df[SLASH_COUNTRY].unique()
    lethality_list = list()
    countries = list()
    date_list = list()
    for country in unique_countries:
        cdf = confirmed_df[confirmed_df[SLASH_COUNTRY] == country]
        ddf = deaths_df[(deaths_df[SLASH_COUNTRY] == country) & (deaths_df['Deaths'] >= 1)]
        if ddf.shape[0] > 0 and cdf.shape[0] > 0 and 'date' in ddf.columns:
            date_ddf = ddf['date'].to_list()
            first_death_date = sorted(date_ddf)[0]
            print('First date {} {}'.format(first_death_date.isoformat(), country))
            for dindex, drow in ddf.iterrows():
                ddt = drow['date']
                for cindex, crow in cdf.iterrows():
                    cdt = crow['date']
                    if ddt == cdt and drow['Deaths'] > 0:
                        lethality = drow['Deaths'] / crow['Confirmed']
                        lethality_list.append(lethality)
                        countries.append(country)
                        td = ddt - first_death_date
                        date_list.append(td.days)
    df = pd.DataFrame(data={'country': countries, 'lethality': lethality_list, 'date': date_list})
    print(df.groupby('date').mean())
    g = sns.lineplot(x='date', y='lethality', hue='country', data=df)
    plt.tight_layout()
    filename = 'covid19-lethality.png'
    plt.savefig(filename, dpi=300)
    plt.close()
    print('Saved {}'.format(filename))


def parse_br_cities(csv_path):
    mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d").date()

    df = pd.read_csv(csv_path, sep=';', parse_dates=['Date'], date_parser=mydateparser)
    return df


def main():

    csv_confirmed = CONFIRMED_CSV_FILE
    selected_countries = SELECTED_COUNTRIES
    # selected_countries = ['Brazil', 'US', 'Italy', 'Spain']
    d = parse_csv_deaths(DEATHS_CSV_FILE, selected_countries)
    c = parse_csv_confirmed(csv_confirmed=csv_confirmed, selected_countries=selected_countries)
    plot_total_cases(df=c, countries=selected_countries)
    for e, col_name, lb in [(c, CONFIRMED_COLUMN, 100), (d, DEATH_COLUMN, 1)]:
        plot_cases_rate(df=e, countries=selected_countries, col_name=col_name, lower_bound=lb)
    plot_total_deaths(d)
    plot_br(confirmed_df=c, deaths_df=d)
    # plot_lethality(confirmed_df=confirmed_df, deaths_df=deaths_df)

    df = parse_br_cities(COVID_DATA_CITY)
    # for city in ['Campinas']:
    #     plot_br_cities(df)
    plot_city_growth_rate(df=df)

if __name__ == '__main__':
    # infile = '/home/leonardo/Projects/corona/src/full_data.csv'
    main()





import sqlite3
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd


# sql db not being used at the moment
# def get_data():
#     cnx = sqlite3.connect('it-job-market.db')
#     df = pd.read_sql_query("SELECT * FROM offers", cnx, dtype=
#     {'job_title': 'object', 'employer': 'object', 'min_salary': 'int64', 'max_salary': 'int64', 'price_unit': 'int64',
#      'url': 'object', 'contract_type': ' object', 'address': 'object', 'city': 'object',
#      'expiration_date': 'object', 'scraping_datetime': 'object'})
#     cnx.commit()
#     cnx.close()
#     print(df.info(verbose=True))
#     print(df.dtypes)
#     return df


def create_coordinates(main_df):
    df = main_df.copy()
    locator = Nominatim(user_agent='myGeocoder')
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    df['location'] = df['address'].apply(lambda x: geocode(x) if x not in [None, "None"] else None)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else (None, None, None))
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
    return df


def make_clickable_job_title(main_df):
    df = main_df.copy()
    clickable_job_titles = [f'<a target="_blank" href="{link}">{title}</a>'
                            for link, title in zip(df['url'], df['job_title'])]

    df['clickable_job_title'] = clickable_job_titles
    return df


def correct_wrong_min_salary(main_df):
    df = main_df.copy()

    def correct_wrong_min_salary_row(row):
        if row['min_salary'] is pd.NA:
            return row['min_salary']
        elif row['min_salary'] == 90:
            return row['min_salary'] * 160
        elif row['min_salary'] == 2600 and row['employer'] == 'TeamQuest':
            return row['min_salary'] * 10
        else:
            return row['min_salary']

    df['min_salary'] = df.apply(correct_wrong_min_salary_row, axis=1)
    return df


def correct_wrong_max_salary(main_df):
    df = main_df.copy()

    def correct_wrong_max_salary_row(row):
        if row['max_salary'] is pd.NA:
            return row['max_salary']
        elif row['max_salary'] == 125 and row['employer'] == 'Devire':
            return row['max_salary'] * 160
        elif row['max_salary'] == 150000 and row['employer'] == 'BCF Software Sp. z o.o.':
            return int(row['max_salary'] / 10)
        else:
            return row['max_salary']

    df['max_salary'] = df.apply(correct_wrong_max_salary_row, axis=1)
    return df


def drop_irrelevant_offers(main_df):
    df = main_df.copy()
    employers_to_delete = ['Pasja - Mariusz Pośnik']

    for emp in employers_to_delete:
        df = df[df['employer'] != emp]

    return df


def correct_data_types(main_df):
    df = main_df.copy()
    df.replace('None', pd.NA, inplace=True)
    df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce').round()
    df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce').round()
    df = df.astype({'max_salary': 'Int64', 'min_salary': 'Int64'})
    return df


df = pd.read_csv("raw_scraped_data.csv")


df = (df.pipe(correct_data_types)
      .pipe(correct_wrong_max_salary)
      .pipe(correct_wrong_min_salary)
      .pipe(make_clickable_job_title)
      .pipe(drop_irrelevant_offers)
      )

# df = df.pipe(make_clickable_job_title)
# df = df.pipe(create_coordinates)

df.to_csv('data-ready.csv', index=False)

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
        if row['min_salary'] == 24:
            return row['min_salary'] * 160
        elif row['min_salary'] == 90:
            return row['min_salary'] * 160
        elif row['min_salary'] == 150:
            return row['min_salary'] * 160
        elif row['min_salary'] == 320000:
            return int(row['min_salary'] / 160)
        elif row['min_salary'] == 100 and row['employer'] == 'Cyclad':
            return 13000
        else:
            return row['min_salary']

    df['min_salary'] = df.apply(correct_wrong_min_salary_row, axis=1)
    return df


def correct_wrong_max_salary(main_df):
    df = main_df.copy()

    def correct_wrong_max_salary_row(row):
        if row['max_salary'] == 26:
            return row['max_salary'] * 160
        elif row['max_salary'] == 110:
            return row['max_salary'] * 160
        elif row['max_salary'] == 200:
            return row['max_salary'] * 160
        elif row['max_salary'] == 640000:
            return int(row['max_salary'] / 160)
        else:
            return row['max_salary']

    df['max_salary'] = df.apply(correct_wrong_max_salary_row, axis=1)
    return df


def correct_data_types(main_df):
    df = main_df.copy()

    df['min_salary'] = df['min_salary'].astype(int)
    return df


df = pd.read_csv("scraped_data.csv")


# df = (df.pipe(correct_wrong_max_salary)
#       .pipe(correct_wrong_min_salary)
#       .pipe(make_clickable_job_title)
#       .pipe(correct_data_types)
#       )

df = df.pipe(make_clickable_job_title)
# df = df.pipe(create_coordinates)

df.to_csv('it-job-market-data.csv', index=False)

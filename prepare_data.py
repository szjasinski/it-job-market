import sqlite3
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd


def get_data():
    cnx = sqlite3.connect('it-job-market.db')
    df = pd.read_sql_query("SELECT * FROM offers", cnx)
    cnx.commit()
    cnx.close()
    return df


def create_coordinates(main_df):
    df = main_df.copy()
    locator = Nominatim(user_agent='myGeocoder')
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    df['location'] = df['address'].apply(lambda x: geocode(x) if x not in [None, "None"] else None)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else (None, None, None))
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
    return df


def create_middle_price(main_df):
    df = main_df.copy()

    df['middle_price'] = (df['min_salary'].astype(int) + df['max_salary'].astype(int)) / 2
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


df = get_data()
# df = pd.read_csv('it-job-market-ready.csv')


df = (df.pipe(correct_wrong_max_salary)
      .pipe(correct_wrong_min_salary)
      .pipe(make_clickable_job_title)
      .pipe(correct_data_types)
      .pipe(create_middle_price)
      )

df = df.pipe(create_coordinates)

df.to_csv('it-job-market-ready.csv', index=False)

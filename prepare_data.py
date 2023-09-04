import sqlite3
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

"""
This python file takes it-job-market.db file and calculates coordinates from address, then saves it as csv.
Output of this process is ready to be read by the app.
"""


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


df = get_data()
df = create_coordinates(df)

df.to_csv('it-job-market.csv', index=False)

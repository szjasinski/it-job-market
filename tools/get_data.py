import pandas as pd


def get_data():
    df = pd.read_csv('it-job-market-data.csv')
    df.replace('None', pd.NA, inplace=True)
    df = df.astype({'max_salary': 'Int64', 'min_salary': 'Int64'})
    return df

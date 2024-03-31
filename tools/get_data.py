import pandas as pd


def get_data():
    df = pd.read_csv('data-ready.csv')
    df = df.astype({'max_salary': 'Int64', 'min_salary': 'Int64'})
    return df

import pandas as pd
import numpy as np


def get_data():
    df = pd.read_csv('it-job-market-data.csv')
    df.replace('None', pd.NA, inplace=True)
    df['min_salary'] = df['min_salary'].apply(lambda x: round(float(x)) if x is not pd.NA else x)
    df['max_salary'] = df['max_salary'].apply(lambda x: round(float(x)) if x is not pd.NA else x)
    df = df.astype({'max_salary': 'Int64', 'min_salary': 'Int64'})
    return df

import pandas as pd


df = pd.read_csv('it-job-market.csv')


def correct_wrong_min_salary(row):
    if row['min_salary'] == 24:
        return row['min_salary']*160
    elif row['min_salary'] == 90:
        return row['min_salary']*160
    elif row['min_salary'] == 320000:
        return int(row['min_salary']/160)
    elif row['min_salary'] == 100 and row['employer'] == 'Cyclad':
        return 13000
    else:
        return row['min_salary']


def correct_wrong_max_salary(row):
    if row['max_salary'] == 26:
        return row['max_salary']*160
    elif row['max_salary'] == 110:
        return row['max_salary']*160
    elif row['max_salary'] == 640000:
        return int(row['max_salary']/160)
    else:
        return row['max_salary']


df['min_salary'] = df.apply(correct_wrong_min_salary, axis=1)
df['max_salary'] = df.apply(correct_wrong_max_salary, axis=1)

df.to_csv('it-job-market-ready.csv', index=False)


print(df.min_salary.min())
print(df.max_salary.max())

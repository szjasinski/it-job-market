import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter


@st.cache_data
def get_data_and_time():
    cnx = sqlite3.connect('it-job-market.db')
    df = pd.read_sql_query("SELECT * FROM offers", cnx)
    cnx.commit()
    cnx.close()
    return df, datetime.now()


@st.cache_data
def create_coordinates(main_df):
    df = main_df.copy()
    locator = Nominatim(user_agent='myGeocoder')
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    df['location'] = df['address'].apply(lambda x: geocode(x) if x not in [None, "None"] else None)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else (None, None, None))
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
    return df


def make_links_and_clean(main_df):
    df = main_df.copy()
    clickable_job_titles = [f'<a target="_blank" href="{link}">{title}</a>'
                            for link, title in zip(df['url'], df['job_title'])]

    df['job_title'] = clickable_job_titles
    df.drop(['url', 'price_unit'], axis=1, inplace=True)
    df.drop(['location', 'point', 'altitude', 'address', 'city'], axis=1, inplace=True)
    return df


df, timestamp = get_data_and_time()
offers_num = len(df)

df = (df.pipe(create_coordinates)
      .pipe(make_links_and_clean)
      )


# -------- SIDEBAR MENU --------
st.sidebar.title("Options")
selected_sort_by = st.sidebar.selectbox('Sort by:', ['Price From', 'Price To'])
selected_is_descending = st.sidebar.checkbox('Descending')
selected_job_title_keywords = st.sidebar.text_input('Job title contains:')
selected_company_name_keywords = st.sidebar.text_input('Company name contains: (lowercase dont work)')
selected_contract_type = st.sidebar.selectbox('Contract type:', ["All", "B2B", "employment", "mandate"])
selected_show_company_logo = st.sidebar.checkbox('Show company logos (to do)')

min_salary = df['price_from'].min()
max_salary = df['price_to'].max()
selected_salary_range = st.sidebar.slider('Select salary range (PLN gross/month)',
                                          min_salary, max_salary, (min_salary, max_salary))
clicked_reset_button = st.sidebar.button('Reset options (to do)')

st.sidebar.write("TO DO: oop app, geo data, icons, data source column, sourcing data from nofluffjobs, rocketjobs, "
                 "justjoinit, get second type of address from pracuj.pl, days to expiration, schedule, deploy...")


# -------------------------------


# sort dataframe values
def sort_df(main_df):
    df = main_df.copy()
    if selected_sort_by == 'Price To' and selected_is_descending:
        df = df.sort_values(by=['price_to'], ascending=False)
    elif selected_sort_by == 'Price From' and selected_is_descending:
        df = df.sort_values(by=['price_from'], ascending=False)
    elif selected_sort_by == 'Price To':
        df = df.sort_values(by=['price_to'])
    elif selected_sort_by == 'Price From':
        df = df.sort_values(by=['price_from'])
    return df


# filter df with job title keywords
def filter_job_title(main_df):
    df = main_df.copy()
    job_title_keywords = selected_job_title_keywords.split()
    data = pd.DataFrame()
    for keyword in job_title_keywords:
        filtered_df = df[df['job_title'].str.contains(keyword)]
        data = pd.concat([data, filtered_df])
    data.drop_duplicates()
    if job_title_keywords:
        df = data
    return df


# filter df with company name keywords
def filter_company_name(main_df):
    df = main_df.copy()
    company_name_keywords = selected_company_name_keywords.split()
    data = pd.DataFrame()
    for keyword in company_name_keywords:
        filtered_df = df[df['employer'].str.contains(keyword)]
        data = pd.concat([data, filtered_df])
    data.drop_duplicates()
    if company_name_keywords:
        df = data
    return df


# filter df with contract types
def filter_contract_type(main_df):
    df = main_df.copy()
    if selected_contract_type != "All":
        df = df[df['contract_type'].str.contains(selected_contract_type)]
    return df


# filter df for salary range
def filter_salary_range(main_df):
    df = main_df.copy()
    df = df.loc[(df['price_from'] >= selected_salary_range[0]) &
                (df['price_to'] <= selected_salary_range[1]),]
    return df


# show or dont show company logos

# reset options after button click
if clicked_reset_button:
    pass


# APPLYING OPTIONS SELECTED BY USER
df = (df.pipe(sort_df)
      .pipe(filter_job_title)
      .pipe(filter_company_name)
      .pipe(filter_contract_type)
      .pipe(filter_salary_range)
      )


table = df.copy()
table.rename(
    columns={'job_title': 'Job Title', 'employer': 'Employer', 'price_from': 'Price From', 'price_to': 'Price To',
             'contract_type': 'Contract Type'}, inplace=True)
visible_offers_num = len(table)

# DISPLAY ON MAIN PAGE
st.title('IT job offers with salary brackets (Poland)')
st.write("Number of offers:", visible_offers_num, " out of ", offers_num)
st.write(table.to_html(escape=False, index=False), unsafe_allow_html=True)


# PLOTS AND STATS
# histogram
st.subheader('Number of offers in salary brackets')
hist_values = np.histogram(df['price_to'], bins=10, range=(0, 50000))[0]
st.bar_chart(hist_values)

st.subheader('Top 5 employers with the most offers')
emp = table[['Employer', 'Job Title']].groupby(['Employer']).count().nlargest(5, 'Job Title')
emp.rename(columns={'Job Title': 'Count'}, inplace=True)
st.write(emp)

st.subheader('Percentages of offers with given contract type')

st.subheader('Most popular cities')

to_map_df = df[['latitude', 'longitude']].dropna()

st.map(to_map_df)

st.subheader('Descriptive statistics of prices')

st.write("Data last updated (read from sql db):", timestamp)

st.caption('Additional info')

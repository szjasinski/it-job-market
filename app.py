import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import seaborn as sns
import matplotlib.pyplot as plt


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


def create_days_to_expirations(main_df):
    df = main_df.copy()

    def get_days(x):
        datetime_object = datetime.strptime(x, '%d-%m-%Y').date()
        delta = datetime_object - datetime.now().date()
        return int(delta.days)

    df['days_to_expiration'] = df['expiration_date'].apply(get_days)
    df.drop(['expiration_date'], axis=1, inplace=True)
    return df


def create_middle_price(main_df):
    df = main_df.copy()

    df['middle_price'] = (df['price_to'] + df['price_from']) / 2
    return df



df, timestamp = get_data_and_time()
offers_num = len(df)

df = (df.pipe(create_coordinates)
      .pipe(make_links_and_clean)
      .pipe(create_days_to_expirations)
      .pipe(create_middle_price)
      )


# -------- SIDEBAR MENU --------
st.sidebar.title("Options")
selected_sort_by = st.sidebar.selectbox('Sort by:', ['Price From', 'Price To'])
selected_is_descending = st.sidebar.checkbox('Descending')
selected_job_title_keywords = st.sidebar.text_input('Job title contains:')
selected_company_name_keywords = st.sidebar.text_input('Company name contains: (lowercase dont work)')
selected_contract_type = st.sidebar.selectbox('Contract type:', ["All", "B2B", "employment", "mandate"])

min_salary = df['price_from'].min()
max_salary = df['price_to'].max()
selected_salary_range = st.sidebar.slider('Select salary range (PLN gross/month)',
                                          min_salary, max_salary, (min_salary, max_salary))
clicked_reset_button = st.sidebar.button('Reset options (to do)')

st.sidebar.write("TO DO: oop app, geo data, data source column, sourcing data from nofluffjobs, rocketjobs, "
                 "justjoinit, days to expiration, seaborn plots, schedule, PDF report generation, export report "
                 "button, show plots and statistics buttton,"
                 "deploy...")


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
table.drop(['latitude', 'longitude'], axis=1, inplace=True)
table.rename(
    columns={'job_title': 'Job Title', 'employer': 'Employer', 'price_from': 'Price From', 'price_to': 'Price To',
             'contract_type': 'Contract Type', 'days_to_expiration': 'Days Left'}, inplace=True)
visible_offers_num = len(table)

# DISPLAY ON MAIN PAGE
st.title('IT job offers with salary brackets (Poland)')
st.write("Number of offers:", visible_offers_num, " out of ", offers_num)
st.write(table.to_html(escape=False, index=False), unsafe_allow_html=True)


# PLOTS AND STATS

def plot_middle_price_histogram():
    fig = plt.figure(figsize=(12, 5))
    sns.histplot(data=df["middle_price"], kde=True, bins=14, binrange=(0,70000))
    st.pyplot(fig)


def plot_days_to_expiration_histogram():
    fig = plt.figure(figsize=(12, 5))
    sns.histplot(data=df["days_to_expiration"], kde=True, bins=20, binrange=(0,100))
    st.pyplot(fig)


def plot_map():
    to_map_df = df[['latitude', 'longitude']].dropna()
    st.map(to_map_df, color="#009d00", size=15000, zoom=5)


def write_employers_with_most_offers_df():
    emp = table[['Employer', 'Job Title']].groupby(['Employer']).count().nlargest(5, 'Job Title')
    emp.rename(columns={'Job Title': 'Count'}, inplace=True)
    st.write(emp)


def write_top_employers_by_middle_price_df():
    mean_middle_price_by_employer = df[['middle_price', 'employer']].groupby('employer', as_index=False).mean()
    mean_middle_price_by_employer = mean_middle_price_by_employer.reindex(columns=['middle_price', 'employer'])
    mean_middle_price_by_employer.round(1)
    st.write(mean_middle_price_by_employer.nlargest(5, 'middle_price'))

    # TO CORRECT


def plot_pie_chart():
    fig = plt.figure(figsize=(12, 5))
    data = df[['contract_type', 'employer']].groupby('contract_type', as_index=False).count()
    palette_color = sns.color_palette('deep')
    plt.pie(data['employer'], labels=data['contract_type'], colors=palette_color, autopct='%.0f%%')
    st.pyplot(fig)


st.subheader('Descriptive statistics of prices')
st.write("Median middle price:", int(df[['middle_price']].median()))

st.subheader('Number of offers in salary brackets')
plot_middle_price_histogram()

st.subheader('Days to expiration')
plot_days_to_expiration_histogram()

st.subheader('Most popular cities')
plot_map()


col1, col2 = st.columns(2)

with col1:
    st.subheader('Top 5 employers with the most offers')
    write_employers_with_most_offers_df()

with col2:
    st.subheader('Top 5 employers by mean middle price')
    write_top_employers_by_middle_price_df()

st.subheader('Percentages of offers with given contract type')
plot_pie_chart()

st.write("Data last updated (read from sql db):", timestamp)
st.caption('Additional info')

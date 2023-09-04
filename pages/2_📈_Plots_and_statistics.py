import streamlit as st
import pandas as pd
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


# ----------- PLOTS FUNCTIONS

def plot_middle_price_histogram(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    sns.histplot(data=df["middle_price"], kde=True, bins=14, binrange=(0,70000))
    st.pyplot(fig)


def plot_days_to_expiration_histogram(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    sns.histplot(data=df["days_to_expiration"], kde=True, bins=20, binrange=(0,100))
    st.pyplot(fig)


def plot_map(main_df):
    df = main_df.copy()
    to_map_df = df[['latitude', 'longitude']].dropna()
    st.map(to_map_df, color="#009d00", size=15000, zoom=5)


def write_employers_with_most_offers_df(main_df):
    df = main_df.copy()
    emp = df[['employer', 'job_title']].groupby(['employer'], as_index=False).count().nlargest(5, 'job_title')
    emp = emp.reindex(columns=['job_title', 'employer'])
    emp.rename(columns={'job_title': 'Count'}, inplace=True)
    st.write(emp.set_index('Count'))


def write_offers_with_the_highest_max_salary_df(main_df):
    df = main_df.copy()
    output_df = df[['job_title', 'price_to']].nlargest(5, 'price_to')
    # emp.rename(columns={'Job Title': 'Count'}, inplace=True)
    output_df = output_df.set_index('price_to')
    st.write(output_df)


def write_offers_with_the_lowest_min_salary_df(main_df):
    df = main_df.copy()
    output_df = df[['job_title', 'price_from']].nsmallest(5, 'price_from')
    # emp.rename(columns={'Job Title': 'Count'}, inplace=True)
    output_df = output_df.set_index('price_from')
    st.write(output_df)


def write_top_employers_by_middle_price_df(main_df):
    df = main_df.copy()
    mean_middle_price_by_employer = df[['middle_price', 'employer']].groupby('employer', as_index=False).mean()
    output_df = mean_middle_price_by_employer.reindex(columns=['middle_price', 'employer'])
    mean_middle_price_by_employer.round(1)
    output_df = output_df.nlargest(5, 'middle_price')
    output_df['middle_price'] = output_df['middle_price'].apply(lambda x: round(x, 0))
    st.write(output_df.set_index('middle_price'))

    # TO CORRECT


def plot_pie_chart(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    data = df[['contract_type', 'employer']].groupby('contract_type', as_index=False).count()
    palette_color = sns.color_palette('deep')
    plt.pie(data['employer'], labels=data['contract_type'], colors=palette_color, autopct='%.0f%%')
    st.pyplot(fig)


@st.cache_data
def load_plots(main_df):
    df = main_df.copy()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Average salary')
        plot_middle_price_histogram(df)

        st.subheader('Top 5 job titles with the highest max salary')
        write_offers_with_the_highest_max_salary_df(df)

        st.subheader('Top 5 employers with the most offers')
        write_employers_with_most_offers_df(df)

        st.subheader('Most popular cities for companies\' headquarters ')
        plot_map(df)

    with col2:
        st.subheader('Days to expiration')
        plot_days_to_expiration_histogram(df)

        st.subheader('Top 5 job titles with the lowest min salary')
        write_offers_with_the_lowest_min_salary_df(df)

        st.subheader('Top 5 employers by mean middle price')
        write_top_employers_by_middle_price_df(df)

        st.subheader('Percentages of offers with given contract type')
        plot_pie_chart(df)


# GETTING DATA
df, timestamp = get_data_and_time()
visible_offers_num = len(df)
offers_num = len(df)

df = (df.pipe(create_coordinates)
      .pipe(create_days_to_expirations)
      .pipe(create_middle_price)
      )


# -------- SIDEBAR MENU --------
st.sidebar.title("Options")
st.sidebar.button("Export as pdf (to do)")


# -------- MAIN PAGE --------
st.write("Number of offers:", visible_offers_num, " out of ", offers_num)

st.subheader('Descriptive statistics of prices')
st.write("Median average salary:", int(df[['middle_price']].median()))

load_plots(df)
st.write("Data last updated (read from sql db):", timestamp)
st.caption('Additional info')

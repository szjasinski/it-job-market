import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime


@st.cache_data
def get_data_and_time():
    cnx = sqlite3.connect('it-job-market.db')
    df = pd.read_sql_query("SELECT * FROM offers", cnx)
    cnx.commit()
    cnx.close()
    return df, datetime.now()


def make_clickable_job_title(main_df):
    df = main_df.copy()
    clickable_job_titles = [f'<a target="_blank" href="{link}">{title}</a>'
                            for link, title in zip(df['url'], df['job_title'])]

    df['clickable_job_title'] = clickable_job_titles
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


@st.cache_data
def convert_df_to_csv(df):
    """ Function needed for downloading CSV file """
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_to_export.to_csv().encode('utf-8')


df, timestamp = get_data_and_time()
offers_num = len(df)


df = (df.pipe(make_clickable_job_title)
      .pipe(create_days_to_expirations)
      )


# -------- SIDEBAR MENU --------
st.sidebar.title("Options")

min_salary = df['price_from'].min()
max_salary = df['price_to'].max()
selected_salary_range = st.sidebar.slider('Select salary range (PLN gross/month)',
                                          min_salary, max_salary, (min_salary, max_salary))

selected_sort_by = st.sidebar.selectbox('Sort by:', ['Price From', 'Price To'])
selected_is_descending = st.sidebar.checkbox('Descending')
selected_job_title_keywords = st.sidebar.text_input('Job title contains:')
selected_company_name_keywords = st.sidebar.text_input('Company name contains: (lowercase dont work)')
selected_contract_type = st.sidebar.selectbox('Contract type:', ["All", "B2B", "employment", "mandate"])


df_to_export = df.drop(['clickable_job_title'], axis=1)
st.sidebar.download_button(
    label="Download all data as CSV",
    data=convert_df_to_csv(df_to_export),
    file_name='it_job_market_data.csv',
    mime='text/csv',
)


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


# APPLYING OPTIONS SELECTED BY USER
df = (df.pipe(sort_df)
      .pipe(filter_job_title)
      .pipe(filter_company_name)
      .pipe(filter_contract_type)
      .pipe(filter_salary_range)
      )

df.drop(['price_unit', 'url', 'job_title'], axis=1, inplace=True)
df.drop(['address', 'city'], axis=1, inplace=True)


df = df.reindex(columns=['clickable_job_title', 'employer', 'price_from', 'price_to', 'contract_type', 'days_to_expiration'])
table = df.copy()
table.rename(
    columns={'clickable_job_title': 'Job Title', 'employer': 'Employer', 'price_from': 'Price From', 'price_to': 'Price To',
             'contract_type': 'Contract Type', 'days_to_expiration': 'Days Left'}, inplace=True)

visible_offers_num = len(table)

# DISPLAY ON MAIN PAGE
st.title('IT job offers with salary brackets from pracuj.pl')
st.write("Number of offers:", visible_offers_num, " out of ", offers_num)
st.write(table.to_html(escape=False, index=False), unsafe_allow_html=True)

st.write("Data last updated (read from sql db):", timestamp)
st.caption('Additional info')

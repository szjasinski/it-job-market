import streamlit as st
import pandas as pd
from datetime import datetime

from functions_module.filtering_functions import sort_df
from functions_module.filtering_functions import filter_job_title
from functions_module.filtering_functions import filter_company_name
from functions_module.filtering_functions import filter_contract_type
from functions_module.filtering_functions import filter_salary_range

from functions_module.display_table_function import write_data_table


@st.cache_data
def convert_df_to_csv(df):
    """ Function needed for downloading CSV file """
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df_to_export.to_csv().encode('utf-8')


df = pd.read_csv('it-job-market-ready.csv')
offers_num = len(df)


string_dates_list = df['scraping_datetime'].tolist()
datetime_dates_list = [datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in string_dates_list]


# -------- SIDEBAR MENU --------
st.sidebar.title("Options")

min_salary = df['min_salary'].min()
max_salary = df['max_salary'].max()
selected_salary_range = st.sidebar.slider('Select salary range (PLN gross/month)',
                                          min_salary, max_salary, (min_salary, max_salary))

selected_sort_by = st.sidebar.selectbox('Sort by:', ['Min Salary', 'Max Salary'])
selected_is_descending = st.sidebar.checkbox('Descending')
selected_job_title_keywords = st.sidebar.text_input('Job title contains:')
selected_company_name_keywords = st.sidebar.text_input('Company name contains:')
selected_contract_type = st.sidebar.selectbox('Contract type:', ["All", "B2B", "employment", "mandate"])


df_to_export = df.drop(['clickable_job_title'], axis=1)
st.sidebar.download_button(
    label="Download raw data as CSV",
    data=convert_df_to_csv(df_to_export),
    file_name='it_job_market_data.csv',
    mime='text/csv',
)


# APPLYING OPTIONS SELECTED BY USER
df = (df.pipe(sort_df, selected_sort_by=selected_sort_by, selected_is_descending=selected_is_descending)
      .pipe(filter_job_title, selected_job_title_keywords)
      .pipe(filter_company_name, selected_company_name_keywords)
      .pipe(filter_contract_type, selected_contract_type)
      .pipe(filter_salary_range, selected_salary_range)
      )

visible_offers_num = len(df)


# DISPLAY ON MAIN PAGE
st.title('IT job offers with salary brackets from pracuj.pl')
st.write("Data was scraped from pracuj.pl between:", min(datetime_dates_list), " and ", max(datetime_dates_list))
st.write("Number of offers:", visible_offers_num, " out of ", offers_num)
write_data_table(df)

st.caption('Created by Szymon Jasinski')

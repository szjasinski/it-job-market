import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

from tools.filters import sort_df
from tools.filters import filter_job_title
from tools.filters import filter_company_name
from tools.filters import filter_contract_type
from tools.filters import filter_salary_range

from tools.display_offers import display_offers

from tools.get_data import get_data

from tools.data_manipulation import create_days_to_expirations


# PREPARING DATA
df = get_data()
df = create_days_to_expirations(df)

# -------- SIDEBAR MENU --------
st.sidebar.title("Options")

min_salary = df.loc[:, 'min_salary'].dropna().min()
max_salary = df.loc[:, 'max_salary'].dropna().max()

selected_salary_range = st.sidebar.slider('Select salary range (PLN gross/month)',
                                          min_salary, max_salary, (min_salary, max_salary))

selected_sort_by = st.sidebar.selectbox('Sort by:', ['Min Salary', 'Max Salary'])
selected_is_descending = st.sidebar.checkbox('Descending')
selected_job_title_keywords = st.sidebar.text_input('Position title contains:')
selected_company_name_keywords = st.sidebar.text_input('Company name contains:')
# selected_contract_type = st.sidebar.selectbox('Contract type:', ["All", "B2B", "employment", "mandate"])

# df_to_export = df.drop(['point'], axis=1)
df_to_export = df
st.sidebar.download_button(
    label="Download raw data as CSV",
    data=df_to_export.to_csv().encode('utf-8'),
    file_name='it_job_market_data.csv',
    mime='text/csv',
)
# ---------------------------

# APPLYING OPTIONS SELECTED BY USER
df_to_display = (df.pipe(sort_df, selected_sort_by=selected_sort_by, selected_is_descending=selected_is_descending)
                 .pipe(filter_job_title, selected_job_title_keywords=selected_job_title_keywords)
                 .pipe(filter_company_name, selected_company_name_keywords=selected_company_name_keywords)
                 .pipe(filter_salary_range, selected_salary_range=selected_salary_range)
                 )

# calculate variables to display
all_offers_num = len(df)
visible_offers_num = len(df_to_display)

datetime_dates_list = [datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in df['scraping_datetime'].tolist()]
start_scraping_datetime = min(datetime_dates_list)
end_scraping_datetime = max(datetime_dates_list)

# DISPLAY ON MAIN PAGE
st.title("IT Job Listings with Salary Ranges")
st.write("The data was gathered by scraping", all_offers_num, "job offers from pracuj.pl between the timestamps of :", start_scraping_datetime,
         " and ", end_scraping_datetime)
st.write("Presenting solely the", visible_offers_num, "offers that contained salary details. All salary amounts were "
                                                      "computed as gross PLN per month.")
display_offers(df_to_display)
st.caption('Created by Szymon Jasinski')

import streamlit as st
import pandas as pd
from datetime import datetime

from functions_module.filtering_functions import sort_df
from functions_module.filtering_functions import filter_job_title
from functions_module.filtering_functions import filter_company_name
from functions_module.filtering_functions import filter_contract_type
from functions_module.filtering_functions import filter_salary_range

from functions_module.display_table_function import write_data_table


# GETTING DATA
df = pd.read_csv('it-job-market-ready.csv')

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

df_to_export = df.drop(['point'], axis=1)
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
                 .pipe(filter_contract_type, selected_contract_type=selected_contract_type)
                 .pipe(filter_salary_range, selected_salary_range=selected_salary_range)
                 )

# calculate variables to display
all_offers_num = len(df)
visible_offers_num = len(df_to_display)

string_dates_list = df['scraping_datetime'].tolist()
datetime_dates_list = [datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in string_dates_list]
start_scraping_datetime = min(datetime_dates_list)
end_scraping_datetime = max(datetime_dates_list)

# DISPLAY ON MAIN PAGE
st.title('IT job offers with salary brackets from pracuj.pl')
st.write("Data was scraped from pracuj.pl between:", start_scraping_datetime, " and ", end_scraping_datetime)
st.write("Number of offers:", visible_offers_num, " out of ", all_offers_num)
st.write("All salary values are in PLN/month gross")
write_data_table(df_to_display)
st.caption('Created by Szymon Jasinski')

import streamlit as st
import pandas as pd
from datetime import datetime

from functions_module.summary_dfs import write_offers_with_the_lowest_min_salary_df
from functions_module.summary_dfs import write_offers_with_the_highest_max_salary_df
from functions_module.summary_dfs import write_employers_with_most_offers_df
from functions_module.summary_dfs import write_top_employers_by_average_price_df

from functions_module.plot_functions import plot_pydeck_map
from functions_module.plot_functions import plot_average_price_histogram
from functions_module.plot_functions import plot_contract_type_pie_chart
from functions_module.plot_functions import plot_days_to_expiration_histogram
from functions_module.plot_functions import plot_words_in_job_title_barplot


# GETTING DATA
df = pd.read_csv('it-job-market-ready.csv')
visible_offers_num = len(df)
offers_num = len(df)
string_dates_list = df['scraping_datetime'].tolist()
datetime_dates_list = [datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in string_dates_list]

# -------- SIDEBAR MENU --------
st.sidebar.title("Options")
st.sidebar.button("Export as pdf (to do)")

# -------- MAIN PAGE --------
st.title('Plots and data summaries')
st.write("Data was scraped from pracuj.pl between:", min(datetime_dates_list), " and ", max(datetime_dates_list))
st.write("Number of offers:", visible_offers_num, " out of ", offers_num)
st.subheader("Average salary information")
st.write("Average salary is calculated for each job offer as an average of max and min salary")
st.write("Median of average salary:", int(df[['middle_price']].median()))
st.write("Standard deviation of average salary:", int(df[['middle_price']].std()))

col1, col2 = st.columns(2)
with col1:
    st.subheader('Top 5 job titles with the highest max salary')
    write_offers_with_the_highest_max_salary_df(df)
    st.subheader('Top 5 employers with the most offers')
    write_employers_with_most_offers_df(df)
    st.subheader('Days to expiration')
    plot_days_to_expiration_histogram(df)
with col2:
    st.subheader('Top 5 job titles with the lowest min salary')
    write_offers_with_the_lowest_min_salary_df(df)
    st.subheader('Top 5 employers by average salary')
    write_top_employers_by_average_price_df(df)
    st.subheader('Contract type')
    plot_contract_type_pie_chart(df)

st.subheader('Average salary')
plot_average_price_histogram(df)
st.subheader('Most popular words in Job Title')
plot_words_in_job_title_barplot(df)
st.subheader('Localizations of employers headquarters')
plot_pydeck_map(df)

st.caption('Created by Szymon Jasinski')

import numpy as np
import streamlit as st
import pandas as pd
from datetime import datetime

from tools.summaries import display_offers_with_the_lowest_min_salary
from tools.summaries import display_offers_with_the_highest_max_salary
from tools.summaries import display_employers_with_most_offers
from tools.summaries import display_top_employers_by_average_max_salary

from tools.plots import plot_pydeck_map
from tools.plots import plot_min_salary
from tools.plots import plot_max_salary
from tools.plots import plot_contract_type
from tools.plots import plot_days_to_expiration
from tools.plots import plot_words_in_job_title
from tools.plots import plot_expected_technologies
from tools.plots import plot_optional_technologies
from tools.plots import plot_benefits
from tools.plots import plot_specializations

from tools.get_data import get_data

from tools.data_manipulation import create_days_to_expirations


# GETTING DATA
df = get_data()
df = create_days_to_expirations(df)


# -------- SIDEBAR MENU --------
st.sidebar.title("Options")
# st.sidebar.button("Export as pdf (to do)")

# -------- MAIN PAGE --------
st.title('Data Insights')
datetime_dates_list = [datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in df['scraping_datetime'].tolist()]
st.write("The data was gathered by scraping pracuj.pl between the timestamps of :", min(datetime_dates_list), " and ", max(datetime_dates_list))
offers_num = len(df)
offers_with_salary_num = df['min_salary'].notna().sum()
# assert offers_with_salary == df['max_salary'].notna().sum()
print(df['max_salary'].notna().sum())
print(offers_with_salary_num)
st.write("Out of", offers_num, "offers analyzed,", offers_with_salary_num, "included salary information. Missing values "
                                                                       "were disregarded.")


st.subheader("Minimum salary ranges")
plot_min_salary(df)
st.subheader("Maximum salary ranges")
plot_max_salary(df)
st.subheader("Top 20 Expected Technologies in demand")
plot_expected_technologies(df)
st.subheader("Top 20 Optional Technologies in demand")
plot_optional_technologies(df)
st.subheader("Top 20 preferred Specializations")
plot_specializations(df)
st.subheader("Most frequently offered Benefits")
plot_benefits(df)
st.subheader("Top keywords in Job Titles")
plot_words_in_job_title(df)
# st.subheader("Company Headquarters Location")
# plot_pydeck_map(df)


col1, col2 = st.columns(2)
with col1:
    st.subheader("Leading Employers with Highest Offer Counts")
    display_employers_with_most_offers(df)
    st.subheader("Days until Offer Expiration")
    plot_days_to_expiration(df)
with col2:
    st.subheader("Top Employers by Average Maximum Salary")
    display_top_employers_by_average_max_salary(df)
    st.subheader("Type of Contract")
    plot_contract_type(df)


st.caption('Created by Szymon Jasinski')

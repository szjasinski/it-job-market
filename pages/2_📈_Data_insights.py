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
st.write("Data was scraped from pracuj.pl between:", min(datetime_dates_list), " and ", max(datetime_dates_list))
offers_num = len(df)
st.write("Number of analyzed offers:", offers_num)


st.subheader('Lower salary brackets')
st.write("Median:", int(df['min_salary'].median()), "PLN")
plot_min_salary(df)
st.subheader('Upper salary brackets')
st.write("Median:", int(df['max_salary'].median()), "PLN")
plot_max_salary(df)
st.subheader('Most popular expected technologies')
plot_expected_technologies(df)
st.subheader('Most popular optional technologies')
plot_optional_technologies(df)
st.subheader("Most popular specializations")
plot_specializations(df)
st.subheader('Most popular benefits')
plot_benefits(df)
st.subheader('Most popular words in job title')
plot_words_in_job_title(df)
st.subheader('Location of the company headquarters')
# plot_pydeck_map(df)


col1, col2 = st.columns(2)
with col1:
    st.subheader('Top employers with the most offers')
    display_employers_with_most_offers(df)
    st.subheader('Days to expiration')
    plot_days_to_expiration(df)
with col2:
    st.subheader('Top employers by average max salary')
    display_top_employers_by_average_max_salary(df)
    st.subheader('Contract type')
    plot_contract_type(df)


st.caption('Created by Szymon Jasinski')

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3


@st.cache_data
def get_data():
    cnx = sqlite3.connect('it-job-market.db')
    df = pd.read_sql_query("SELECT * FROM offers", cnx)
    cnx.commit()
    cnx.close()
    return df


df = get_data()

st.title('IT job offers with salary brackets (Poland)')

# st.write(df)


clickable_job_titles = [f'<a target="_blank" href="{link}">{title}</a>'
                        for link, title in zip(df['url'], df['job_title'])]

df['job_title'] = clickable_job_titles
df.drop(['url', 'price_unit'], axis=1, inplace=True)


st.sidebar.title("Options")
selected_sort_by = st.sidebar.selectbox('Sort by:', ['Price From', 'Price To'])
selected_is_descending = st.sidebar.checkbox('Descending')
selected_job_title_keywords = st.sidebar.text_input('Job title contains:')
selected_company_name_keywords = st.sidebar.text_input('Company name contains:')
selected_contract_type = st.sidebar.selectbox('Contract type: (to do)', ["All", "B2B", "Employment"])
selected_show_company_logo = st.sidebar.checkbox('Show company logos (to do)')

# update immediately after changing option
t = True

if st.sidebar.button('Run') or t:


    # sort dataframe values
    if selected_sort_by == 'Price To' and selected_is_descending:
        df = df.sort_values(by=['price_to'], ascending=False)
    elif selected_sort_by == 'Price From' and selected_is_descending:
        df = df.sort_values(by=['price_from'], ascending=False)
    elif selected_sort_by == 'Price To':
        df = df.sort_values(by=['price_to'])
    elif selected_sort_by == 'Price From':
        df = df.sort_values(by=['price_from'])

    # filter df with job title keywords
    job_title_keywords = selected_job_title_keywords.split()
    data = pd.DataFrame()
    for keyword in job_title_keywords:
        filtered_df = df[df['job_title'].str.contains(keyword)]
        data = pd.concat([data, filtered_df])
    data.drop_duplicates()
    if job_title_keywords:
        df = data

    # filter df with company name keywords
    company_name_keywords = selected_company_name_keywords.split()
    data = pd.DataFrame()
    for keyword in company_name_keywords:
        filtered_df = df[df['employer'].str.contains(keyword)]
        data = pd.concat([data, filtered_df])
    data.drop_duplicates()
    if company_name_keywords:
        df = data

    # filter df with contract types

    # show or dont show company logos


    table = df.copy()
    table.rename(columns={'job_title': 'Job Title', 'employer': 'Employer', 'price_from': 'Price From', 'price_to': 'Price To',
                       'contract_type': 'Contract Type'}, inplace=True)
    row_count = len(table)
    st.write("Number of offers:", row_count)

    st.write(table.to_html(escape=False, index=False), unsafe_allow_html=True)


# histogram
st.subheader('Number of offers in salary brackets')
hist_values = np.histogram(df['price_to'], bins=10, range=(0,50000))[0]
st.bar_chart(hist_values)

st.subheader('Top 10 employers with the most offers with salaries')

st.subheader('Percentages of offers with given contract type')

st.subheader('Most popular cities')

st.subheader('Descriptive statistics of prices')
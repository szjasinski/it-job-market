import streamlit as st


def display_offers(main_df):
    table = main_df.copy()
    table.drop(['price_unit', 'url', 'job_title', 'address', 'city', 'contract_type'], axis=1, inplace=True)
    table = table.reindex(columns=['clickable_job_title', 'employer', 'min_salary', 'max_salary',
                                   'days_to_expiration'])
    table.rename(
        columns={'clickable_job_title': 'Position Title', 'employer': 'Company', 'min_salary': 'Min Salary',
                 'max_salary': 'Max Salary', 'days_to_expiration': 'Days Left'}, inplace=True)
    st.write(table.to_html(escape=False, index=False), unsafe_allow_html=True)


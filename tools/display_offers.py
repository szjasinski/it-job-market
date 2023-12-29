import streamlit as st


def display_offers(main_df):
    table = main_df.copy()
    table.drop(['price_unit', 'url', 'job_title', 'address', 'city'], axis=1, inplace=True)
    table = table.reindex(columns=['clickable_job_title', 'employer', 'min_salary', 'max_salary', 'contract_type', 'days_to_expiration'])
    table.rename(
        columns={'clickable_job_title': 'Job Title', 'employer': 'Employer', 'min_salary': 'Min Salary', 'max_salary': 'Max Salary',
                 'contract_type': 'Contract Type', 'days_to_expiration': 'Days Left'}, inplace=True)
    st.write(table.to_html(escape=False, index=False), unsafe_allow_html=True)


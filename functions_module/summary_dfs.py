import streamlit as st


def write_employers_with_most_offers_df(main_df):
    df = main_df.copy()
    df = df[['employer', 'job_title']].groupby(['employer'], as_index=False).count().nlargest(5, 'job_title')
    df = df.reindex(columns=['job_title', 'employer'])
    df.rename(columns={'job_title': 'Count', 'employer': 'Employer'}, inplace=True)
    st.write(df.set_index('Count'))


def write_offers_with_the_highest_max_salary_df(main_df):
    df = main_df.copy()
    df.rename(columns={'job_title': 'Job Title', 'max_salary': 'Max Salary'}, inplace=True)
    df = df[['Job Title', 'Max Salary']].nlargest(5, 'Max Salary')
    df = df.set_index('Max Salary')
    st.write(df)


def write_offers_with_the_lowest_min_salary_df(main_df):
    df = main_df.copy()
    df.rename(columns={'job_title': 'Job Title', 'min_salary': 'Min Salary'}, inplace=True)
    df = df[['Job Title', 'Min Salary']].nsmallest(5, 'Min Salary')
    df = df.set_index('Min Salary')
    st.write(df)


def write_top_employers_by_average_price_df(main_df):
    df = main_df.copy()
    df.rename(columns={'middle_price': 'Average Price', 'min_salary': 'Min Salary', 'employer': 'Employer'}, inplace=True)
    df = df[['Average Price', 'Employer']].groupby('Employer', as_index=False).mean()
    df = df.reindex(columns=['Average Price', 'Employer'])
    df = df.nlargest(5, 'Average Price')
    df['Average Price'] = df['Average Price'].apply(lambda x: round(x, 0))
    st.write(df.set_index('Average Price'))

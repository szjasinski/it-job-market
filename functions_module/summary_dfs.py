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


def write_top_employers_by_average_max_salary_df(main_df):
    df = main_df.copy()
    df.rename(columns={'max_salary': 'Max Salary', 'employer': 'Employer'}, inplace=True)
    df = df[['Max Salary', 'Employer']].groupby('Employer', as_index=False).mean()
    df = df.reindex(columns=['Max Salary', 'Employer'])
    df = df.nlargest(5, 'Max Salary')
    df['Max Salary'] = df['Max Salary'].apply(lambda x: round(x, 0))
    df.rename(columns={'Max Salary': 'Avg Max Salary'}, inplace=True)
    st.write(df.set_index('Avg Max Salary'))

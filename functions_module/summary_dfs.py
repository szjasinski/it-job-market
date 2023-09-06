import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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


def write_top_employers_by_middle_price_df(main_df):
    df = main_df.copy()
    df.rename(columns={'middle_price': 'Average Price', 'min_salary': 'Min Salary', 'employer': 'Employer'}, inplace=True)
    df = df[['Average Price', 'Employer']].groupby('Employer', as_index=False).mean()
    df = df.reindex(columns=['Average Price', 'Employer'])
    df = df.nlargest(5, 'Average Price')
    df['Average Price'] = df['Average Price'].apply(lambda x: round(x, 0))
    st.write(df.set_index('Average Price'))


def write_most_popular_words(main_df):
    df = main_df.copy()

    def custom_replace(x):
        to_replace = ["(", ")", "-", "+", ",", "/", "–", "&"]
        replaced = x
        for char in to_replace:
            replaced = replaced.replace(char, "")
        return replaced

    # replace unnecessary characters with spaces
    job_title_list = df['job_title'].tolist()
    for i in range(len(job_title_list)):
        job_title_list[i] = custom_replace(job_title_list[i])

    # create dict to count word occurrences
    words_dict = {}
    for job in job_title_list:
        for word in job.split():
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1

    sorted_words = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)
    words_df = pd.DataFrame(sorted_words, columns=['Word', 'Count'])
    words_to_drop = ["of", "in", "z", "for", "ds."]
    df_filtered = words_df[~words_df['Word'].isin(words_to_drop)]
    words_to_plot = df_filtered.iloc[:10, :]

    fig = plt.figure(figsize=(12, 5))
    sns.barplot(data=words_to_plot, x="Word", y="Count")
    st.pyplot(fig)

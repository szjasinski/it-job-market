import streamlit as st
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk


# ----------- PLOTS FUNCTIONS

def plot_middle_price_histogram(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    plt.xlim(-1000, 70000)
    df.rename(columns={'middle_price': 'Average Salary'}, inplace=True)
    sns.histplot(data=df["Average Salary"], kde=True, bins=28, binrange=(0, 70000))
    st.pyplot(fig)


def plot_days_to_expiration_histogram(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 7))
    plt.xlim(-1, 60)
    df.rename(columns={'days_to_expiration': 'Days to expiration'}, inplace=True)
    sns.histplot(data=df["Days to expiration"], kde=True, bins=20, binrange=(0, 100))
    st.pyplot(fig)


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

    # TO CORRECT


def plot_pie_chart(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    df = df[['contract_type', 'employer']].groupby('contract_type', as_index=False).count()
    palette_color = sns.color_palette('deep')
    plt.pie(df['employer'], labels=df['contract_type'], colors=palette_color, autopct='%.0f%%')
    st.pyplot(fig)


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


def plot_pydeck_map(main_df):
    df = main_df.copy()
    chart_data = df[['latitude', 'longitude']].dropna()

    st.pydeck_chart(
        pdk.Deck(map_style=None, initial_view_state=pdk.ViewState(latitude=51.75, longitude=19.46, zoom=5, pitch=50, ),
                 layers=[pdk.Layer(
                     'HexagonLayer',
                     data=chart_data,
                     get_position='[longitude, latitude]',
                     radius=20000,
                     elevation_scale=300,
                     elevation_range=[0, 1000],
                     pickable=True,
                     extruded=True, ),
                     pdk.Layer(
                         'ScatterplotLayer',
                         data=chart_data,
                         get_position='[longitude, latitude]',
                         get_color='[200, 30, 0, 160]',
                         get_radius=20000, )]))


# @st.cache_data
def load_plots(main_df):
    df = main_df.copy()

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
        write_top_employers_by_middle_price_df(df)

        st.subheader('Contract type')
        plot_pie_chart(df)

    st.subheader('Average salary')
    plot_middle_price_histogram(df)
    st.subheader('Most popular words in Job Title')
    write_most_popular_words(df)
    st.subheader('Localizations of employers headquarters')
    plot_pydeck_map(df)


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

load_plots(df)
st.caption('Created by Szymon Jasinski')

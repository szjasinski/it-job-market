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
    sns.histplot(data=df["middle_price"], kde=True, bins=28, binrange=(0, 70000))
    st.pyplot(fig)


def plot_days_to_expiration_histogram(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 7))
    plt.xlim(-1, 60)
    sns.histplot(data=df["days_to_expiration"], kde=True, bins=20, binrange=(0, 100))
    st.pyplot(fig)


def write_employers_with_most_offers_df(main_df):
    df = main_df.copy()
    emp = df[['employer', 'job_title']].groupby(['employer'], as_index=False).count().nlargest(5, 'job_title')
    emp = emp.reindex(columns=['job_title', 'employer'])
    emp.rename(columns={'job_title': 'Count'}, inplace=True)
    st.write(emp.set_index('Count'))


def write_offers_with_the_highest_max_salary_df(main_df):
    df = main_df.copy()
    output_df = df[['job_title', 'max_salary']].nlargest(5, 'max_salary')
    # emp.rename(columns={'Job Title': 'Count'}, inplace=True)
    output_df = output_df.set_index('max_salary')
    st.write(output_df)


def write_offers_with_the_lowest_min_salary_df(main_df):
    df = main_df.copy()
    output_df = df[['job_title', 'min_salary']].nsmallest(5, 'min_salary')
    # emp.rename(columns={'Job Title': 'Count'}, inplace=True)
    output_df = output_df.set_index('min_salary')
    st.write(output_df)


def write_top_employers_by_middle_price_df(main_df):
    df = main_df.copy()
    mean_middle_price_by_employer = df[['middle_price', 'employer']].groupby('employer', as_index=False).mean()
    output_df = mean_middle_price_by_employer.reindex(columns=['middle_price', 'employer'])
    mean_middle_price_by_employer.round(1)
    output_df = output_df.nlargest(5, 'middle_price')
    output_df['middle_price'] = output_df['middle_price'].apply(lambda x: round(x, 0))
    st.write(output_df.set_index('middle_price'))

    # TO CORRECT


def plot_pie_chart(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    data = df[['contract_type', 'employer']].groupby('contract_type', as_index=False).count()
    palette_color = sns.color_palette('deep')
    plt.pie(data['employer'], labels=data['contract_type'], colors=palette_color, autopct='%.0f%%')
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

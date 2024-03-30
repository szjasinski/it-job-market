import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import numpy as np


def plot_min_salary(main_df):
    df = main_df.copy()
    sns.set_theme()
    fig = plt.figure(figsize=(12, 5))
    plt.xlim(-1000, 70000)
    ax = sns.histplot(data=df[df["min_salary"].notna()]["min_salary"].astype(float), kde=True, bins=28, binrange=(0, 70000))

    median = int(df['min_salary'].median())
    mean = int(df['min_salary'].mean())
    plt.axvline(median, color='k', linestyle='dashed', linewidth=1.3)
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1.3)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean * 1.5, max_ylim * 0.9, 'Median: ' + str(median))
    plt.text(mean * 1.5, max_ylim * 0.8, 'Mean: ' + str(mean))
    plt.xlabel("Minimum Salary (PLN)")
    ax.legend(['Density', 'Median', 'Mean'])
    st.pyplot(fig)


def plot_max_salary(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    plt.xlim(-1000, 70000)
    ax = sns.histplot(data=df[df["max_salary"].notna()]["max_salary"].astype(float), kde=True, bins=28, binrange=(0, 70000))

    median = int(df['max_salary'].median())
    mean = int(df['max_salary'].mean())
    plt.axvline(median, color='k', linestyle='dashed', linewidth=1.3)
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1.3)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean * 1.5, max_ylim * 0.9, 'Median: ' + str(median))
    plt.text(mean * 1.5, max_ylim * 0.8, 'Mean: ' + str(mean))
    plt.xlabel("Maximum Salary (PLN)")
    ax.legend(['Density', 'Median', 'Mean'])
    st.pyplot(fig)


def plot_days_to_expiration(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 7))
    plt.xlim(-1, 60)
    df.rename(columns={'days_to_expiration': 'Days to expiration'}, inplace=True)
    sns.histplot(data=df["Days to expiration"], kde=True, bins=20, binrange=(0, 100))
    plt.xlabel("Days until Offer Expiration")
    st.pyplot(fig)


def plot_contract_type(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    df = df[['contract_type', 'employer']].groupby('contract_type', as_index=False).count()
    plt.pie(df['employer'], labels=df['contract_type'], autopct='%.0f%%')
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


def plot_words_in_job_title(main_df):
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
    sns.barplot(data=words_to_plot, x="Word", y="Count", palette="deep")
    plt.xlabel("Keyword")
    st.pyplot(fig)


def plot_expected_technologies(main_df):
    df = main_df.copy()
    df["expected_technologies"] = df["expected_technologies"].apply(eval)
    data = df["expected_technologies"].explode().value_counts().head(20)
    data_df = data.reset_index()
    data_df.columns = ["expected_technology", "frequency"]
    fig = plt.figure(figsize=(7, 7))
    sns.barplot(data=data_df, y='expected_technology', x='frequency', orient="h", palette="deep")
    plt.ylabel("Expected Technology")
    plt.xlabel("Frequency")
    st.pyplot(fig)


def plot_optional_technologies(main_df):
    df = main_df.copy()
    df["optional_technologies"] = df["optional_technologies"].apply(eval)
    data = df["optional_technologies"].explode().value_counts().tail(-1).head(20)
    data_df = data.reset_index()
    data_df.columns = ["optional_technology", "frequency"]
    fig = plt.figure(figsize=(7, 7))
    sns.barplot(data=data_df, y='optional_technology', x='frequency', orient="h", palette="deep")
    plt.ylabel("Optional Technology")
    plt.xlabel("Frequency")
    st.pyplot(fig)


def plot_benefits(main_df):
    df = main_df.copy()
    df["benefits"] = df["benefits"].apply(eval)
    data = df["benefits"].explode().value_counts().tail(-1).head(20)
    data_df = data.reset_index()
    data_df.columns = ["benefits", "frequency"]
    fig = plt.figure(figsize=(7, 7))
    sns.barplot(data=data_df, y='benefits', x='frequency', orient="h", palette="deep")
    plt.ylabel("Benefit")
    plt.xlabel("Frequency")
    st.pyplot(fig)


def plot_specializations(main_df):
    df = main_df.copy()
    data = df[["specialization", "url"]].groupby(by=["specialization"], dropna=False).count().sort_values(by=['url'],
                                                                                                          ascending=False)
    data = data.reset_index().head(20)
    data.columns = ["specialization", "frequency"]
    fig = plt.figure(figsize=(5, 7))
    sns.barplot(data=data, y='specialization', x='frequency', orient="h", palette="deep")
    plt.ylabel("Specialization")
    plt.xlabel("Frequency")
    st.pyplot(fig)
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk


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


def plot_pie_chart(main_df):
    df = main_df.copy()
    fig = plt.figure(figsize=(12, 5))
    df = df[['contract_type', 'employer']].groupby('contract_type', as_index=False).count()
    palette_color = sns.color_palette('deep')
    plt.pie(df['employer'], labels=df['contract_type'], colors=palette_color, autopct='%.0f%%')
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

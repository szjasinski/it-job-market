import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is IT-job-market project!"
    }
)

st.write("# Welcome to my IT-job-market project! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    The project is about getting insight into the state of polish IT job market.
    **👈 Select a page from the sidebar** to find a job or see interesting plots and data! 
    All offers are scraped from pracuj.pl website.
    Feel free to see the code on my [github](https://github.com/szjasinski/it-job-market).
    ### Want to find a new job?
    - Every job offer has a salary brackets and link to page with offer details!
    - You can sort offers by salary or filter them by salary, job title, employer and contract type!
    - Download all data to csv file and explore it yourself!
    ### Plots and statistics!
    - See the median salary and salary distribution plot!
    - Which employers have the most offers and which offer the highest salary on average?
    - See location of companies' headquarters on the map!
"""
)

st.write(" ")
st.write(" ")
st.write(" ")
st.write("TO DO (?): object oriented design, new data sources (nofluffjobs, rocketjobs, "
         "justjoinit), schedule offers scraping, most popular words from job titles,"
         "export plots as pdf report (images), make plot functions have arguments, monitor day to day changes in "
         "offer num/quality, "
         "map cirlce size slider...")
st.caption('Created by Szymon Jasinski')
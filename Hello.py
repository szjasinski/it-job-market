import streamlit as st


st.set_page_config(
    page_title="IT-job-market project",
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
    - Every job offer has a salary brackets and link to page with offer details
    - Sort offers by salary or filter them by salary, job title, employer and contract type
    - Download all data to csv file and explore it yourself
    ### Plots and statistics!
    - Which employers have the most offers and which offer the highest salary on average?
    - See the median salary and salary distribution plot
    - See location of companies' headquarters on the map
"""
)

st.write(" ")
st.write(" ")
st.write(" ")
st.write("TO DO (?): analyze content of job offers (programming languages, technologies), new data sources ("
         "nofluffjobs, rocketjobs, justjoinit), schedule offers scraping,"
         "export plots as pdf report (images), monitor day to day changes in "
         "offer num/quality, business value of project")
st.caption('Created by Szymon Jasinski')
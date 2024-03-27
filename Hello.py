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

st.sidebar.success("Select a page above.")

st.markdown(
    """ 
    # Welcome to Job Market Analysis Tool! 👋
    
    ## Introduction
    Hello and thank you for visiting my job market project! I'm excited to share this project with you, showcasing my skills in Python, data analysis and web scraping. Feel free to see the code on my [github](https://github.com/szjasinski/it-job-market).
    
    ## What You'll Find
    - **Comprehensive Insights**: Dive deep into the latest job listings sourced directly from pracuj.pl.
    - **Interactive Features**: Sort, filter, and explore job offers based on your preferences.
    - **Visualized Data**: Gain valuable insights through interactive plots and statistics.
    - **Easy Data Exploration**: Download all data to CSV for further analysis.
    
    ## Why You Should Explore
    This project demonstrates my proficiency in Python, data analysis and web scraping, as well as my commitment to providing valuable insights. I invite you to explore the project further and witness firsthand the skills and dedication I bring to the table.
    
    Ready to dive in? Let's explore together!
    """
)

st.write(" ")
st.write(" ")
st.write(" ")
st.caption('Created by Szymon Jasinski')

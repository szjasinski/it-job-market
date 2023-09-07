import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import streamlit as st


df = pd.read_csv('it-job-market-ready.csv')

user_prompt = st.text_input('Enter you query here:')
st.caption("What is the average max salary for job titles containing 'Python'?")
st.caption("What are top 5 most popular Job Titles?")
st.caption("What are top 5 employers that have the highest average days to expiration?")
st.caption("What are top 5 cities that have the highest average max salary and at least 5 offers?")
st.caption("What are top 5 employers that have the lowest average min salary and have at least 5 offers?")

output = ''
if st.button('Get answer!'):
    if user_prompt:
        llm = OpenAI(api_token=st.secrets['MY_OPENAI_API_KEY'])
        output = SmartDataframe(df, config={"llm": llm})
        output = output.chat(user_prompt)
    else:
        st.write("Please ask a question :)")
st.write(output)

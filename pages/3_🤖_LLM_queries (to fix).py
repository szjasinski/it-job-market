import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import pandasai as pai
import streamlit as st

st.title('Query the dataset using large language model')

df = pd.read_csv('it-job-market-ready.csv')

user_prompt = st.text_input('Enter you query here: (see examples below)')
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

pai.clear_cache()

# LANGCHAIN VERSION
# from langchain.agents import create_pandas_dataframe_agent
# from langchain.chat_models import ChatOpenAI
# from langchain.agents.agent_types import AgentType
#
# from langchain.llms import OpenAI
# import pandas as pd
#
# import streamlit as st
#
# df = pd.read_csv("titanic.csv")
#
# agent = create_pandas_dataframe_agent(
#     ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=st.secrets['MY_OPENAI_API_KEY']),
#     df,
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS,
# )
#
#
# out1 = agent.run("how many rows are there?")
# out2 = agent.run("how many people have more than 3 siblings")

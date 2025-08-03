from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.agents import create_openai_functions_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import LLMChain
from langchain.agents import Agent
from langchain.agents import AgentExecutor
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ['TAVILY_API_KEY']=os.getenv("TAVILY_API_KEY")
from tools import (
    calc_future_value,
    calc_present_value,
    calc_fv_annuity,
    calc_pv_annuity,
    calc_by_72,
    calc_nper,
    estimate_retirement_age,
    required_monthly_savings_tool,
    search_side_hustles,
    time_for_savings_to_last,
    time_for_savings_to_last_with_inflation)

from langchain_core.runnables import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory 


prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful and financially smart AI assistant."),
    ("system","Use financial tools when required. Use user data if available."),
    ("system","If asked by the user,show the calculations done by you to reach the final answer."),
    ("system","User data:{persona_data}"),
    ("system","If asked,explain your maths and calculations in detail. Show the exact formulae,variable values and steps taken to reach the final answer."),
    ("system","If user mentions inflation,use the inflation adjusted savings tool to calculate the answer"),
    ("system","If user mentions when can they retire,estimate the retirement age based on current age, savings, monthly contributions, target nest egg, and expected return using the tool provided."),
    ("system","If the user's current plan can't meet the goal by the maximum age of 80, try to readjust their monthly savings to help them in this by using the tool provided and also suggest some side hustles to meet their goal using the tool"),
    MessagesPlaceholder(variable_name='chat_history'),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")])
message_history={}

def get_session_history(session_id:str)->ChatMessageHistory:

    '''
    Used to retrieve the chat history of a session.
    '''

    if session_id not in message_history:
        message_history[session_id] = ChatMessageHistory()
    return message_history[session_id]

def llm_with_tools():
    '''
    Initialize the LLM with tools used to perform various operations'''
    
    
    tools=[calc_future_value,calc_present_value,calc_fv_annuity,calc_pv_annuity,calc_by_72,calc_nper, estimate_retirement_age,required_monthly_savings_tool,time_for_savings_to_last,search_side_hustles,time_for_savings_to_last_with_inflation]
    
    llm=ChatOpenAI(model='gpt-4o',temperature=0.3)
    agent=create_openai_functions_agent(llm=llm,tools=tools,prompt=prompt)
    agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)

    agent_by_history=RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history'
    )

    return agent_by_history

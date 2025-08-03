import streamlit as st
import personabuilder
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.schema import AIMessage
print("Using:", personabuilder.__file__)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from personabuilder import Persona
from agent import llm_with_tools,get_session_history
from formulaengine import (
    future_value,
    present_value,
    fv_annuity,
    pv_annuity,
    ruleof_72,
    nper,
    required_month_savings)
st.set_page_config(
    page_title="Financial Assistant",
    layout="centered")
st.title("FinBuddy- Your Personal Finance Assistant")
st.set_page_config(page_title="Financial Assistant", layout="centered")




if "session_id" not in st.session_state:
    st.session_state.session_id = "default_session"
if "persona" not in st.session_state:
    st.session_state.persona=Persona()

persona=st.session_state.persona

st.header('Please fill your details to get started')

with st.form("Personal Details"):
    name=st.text_input(" Your Name",value=persona.name or "")
    age=st.number_input("Your Age",min_value=0,max_value=120,value=persona.age or 0)
    annual_income=st.number_input(" Your Annual Income",min_value=0,value=persona.annual_income or 0)
    current_savings=st.number_input("Current Savings",min_value=0,value=persona.current_savings or 0)
    monthly_savings=st.number_input('Monthly Savings',min_value=0,value=persona.monthly_savings or 0)
    monthly_expenses=st.number_input("Monthly Expenses",min_value=0,value=st.session_state.persona.monthly_expenses)
    target_nest=st.number_input("What is your Target Nest Egg ?",min_value=0,value=persona.target_nest or 0)
    expected_return=st.number_input("Your Expected Return on Investment (in %)",min_value=0.0,value=persona.expected_return or 0.0)
    inflation_rate=st.number_input('Inflation Rate (in %)',min_value=0.0,value=persona.inflation_rate or 0.0)

    submit_pointer=st.form_submit_button("Submit your details")
    if submit_pointer:
        st.session_state.persona=Persona(
            name=name,
            age=age,
            annual_income=annual_income,
            current_savings=current_savings,
            monthly_savings=monthly_savings,
            monthly_expenses=monthly_expenses,
            target_nest=target_nest,
            expected_return=expected_return,
            inflation_rate=inflation_rate

 
        )
        st.success('Details submitted successfully')
        persona=st.session_state.persona
        st.write("Your details have been saved. You can now ask questions related to your finances.")


if persona.name:
    st.sidebar.write(f"A short summary of {persona.name}'s profile")
    st.sidebar.write(f"Age: {persona.age}")
    st.sidebar.write(f"Annual Income: {persona.annual_income}")
    st.sidebar.write(f"Current Savings: {persona.current_savings}")
    st.sidebar.write(f"Monthly Savings: {persona.monthly_savings}")
    st.sidebar.write(f"Monthly Expenses: {persona.monthly_expenses}")
    st.sidebar.write(f"Target Nest Egg: {persona.target_nest}")
    st.sidebar.write(f"Expected Return: {persona.expected_return}%")
    


    st.json(persona.dictionary_store())



    if "confirm_edit" not in st.session_state:
        st.session_state.confirm_edit = False

    if st.sidebar.button("Edit Personal Details"):
        st.session_state.confirm_edit = True
    
    if st.session_state.confirm_edit:
        st.sidebar.warning('Are you sure you want to edit your information?')
        col1,col2=st.sidebar.columns(2)
        with col1:
            if st.button("Yes, Edit"):
                st.session_state.confirm_edit = False
                st.session_state.pop('persona',None)
                st.session_state.pop("agent_chain", None)
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.confirm_edit = False



    
    if "agent_chain" not in st.session_state:
        st.session_state.agent_chain=llm_with_tools()
    st.subheader("Ask your financial query here")
    st.caption(" Tip: 'Try asking about when can you retire with your savings?' or ' How long shall my savings last?' or 'Ask about the formulae used.'")
    question=st.text_input("Your Query")
    submit_query=st.button("Submit")

    if submit_query and question.strip():
        with st.spinner('Thinking...'):
            response=st.session_state.agent_chain.invoke(
                {
                "input": question,
                "persona_data": persona.dictionary_store()
                },
                config={
                    'configurable':{'session_id': st.session_state.session_id}
                }
            )

    

            message_history=get_session_history(st.session_state.session_id).messages
            ai_messages=[m for m in message_history if isinstance(m, AIMessage)]
            if ai_messages:
                response = ai_messages[-1].content
                st.markdown(f"**Response:**{response}")
            else:
                st.warning("No relevant response generated. Please try again.")
    
        
    max_retirement_age=85
    years_left=max_retirement_age-persona.age
    if persona.target_nest and persona.expected_return and persona.monthly_savings:
        fv_current=future_value(persona.current_savings,persona.expected_return/100,years_left)
        fv_ann=fv_annuity(persona.monthly_savings,persona.expected_return/100/12,years_left)
        total_future_value=fv_current+fv_ann
        shortfall=max(0,persona.target_nest-total_future_value)

        if shortfall>0:
            needed_monthly=required_month_savings(persona.target_nest,persona.current_savings,persona.expected_return/100/12,years=years_left
            )
            st.warning(f"With your current plan you'll fall short by {shortfall:,.0f} for a maximum retirement age of {max_retirement_age}.")
            st.info(f'To reach a {persona.target_nest:,.0f} by age of {max_retirement_age}, you should save around {needed_monthly:,.0f} per month')

            if st.button("Suggest some side hustles to cover the gap"):
                response=st.session_state.agent_chain.invoke({
                    "input": f" Suggest some side hustles that can help me earn {(needed_monthly-persona.monthly_savings):.0f} per month",
                    "persona_data": persona.dictionary_store()
                },
                config={'configurable':{"session_id": st.session_state.session_id}})
                history = get_session_history(st.session_state.session_id).messages
                ai_msgs = [message for message in history if isinstance(message, AIMessage)]
                if ai_msgs:
                    st.markdown(f'**Response:** {ai_msgs[-1].content}')

                else:
                    st.warning("No Results Found.")



import pytest
from formulaengine import(
    future_value,
    present_value,
    fv_annuity,
    pv_annuity,
    ruleof_72,
    nper,
    required_month_savings
)

def test_future_value():
    assert round(future_value(10000,0.08,10),-2)==21589.25

def test_present_value():
    assert round(present_value(21589.25,0.08,10),-2)==10000.00

def test_fv_annuity():
    assert round(pv_annuity(1000,0.08/12,10),2)==183946.00

def test_pv_annuity():
    assert round(pv_annuity(1000,0.08/12,10),2)==90417.00

def test_ruleof_72():
    assert ruleof_72(8)==9.0

def test_nper():
    result=nper(0.08/12,1000,10000,100000)
    assert 7.5<result/12<8.5

def test_required_monthly_savings():
    result=required_month_savings(1000000,100000,0.08/12,20)
    assert 2500<result<3000


from agent import llm_with_tools,get_session_history
from personabuilder import Persona

def test_retirement_age_estimation():
    agent=llm_with_tools()
    session_id="test_session_001"

    persona=Persona(
        name='Test User',
        age=30,
        annual_income=600000,
        current_savings=200000,
        monthly_savings=10000,
        monthly_expenses=20000,
        target_nest=10000000,
        expected_return=8,
        inflation_rate=6
    )

    input_query="At what age should I retire ?"
    history=get_session_history(session_id).messages
    ai_response=[m.content for m in history if m.lower().type=="ai"][-1]
    assert "retire at" in ai_response.lower() or "age" in ai_response.lower()

from langchain.tools import tool
import formulaengine as fe
from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools import TavilySearchResults
import os
os.environ['TAVILY_API_KEY']=os.getenv('TAVILY_API_KEY')
@tool
def calc_future_value(pvalue:float,rate:float,years:int)-> str:
    '''
    Calculate the future value of an investment.'''
    r=rate / 100 
    fv=fe.future_value(pvalue, r, years)
    return f"Future Value: {pvalue}*(1 + {r})^{years}= {fv :.2f}"

@tool
def calc_present_value(fvalue:float,rate:float,years:int)->str:
    '''
    Calculate the present value of an investment.'''
    r=rate/100/12
    pv= fe.present_value(fvalue, r, years)
    return f"Present Value: {fvalue}/(1 + {r})^{years}= {pv :.2f}"

@tool
def calc_fv_annuity(pmt:float,rate:float,years:int)->str:
    '''
    Calculate the future value of the annuity.'''
    r=rate/100/12
    fv=fe.fv_annuity(pmt, r, years)
    return f"Future Value of Annuity: {pmt}*(((1 + {r})^{years*12})-1)/{r} = {fv :.2f}"


@tool
def calc_pv_annuity(pmt:float,rate:float,years:int)->str:
    '''
    Calculate the present value of the annuity.'''
    r=rate/100/12
    pv=fe.pv_annuity(pmt, r, years)
    return f"Present Value of Annuity: {pmt}*(1 - (1 + {r})^(-{years*12}))/{r} = {pv :.2f}"

@tool
def calc_by_72(rate_pct:float)->str:
    '''
    Calculate the number of years it takes for an investment to double using the Rule of 72.'''
    years=fe.ruleof_72(rate_pct)
    return f"Rule of 72: 72/{rate_pct} = {years:.2f} years to double your investment"
    

@tool
def calc_nper(rate:float,pmt:float,pvalue:float,fvalue:float)->str:
    '''
    Calculate the number of periods required to reach a future value given a present value and payment amount.'''
    r=rate/100/12
    periods=fe.nper(r, pmt, pvalue, fvalue)
    return f"Number of periods: log(({pmt} + {r}*{fvalue})/({pmt} + {r}*{pvalue})) / log(1 + {r}) = {periods:.2f} months"
    

@tool
def required_monthly_savings_tool(future_value:float,current_savings:float,expected_return_pct:float,years:int)->str:

    '''
    Reverse engineer current monthly savings and calculate new savings to reach the expected return value in the future.'''
    r=expected_return_pct/100/12
    required_savings=fe.required_month_savings(future_value, current_savings, r, years)
    return f"Required Monthly Savings: {required_savings:.2f} to reach {future_value} in {years} years with current monthly savings of {current_savings} and expected return of {expected_return_pct}%"


@tool
def estimate_retirement_age(curr_age:int,curr_savings:float,monthly_savings:float,target_nest:float,expected_return_pct:float)->str:
    '''
    Estimate the retirement age based on current age, savings, monthly contributions, target nest egg, and expected return.'''
    r=expected_return_pct/100/12
    months_to_retirement = fe.nper(r, monthly_savings, curr_savings, target_nest)
    retirement_age = curr_age + int(months_to_retirement // 12)
    if (retirement_age<=85):
        return f"You can approximately retire at an age of {retirement_age:.2f} years to reach the target"
    else:
        return "Sorry the estimated retirement age is beyond the maximum retirement age og 80. Can't be estimated."

@tool
def time_for_savings_to_last_with_inflation(initial_savings:float,monthly_expenses:float,expected_return_pct:float,inflation_rate_pct:float)->str:
    '''
    Calculate the time for savings to last given initial savings, monthly expenses, expected return, and inflation rate.'''
    balance=initial_savings
    annual_expenses = monthly_expenses * 12
    r = expected_return_pct / 100 
    i = inflation_rate_pct / 100
    year=0
    while balance>0:
        balance-= annual_expenses
        if balance<0:
            break
        balance *= (1 + r)
        annual_expenses *= (1 + i)
        year += 1
    return f"Your savings will last approximately {year} years with an initial savings of {initial_savings}, monthly expenses of {monthly_expenses}, expected return of {expected_return_pct}%, and inflation rate of {inflation_rate_pct}%."


@tool
def time_for_savings_to_last(initial_savings:float,monthly_expenses:float,expected_return_pct:float)->str:
    '''
    Calculate the time for savings to last given initial savings, monthly expenses, and expected return.
    '''
    rate= expected_return_pct / 100 / 12
    periods = fe.nper(rate, -monthly_expenses, initial_savings, 0)
    years = periods // 12
    return f"Your savings will last approximately {years:.2f} years with an initial savings of {initial_savings} and monthly expenses of {monthly_expenses} at an expected return of {expected_return_pct}%."

@tool
def search_side_hustles(short_amount:float)->str:
    '''Return the top 5 side hustles which can make up for the amount of savings being short to reach the target nest'''
    tavily=TavilySearchResults(k=5)
    query=f"What are some side hustles to earn {short_amount} per month"
    results=tavily.run(query)

    if not results or "results" not in results or len(results['results'])==0:
        return "Couldn't find relevant side hustles at the moment."
    top_results=results["results"][:5]
    formatted="\n".join([f" **{item['title']}**\n{item['content']}\n {item['url']}" for item in top_results])
    return f'Here are some relevant side hustles you could explore: \n\n{formatted}'
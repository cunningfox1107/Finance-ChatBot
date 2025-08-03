import numpy as np
def future_value(pvalue,rate,time):
    f_value=pvalue*(1+rate)**time
    return f_value

def present_value(fvalue,rate,time):
    p_value=fvalue/(1+rate)**time

def fv_annuity(pmt,rate,time):
    if(rate==0):
        return pmt*time
    return pmt*(((1+rate)**time)-1)/rate

def pv_annuity(pmt,rate,time):
    if (rate==0):
        return pmt*time
    return pmt*(1-(1+rate)**(-time))/rate

def ruleof_72(rate_pct):
    if(rate_pct==0):
        raise ValueError("Rate percentage should be non-zero")
    return 72/rate_pct

def nper(rate,pmt,pvalue,fvalue):
    if(rate==0):
        if(pmt==0):
            raise ValueError("Oops! The value of payments and rate, both cannot be zero")
        return (fvalue-pvalue)/pmt
    return np.log((pmt+rate*fvalue)/(pmt+rate*pvalue))/np.log(1+rate)

def required_month_savings(target_nest,current_savings,rate,years):
    fv_current=future_value(current_savings,rate,years)
    fv_required=target_nest-fv_current
    if fv_required <= 0:
        return 0
    if(rate==0):
        return fv_required/(years*12)
    return fv_required*rate/(((1+rate)**(years*12))-1)


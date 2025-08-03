class Persona:
    def __init__(self,name=None,age=None,annual_income=None,current_savings=None,monthly_savings=None,monthly_expenses=None,target_nest=None,expected_return=None,inflation_rate=None):
        self.name=name
        self.age=age
        
        self.annual_income=annual_income
        self.current_savings=current_savings
        self.monthly_savings=monthly_savings
        self.monthly_expenses=monthly_expenses
        self.target_nest=target_nest
        self.expected_return=expected_return
        self.inflation_rate=inflation_rate
    
    def dictionary_store(self):
        return{
            'name':self.name,
            'age':self.age,
            
            'annual income':self.annual_income,
            'current_savings':self.current_savings,
            'monthly_savings':self.monthly_savings,
            'monthly_expenses':self.monthly_expenses,
            'taregt_nest':self.target_nest,
            'expected_return':self.expected_return,
            'inflation_rate':self.inflation_rate

        }

    

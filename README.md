# Finance-ChatBot

**Features of this Chatbot**
Personalized Query Handling: Responds to user-specific questions like “When can I retire?”, “Will my savings last until I’m 80?”, or “How much do I need to save monthly to reach ₹50 lakhs?”.
Smart Financial Calculations: Uses industry-standard formulas for future value, present value, annuities, NPER, and the Rule of 72 to provide accurate insights tailored to your profile.
Conversational AI: Powered by OpenAI’s GPT model via LangChain, it retains memory across sessions to maintain context during conversations.

**Income Gap Recommendations: If you’re not on track to meet your financial goals, FinBuddy can analyze the shortfall and suggest side hustles or alternative income sources to close the gap.
Formula Explanations: Curious how a value was calculated? Just ask — FinBuddy will explain the formulas and logic used behind the scenes.**

**Key Features**
Conversational interface via Streamlit
User profile setup via a form.
Dynamic, real-time financial reasoning.
Interactive response rendering with history.
Extendable with more tools, APIs, and modulesUser Journey / Interaction Flow.

**Workflow of the Application**
1. Launch the App	User opens the app via Streamlit (app.py).
2. Enter Financial Details	A form captures personal info like age, income, savings, expenses, target nest egg, and expected return. This data is stored in the session.
3. View Profile Summary	The sidebar displays a real-time summary of the user’s financial profile (via the Persona class).
4. Ask Financial Questions	Users can enter natural-language queries (e.g., “When can I retire?”, “How much should I save?”)
5. AI Processes the user's financial dataand the query is sent to the LangChain-powered agent that calls the OpenAI model to reason and respond.
6. Intelligent Responses	The chatbot uses memory to maintain context and responds with personalized financial advice.
7. **Gap Analysis & Side Hustles** :If there’s a shortfall in reaching a target goal, the bot calculates how much more the user needs to save and suggests side hustles to bridge the gap.
   
9. Explain the Math, If asked, FinBuddy explains the exact financial formulas used behind its suggestions.

**Technical Architecture & Components**
a) **personabuilder.py** – User Profile Manager
Defines a Persona class to store and update:
Name, age, income, expenses, Savings, return expectations, and goals

b) **formulaengine.py** – Financial Calculator Engine
Contains reusable functions that model standard financial concepts.

**Function	Description**

**future_value()**:FV of current savings over time
**fv_annuity()**: FV of monthly savings
**nper()**: Time required to reach a goal
**ruleof_72()**: Time to double investment
**required_month_savings()** :Monthly amount needed to meet a future goal

c) **agent.py** – LangChain Agent & Memory Handler
Agent Creation: Sets up a LangChain agent with tools and an OpenAI LLM.
Session Memory: Uses session-specific history so the bot remembers the ongoing conversation.
Tool Invocation: The agent can call formula functions or calculators if needed.

d) **app.py** – Streamlit Frontend
Renders the full UI (form, chatbot, sidebar, suggestions)
Stores session states (persona, agent_chain, etc.)
Captures user input and submits it to the agent
Displays smart responses, alerts, and info boxes

5. **State & Memory Management**
FinBuddy maintains chat context throughout user interactions by utilizing LangChain's RunnableWithMessageHistory to enable session-aware conversations. It uses a lightweight message history system to automatically store and retrieve previous messages, and it keeps track of each user's unique session_id. This enables the chatbot to recall past questions and answers, allowing for follow-up inquiries, logical conversation, and tailored financial advice based on the current exchange — all without requiring users to repeatedly enter their information.

**Functions Used in FinBuddy:**
1.future_value(principal, rate, years)
Calculates the future value of a one-time investment over a period at a given annual return rate.

2.present_value(future_value, rate, years)
Computes how much a future amount is worth today, adjusted for inflation or return.

3.fv_annuity(payment, rate, years)
Estimates the future value of regular monthly savings (annuity) over a number of years.

4.pv_annuity(payment, rate, years)
Calculates the present value of a series of monthly payments.

5.nper(rate, payment, present_value, future_value)
Determines how many months/years are needed to reach a financial goal given savings and returns.

6.ruleof_72(rate)
Estimates how many years it will take to double your investment at a given interest rate.

7.required_month_savings(future_value_target, current_savings, rate, years)
Computes the monthly savings required to reach a target future amount, factoring in existing savings and returns.



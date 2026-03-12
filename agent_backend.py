import os
import requests
import pandas as pd
import plotly.express as px
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

@tool
def fetch_ons_gdp_data(start_year: int, end_year: int) -> str:
    """Fetches historical quarterly UK GDP data from the Office for National Statistics (ONS). Use when asked about GDP trends."""
    # We now use the main website's direct data endpoint instead of the retired API
    url = "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/abmi/qna/data"
    
    # ONS requires a User-Agent header for direct website queries
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        quarters = data.get('quarters', [])
        if not quarters: return "Error: No data found."
        
        df = pd.DataFrame(quarters)
        df['year'] = pd.to_numeric(df['year'])
        filtered_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        
        if filtered_df.empty: return f"No data between {start_year} and {end_year}."
        return filtered_df[['date', 'value']].to_json(orient="records")
    except Exception as e:
        return f"Error fetching data: {str(e)}"

@tool
def generate_gdp_chart(json_data: str, title: str) -> str:
    """Generates an interactive line chart. Use AFTER fetching data if a visual is requested."""
    try:
        df = pd.read_json(json_data)
        fig = px.line(df, x='date', y='value', title=title)
        return fig.to_json()
    except Exception as e:
        return f"Error generating chart: {str(e)}"

# Initialize tools and LLM
tools = [fetch_ons_gdp_data, generate_gdp_chart]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert UK macroeconomist AI. 
    1. Always use 'fetch_ons_gdp_data' for GDP trends.
    2. Use 'generate_gdp_chart' if a chart is requested.
    3. Provide a brief, analytical text summary.
    4. CRITICAL: NEVER include the raw JSON chart data or code in your final text response. The frontend will render the chart automatically behind the scenes. Just provide the text analysis."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

# return_intermediate_steps=True is CRITICAL for the Streamlit frontend to grab the chart
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    return_intermediate_steps=True
)
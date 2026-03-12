import streamlit as st
import plotly.io as pio
from agent_backend import agent_executor

st.set_page_config(page_title="Agentic UK GDP Dashboard", layout="wide")
st.title("📈 Agentic UK GDP Dashboard")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! What UK GDP trends would you like to explore today?", "chart": None}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("chart"):
            fig = pio.from_json(msg["chart"])
            st.plotly_chart(fig, use_container_width=True)

if prompt := st.chat_input("E.g., Graph the UK GDP trends from 2020 to 2024."):
    st.session_state.messages.append({"role": "user", "content": prompt, "chart": None})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = agent_executor.invoke({"input": prompt})
                
                # --- NEW FIX: Clean up Gemini's list format ---
                raw_output = response["output"]
                if isinstance(raw_output, list):
                    # Stitch the text chunks together into a single string
                    output_text = "".join([
                        chunk["text"] if isinstance(chunk, dict) and "text" in chunk 
                        else str(chunk) 
                        for chunk in raw_output
                    ])
                else:
                    output_text = str(raw_output)
                # ----------------------------------------------
                
                chart_json = None
                # Extract chart from agent's reasoning steps
                if "intermediate_steps" in response:
                    for action, observation in response["intermediate_steps"]:
                        if action.tool == "generate_gdp_chart":
                            chart_json = observation
                
                st.markdown(output_text)
                if chart_json and not chart_json.startswith("Error"):
                    fig = pio.from_json(chart_json)
                    st.plotly_chart(fig, use_container_width=True)
                
                st.session_state.messages.append({"role": "assistant", "content": output_text, "chart": chart_json})
                
            except Exception as e:
                st.error(f"Agent Error: {str(e)}")
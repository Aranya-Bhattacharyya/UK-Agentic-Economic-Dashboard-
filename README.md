# 📈 Agentic UK GDP Dashboard
**An Intelligent Macroeconomic Analysis Tool powered by Gemini & LangChain**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL_HERE)

## 📖 Overview
This project is an AI-driven dashboard designed to explore UK Gross Domestic Product (GDP) trends. Unlike standard dashboards that rely on static datasets, this application employs an **Agentic AI architecture**. 

The system uses a Large Language Model (Gemini) as a "reasoning engine" to autonomously decide which tools to use—whether fetching live data from the **Office for National Statistics (ONS)** or generating interactive visualizations—to answer complex economic queries in plain English.

---

## 🚀 Key Features
* **Autonomous Data Sourcing:** Dynamically queries the ONS API for historical quarterly GDP data.
* **Agentic Reasoning:** Uses LangChain to interpret user intent and sequence tool calls (Fetch -> Analyze -> Visualize).
* **Interactive Visuals:** Generates custom Plotly line charts tailored to the user's specific timeframe request.
* **Secure Infrastructure:** Implements `python-dotenv` for local secret management and Streamlit Secrets for cloud security.

---

## 🛠️ Technical Architecture
The application follows a modular "Tool-Use" pattern:
1.  **Frontend:** Streamlit provides the conversational chat interface.
2.  **Brain:** `Gemini-2.0-Flash` processes natural language and manages the logic flow.
3.  **Tools:** * `fetch_ons_gdp_data`: A Python tool that handles HTTP requests and Pandas filtering.
    * `generate_gdp_chart`: A visualization tool that transforms JSON data into Plotly objects.



---

## 💻 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/uk-agentic-economic-dashboard.git](https://github.com/YOUR_USERNAME/uk-agentic-economic-dashboard.git)
cd uk-agentic-economic-dashboard
```
### 2. Configure Environment 
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```
### 3. API Keys
Create a ```.env``` file in the root directory
```bash
GOOGLE_API_KEY="your_api_key_here"
```
### 4. Run Locally 
```bash
streamlit run app.py
```
## 🌐 Deployment
This app is optimized for Streamlit Community Cloud.
# Python Version: 3.12 (Recommended for library stability)
# Secrets: Add your GOOGLE_API_KEY in the Streamlit Advanced Settings using the TOML format.

## 📝 Future Roadmap
# Add Conversation Memory to allow for follow-up economic analysis.
# Integrate a News Search Tool to correlate GDP shifts with global events.
# Support for additional ONS datasets (Inflation, Employment, etc.).

## 👤 Author
Aranya Bhattacharyya MSc Data Science and Communication Candidate | University of Liverpool | www.linkedin.com/in/aranya-bhattacharyya
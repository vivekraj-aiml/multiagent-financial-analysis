Multi-Agent Financial Analysis System
A multi-agent AI-powered app to analyze quarterly financial data for major Indian/global tech companies:

Wand AI
Jio Platforms Limited
Nityo Infotech
This project uses CrewAI agents, FastMCP, and Streamlit to provide:

Automated decomposition, analysis, visualization, and reporting of financial performance.
Ready-to-use interactive dashboards and executive summaries.
Features
Multi-agent coordination: Specialized agents for planning, data analysis, visualization (Plotly), and executive report writing.
Sample quarterly financial data for 2025 (customizable).
Natural language analysis requests: Just type your query or select a template (e.g. "Compare revenue and growth trends for Wand AI and Jio Platforms...").
Professional charting: Trend lines, bar and pie charts (using Plotly), embedded directly in the dashboard.
Business-friendly reporting: Summary, key insights, recommendations for CxOs and leaders.
Quickstart
Clone this repository

git clone https://github.com/vivekraj-aiml/multiagent-financial-analysis.git
cd yourproject

Install dependencies

pip install -r requirements.txt

Start the MCP Server
(In a new terminal/tab, from project root)

python mcp_server.py

This runs the tool backend needed for agents to function.

Launch the Streamlit dashboard

streamlit run streamlit_main.py

Explore the UI:

Use sidebar templates or enter your own analysis request.

View interactive charts and executive summary.

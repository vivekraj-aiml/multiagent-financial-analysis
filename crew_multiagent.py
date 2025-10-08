"""
CrewAI agents for Multi-Agent Financial Analysis System.
Specialized agents for planning, analysis, visualization, and reporting.
Now for Wand AI, Jio Platforms Limited, Nityo Infotech financial data.
"""
import logging
from typing import Optional, List
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# MCP Server Configuration
MCP_SERVER_PARAMS = {
    "url": "http://127.0.0.1:4211/mcp",
    "transport": "streamable-http"
}

# LLM Configuration (update with your credentials)
CUSTOM_LLM_CONFIG = {
    "model": "gpt-4o",
    "api_key": "YOUR_API_KEY",
    "api_version": "API_VERSION",
    "base_url": "BASE_URL",
    "temperature": 0.7
}

def tool_names(mcp_tools) -> List[str]:
    """Extract tool names from MCP tools list."""
    return [tool.name for tool in mcp_tools]

def run_multi_agent_analysis(
    user_request: str,
    verbose: bool = True
) -> Optional[dict]:
    """
    Main function to run multi-agent financial analysis workflow.

    Args:
        user_request: Plain language business request
        verbose: Enable detailed logging

    Returns:
        Dictionary with analysis results
    """
    custom_llm = LLM(**CUSTOM_LLM_CONFIG)

    try:
        with MCPServerAdapter(MCP_SERVER_PARAMS) as mcp_tools:
            tools_available = tool_names(mcp_tools)
            if verbose:
                logger.info(f"[MCP] Connected to server. Available tools: {tools_available}")

            # Filter tools for different agent roles
            tools_planning = [t for t in mcp_tools if t.name in ("list_companies", "get_company_data", "get_quarter_data")]
            tools_analysis = [t for t in mcp_tools if t.name in ("get_company_data", "get_quarter_data", "analyze_metrics", "compare_companies")]
            tools_visualization = [t for t in mcp_tools if t.name in ("generate_plotly_json", "get_company_data", "analyze_metrics")]
            tools_reporting = [t for t in mcp_tools if t.name in ("generate_report", "analyze_metrics")]

            planning_agent = Agent(
                role="Financial Planning Coordinator",
                goal="Break down complex financial analysis requests into clear, actionable subtasks for specialist agents",
                backstory="""You are an expert financial analyst coordinator with 15 years of experience
                in Indian and global digital/IT sector analysis. You understand business models of Wand AI, Jio Platforms Limited, and Nityo Infotech deeply.
                You excel at decomposing high-level business questions into specific data requirements,
                identifying which quarters and metrics need analysis, and planning the execution sequence.""",
                tools=tools_planning,
                llm=custom_llm,
                verbose=True,
                allow_delegation=False
            )

            data_analyst = Agent(
                role="Senior Financial Data Analyst",
                goal="Extract, analyze, and interpret financial data to identify trends, patterns, and business insights",
                backstory="""You are a senior data analyst specializing in digital platform, telecom, and IT companies
                (Wand AI, Jio Platforms Limited, Nityo Infotech) with expertise in revenue analysis, profitability trends, and operational metrics.
                You have deep knowledge of quarterly reporting, YoY growth calculations, and industry benchmarking.
                You always validate data quality and provide quantitative insights with specific numbers.""",
                tools=tools_analysis,
                llm=custom_llm,
                verbose=True,
                allow_delegation=False
            )
            visualization_specialist = Agent(
                role="Data Visualization Expert",
                goal="Generate actual Plotly chart JSON configurations that can be directly rendered in Streamlit",
                backstory="""You are a data visualization engineer who specializes in creating Plotly charts.
    Your PRIMARY responsibility is to CALL the generate_plotly_json TOOL to create actual chart JSON.
    You DO NOT write descriptions of charts - you GENERATE them using the tool.
    
    CRITICAL: For every chart requested, you must:
    1. Call generate_plotly_json tool with exact parameters
    2. Return the tool's JSON output without modification
    3. Never write text like "Refer to the chart..." - only return tool outputs
    
    You work with financial data for Wand AI, Jio Platforms Limited, and Nityo Infotech.
    Your charts must be production-ready and directly renderable in Streamlit using st.plotly_chart().""",
    tools=tools_visualization,
    llm=custom_llm,
    verbose=True,
    allow_delegation=False
            )

            report_writer = Agent(
                role="Business Report Writer",
                goal="Synthesize analysis and visualizations into professional, executive-ready financial reports",
                backstory="""You are a seasoned business writer who creates executive reports for senior leaders
                in digital platform and IT services companies.
                You excel at structuring complex financial information into clear narratives,
                highlighting key takeaways, and providing actionable recommendations for organizations like Wand AI, Jio Platforms Limited, and Nityo Infotech.
                Your reports are always concise, data-driven, and decision-focused with proper business context.""",
                tools=tools_reporting,
                llm=custom_llm,
                verbose=True,
                allow_delegation=False
            )

            planning_task = Task(
                description=f"""Analyze this business request and create a detailed execution plan:

                USER REQUEST: {user_request}

                Your plan must:
                1. Identify which companies need to be analyzed (Wand AI, Jio Platforms Limited, Nityo Infotech)
                2. Determine which quarters are relevant (Q1_2025, Q2_2025, Q3_2025)
                3. Specify which metrics should be analyzed (revenue, profit, growth_yoy, attrition_rate, employee_count, deal_value)
                4. List required data queries and tools to use
                5. Define the visualization requirements
                6. Outline the final report structure

                Be very specific about record IDs and tool parameters.""",
                agent=planning_agent,
                expected_output="""A structured execution plan with:
                - List of companies and quarters to analyze
                - Specific metrics to calculate
                - Required MCP tool calls with exact parameters
                - Chart specifications
                - Report outline with sections"""
            )

            analysis_task = Task(
                description="""Based on the planning output, perform comprehensive financial analysis:

                1. Use get_company_data tool to fetch quarterly data for identified companies (Wand AI, Jio Platforms Limited, Nityo Infotech)
                2. Use analyze_metrics tool to calculate trends for key metrics (revenue, profit, growth_yoy, attrition_rate, employee_count, deal_value)
                3. Use compare_companies tool if comparing multiple companies
                4. Calculate YoY growth trends, revenue patterns, profitability metrics, attrition rates
                5. Identify significant insights and anomalies

                Provide quantitative findings with specific numbers (revenue in Crores INR, growth percentages).
                Always include company names, quarters, and context in your analysis.""",
                agent=data_analyst,
                expected_output="""Detailed analysis including:
                - Raw financial data for each company/quarter
                - Calculated metrics (averages, trends, growth rates)
                - Comparative analysis between companies (Wand AI vs Jio Platforms Limited vs Nityo Infotech)
                - Key insights with specific numbers
                - Data validation notes""",
                context=[planning_task]
            )
            visualization_task = Task(
                description="""Create ACTUAL Plotly chart JSONs using the generate_plotly_json tool.

    CRITICAL INSTRUCTIONS:
    1. You MUST call the generate_plotly_json tool for EACH chart you create
    2. DO NOT write descriptions of charts - generate the actual JSON
    3. Create exactly 3 charts by calling the tool 3 times:
    
    Chart 1: Revenue comparison (line chart)
    - Call: generate_plotly_json(chart_type="line", company_names=["Wand AI", "Jio Platforms Limited"], metric="revenue", title="Revenue Trends Q1-Q3 2025")
    
    Chart 2: Growth YoY comparison (line chart)
    - Call: generate_plotly_json(chart_type="line", company_names=["Wand AI", "Jio Platforms Limited"], metric="growth_yoy", title="YoY Growth Rate Comparison")
    
    Chart 3: Profit comparison (bar chart)
    - Call: generate_plotly_json(chart_type="bar", company_names=["Wand AI", "Jio Platforms Limited"], metric="profit", title="Profit Comparison Q1-Q3 2025")
    
    4. Return the EXACT tool output for each chart (the plotly_json string)
    5. Format your response as a JSON array of chart objects
    
    EXAMPLE OUTPUT FORMAT:
```json
    [
        {
            "chart_type": "line",
            "metric": "revenue",
            "plotly_json": "{{\"data\": [...], \"layout\": {...}}}",
            "chart_id": "line_revenue_2_companies"
        },
        {
            "chart_type": "line",
            "metric": "growth_yoy",
            "plotly_json": "{{\"data\": [...], \"layout\": {...}}}",
            "chart_id": "line_growth_yoy_2_companies"
        },
        {
            "chart_type": "bar",
            "metric": "profit",
            "plotly_json": "{{\"data\": [...], \"layout\": {...}}}",
            "chart_id": "bar_profit_2_companies"
        }
    ]
    DO NOT write text descriptions. ONLY call the tool and return the JSON results.""",
    agent=visualization_specialist,
    expected_output="""A JSON array containing exactly 3 chart objects, each with:
- chart_type: The type of chart
- metric: The metric being visualized
- plotly_json: The complete Plotly figure JSON string
- chart_id: Unique identifier for the chart

No additional text or descriptions - ONLY the JSON array.""",
context=[planning_task, analysis_task]
            )
            
            reporting_task = Task(
                description="""Create a comprehensive executive report synthesizing all findings:

                1. Review the execution plan, analysis results, and chart configurations
                2. Use generate_report tool to compile the summary
                3. Structure the report with:
                   - Executive Summary (2-3 key findings)
                   - Detailed Analysis (trends, comparisons, metrics)
                   - Visual Insights (reference to charts)
                   - Recommendations (actionable business insights)
                   - Conclusion

                Write for senior executives at digital, AI, telecom, and IT companies (i.e., Wand AI, Jio Platforms Limited, Nityo Infotech). Use business-appropriate language.""",
                agent=report_writer,
                expected_output="""Professional financial report with:
                - Executive summary highlighting top 3 insights
                - Detailed findings section with all metrics
                - References to visualization charts
                - Comparative analysis between companies
                - Actionable recommendations
                - Data-backed conclusion""",
                context=[planning_task, analysis_task, visualization_task]
            )

            crew = Crew(
                agents=[planning_agent, data_analyst, visualization_specialist, report_writer],
                tasks=[planning_task, analysis_task, visualization_task, reporting_task],
                process=Process.sequential,  
                verbose=verbose
            )
            
            logger.info("[CREW] Starting multi-agent workflow...")
            result = crew.kickoff()
            task_outputs = {}
            for task in crew.tasks:
                task_name = task.description[:100] 
                if hasattr(task, 'output'):
                    task_output = task.output.raw if hasattr(task.output, 'raw') else str(task.output)
                    task_outputs[task_name] = task_output
            logger.info("[CREW] Workflow completed successfully")
            return {
                "status": "success",
                "result": str(result),
                "task_outputs": task_outputs, 
                "agents_used": len(crew.agents),
                "tasks_completed": len(crew.tasks)
                }
    except Exception as e:
        logger.error(f"[ERROR] Multi-agent workflow failed: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    sample_request = """
    Analyze the financial performance of Wand AI and Jio Platforms Limited over the last 3 quarters (Q1, Q2, Q3 2025).
    Compare their revenue growth, profitability trends, and attrition rates.
    Create visualizations showing quarterly trends and provide a comprehensive report with insights.
    """

    print("\n" + "="*70)
    print("MULTI-AGENT FINANCIAL ANALYSIS SYSTEM")
    print("="*70)
    print(f"\n Request: {sample_request}\n")

    result = run_multi_agent_analysis(sample_request, verbose=True)

    if result and result["status"] == "success":
        print("\n" + "="*70)
        print(" ANALYSIS COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"\n Result:\n{result['result']}\n")
    else:
        print(f"\n Analysis failed: {result.get('error', 'Unknown error')}\n")
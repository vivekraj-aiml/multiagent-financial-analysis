"""
FastMCP Server for Company Financial Analysis.
Provides tools for analyzing Wand AI, Jio Platforms Limited, Nityo Infotech financial data.
"""
import logging
from fastmcp import FastMCP
from typing import List, Dict
import plotly.graph_objects as go


from sample_dataset import (
    get_all_companies,
    get_all_records,
    get_record_by_id,
    get_records_by_company,
    get_records_by_quarter,
    calculate_metrics,
    compare_companies,
    generate_report_summary
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


mcp = FastMCP(name="company_financial_analysis_mcp")

@mcp.tool(
    name="get_all_record_ids",
    description="Get list of all valid record IDs in the system. Use this to get correct record ID format."
)
def get_all_record_ids() -> dict:
    """
    Returns all valid record IDs with company mapping.
    
    Returns:
        Dictionary with all record IDs grouped by company
    """
    try:
        records = get_all_records()
        
        by_company = {}
        all_ids = []
        
        for record in records:
            company = record["company"]
            record_id = record["id"]
            all_ids.append(record_id)
            
            if company not in by_company:
                by_company[company] = []
            by_company[company].append(record_id)
        
        return {
            "all_record_ids": all_ids,
            "by_company": by_company,
            "format_info": {
                "Wand AI": "WAND_Q1_2025, WAND_Q2_2025, WAND_Q3_2025",
                "Jio Platforms Limited": "JIO_Q1_2025, JIO_Q2_2025, JIO_Q3_2025",
                "Nityo Infotech": "NITYO_Q1_2025, NITYO_Q2_2025, NITYO_Q3_2025"
            },
            "total_records": len(all_ids),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error getting record IDs: {e}")
        return {"error": str(e), "status": "failed"}

@mcp.tool(
    name="generate_plotly_chart",
    description="Generate complete Plotly chart JSON configuration ready for st.plotly_chart()"
)
def generate_plotly_chart(
    chart_type: str,
    company_names: List[str],
    metric: str,
    title: str
) -> dict:
    """
    Generate complete Plotly figure JSON for Streamlit rendering.

    Args:
        chart_type: 'line', 'bar', or 'pie'
        company_names: List of companies to include
        metric: Metric to visualize (revenue, profit, growth_yoy, etc.)
        title: Chart title

    Returns:
        Complete Plotly figure JSON
    """
    try:
        
        fig_data = []
        
        if chart_type == "line":
            for company in company_names:
                records = get_records_by_company(company)
                if records:
                    quarters = [r["quarter"] for r in records]
                    values = [r.get(metric, 0) for r in records]
                    fig_data.append(go.Scatter(
                        x=quarters,
                        y=values,
                        mode='lines+markers',
                        name=company,
                        line=dict(width=3),
                        marker=dict(size=8)
                    ))
        
        elif chart_type == "bar":
            for company in company_names:
                records = get_records_by_company(company)
                if records:
                    quarters = [r["quarter"] for r in records]
                    values = [r.get(metric, 0) for r in records]
                    fig_data.append(go.Bar(
                        x=quarters,
                        y=values,
                        name=company
                    ))
        
        elif chart_type == "pie":
            labels = []
            values = []
            for company in company_names:
                records = get_records_by_company(company)
                if records:
                    total = sum(r.get(metric, 0) for r in records)
                    labels.append(company)
                    values.append(total)
            fig_data = [go.Pie(labels=labels, values=values, hole=0.3)]
        
        fig = go.Figure(data=fig_data)
        fig.update_layout(
            title=title,
            xaxis_title="Quarter" if chart_type != "pie" else None,
            yaxis_title=metric.replace("_", " ").title(),
            template="plotly_white",
            height=500
        )
        
        # Return as JSON-serializable dict
        return {
            "status": "success",
            "chart_type": chart_type,
            "plotly_json": fig.to_json(),
            "metric": metric,
            "companies": company_names
        }
    
    except Exception as e:
        logger.error(f"Error generating Plotly chart: {e}")
        return {"error": str(e), "status": "failed"}

@mcp.tool(
    name="list_companies",
    description="Get list of all available companies (Wand AI, Jio Platforms Limited, Nityo Infotech)"
)
def list_companies() -> dict:
    """Returns list of all companies with financial data."""
    try:
        companies = get_all_companies()
        return {
            "companies": companies,
            "count": len(companies),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error listing companies: {e}")
        return {"error": str(e), "status": "failed"}



@mcp.tool(
    name="get_company_data",
    description="Get all quarterly financial data for a specific company (Wand AI, Jio Platforms Limited, Nityo Infotech)"
)
def get_company_data(company_name: str) -> dict:
    """
    Fetch all quarterly records for a company.

    Args:
        company_name: Company name (e.g., 'Wand AI', 'Jio Platforms Limited', 'Nityo Infotech')

    Returns:
        Dictionary with all quarterly data for the company
    """
    try:
        records = get_records_by_company(company_name)
        if not records:
            return {
                "error": f"No data found for company: {company_name}",
                "status": "not_found"
            }

        return {
            "company": company_name,
            "records": records,
            "count": len(records),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error fetching company data: {e}")
        return {"error": str(e), "status": "failed"}



@mcp.tool(
    name="get_quarter_data",
    description="Get financial data for all companies in a specific quarter (Q1_2025, Q2_2025, Q3_2025)"
)
def get_quarter_data(quarter: str) -> dict:
    """
    Fetch data for all companies in a specific quarter.

    Args:
        quarter: Quarter identifier (e.g., 'Q1_2025', 'Q2_2025', 'Q3_2025')

    Returns:
        Dictionary with all company data for that quarter
    """
    try:
        records = get_records_by_quarter(quarter)
        if not records:
            return {
                "error": f"No data found for quarter: {quarter}",
                "status": "not_found"
            }

        return {
            "quarter": quarter,
            "records": records,
            "companies": [r["company"] for r in records],
            "count": len(records),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error fetching quarter data: {e}")
        return {"error": str(e), "status": "failed"}



@mcp.tool(
    name="analyze_metrics",
    description="Analyze specific metrics (revenue, profit, growth_yoy, attrition_rate, employee_count) across multiple records"
)
def analyze_metrics(record_ids: List[str], metric: str) -> dict:
    """
    Calculate statistics and trends for a metric across records.

    Args:
        record_ids: List of record IDs (e.g., ['WAND_Q1_2025', 'JIO_Q2_2025', ...])
        metric: Metric to analyze (revenue, profit, growth_yoy, employee_count, attrition_rate)

    Returns:
        Dictionary with average, max, min, trend analysis
    """
    try:
        result = calculate_metrics(record_ids, metric)
        result["status"] = "success" if "error" not in result else "failed"
        return result
    except Exception as e:
        logger.error(f"Error analyzing metrics: {e}")
        return {"error": str(e), "status": "failed"}



@mcp.tool(
    name="compare_companies",
    description="Compare two companies on a specific metric (revenue, profit, growth_yoy, attrition_rate, employee_count)"
)
def compare_two_companies(company1: str, company2: str, metric: str = "revenue") -> dict:
    """
    Compare two companies on a specific financial metric.

    Args:
        company1: First company name (e.g., 'Wand AI')
        company2: Second company name (e.g., 'Jio Platforms Limited')
        metric: Metric to compare (default: revenue)

    Returns:
        Dictionary with comparison results
    """
    try:
        result = compare_companies(company1, company2, metric)
        result["status"] = "success" if "error" not in result else "failed"
        return result
    except Exception as e:
        logger.error(f"Error comparing companies: {e}")
        return {"error": str(e), "status": "failed"}



@mcp.tool(
    name="generate_plotly_json",
    description="Generate actual Plotly chart JSON that can be directly rendered in Streamlit. Returns complete figure JSON."
)
def generate_plotly_json(
    chart_type: str,
    company_names: List[str],
    metric: str,
    title: str
) -> dict:
    """
    Generate complete Plotly figure JSON for direct rendering.

    Args:
        chart_type: 'line', 'bar', or 'pie'
        company_names: List of companies (e.g., ['Wand AI', 'Jio Platforms Limited'])
        metric: Metric to visualize (revenue, profit, growth_yoy, attrition_rate, employee_count)
        title: Chart title

    Returns:
        Dictionary with Plotly figure JSON string and metadata
    """
    try:
        traces = []
        
        if chart_type == "line":
            for company in company_names:
                records = get_records_by_company(company)
                if records:
                    quarters = [r["quarter"].replace("_", " ") for r in records]
                    values = [r.get(metric, 0) for r in records]
                    
                    trace = {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": company,
                        "x": quarters,
                        "y": values,
                        "line": {"width": 3},
                        "marker": {"size": 10}
                    }
                    traces.append(trace)
        
        elif chart_type == "bar":
            for company in company_names:
                records = get_records_by_company(company)
                if records:
                    quarters = [r["quarter"].replace("_", " ") for r in records]
                    values = [r.get(metric, 0) for r in records]
                    
                    trace = {
                        "type": "bar",
                        "name": company,
                        "x": quarters,
                        "y": values
                    }
                    traces.append(trace)
        
        elif chart_type == "pie":
            labels = []
            values = []
            for company in company_names:
                records = get_records_by_company(company)
                if records:
                    total = sum(r.get(metric, 0) for r in records)
                    labels.append(company)
                    values.append(total)
            
            traces = [{
                "type": "pie",
                "labels": labels,
                "values": values,
                "hole": 0.3
            }]
        
        layout = {
            "title": title,
            "template": "plotly_white",
            "height": 500
        }
        
        if chart_type != "pie":
            layout["xaxis"] = {"title": "Quarter"}
            layout["yaxis"] = {"title": metric.replace("_", " ").title()}
        
        figure = {
            "data": traces,
            "layout": layout
        }
        
        import json
        return {
            "status": "success",
            "chart_type": chart_type,
            "metric": metric,
            "companies": company_names,
            "plotly_json": json.dumps(figure),
            "chart_id": f"{chart_type}_{metric}_{len(company_names)}_companies"
        }
    
    except Exception as e:
        logger.error(f"Error generating Plotly JSON: {e}")
        return {"error": str(e), "status": "failed"}


@mcp.tool(
    name="generate_report",
    description="Generate comprehensive financial report summary from multiple records"
)
def generate_report(record_ids: List[str], report_title: str = "Financial Analysis Report") -> dict:
    """
    Generate comprehensive report from financial records.

    Args:
        record_ids: List of record IDs to include in report (e.g., ['WAND_Q1_2025', 'JIO_Q2_2025', ...])
        report_title: Title for the report

    Returns:
        Dictionary with structured report data
    """
    try:
        summary = generate_report_summary(record_ids)
        if "error" in summary:
            return {"error": summary["error"], "status": "failed"}

        report = {
            "title": report_title,
            "summary": summary,
            "record_ids": record_ids,
            "generated_at": "2025-10-05T20:59:00",
            "status": "success"
        }
        return report
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {"error": str(e), "status": "failed"}



if __name__ == "__main__":
    import asyncio

    async def main():
        logger.info("Starting Companies Analysis FastMCP on http://127.0.0.1:4211/mcp")
        await mcp.run_async(
            transport="streamable-http",
            host="127.0.0.1",
            port=4211,
            path="/mcp",
            log_level="info"
        )

    asyncio.run(main())

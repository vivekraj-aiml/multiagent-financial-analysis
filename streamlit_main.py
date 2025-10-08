"""
Streamlit UI for Multi-Agent Financial Analysis System
Analyzes Wand AI, Jio Platforms Limited, and Nityo Infotech financial data
"""
import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd
from crew_multiagent import run_multi_agent_analysis
from sample_dataset import get_all_records

# Page configuration
st.set_page_config(
    page_title="Financial Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"> Multi-Agent Financial Analysis System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Analysis for Wand AI, Jio Platforms Limited, and Nityo Infotech</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.subheader("Quick Queries")
    query_options = {
        "Custom Query": "",
        "Revenue & Growth Comparison": "Compare revenue and growth trends for Wand AI and Jio Platforms across Q1-Q3 2025",
        "Profitability Analysis": "Analyze profit margins and profitability trends for all three companies in Q2 and Q3 2025",
        "Employee Metrics": "Compare employee count and attrition rates across Wand AI, Jio Platforms, and Nityo Infotech for all quarters",
        "Quarterly Performance": "Provide a comprehensive quarterly performance analysis for all companies focusing on revenue and deal value",
        "Growth Rate Leaders": "Identify which company has the highest growth rate and analyze their key success factors"
    }
    
    selected_query = st.selectbox("Select a query template:", list(query_options.keys()))
    
    st.markdown("---")
    
    st.subheader("Your Analysis Request")
    if selected_query == "Custom Query":
        user_query = st.text_area(
            "Enter your custom analysis request:",
            value="Compare revenue and growth trends for Wand AI and Jio Platforms across Q1-Q3 2025",
            height=150,
            help="Describe what financial analysis you need"
        )
    else:
        user_query = st.text_area(
            "Edit query or use as-is:",
            value=query_options[selected_query],
            height=150,
            help="You can modify the template query"
        )
    analyze_btn = st.button(" Run Analysis", type="primary", use_container_width=True)
    
    st.markdown("---")
    
if analyze_btn:
    if not user_query.strip():
        st.error(" Please enter an analysis request!")
    else:

        progress_container = st.container()
        with progress_container:
            st.markdown("###  Agent Workflow in Progress")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text(" Initializing multi-agent system...")
            progress_bar.progress(10)
    
        try:
            status_text.text(" Planning Agent: Breaking down request...")
            progress_bar.progress(25)
            
            result = run_multi_agent_analysis(user_query, verbose=False)
            
            status_text.text(" Analysis Agent: Processing financial data...")
            progress_bar.progress(50)
            
            status_text.text(" Visualization Agent: Creating charts...")
            progress_bar.progress(75)
            
            status_text.text(" Report Agent: Generating final report...")
            progress_bar.progress(90)
            
            if result and result["status"] == "success":
                progress_bar.progress(100)
                status_text.text(" Analysis completed successfully!")
                
                import time
                time.sleep(1)
                progress_container.empty()
                
                st.markdown("---")
                st.markdown("##  Analysis Results")
                
                task_outputs = result.get("task_outputs", {})
                
                viz_output = None
                for task_desc, output in task_outputs.items():
                    if "visualization" in task_desc.lower() or "chart" in str(task_desc).lower() or "plotly" in str(output).lower():
                        viz_output = output
                        break
                
                st.markdown("### Interactive Visualizations")
                
                charts_rendered = False
                
                if viz_output:
                    try:
                        viz_output_clean = str(viz_output).strip()
                        
                        if viz_output_clean.startswith("```json"):
                            viz_output_clean = viz_output_clean.replace("```json", "").replace("```", "").strip()
                        elif viz_output_clean.startswith("```"):
                            viz_output_clean = viz_output_clean.replace("```", "").strip()
                        
                        charts_data = json.loads(viz_output_clean)
                        
                        if isinstance(charts_data, list) and len(charts_data) > 0:
                            num_charts = len(charts_data)
                            
                            for idx in range(0, num_charts, 2):
                                cols = st.columns(2)
                                
                                chart_obj = charts_data[idx]
                                plotly_json_str = chart_obj.get("plotly_json", "")
                                
                                if plotly_json_str:
                                    try:
                                        fig_dict = json.loads(plotly_json_str)
                                        fig = go.Figure(fig_dict)
                                        
                                        with cols[0]:
                                            st.plotly_chart(fig, use_container_width=True)
                                            charts_rendered = True
                                    except Exception as e:
                                        with cols[0]:
                                            st.error(f"Chart {idx+1} rendering failed: {str(e)[:100]}")
                                
                                if idx + 1 < num_charts:
                                    chart_obj = charts_data[idx + 1]
                                    plotly_json_str = chart_obj.get("plotly_json", "")
                                    
                                    if plotly_json_str:
                                        try:
                                            fig_dict = json.loads(plotly_json_str)
                                            fig = go.Figure(fig_dict)
                                            
                                            with cols[1]:
                                                st.plotly_chart(fig, use_container_width=True)
                                                charts_rendered = True
                                        except Exception as e:
                                            with cols[1]:
                                                st.error(f"Chart {idx+2} rendering failed: {str(e)[:100]}")
                        
                        elif isinstance(charts_data, dict) and "plotly_json" in charts_data:
                        
                            try:
                                fig_dict = json.loads(charts_data["plotly_json"])
                                fig = go.Figure(fig_dict)
                                st.plotly_chart(fig, use_container_width=True)
                                charts_rendered = True
                            except Exception as e:
                                st.error(f"Chart rendering failed: {str(e)[:100]}")
                        
                    except json.JSONDecodeError as e:
                        st.warning(f" Could not parse agent-generated charts: {str(e)[:100]}")

                if not charts_rendered:
                    st.info(" Generating fallback charts from dataset...")
                    
                    records = get_all_records()
                    df = pd.DataFrame(records)
                    
                    companies_mentioned = []
                    for company in df['company'].unique():
                        if company.lower() in user_query.lower():
                            companies_mentioned.append(company)
                    
                    if not companies_mentioned:
                        companies_mentioned = df['company'].unique().tolist()
                    
                    df_filtered = df[df['company'].isin(companies_mentioned)]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig1 = go.Figure()
                        for company in companies_mentioned:
                            company_data = df_filtered[df_filtered['company'] == company]
                            if not company_data.empty:
                                fig1.add_trace(go.Scatter(
                                    x=company_data['quarter'].str.replace('_', ' '),
                                    y=company_data['revenue'],
                                    mode='lines+markers',
                                    name=company,
                                    line=dict(width=3),
                                    marker=dict(size=10)
                                ))
                        fig1.update_layout(
                            title="Revenue Trends Q1-Q3 2025",
                            xaxis_title="Quarter",
                            yaxis_title="Revenue (INR Crores)",
                            template="plotly_white",
                            height=450
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        fig2 = go.Figure()
                        for company in companies_mentioned:
                            company_data = df_filtered[df_filtered['company'] == company]
                            if not company_data.empty:
                                fig2.add_trace(go.Scatter(
                                    x=company_data['quarter'].str.replace('_', ' '),
                                    y=company_data['growth_yoy'],
                                    mode='lines+markers',
                                    name=company,
                                    line=dict(width=3),
                                    marker=dict(size=10)
                                ))
                        fig2.update_layout(
                            title="YoY Growth Rate Comparison",
                            xaxis_title="Quarter",
                            yaxis_title="Growth Rate (%)",
                            template="plotly_white",
                            height=450
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    if "profit" in user_query.lower() or "profitability" in user_query.lower():
                        col3, col4 = st.columns(2)
                        
                        with col3:
                            fig3 = go.Figure()
                            for company in companies_mentioned:
                                company_data = df_filtered[df_filtered['company'] == company]
                                if not company_data.empty:
                                    fig3.add_trace(go.Bar(
                                        x=company_data['quarter'].str.replace('_', ' '),
                                        y=company_data['profit'],
                                        name=company
                                    ))
                            fig3.update_layout(
                                title="Profit Comparison",
                                xaxis_title="Quarter",
                                yaxis_title="Profit (INR Crores)",
                                template="plotly_white",
                                height=450
                            )
                            st.plotly_chart(fig3, use_container_width=True)
                    
                    if "attrition" in user_query.lower() or "employee" in user_query.lower():
                        col5, col6 = st.columns(2)
                        
                        with col5:
                            fig4 = go.Figure()
                            for company in companies_mentioned:
                                company_data = df_filtered[df_filtered['company'] == company]
                                if not company_data.empty:
                                    fig4.add_trace(go.Scatter(
                                        x=company_data['quarter'].str.replace('_', ' '),
                                        y=company_data['attrition_rate'],
                                        mode='lines+markers',
                                        name=company,
                                        line=dict(width=3)
                                    ))
                            fig4.update_layout(
                                title="Attrition Rate Trends",
                                xaxis_title="Quarter",
                                yaxis_title="Attrition Rate (%)",
                                template="plotly_white",
                                height=450
                            )
                            st.plotly_chart(fig4, use_container_width=True)
                
                st.markdown("---")
                
                st.markdown("###  Comprehensive Analysis Report")
                with st.expander("Click to view full report", expanded=True):
                    st.markdown(result["result"])
                
                
                st.markdown("---")
                col_meta1, col_meta2, col_meta3 = st.columns(3)
                with col_meta1:
                    st.metric("Agents Used", result.get("agents_used", "N/A"))
                with col_meta2:
                    st.metric("Tasks Completed", result.get("tasks_completed", "N/A"))
                with col_meta3:
                    st.metric("Status", " Success")
                
            
            else:
                progress_bar.progress(0)
                status_text.text(" Analysis failed")
                st.error(f" Analysis failed: {result.get('error', 'Unknown error')}")

        
        except Exception as e:
            st.error(f" Unexpected error: {str(e)}")
else:
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ###  Companies
        - **Wand AI** - AI SaaS startup
        - **Jio Platforms** - Telecom giant
        - **Nityo Infotech** - IT services
        """)
        
    with col2:
        st.markdown("""
        ### Time Period
        - **Q1 2025** (Jan-Mar)
        - **Q2 2025** (Apr-Jun)
        - **Q3 2025** (Jul-Sep)
        """)

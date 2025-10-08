"""
Sample dataset for Indian & global company financial data.
Companies: Wand AI, Jio Platforms Limited, Nityo Infotech with quarterly data.
"""
from typing import Dict, List, Optional

# Quarter format
QUARTERS = ["Q1_2025", "Q2_2025", "Q3_2025"]

# Optimized and up-to-date sample data (INR Crores)
FINANCIAL_DATA = {
    # Jio Platforms Limited (Based on RIL, Quarter ended June/Sept/Dec 2024, est. INR crores)
    # Reference: https://www.ril.com/InvestorRelations/FinancialReporting.aspx and news
    "JIO_Q1_2025": {
        "id": "JIO_Q1_2025",
        "company": "Jio Platforms Limited",
        "quarter": "Q1_2025",
        "revenue": 31100,           # Revenue for Jio Platforms, Q1 FY25 (INR Crores)
        "profit": 5130,             # Net profit (estimate)
        "growth_yoy": 12.8,         # YoY growth
        "employee_count": 91700,    
        "attrition_rate": 8.9,      # Industry estimate (conservative, for large stable orgs)
        "deal_value": 2300,         # Sample: major deals closed in quarter (approx)
        "sector": "Telecom/Digital Services"
    },
    "JIO_Q2_2025": {
        "id": "JIO_Q2_2025",
        "company": "Jio Platforms Limited",
        "quarter": "Q2_2025",
        "revenue": 32050,
        "profit": 5375,
        "growth_yoy": 13.5,
        "employee_count": 92400,
        "attrition_rate": 8.6,
        "deal_value": 2400,
        "sector": "Telecom/Digital Services"
    },
    "JIO_Q3_2025": {
        "id": "JIO_Q3_2025",
        "company": "Jio Platforms Limited",
        "quarter": "Q3_2025",
        "revenue": 33100,
        "profit": 5610,
        "growth_yoy": 14.2,
        "employee_count": 93000,
        "attrition_rate": 8.5,
        "deal_value": 2500,
        "sector": "Telecom/Digital Services"
    },
    # https://www.nityo.com/
    "NITYO_Q1_2025": {
        "id": "NITYO_Q1_2025",
        "company": "Nityo Infotech",
        "quarter": "Q1_2025",
        "revenue": 1350,               
        "profit": 210,                 
        "growth_yoy": 10.5,
        "employee_count": 25200,
        "attrition_rate": 14.2,        
        "deal_value": 560,              
        "sector": "IT Services"
    },
    "NITYO_Q2_2025": {
        "id": "NITYO_Q2_2025",
        "company": "Nityo Infotech",
        "quarter": "Q2_2025",
        "revenue": 1410,
        "profit": 220,
        "growth_yoy": 12.3,
        "employee_count": 25450,
        "attrition_rate": 13.8,
        "deal_value": 600,
        "sector": "IT Services"
    },
    "NITYO_Q3_2025": {
        "id": "NITYO_Q3_2025",
        "company": "Nityo Infotech",
        "quarter": "Q3_2025",
        "revenue": 1485,
        "profit": 235,
        "growth_yoy": 13.7,
        "employee_count": 25700,
        "attrition_rate": 13.2,
        "deal_value": 670,
        "sector": "IT Services"
    },
    "WAND_Q1_2025": {
        "id": "WAND_Q1_2025",
        "company": "Wand AI",
        "quarter": "Q1_2025",
        "revenue": 92,            
        "profit": 8,
        "growth_yoy": 41.0,        # High growth!
        "employee_count": 130,
        "attrition_rate": 22.5,    # Startups, high attrition
        "deal_value": 24,
        "sector": "AI SaaS"
    },
    "WAND_Q2_2025": {
        "id": "WAND_Q2_2025",
        "company": "Wand AI",
        "quarter": "Q2_2025",
        "revenue": 104,
        "profit": 12,
        "growth_yoy": 44.6,
        "employee_count": 142,
        "attrition_rate": 19.6,
        "deal_value": 32,
        "sector": "AI SaaS"
    },
    "WAND_Q3_2025": {
        "id": "WAND_Q3_2025",
        "company": "Wand AI",
        "quarter": "Q3_2025",
        "revenue": 120,
        "profit": 17,
        "growth_yoy": 48.5,
        "employee_count": 150,
        "attrition_rate": 16.0,
        "deal_value": 41,
        "sector": "AI SaaS"
    }
}

def get_all_companies() -> List[str]:
    """Get list of all companies."""
    return sorted({data["company"] for data in FINANCIAL_DATA.values()})

def get_all_records() -> List[Dict]:
    """Get all financial records."""
    return list(FINANCIAL_DATA.values())

def get_record_by_id(record_id: str) -> Optional[Dict]:
    """Get specific financial record by ID."""
    return FINANCIAL_DATA.get(record_id)

def get_records_by_company(company: str) -> List[Dict]:
    """Get all records for a specific company."""
    return [
        data for data in FINANCIAL_DATA.values()
        if data["company"].lower() == company.lower()
    ]

def get_records_by_quarter(quarter: str) -> List[Dict]:
    """Get all company records for a specific quarter."""
    return [
        data for data in FINANCIAL_DATA.values()
        if data["quarter"] == quarter
    ]

def calculate_metrics(record_ids: List[str], metric: str) -> Dict:
    """Calculate aggregate metrics for given records."""
    values = []
    records = []

    for rid in record_ids:
        record = get_record_by_id(rid)
        if record and metric in record:
            values.append(record[metric])
            records.append({
                "id": rid,
                "company": record["company"],
                "quarter": record["quarter"],
                metric: record[metric]
            })

    if not values:
        return {"error": f"No valid data for metric: {metric}"}

    avg_value = sum(values) / len(values)
    max_value = max(values)
    min_value = min(values)

    trend = "stable"
    if len(values) > 1:
        increasing = all(values[i] <= values[i+1] for i in range(len(values)-1))
        decreasing = all(values[i] >= values[i+1] for i in range(len(values)-1))
        trend = "upward" if increasing else "downward" if decreasing else "mixed"

    return {
        "metric": metric,
        "count": len(values),
        "average": round(avg_value, 2),
        "max": max_value,
        "min": min_value,
        "trend": trend,
        "records": records
    }

def compare_companies(company1: str, company2: str, metric: str = "revenue") -> Dict:
    """Compare two companies on a specific metric."""
    comp1_data = get_records_by_company(company1)
    comp2_data = get_records_by_company(company2)

    if not comp1_data or not comp2_data:
        return {"error": "One or both companies not found"}

    comp1_values = [r[metric] for r in comp1_data if metric in r]
    comp2_values = [r[metric] for r in comp2_data if metric in r]

    comp1_avg = sum(comp1_values) / len(comp1_values) if comp1_values else 0
    comp2_avg = sum(comp2_values) / len(comp2_values) if comp2_values else 0

    return {
        "company1": company1,
        "company2": company2,
        "metric": metric,
        "company1_avg": round(comp1_avg, 2),
        "company2_avg": round(comp2_avg, 2),
        "difference": round(comp1_avg - comp2_avg, 2),
        "leader": company1 if comp1_avg > comp2_avg else company2
    }

def generate_report_summary(record_ids: List[str]) -> Dict:
    """Generate comprehensive summary for given records."""
    if not record_ids:
        return {"error": "No records provided"}

    records = [get_record_by_id(rid) for rid in record_ids if get_record_by_id(rid)]
    if not records:
        return {"error": "No valid records found"}

    by_company = {}
    for record in records:
        company = record["company"]
        by_company.setdefault(company, []).append(record)

    summary = {
        "total_records": len(records),
        "companies": list(by_company.keys()),
        "company_count": len(by_company),
        "quarters": sorted({r["quarter"] for r in records}),
        "total_revenue": sum(r["revenue"] for r in records),
        "total_profit": sum(r["profit"] for r in records),
        "avg_growth": round(sum(r["growth_yoy"] for r in records) / len(records), 2),
        "by_company": {}
    }

    for company, company_records in by_company.items():
        summary["by_company"][company] = {
            "quarters": len(company_records),
            "total_revenue": sum(r["revenue"] for r in company_records),
            "avg_growth": round(sum(r["growth_yoy"] for r in company_records) / len(company_records), 2)
        }

    return summary
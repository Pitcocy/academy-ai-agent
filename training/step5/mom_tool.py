import pandas as pd
import os
from google.adk.tools import FunctionTool
from datetime import datetime
import re


def analyze_mom_data(period1: str, period2: str) -> dict:
    """Analyzes Month-over-Month (MoM) marketing data comparing two periods.
    
    Use this tool when the user wants to compare marketing performance between two periods.
    Periods should be in format like 'Feb 24', 'March 2025', 'Jan 25', etc.
    
    Args:
        period1 (str): First period to compare (e.g., 'Feb 24', 'March 2025')
        period2 (str): Second period to compare (e.g., 'Feb 25', 'March 2024')
    
    Returns:
        dict: A dictionary containing MoM analysis with status and comparison results
    """
    try:
        # Read the CSV file - try multiple possible paths
        file_paths = [
            "multi_tool_agent/step3_data.csv",
            "step3_data.csv", 
            "./step3_data.csv"
        ]
        
        df = None
        for file_path in file_paths:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                break
        
        if df is None:
            return {
                "status": "error",
                "error_message": "CSV file not found. Please ensure step3_data.csv is accessible."
            }
        
        # Convert event_month to datetime for easier filtering
        df['event_month'] = pd.to_datetime(df['event_month'])
        
        # Parse the period strings to datetime
        def parse_period(period_str):
            """Parse period string like 'Feb 24', 'March 2025' to datetime"""
            period_str = period_str.strip().lower()
            
            # Handle different formats
            if re.match(r'^[a-z]{3}\s+\d{2}$', period_str):  # 'feb 24'
                month_abbr, year_short = period_str.split()
                year = 2000 + int(year_short)
                return datetime.strptime(f"{month_abbr} {year}", "%b %Y")
            elif re.match(r'^[a-z]+\s+\d{4}$', period_str):  # 'march 2025'
                month_name, year = period_str.split()
                return datetime.strptime(f"{month_name} {year}", "%B %Y")
            elif re.match(r'^[a-z]{3}\s+\d{4}$', period_str):  # 'feb 2024'
                month_abbr, year = period_str.split()
                return datetime.strptime(f"{month_abbr} {year}", "%b %Y")
            else:
                raise ValueError(f"Unsupported period format: {period_str}")
        
        try:
            date1 = parse_period(period1)
            date2 = parse_period(period2)
        except ValueError as e:
            return {
                "status": "error",
                "error_message": f"Error parsing periods: {str(e)}. Please use formats like 'Feb 24', 'March 2025', etc."
            }
        
        # Filter data for each period
        period1_data = df[df['event_month'].dt.to_period('M') == date1.strftime('%Y-%m')]
        period2_data = df[df['event_month'].dt.to_period('M') == date2.strftime('%Y-%m')]
        
        if period1_data.empty:
            return {
                "status": "error",
                "error_message": f"No data found for period: {period1}"
            }
        
        if period2_data.empty:
            return {
                "status": "error",
                "error_message": f"No data found for period: {period2}"
            }
        
        # Calculate aggregated metrics for each period
        def calculate_period_metrics(data, period_name):
            return {
                "period": period_name,
                "total_sessions": int(data['sessions'].sum()),
                "total_conversions": int(data['conversions'].sum()),
                "avg_engagement_rate": round(data['engagement_rate'].mean(), 4),
                "total_users": int(data['total_users'].sum()),
                "total_new_users": int(data['new_users'].sum()),
                "unique_campaigns": len(data['campaign_name'].unique()),
                "channel_breakdown": data.groupby('channel_grouping')['sessions'].sum().to_dict()
            }
        
        metrics1 = calculate_period_metrics(period1_data, period1)
        metrics2 = calculate_period_metrics(period2_data, period2)
        
        # Calculate MoM changes
        def calculate_change(val1, val2):
            if val2 == 0:
                return "N/A" if val1 == 0 else "∞"
            return round(((val1 - val2) / val2) * 100, 2)
        
        mom_changes = {
            "sessions_change_pct": calculate_change(metrics1["total_sessions"], metrics2["total_sessions"]),
            "conversions_change_pct": calculate_change(metrics1["total_conversions"], metrics2["total_conversions"]),
            "engagement_rate_change_pct": calculate_change(metrics1["avg_engagement_rate"], metrics2["avg_engagement_rate"]),
            "users_change_pct": calculate_change(metrics1["total_users"], metrics2["total_users"]),
            "new_users_change_pct": calculate_change(metrics1["total_new_users"], metrics2["total_new_users"])
        }
        
        # Top performing campaigns comparison
        top_campaigns_p1 = period1_data.groupby('campaign_name')['sessions'].sum().sort_values(ascending=False).head(3).to_dict()
        top_campaigns_p2 = period2_data.groupby('campaign_name')['sessions'].sum().sort_values(ascending=False).head(3).to_dict()
        
        return {
            "status": "success",
            "comparison_summary": {
                "period1": metrics1,
                "period2": metrics2,
                "mom_changes": mom_changes
            },
            "top_campaigns": {
                period1: top_campaigns_p1,
                period2: top_campaigns_p2
            },
            "insights": {
                "sessions_trend": "increased" if mom_changes["sessions_change_pct"] != "N/A" and mom_changes["sessions_change_pct"] > 0 else "decreased",
                "conversions_trend": "increased" if mom_changes["conversions_change_pct"] != "N/A" and mom_changes["conversions_change_pct"] > 0 else "decreased",
                "engagement_trend": "improved" if mom_changes["engagement_rate_change_pct"] != "N/A" and mom_changes["engagement_rate_change_pct"] > 0 else "declined"
            }
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error analyzing MoM data: {str(e)}"
        }


# Create the MoM analysis tool
mom_tool = FunctionTool(func=analyze_mom_data) 
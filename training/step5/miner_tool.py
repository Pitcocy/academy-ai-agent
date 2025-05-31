import pandas as pd
import os
from google.adk.tools import FunctionTool


def analyze_marketing_data() -> dict:
    """Analyzes the marketing data from step3_data.csv file and provides basic insights.
    
    Use this tool when the user asks about marketing data, campaign performance, 
    or wants to know statistics about the data.
    
    Returns:
        dict: A dictionary containing marketing data insights with status and results
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
        
        # Basic dataset info
        total_rows = len(df)
        date_range = f"{df['event_month'].min()} to {df['event_month'].max()}"
        unique_channels = df['channel_grouping'].unique().tolist()
        
        # Top 5 campaigns by total sessions
        top_campaigns_sessions = df.groupby('campaign_name')['sessions'].sum().sort_values(ascending=False).head(5).to_dict()
        
        # Top 5 campaigns by total conversions  
        top_campaigns_conversions = df.groupby('campaign_name')['conversions'].sum().sort_values(ascending=False).head(5).to_dict()
        
        # Channel performance summary
        channel_summary = df.groupby('channel_grouping').agg({
            'sessions': 'sum',
            'conversions': 'sum', 
            'engagement_rate': 'mean'
        }).round(4).to_dict()
        
        # Overall totals
        total_sessions = int(df['sessions'].sum())
        total_conversions = int(df['conversions'].sum()) 
        avg_engagement_rate = round(df['engagement_rate'].mean(), 4)
        
        return {
            "status": "success",
            "dataset_overview": {
                "total_rows": total_rows,
                "date_range": date_range,
                "unique_channels": unique_channels,
                "total_campaigns": len(df['campaign_name'].unique())
            },
            "overall_metrics": {
                "total_sessions": total_sessions,
                "total_conversions": total_conversions,
                "average_engagement_rate": avg_engagement_rate
            },
            "top_campaigns_by_sessions": top_campaigns_sessions,
            "top_campaigns_by_conversions": top_campaigns_conversions,
            "channel_performance": channel_summary
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error analyzing data: {str(e)}"
        }


# Create the marketing analysis tool
marketing_tool = FunctionTool(func=analyze_marketing_data) 
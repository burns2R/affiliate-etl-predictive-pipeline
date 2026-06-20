# Pandas and Requests ETL data ingestion script

# Pandas and Requests ETL data ingestion script
import os
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

def category_name(campaign_id):
    """Custom campaign categorization module directly matching reporting logic"""
    if int(campaign_id) == 26406:
        return "Credit Offers"
    return "Other Financial Offers"

def fetch_standard_api():
    """Extracts from the modern partner JSON endpoint"""
    url = os.getenv("API_STANDARD_URL", "http://api_standard:5000/data")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        if not df.empty and 'total_clicks' in df.columns:
            df.rename(columns={'total_clicks': 'clicks'}, inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Standard API extraction failed: {e}")
        return pd.DataFrame()

def fetch_legacy_api():
    """Extracts and parses from the legacy partner XML endpoint"""
    url = os.getenv("API_LEGACY_URL", "http://api_legacy:5001/data")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        records = []
        for row in root.findall('.//row'):
            records.append({
                'date': row.find('date').text if row.find('date') is not None else None,
                'campaign_id': row.find('campaign_id').text if row.find('campaign_id') is not None else None,
                'campaign_name': row.find('campaign_name').text if row.find('campaign_name') is not None else None,
                'clicks': row.find('clicks').text if row.find('clicks') is not None else 0,
                'conversions': row.find('conversions').text if row.find('conversions') is not None else 0,
                'earnings': row.find('earnings').text if row.find('earnings') is not None else 0,
                'advertiser': row.find('advertiser').text if row.find('advertiser') is not None else 'Legacy'
            })
        return pd.DataFrame(records)
    except Exception as e:
        print(f"[ERROR] Legacy XML API extraction failed: {e}")
        return pd.DataFrame()

def main():
    print("[ETL] Initiating data ingestion sequence...")
    
    df_std = fetch_standard_api()
    df_leg = fetch_legacy_api()
    
    # Consolidate available extracts
    active_dfs = [df for df in [df_std, df_leg] if not df.empty]
    if not active_dfs:
        print("[ETL] No active datasets retrieved. Execution terminated.")
        return
        
    affiliate_df = pd.concat(active_dfs, ignore_index=True)
    
    # Production-grade cast transformations matching notebook constraints
    affiliate_df['earnings'] = affiliate_df['earnings'].astype(float)
    affiliate_df['clicks'] = affiliate_df['clicks'].astype(float)
    affiliate_df['conversions'] = affiliate_df['conversions'].astype(float)
    affiliate_df['campaign_id'] = affiliate_df['campaign_id'].astype(int)
    affiliate_df['date'] = pd.to_datetime(affiliate_df['date']).dt.date
    
    # Categorization mapping execution
    affiliate_df['category'] = affiliate_df['campaign_id'].apply(category_name)
    
    # Persistence layer ingestion
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@warehouse:5432/affiliate_warehouse")
    engine = create_engine(db_url)
    
    affiliate_df.to_sql('campaign_performance', con=engine, if_exists='append', index=False)
    print(f"[ETL] Successfully written {len(affiliate_df)} normalized records to warehouse.")

if __name__ == "__main__":
    main()
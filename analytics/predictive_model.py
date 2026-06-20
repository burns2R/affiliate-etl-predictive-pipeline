# Machine learning algorithm to optimize campaign traffic weights

# Machine learning algorithm to optimize campaign traffic weights
import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def run_optimization():
    print("[ANALYTICS] Fetching data for modeling optimization...")
    
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@warehouse:5432/affiliate_warehouse")
    engine = create_engine(db_url)
    
    try:
        df = pd.read_sql("SELECT campaign_id, campaign_name, clicks, earnings, category FROM campaign_performance;", con=engine)
    except Exception as e:
        print(f"[ANALYTICS ERROR] Unable to query target data warehouse: {e}")
        return
        
    if df.empty or df['clicks'].sum() == 0:
        print("[ANALYTICS] Insufficient historical click volume to run optimization models.")
        return

    # Rollup history at campaign granularity
    aggregated = df.groupby(['campaign_id', 'campaign_name', 'category']).agg({
        'clicks': 'sum',
        'earnings': 'sum'
    }).reset_index()
    
    # Compute base EPC (Earnings Per Click) metrics
    aggregated['EPC'] = aggregated['earnings'] / np.where(aggregated['clicks'] == 0, 1, aggregated['clicks'])
    
    optimized_output = []
    
    # Softmax traffic split calculation per category group to balance exploration/exploitation
    for category_group, cat_df in aggregated.groupby('category'):
        epc_values = cat_df['EPC'].values
        
        # Scaling temperature parameter (lower values drive greedier traffic shifts to high producers)
        temperature = 0.4
        exp_scaled = np.exp(epc_values / temperature)
        routing_weights = exp_scaled / np.sum(exp_scaled)
        
        cat_df['optimized_weight'] = np.round(routing_weights, 2)
        optimized_output.append(cat_df)
        
    final_model_df = pd.concat(optimized_output, ignore_index=True)
    
    # Standardize data shape for warehouse consumption
    payload = final_model_df[['campaign_id', 'campaign_name', 'category', 'optimized_weight', 'EPC']].rename(
        columns={'EPC': 'predicted_epc'}
    )
    
    payload.to_sql('traffic_weights_optimization', con=engine, if_exists='replace', index=False)
    print("[ANALYTICS] Optimization pass successful. Distributed traffic weights updated in database.")

if __name__ == "__main__":
    run_optimization()

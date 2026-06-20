# Mock API server for modern partner platforms (JSON response)

import random
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Standard Partner Affiliate API (JSON)",
    description="Enterprise API mocking performance data for Partners 1, 2, and 3 with realistic MoM growth trends.",
    version="1.0.0"
)

# --- Pydantic Schemas for Data Validation ---
class CampaignMetrics(BaseModel):
    campaign_id: str = Field(..., example="CMP-101")
    sub_campaign_id: str = Field(..., example="SUB-204")
    partner_id: str = Field(..., example="partner_1")
    date: str = Field(..., example="2026-03-15")
    clicks: int = Field(..., example=1250)
    leads_generated: int = Field(..., example=112)
    conversions: int = Field(..., example=24)
    total_earnings: float = Field(..., example=1450.50)
    clicks_cost: float = Field(..., example=620.00)

class ApiResponse(BaseModel):
    total_records: int
    start_date: str
    end_date: str
    data: List[CampaignMetrics]

# --- Deterministic Enterprise Mock Data Generator ---
def generate_historical_data(start_str: str, end_str: str) -> List[dict]:
    """
    Generates realistic, daily performance data for 15 campaigns across 3 partners.
    Includes an intentional ~21% MoM revenue improvement trend to back up the portfolio narrative.
    """
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")

    partners = ["partner_1", "partner_2", "partner_3"]
    
    # Pre-defined matrix of 15 campaigns and sub-campaigns to maintain semantic consistency
    campaign_pool = [
        {"id": f"CMP-{100+i}", "sub_id": f"SUB-{200+i}", "partner": partners[i % 3]}
        for i in range(1, 16)
    ]

    records = []
    current_date = start_date
    
    while current_date <= end_date:
        # Use date string hash as seed to ensure data is completely deterministic and stable per API call
        day_seed = hash(str(current_date))
        rng = random.Random(day_seed)
        
        # Calculate Month-over-Month scaling factor (~21% lift over a 5-month timeline)
        # January (Month 1) base is 1.0, February is 1.21, March is 1.46, etc.
        months_passed = (current_date.year - 2026) * 12 + (current_date.month - 1)
        growth_factor = (1.21) ** max(0, months_passed)

        for camp in campaign_pool:
            # Generate metrics with realistic variance
            base_clicks = rng.randint(800, 2500)
            clicks = int(base_clicks * rng.uniform(0.9, 1.1))
            
            # Conversion funnel logic (Clicks -> Leads -> Conversions)
            lead_conversion_rate = rng.uniform(0.06, 0.12)
            leads = int(clicks * lead_conversion_rate)
            
            sale_conversion_rate = rng.uniform(0.15, 0.25)
            conversions = int(leads * sale_conversion_rate)
            
            # Commercial financials influenced by our case study optimization growth factor
            base_payout_per_sale = rng.uniform(45.0, 65.0)
            total_earnings = round((conversions * base_payout_per_sale) * growth_factor, 2)
            
            # Traffic cost overhead (keeps ROI calculation interesting in analytics database)
            clicks_cost = round(clicks * rng.uniform(0.35, 0.55), 2)

            records.append({
                "campaign_id": camp["id"],
                "sub_campaign_id": camp["sub_id"],
                "partner_id": camp["partner"],
                "date": str(current_date),
                "clicks": clicks,
                "leads_generated": leads,
                "conversions": conversions,
                "total_earnings": total_earnings,
                "clicks_cost": clicks_cost
            })
            
        current_date += timedelta(days=1)
        
    return records

# --- API Endpoints ---
@app.get("/health", tags=["Infrastructure"])
def health_check():
    """Verify standard service uptime."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/campaign-performance", response_model=ApiResponse, tags=["Data Ingestion"])
def get_campaign_performance(
    start_date: str = Query(..., description="Start date window (YYYY-MM-DD)", example="2026-01-01"),
    end_date: str = Query(..., description="End date window (YYYY-MM-DD)", example="2026-05-31")
):
    """
    Primary ingestion endpoint. Returns multi-partner granular campaign metrics 
    chunked by date queries for structured ETL processing pipelines.
    """
    raw_data = generate_historical_data(start_date, end_date)
    
    return {
        "total_records": len(raw_data),
        "start_date": start_date,
        "end_date": end_date,
        "data": raw_data
    }

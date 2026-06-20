from fastapi import FastAPI
app = FastAPI()
@app.get("/data")
def get_data():
    return [
        {"date": "2026-06-20", "campaign_id": 26406, "campaign_name": "Modern Campaign", "total_clicks": 150, "conversions": 10, "earnings": 250.50, "advertiser": "StandardNet"}
    ]

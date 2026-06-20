from fastapi import FastAPI, Response
app = FastAPI()
@app.get("/data")
def get_data():
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <root>
        <row>
            <date>2026-06-20</date>
            <campaign_id>10882</campaign_id>
            <campaign_name>Legacy Campaign</campaign_name>
            <clicks>120</clicks>
            <conversions>8</conversions>
            <earnings>180.25</earnings>
            <advertiser>LegacyCorp</advertiser>
        </row>
    </root>'''
    return Response(content=xml_content, media_type="application/xml")

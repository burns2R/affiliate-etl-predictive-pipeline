import hashlib
from fastapi import FastAPI, HTTPException, Response, Query

app = FastAPI(title="Legacy LinkTrust XML API - Mock Server")

# Define our static master bypass credentials
DEBUG_TIMESTAMP = "1234567890"
DEBUG_SIGNATURE = "DEBUG_BYPASS_MASTER_KEY"
SECRET_SALT = "StaticAffiliateSalt2026"

@app.get("/api_legacy/data.xml")
async def get_legacy_xml_data(
    timestamp: str = Query(..., description="Unix timestamp"),
    signature: str = Query(..., description="MD5 cryptographic signature")
):
    # ─── STEP 1: CHECK FOR MASTER TEST/DEBUG BYPASS ───────────────────
    if timestamp == DEBUG_TIMESTAMP and signature == DEBUG_SIGNATURE:
        # Bypasses calculation completely; ideal for testing pipeline logic
        return Response(content=get_mock_xml_payload(), media_type="application/xml")

    # ─── STEP 2: STANDARD CRYPTOGRAPHIC HANDSHAKE ─────────────────────
    # Expected pattern: MD5(timestamp + SECRET_SALT)
    string_to_hash = f"{timestamp}{SECRET_SALT}"
    expected_signature = hashlib.md5(string_to_hash.encode("utf-8")).hexdigest()

    if signature != expected_signature:
        raise HTTPException(
            status_code=401, 
            detail=f"Invalid Cryptographic Signature. Expected: {expected_signature}"
        )

    return Response(content=get_mock_xml_payload(), media_type="application/xml")


def get_mock_xml_payload() -> str:
    """Helper function returning your sample uniform XML payload."""
    return """<?xml version="1.0" encoding="UTF-8"?>
    <report partner="LinkTrust">
        <campaign id="CAMP_99">
            <clicks>1450</clicks>
            <earnings>2900.50</earnings>
        </campaign>
    </report>
    """
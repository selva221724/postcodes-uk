import pytest
import httpx
from postcodes_mcp import get_postcode_details, bulk_postcode_lookup, nearest_postcodes

@pytest.mark.asyncio
async def test_get_postcode_details():
    result = await get_postcode_details("SW1A 1AA")  # UK Parliament postcode
    assert "Postcode: SW1A 1AA" in result
    assert "Latitude" in result
    assert "Longitude" in result

@pytest.mark.asyncio
async def test_bulk_postcode_lookup():
    result = await bulk_postcode_lookup(["SW1A 1AA", "EC1A 1BB"])
    assert len(result.split("---")) == 2
    assert "Postcode: SW1A 1AA" in result
    assert "Postcode: EC1A 1BB" in result

@pytest.mark.asyncio
async def test_nearest_postcodes():
    # Coordinates for central London
    result = await nearest_postcodes(51.5074, -0.1278)
    assert "Postcode:" in result
    assert "Latitude:" in result
    assert "Longitude:" in result

def test_format_postcode_details():
    from postcodes_mcp import format_postcode_details
    
    sample_details = {
        "postcode": "SW1A 1AA",
        "latitude": 51.5010,
        "longitude": -0.1415,
        "region": "London",
        "country": "England",
        "admin_district": "Westminster",
        "parliamentary_constituency": "Cities of London and Westminster"
    }
    
    formatted = format_postcode_details(sample_details)
    assert "Postcode: SW1A 1AA" in formatted
    assert "Latitude: 51.5010" in formatted
    assert "Country: England" in formatted

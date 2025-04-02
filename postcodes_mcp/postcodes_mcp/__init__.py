from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("postcodes")

# Constants
POSTCODES_API_BASE = "https://api.postcodes.io/postcodes"
USER_AGENT = "postcodes-uk-app/1.0"

async def make_postcodes_request(url: str, method: str = 'get', json: dict | None = None) -> dict[str, Any] | None:
    """Make a request to the Postcodes.io API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            if method == 'get':
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method == 'post':
                response = await client.post(url, headers=headers, json=json, timeout=30.0)
            else:
                return None
            
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_postcode_details(details: dict) -> str:
    """Format postcode details into a readable string."""
    if not details:
        return "No details found for this postcode."
    
    return f"""
Postcode: {details.get('postcode', 'N/A')}
Latitude: {details.get('latitude', 'N/A')}
Longitude: {details.get('longitude', 'N/A')}
Region: {details.get('region', 'N/A')}
Country: {details.get('country', 'N/A')}
Administrative Area: {details.get('admin_district', 'N/A')}
Parliamentary Constituency: {details.get('parliamentary_constituency', 'N/A')}
"""

@mcp.tool()
async def get_postcode_details(postcode: str) -> str:
    """Get details for a UK postcode.

    Args:
        postcode: UK postcode to look up
    """
    url = f"{POSTCODES_API_BASE}/{postcode}"
    data = await make_postcodes_request(url)

    if not data or 'result' not in data:
        return "Unable to fetch details for this postcode."

    return format_postcode_details(data['result'])

@mcp.tool()
async def bulk_postcode_lookup(postcodes: list[str]) -> str:
    """Perform bulk lookup of multiple postcodes.

    Args:
        postcodes: List of postcodes to look up
    """
    url = f"{POSTCODES_API_BASE}"
    data = await make_postcodes_request(url, method='post', json={"postcodes": postcodes})

    if not data or 'result' not in data:
        return "Unable to fetch details for the postcodes."

    formatted_results = []
    for result in data['result']:
        if result['result']:
            formatted_results.append(format_postcode_details(result['result']))
        else:
            formatted_results.append(f"No details found for {result['query']}")

    return "\n---\n".join(formatted_results)

@mcp.tool()
async def nearest_postcodes(latitude: float, longitude: float) -> str:
    """Find nearest postcodes by coordinates.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    """
    url = f"{POSTCODES_API_BASE}"
    params = {
        "lon": longitude,
        "lat": latitude
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return "Unable to fetch nearest postcodes."

    if not data or 'result' not in data:
        return "No postcodes found near these coordinates."

    formatted_results = []
    for postcode in data['result']:
        formatted_results.append(format_postcode_details(postcode))

    return "\n---\n".join(formatted_results)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

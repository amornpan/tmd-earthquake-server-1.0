#!/usr/bin/env python3
"""
TMD Earthquake MCP Server
A Model Context Protocol server for accessing Thai Meteorological Department earthquake data
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("tmd-earthquake-server")

# API Configuration
TMD_API_URL = "https://data.tmd.go.th/api/DailySeismicEvent/v1/"
API_PARAMS = {"uid": "api", "ukey": "api12345"}

# Helper Functions
async def fetch_earthquake_data() -> Optional[str]:
    """Fetch earthquake data from TMD API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TMD_API_URL,
                params=API_PARAMS,
                timeout=30.0
            )
            response.raise_for_status()
            return response.text
    except Exception as e:
        logger.error(f"Error fetching data from TMD API: {e}")
        return None

def parse_earthquake_xml(xml_data: str) -> List[Dict[str, Any]]:
    """Parse earthquake XML data into structured format"""
    earthquakes = []
    try:
        root = ET.fromstring(xml_data)
        
        for eq in root.findall('.//DailyEarthquakes'):
            earthquake = {}
            
            # Extract all fields
            fields = [
                'OriginThai', 'DateTimeUTC', 'DateTimeThai', 
                'Depth', 'Magnitude', 'Latitude', 'Longitude', 'TitleThai'
            ]
            
            for field in fields:
                elem = eq.find(field)
                if elem is not None:
                    earthquake[field] = elem.text
            
            # Convert numeric fields
            try:
                earthquake['Magnitude'] = float(earthquake.get('Magnitude', 0))
                earthquake['Latitude'] = float(earthquake.get('Latitude', 0))
                earthquake['Longitude'] = float(earthquake.get('Longitude', 0))
                earthquake['Depth'] = float(earthquake.get('Depth', '0').replace('km.', '').strip())
            except (ValueError, TypeError):
                pass
            
            earthquakes.append(earthquake)
            
    except ET.ParseError as e:
        logger.error(f"Error parsing XML: {e}")
    
    return earthquakes

def format_earthquake_info(earthquake: Dict[str, Any]) -> str:
    """Format earthquake information for display"""
    return f"""
🌍 **แผ่นดินไหว: {earthquake.get('OriginThai', 'ไม่ทราบสถานที่')}**
📅 เวลา (ไทย): {earthquake.get('DateTimeThai', 'ไม่ทราบ')}
📅 เวลา (UTC): {earthquake.get('DateTimeUTC', 'ไม่ทราบ')}
📊 ขนาด: {earthquake.get('Magnitude', 'ไม่ทราบ')} แมกนิจูด
🎯 ความลึก: {earthquake.get('Depth', 'ไม่ทราบ')} กม.
📍 พิกัด: {earthquake.get('Latitude', 'ไม่ทราบ')}, {earthquake.get('Longitude', 'ไม่ทราบ')}
💬 {earthquake.get('TitleThai', '')}
"""

# Tools
@mcp.tool()
async def get_earthquakes(limit: int = 10) -> str:
    """
    Get recent earthquake data from TMD
    
    Args:
        limit: Maximum number of earthquakes to return (default: 10)
    """
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    if not earthquakes:
        return "ไม่พบข้อมูลแผ่นดินไหว"
    
    # Limit the results
    earthquakes = earthquakes[:limit]
    
    result = f"พบข้อมูลแผ่นดินไหว {len(earthquakes)} รายการล่าสุด:\n\n"
    for eq in earthquakes:
        result += format_earthquake_info(eq) + "\n" + "-"*50 + "\n"
    
    return result

@mcp.tool()
async def get_earthquakes_by_magnitude(min_magnitude: float = 3.0) -> str:
    """
    Get earthquakes filtered by minimum magnitude
    
    Args:
        min_magnitude: Minimum magnitude to filter (default: 3.0)
    """
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    # Filter by magnitude
    filtered = [eq for eq in earthquakes if eq.get('Magnitude', 0) >= min_magnitude]
    
    if not filtered:
        return f"ไม่พบแผ่นดินไหวที่มีขนาดตั้งแต่ {min_magnitude} แมกนิจูดขึ้นไป"
    
    result = f"พบแผ่นดินไหวขนาด {min_magnitude}+ แมกนิจูด จำนวน {len(filtered)} รายการ:\n\n"
    for eq in filtered:
        result += format_earthquake_info(eq) + "\n" + "-"*50 + "\n"
    
    return result

@mcp.tool()
async def get_earthquakes_by_location(location: str) -> str:
    """
    Get earthquakes filtered by location/country
    
    Args:
        location: Location or country name to search (in Thai or English)
    """
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    # Filter by location (case insensitive)
    location_lower = location.lower()
    filtered = [
        eq for eq in earthquakes 
        if location_lower in eq.get('OriginThai', '').lower() or
           location_lower in eq.get('TitleThai', '').lower()
    ]
    
    if not filtered:
        return f"ไม่พบแผ่นดินไหวในพื้นที่ '{location}'"
    
    result = f"พบแผ่นดินไหวในพื้นที่ '{location}' จำนวน {len(filtered)} รายการ:\n\n"
    for eq in filtered:
        result += format_earthquake_info(eq) + "\n" + "-"*50 + "\n"
    
    return result

@mcp.tool()
async def get_earthquake_summary() -> str:
    """
    Get a summary of recent earthquake activity
    """
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    if not earthquakes:
        return "ไม่พบข้อมูลแผ่นดินไหว"
    
    # Calculate statistics
    total = len(earthquakes)
    magnitudes = [eq.get('Magnitude', 0) for eq in earthquakes]
    avg_magnitude = sum(magnitudes) / len(magnitudes) if magnitudes else 0
    max_magnitude = max(magnitudes) if magnitudes else 0
    min_magnitude = min(magnitudes) if magnitudes else 0
    
    # Count by location
    locations = {}
    for eq in earthquakes:
        loc = eq.get('OriginThai', 'ไม่ทราบ')
        locations[loc] = locations.get(loc, 0) + 1
    
    # Find most recent
    most_recent = earthquakes[0] if earthquakes else None
    
    result = f"""
📊 **สรุปข้อมูลแผ่นดินไหวล่าสุด**

📈 **สถิติทั่วไป:**
• จำนวนแผ่นดินไหวทั้งหมด: {total} ครั้ง
• ขนาดเฉลี่ย: {avg_magnitude:.2f} แมกนิจูด
• ขนาดสูงสุด: {max_magnitude} แมกนิจูด
• ขนาดต่ำสุด: {min_magnitude} แมกนิจูด

📍 **แผ่นดินไหวแยกตามพื้นที่:**
"""
    for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
        result += f"• {loc}: {count} ครั้ง\n"
    
    if most_recent:
        result += f"\n🔴 **แผ่นดินไหวล่าสุด:**\n{format_earthquake_info(most_recent)}"
    
    return result

@mcp.tool()
async def get_large_earthquakes(magnitude_threshold: float = 5.0) -> str:
    """
    Get earthquakes that are considered large (default: magnitude >= 5.0)
    
    Args:
        magnitude_threshold: Magnitude threshold for large earthquakes (default: 5.0)
    """
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    # Filter large earthquakes
    large_quakes = [eq for eq in earthquakes if eq.get('Magnitude', 0) >= magnitude_threshold]
    
    if not large_quakes:
        return f"✅ ไม่พบแผ่นดินไหวขนาดใหญ่ (>= {magnitude_threshold} แมกนิจูด) ในช่วงนี้"
    
    result = f"⚠️ **พบแผ่นดินไหวขนาดใหญ่ {len(large_quakes)} ครั้ง** (>= {magnitude_threshold} แมกนิจูด):\n\n"
    for eq in large_quakes:
        result += format_earthquake_info(eq) + "\n" + "-"*50 + "\n"
    
    return result

# Resources
@mcp.resource("earthquake://latest")
async def get_latest_earthquake() -> str:
    """Get the most recent earthquake"""
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    if not earthquakes:
        return "ไม่พบข้อมูลแผ่นดินไหว"
    
    latest = earthquakes[0]
    return f"แผ่นดินไหวล่าสุด:\n{format_earthquake_info(latest)}"

@mcp.resource("earthquake://today")
async def get_today_earthquakes() -> str:
    """Get earthquakes from today (Thai time)"""
    xml_data = await fetch_earthquake_data()
    if not xml_data:
        return "ไม่สามารถดึงข้อมูลแผ่นดินไหวได้ในขณะนี้"
    
    earthquakes = parse_earthquake_xml(xml_data)
    
    # Filter for today's earthquakes (Thai time)
    today = datetime.now().strftime('%Y-%m-%d')
    today_quakes = [
        eq for eq in earthquakes 
        if eq.get('DateTimeThai', '').startswith(today)
    ]
    
    if not today_quakes:
        return f"ไม่พบแผ่นดินไหวในวันที่ {today}"
    
    result = f"แผ่นดินไหววันนี้ ({today}) มี {len(today_quakes)} ครั้ง:\n\n"
    for eq in today_quakes:
        result += format_earthquake_info(eq) + "\n" + "-"*50 + "\n"
    
    return result

# Main entry point
if __name__ == "__main__":
    # Run the server
    mcp.run(transport='stdio')

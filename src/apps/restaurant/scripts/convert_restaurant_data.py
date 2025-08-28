#!/usr/bin/env python3
"""
Script to convert restaurant data from various formats to our JSON structure
"""

import json
import re
from typing import Dict, Any, List


def extract_city_from_address(address: str) -> str:
    """Extract city name from address"""
    # Common patterns for city extraction
    patterns = [
        r'([^,]+), [^,]+ городская администрация',
        r'([^,]+), [^,]+ область',
        r'([^,]+), [^,]+ район',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, address)
        if match:
            return match.group(1).strip()
    
    # Fallback: try to extract city from common patterns
    if 'Усть-Каменогорск' in address:
        return 'Усть-Каменогорск'
    elif 'Алматы' in address:
        return 'Алматы'
    elif 'Астана' in address:
        return 'Астана'
    
    return "Unknown"


def extract_region_from_address(address: str) -> str:
    """Extract region name from address"""
    if 'Усть-Каменогорск городская администрация' in address:
        return 'Восточно-Казахстанская область'
    elif 'Алматы' in address:
        return 'Алматы'
    elif 'Астана' in address:
        return 'Астана'
    
    return "Unknown"


def clean_restaurant_name(name: str) -> str:
    """Clean restaurant name for display"""
    # Remove redundant city information
    name = re.sub(r', [^,]+ городская администрация$', '', name)
    name = re.sub(r', [^,]+ область$', '', name)
    
    # Limit length
    if len(name) > 100:
        name = name[:97] + "..."
    
    return name.strip()


def convert_restaurant_data(input_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert restaurant data to our format"""
    restaurants = []
    
    for item in input_data:
        # Handle different input formats
        if 'name' in item and 'lat' in item and 'lon' in item:
            # Already in our format
            restaurant = {
                "name": clean_restaurant_name(item['name']),
                "address": item.get('address', item['name']),
                "lat": float(item['lat']),
                "lon": float(item['lon']),
                "city": item.get('city', extract_city_from_address(item['name'])),
                "region": item.get('region', extract_region_from_address(item['name']))
            }
        elif 'address' in item and 'lat' in item and 'lon' in item:
            # Format with address field
            restaurant = {
                "name": clean_restaurant_name(item['address']),
                "address": item['address'],
                "lat": float(item['lat']),
                "lon": float(item['lon']),
                "city": item.get('city', extract_city_from_address(item['address'])),
                "region": item.get('region', extract_region_from_address(item['address']))
            }
        else:
            print(f"Warning: Skipping item with unknown format: {item}")
            continue
        
        restaurants.append(restaurant)
    
    return {"restaurants": restaurants}


def convert_from_csv_format(csv_data: str) -> Dict[str, Any]:
    """Convert from CSV-like format"""
    lines = csv_data.strip().split('\n')
    restaurants = []
    
    for line in lines[1:]:  # Skip header
        parts = line.split(',')
        if len(parts) >= 3:
            name = parts[0].strip().strip('"')
            lat = float(parts[1].strip())
            lon = float(parts[2].strip())
            
            restaurant = {
                "name": clean_restaurant_name(name),
                "address": name,
                "lat": lat,
                "lon": lon,
                "city": extract_city_from_address(name),
                "region": extract_region_from_address(name)
            }
            restaurants.append(restaurant)
    
    return {"restaurants": restaurants}


def main():
    """Main conversion function"""
    # Example: Convert from simple format
    simple_data = [
        {
            "name": "Проспект Каныша Сатпаева, 8а, Усть-Каменогорск, Усть-Каменогорск городская администрация",
            "lat": 49.899618,
            "lon": 82.618951
        },
        {
            "name": "Самарское шоссе, 5/1, Усть-Каменогорск, Усть-Каменогорск городская администрация",
            "lat": 49.898639,
            "lon": 82.634596
        }
    ]
    
    converted_data = convert_restaurant_data(simple_data)
    
    # Write the converted data
    with open('/app/src/assets/rstrnts_data_converted.json', 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)
    
    print("Conversion completed!")
    print(f"Converted {len(converted_data['restaurants'])} restaurants")
    
    for restaurant in converted_data['restaurants']:
        print(f"  - {restaurant['name']}")
        print(f"    📍 {restaurant['lat']}, {restaurant['lon']}")
        print(f"    🏙️  {restaurant['city']}, {restaurant['region']}")


if __name__ == '__main__':
    main()

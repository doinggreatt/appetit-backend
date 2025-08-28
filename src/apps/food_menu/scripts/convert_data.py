#!/usr/bin/env python3
"""
Script to convert appfood_data.json to menu_data.json format
"""

import json
import re
from typing import Dict, Any, List


def extract_price_from_formatted(price_formatted: str) -> float:
    """Extract numeric price from formatted string like '2490 ₸'"""
    if not price_formatted:
        return 0.0
    
    # Extract numbers from the string
    numbers = re.findall(r'\d+', price_formatted)
    if numbers:
        return float(numbers[0])
    return 0.0


def convert_modifier_to_category(modifier: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a modifier to a modifier category"""
    if modifier['type'] == 'sizes':
        return None  # Sizes are handled separately
    
    category = {
        "name": modifier['title'],
        "options": []
    }
    
    for option in modifier.get('options', []):
        price = extract_price_from_formatted(option.get('price_formatted', '0 ₸'))
        category['options'].append({
            "name": option['name'],
            "price": price
        })
    
    return category


def convert_product_to_food(product: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a product to a food item"""
    food = {
        "name": product['name'],
        "description": product.get('description', ''),
        "sizes": [],
        "modifier_categories": [],
        "priority": None  # Will be set during loading
    }
    
    # Handle sizes
    for modifier in product.get('modifiers', []):
        if modifier['type'] == 'sizes':
            for option in modifier.get('options', []):
                price = extract_price_from_formatted(option.get('price_formatted', '0 ₸'))
                food['sizes'].append({
                    "name": "Стандарт" if not option.get('name') else option['name'],
                    "price": price,
                    "is_new": False  # You can add logic to determine if it's new
                })
            break  # Only take the first sizes modifier
    
    # Handle other modifiers
    for modifier in product.get('modifiers', []):
        if modifier['type'] != 'sizes':
            category = convert_modifier_to_category(modifier)
            if category:
                food['modifier_categories'].append(category)
    
    return food


def convert_section_to_food_type(section: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a section to a food type"""
    food_type = {
        "name": section['title'],
        "foods": []
    }
    
    for product in section.get('products', []):
        food = convert_product_to_food(product)
        food_type['foods'].append(food)
    
    return food_type


def convert_appfood_to_menu_data(appfood_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert the entire appfood data structure to menu data format"""
    menu_data = {
        "food_types": []
    }
    
    for section in appfood_data.get('sections', []):
        food_type = convert_section_to_food_type(section)
        menu_data['food_types'].append(food_type)
    
    return menu_data


def main():
    """Main conversion function"""
    # Read the original data
    with open('/app/src/assets/appfood_data.json', 'r', encoding='utf-8') as f:
        appfood_data = json.load(f)
    
    # Convert to new format
    menu_data = convert_appfood_to_menu_data(appfood_data)
    
    # Write the converted data
    with open('/app/src/assets/menu_data_converted.json', 'w', encoding='utf-8') as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=2)
    
    print("Conversion completed!")
    print(f"Converted {len(menu_data['food_types'])} food types")
    
    total_foods = sum(len(ft['foods']) for ft in menu_data['food_types'])
    print(f"Total foods: {total_foods}")
    
    total_modifier_categories = sum(
        sum(len(food['modifier_categories']) for food in ft['foods'])
        for ft in menu_data['food_types']
    )
    print(f"Total modifier categories: {total_modifier_categories}")


if __name__ == '__main__':
    main()

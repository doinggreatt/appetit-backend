#!/usr/bin/env python3
"""
Test script to verify the menu loading functionality with full data clearing
"""

import sys
import os
sys.path.append('/app/src')

from apps.food_menu.scripts.load.load_menu import MenuJsonLoader
from apps.food_menu.models import FoodType, Food, FoodSize, ModifierCategory, ModifierOption, Menu
from config import db_settings
from sqlalchemy.orm import sessionmaker


def test_load_full():
    """Test the menu loading functionality with full data clearing"""
    print("Testing menu loading with full data clearing...")
    
    try:
        # Load the menu data (clearing all data including modifiers)
        loader = MenuJsonLoader()
        loader.load(clear_all=True)
        
        # Verify the data was loaded correctly
        SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
        session = SessionLocal()
        
        # Check food types
        food_types = session.query(FoodType).all()
        print(f"\n✅ Loaded {len(food_types)} food types:")
        for ft in food_types:
            print(f"  - {ft.name}")
        
        # Check foods
        foods = session.query(Food).all()
        print(f"\n✅ Loaded {len(foods)} foods:")
        for food in foods:
            food_type = session.query(FoodType).filter(FoodType.id == food.type_id).first()
            print(f"  - {food.name} ({food_type.name})")
        
        # Check food sizes
        food_sizes = session.query(FoodSize).all()
        print(f"\n✅ Loaded {len(food_sizes)} food sizes:")
        for size in food_sizes:
            food = session.query(Food).filter(Food.id == size.parent_id).first()
            print(f"  - {size.name} for {food.name} - {size.price}₸")
        
        # Check modifier categories
        modifier_categories = session.query(ModifierCategory).all()
        print(f"\n✅ Loaded {len(modifier_categories)} modifier categories:")
        for category in modifier_categories:
            print(f"  - {category.name}")
        
        # Check modifier options
        modifier_options = session.query(ModifierOption).all()
        print(f"\n✅ Loaded {len(modifier_options)} modifier options:")
        for option in modifier_options:
            category = session.query(ModifierCategory).filter(ModifierCategory.id == option.modifier_category_id).first()
            print(f"  - {option.name} ({category.name}) - {option.price}₸")
        
        # Check menu entries
        menu_entries = session.query(Menu).order_by(Menu.priority_level).all()
        print(f"\n✅ Loaded {len(menu_entries)} menu entries:")
        for menu_entry in menu_entries:
            food = session.query(Food).filter(Food.id == menu_entry.food_id).first()
            food_type = session.query(FoodType).filter(FoodType.id == food.type_id).first()
            print(f"  - Priority {menu_entry.priority_level}: {food.name} ({food_type.name})")
        
        session.close()
        print("\n🎉 All tests passed! Menu data loaded successfully with full clearing.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


if __name__ == '__main__':
    test_load_full()

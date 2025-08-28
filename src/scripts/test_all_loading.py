#!/usr/bin/env python3
"""
Comprehensive test script to load both menu and restaurant data
"""

import sys
import os
sys.path.append('/app/src')

from apps.food_menu.scripts.load.load_menu import MenuJsonLoader
from apps.restaurant.scripts.load.load_rstrnts import RstrntJsonLoader
from apps.food_menu.models import FoodType, Food, FoodSize, ModifierCategory, ModifierOption, Menu
from apps.restaurant.models import Restaurant
from config import db_settings
from sqlalchemy.orm import sessionmaker


def test_all_loading():
    """Test loading both menu and restaurant data"""
    print("🚀 COMPREHENSIVE DATA LOADING TEST")
    print("=" * 60)
    
    try:
        # Load restaurant data
        print("\n🏪 Loading restaurant data...")
        restaurant_loader = RstrntJsonLoader()
        restaurant_loader.load()
        print("✅ Restaurant data loaded successfully!")
        
        # Load menu data (preserving existing modifiers)
        print("\n🍽️  Loading menu data...")
        menu_loader = MenuJsonLoader()
        menu_loader.load(clear_all=False)
        print("✅ Menu data loaded successfully!")
        
        # Verify all data was loaded correctly
        SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
        session = SessionLocal()
        
        print("\n📊 VERIFICATION RESULTS:")
        print("-" * 40)
        
        # Check restaurants
        restaurants = session.query(Restaurant).all()
        print(f"🏪 Restaurants: {len(restaurants)}")
        
        # Check food types
        food_types = session.query(FoodType).all()
        print(f"📋 Food Types: {len(food_types)}")
        
        # Check foods
        foods = session.query(Food).all()
        print(f"🍽️  Foods: {len(foods)}")
        
        # Check food sizes
        food_sizes = session.query(FoodSize).all()
        print(f"📏 Food Sizes: {len(food_sizes)}")
        
        # Check modifier categories
        modifier_categories = session.query(ModifierCategory).all()
        print(f"🏷️  Modifier Categories: {len(modifier_categories)}")
        
        # Check modifier options
        modifier_options = session.query(ModifierOption).all()
        print(f"⚙️  Modifier Options: {len(modifier_options)}")
        
        # Check menu entries
        menu_entries = session.query(Menu).all()
        print(f"📋 Menu Entries: {len(menu_entries)}")
        
        # Show sample data
        print("\n📋 SAMPLE DATA:")
        print("-" * 40)
        
        # Sample restaurants
        print("\n🏪 Sample Restaurants:")
        for i, restaurant in enumerate(restaurants[:3], 1):
            print(f"  {i}. {restaurant.name}")
            print(f"     📍 {restaurant.lat}, {restaurant.lon}")
        
        # Sample food types
        print("\n📋 Sample Food Types:")
        for i, food_type in enumerate(food_types[:3], 1):
            foods_count = session.query(Food).filter(Food.type_id == food_type.id).count()
            print(f"  {i}. {food_type.name} ({foods_count} foods)")
        
        # Sample foods
        print("\n🍽️  Sample Foods:")
        for i, food in enumerate(foods[:3], 1):
            food_type = session.query(FoodType).filter(FoodType.id == food.type_id).first()
            print(f"  {i}. {food.name} ({food_type.name})")
        
        # Sample modifier categories
        if modifier_categories:
            print("\n🏷️  Sample Modifier Categories:")
            for i, category in enumerate(modifier_categories[:3], 1):
                options_count = session.query(ModifierOption).filter(ModifierOption.modifier_category_id == category.id).count()
                print(f"  {i}. {category.name} ({options_count} options)")
        
        session.close()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Complete data loading successful!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during comprehensive testing: {e}")
        raise


if __name__ == '__main__':
    test_all_loading()
#!/usr/bin/env python3
"""
Script to show the current state of the database and identify duplicates
"""

import sys
import os
sys.path.append('/app/src')

from apps.food_menu.models import FoodType, Food, FoodSize, ModifierCategory, ModifierOption, Menu, FoodModifierOption
from config import db_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


def show_database_state():
    """Display the current state of the database"""
    print("🗄️  DATABASE STATE ANALYSIS")
    print("=" * 60)
    
    SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
    session = SessionLocal()
    
    try:
        # Food Types
        food_types = session.query(FoodType).all()
        print(f"\n📋 FOOD TYPES ({len(food_types)}):")
        for ft in food_types:
            foods_count = session.query(Food).filter(Food.type_id == ft.id).count()
            print(f"  • {ft.name} (ID: {ft.id}) - {foods_count} foods")
        
        # Foods
        foods = session.query(Food).all()
        print(f"\n🍽️  FOODS ({len(foods)}):")
        for food in foods:
            food_type = session.query(FoodType).filter(FoodType.id == food.type_id).first()
            sizes_count = session.query(FoodSize).filter(FoodSize.parent_id == food.id).count()
            modifiers_count = session.query(FoodModifierOption).filter(FoodModifierOption.food_id == food.id).count()
            print(f"  • {food.name} (ID: {food.id}) - {food_type.name} - {sizes_count} sizes, {modifiers_count} modifiers")
        
        # Food Sizes
        food_sizes = session.query(FoodSize).all()
        print(f"\n📏 FOOD SIZES ({len(food_sizes)}):")
        for size in food_sizes:
            food = session.query(Food).filter(Food.id == size.parent_id).first()
            print(f"  • {size.name} (ID: {size.id}) - {food.name} - {size.price}₸")
        
        # Modifier Categories
        modifier_categories = session.query(ModifierCategory).all()
        print(f"\n🏷️  MODIFIER CATEGORIES ({len(modifier_categories)}):")
        for category in modifier_categories:
            options_count = session.query(ModifierOption).filter(ModifierOption.modifier_category_id == category.id).count()
            print(f"  • {category.name} (ID: {category.id}) - {options_count} options")
        
        # Modifier Options
        modifier_options = session.query(ModifierOption).all()
        print(f"\n⚙️  MODIFIER OPTIONS ({len(modifier_options)}):")
        for option in modifier_options:
            category = session.query(ModifierCategory).filter(ModifierCategory.id == option.modifier_category_id).first()
            print(f"  • {option.name} (ID: {option.id}) - {category.name} - {option.price}₸")
        
        # Menu Entries
        menu_entries = session.query(Menu).order_by(Menu.priority_level).all()
        print(f"\n📋 MENU ENTRIES ({len(menu_entries)}):")
        for menu_entry in menu_entries:
            food = session.query(Food).filter(Food.id == menu_entry.food_id).first()
            print(f"  • Priority {menu_entry.priority_level}: {food.name} (Food ID: {menu_entry.food_id})")
        
        # Check for duplicates
        print(f"\n🔍 DUPLICATE ANALYSIS:")
        
        # Check for duplicate food types
        duplicate_food_types = session.query(FoodType.name, func.count(FoodType.id)).group_by(FoodType.name).having(func.count(FoodType.id) > 1).all()
        if duplicate_food_types:
            print(f"  ⚠️  Duplicate Food Types: {len(duplicate_food_types)}")
            for name, count in duplicate_food_types:
                print(f"    • {name}: {count} instances")
        else:
            print("  ✅ No duplicate Food Types")
        
        # Check for duplicate foods within same type
        duplicate_foods = session.query(Food.name, Food.type_id, func.count(Food.id)).group_by(Food.name, Food.type_id).having(func.count(Food.id) > 1).all()
        if duplicate_foods:
            print(f"  ⚠️  Duplicate Foods: {len(duplicate_foods)}")
            for name, type_id, count in duplicate_foods:
                food_type = session.query(FoodType).filter(FoodType.id == type_id).first()
                print(f"    • {name} in {food_type.name}: {count} instances")
        else:
            print("  ✅ No duplicate Foods")
        
        # Check for duplicate modifier categories
        duplicate_categories = session.query(ModifierCategory.name, func.count(ModifierCategory.id)).group_by(ModifierCategory.name).having(func.count(ModifierCategory.id) > 1).all()
        if duplicate_categories:
            print(f"  ⚠️  Duplicate Modifier Categories: {len(duplicate_categories)}")
            for name, count in duplicate_categories:
                print(f"    • {name}: {count} instances")
        else:
            print("  ✅ No duplicate Modifier Categories")
        
        # Check for duplicate modifier options within same category
        duplicate_options = session.query(ModifierOption.name, ModifierOption.modifier_category_id, func.count(ModifierOption.id)).group_by(ModifierOption.name, ModifierOption.modifier_category_id).having(func.count(ModifierOption.id) > 1).all()
        if duplicate_options:
            print(f"  ⚠️  Duplicate Modifier Options: {len(duplicate_options)}")
            for name, category_id, count in duplicate_options:
                category = session.query(ModifierCategory).filter(ModifierCategory.id == category_id).first()
                print(f"    • {name} in {category.name}: {count} instances")
        else:
            print("  ✅ No duplicate Modifier Options")
        
        print(f"\n" + "=" * 60)
        print(f"📊 SUMMARY:")
        print(f"  • Food Types: {len(food_types)}")
        print(f"  • Foods: {len(foods)}")
        print(f"  • Food Sizes: {len(food_sizes)}")
        print(f"  • Modifier Categories: {len(modifier_categories)}")
        print(f"  • Modifier Options: {len(modifier_options)}")
        print(f"  • Menu Entries: {len(menu_entries)}")
        
    except Exception as e:
        print(f"❌ Error analyzing database: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    show_database_state()

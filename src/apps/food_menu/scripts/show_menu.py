#!/usr/bin/env python3
"""
Script to display the menu in priority order
"""

import sys
import os
sys.path.append('/app/src')

from apps.food_menu.models import Menu, Food, FoodType, FoodSize, ModifierCategory, ModifierOption
from config import db_settings
from sqlalchemy.orm import sessionmaker


def show_menu():
    """Display the menu in priority order"""
    print("🍽️  APPETIT MENU")
    print("=" * 50)
    
    SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
    session = SessionLocal()
    
    try:
        # Get menu entries ordered by priority
        menu_entries = session.query(Menu).order_by(Menu.priority_level).all()
        
        current_food_type = None
        
        for menu_entry in menu_entries:
            # Get food and food type
            food = session.query(Food).filter(Food.id == menu_entry.food_id).first()
            food_type = session.query(FoodType).filter(FoodType.id == food.type_id).first()
            
            # Print food type header if it's new
            if current_food_type != food_type.name:
                current_food_type = food_type.name
                print(f"\n📋 {food_type.name.upper()}")
                print("-" * 30)
            
            # Print food item
            print(f"\n🍽️  {food.name}")
            print(f"   📝 {food.description}")
            
            # Print sizes and prices
            sizes = session.query(FoodSize).filter(FoodSize.parent_id == food.id).all()
            if sizes:
                print("   📏 Размеры:")
                for size in sizes:
                    new_badge = " 🆕" if size.is_new else ""
                    print(f"      • {size.name}: {size.price}₸{new_badge}")
            
            # Print modifier categories
            modifier_categories = session.query(ModifierCategory).join(
                ModifierOption, ModifierCategory.id == ModifierOption.modifier_category_id
            ).join(
                FoodModifierOption, ModifierOption.id == FoodModifierOption.modifier_option_id
            ).filter(
                FoodModifierOption.food_id == food.id
            ).distinct().all()
            
            if modifier_categories:
                print("   🧂 Дополнительно:")
                for category in modifier_categories:
                    print(f"      📌 {category.name}:")
                    options = session.query(ModifierOption).filter(
                        ModifierOption.modifier_category_id == category.id
                    ).all()
                    for option in options:
                        price_text = f" +{option.price}₸" if option.price > 0 else " (бесплатно)"
                        print(f"         • {option.name}{price_text}")
            
            print(f"   🏷️  Приоритет: {menu_entry.priority_level}")
        
        print("\n" + "=" * 50)
        print(f"📊 Всего блюд в меню: {len(menu_entries)}")
        
    except Exception as e:
        print(f"❌ Error displaying menu: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    show_menu()

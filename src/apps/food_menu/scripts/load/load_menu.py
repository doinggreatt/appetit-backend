import json
import asyncio
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from apps.food_menu.models import (
    FoodType, Food, Menu, FoodModifierOption, 
    FoodSize, ModifierCategory, ModifierOption
)
from config import db_settings


class MenuJsonLoader:
    def __init__(self, menu_filepath: str = '/app/src/assets/menu_data.json'):
        with open(menu_filepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
        self.db_sess = SessionLocal()

    def _drop_everything(self):
        """Clear all existing data"""
        print("Clearing existing data...")
        self.db_sess.query(Menu).delete()
        self.db_sess.query(FoodModifierOption).delete()
        self.db_sess.query(FoodSize).delete()
        self.db_sess.query(Food).delete()
        self.db_sess.query(ModifierOption).delete()
        self.db_sess.query(ModifierCategory).delete()
        self.db_sess.query(FoodType).delete()
        self.db_sess.commit()
        print("Existing data cleared.")
    
    def _drop_everything_except_modifiers(self):
        """Clear data but keep modifier categories and options"""
        print("Clearing existing data (keeping modifiers)...")
        self.db_sess.query(Menu).delete()
        self.db_sess.query(FoodModifierOption).delete()
        self.db_sess.query(FoodSize).delete()
        self.db_sess.query(Food).delete()
        self.db_sess.query(FoodType).delete()
        self.db_sess.commit()
        print("Existing data cleared (modifiers preserved).")

    def _load_food_types_and_foods(self):
        """Load food types and their associated foods"""
        print("Loading food types and foods...")
        
        priority_counter = 1  # Start priority level at 1
        
        for food_type_data in self.data['food_types']:
            # Check if FoodType already exists
            existing_food_type = self.db_sess.query(FoodType).filter(
                FoodType.name == food_type_data['name']
            ).first()
            
            if existing_food_type:
                food_type = existing_food_type
                print(f"Using existing FoodType: {food_type.name}")
            else:
                food_type = FoodType(name=food_type_data['name'])
                self.db_sess.add(food_type)
                self.db_sess.flush()  # Get the ID
                print(f"Created FoodType: {food_type.name}")
            
            # Create Foods for this type
            for food_data in food_type_data['foods']:
                # Check if Food already exists in this type
                existing_food = self.db_sess.query(Food).filter(
                    Food.name == food_data['name'],
                    Food.type_id == food_type.id
                ).first()
                
                if existing_food:
                    food = existing_food
                    print(f"  Using existing Food: {food.name}")
                else:
                    food = Food(
                        name=food_data['name'],
                        type_id=food_type.id,
                        description=food_data['description']
                    )
                    self.db_sess.add(food)
                    self.db_sess.flush()  # Get the ID
                    print(f"  Created Food: {food.name}")
                
                # Check if Menu entry already exists for this food
                existing_menu_entry = self.db_sess.query(Menu).filter(
                    Menu.food_id == food.id
                ).first()
                
                if existing_menu_entry:
                    menu_entry = existing_menu_entry
                    print(f"    Using existing Menu entry with priority: {menu_entry.priority_level}")
                else:
                    # Create Menu entry with priority from JSON or incrementing counter
                    priority = food_data.get('priority', priority_counter)
                    menu_entry = Menu(
                        food_id=food.id,
                        priority_level=priority
                    )
                    self.db_sess.add(menu_entry)
                    print(f"    Created Menu entry with priority: {priority}")
                    priority_counter += 1
                
                # Create FoodSizes
                for size_data in food_data['sizes']:
                    # Check if FoodSize already exists for this food
                    existing_size = self.db_sess.query(FoodSize).filter(
                        FoodSize.name == size_data['name'],
                        FoodSize.parent_id == food.id
                    ).first()
                    
                    if existing_size:
                        food_size = existing_size
                        print(f"    Using existing FoodSize: {food_size.name} - {food_size.price}₸")
                    else:
                        food_size = FoodSize(
                            name=size_data['name'],
                            parent_id=food.id,
                            price=size_data['price'],
                            is_new=size_data['is_new']
                        )
                        self.db_sess.add(food_size)
                        print(f"    Created FoodSize: {food_size.name} - {food_size.price}₸")
                
                # Create ModifierCategories and ModifierOptions
                for category_data in food_data['modifier_categories']:
                    # Check if modifier category already exists
                    existing_category = self.db_sess.query(ModifierCategory).filter(
                        ModifierCategory.name == category_data['name']
                    ).first()
                    
                    if existing_category:
                        modifier_category = existing_category
                        print(f"    Using existing ModifierCategory: {modifier_category.name}")
                    else:
                        modifier_category = ModifierCategory(name=category_data['name'])
                        self.db_sess.add(modifier_category)
                        self.db_sess.flush()  # Get the ID
                        print(f"    Created ModifierCategory: {modifier_category.name}")
                    
                    # Create ModifierOptions for this category
                    for option_data in category_data['options']:
                        # Check if modifier option already exists in this category
                        existing_option = self.db_sess.query(ModifierOption).filter(
                            ModifierOption.name == option_data['name'],
                            ModifierOption.modifier_category_id == modifier_category.id
                        ).first()
                        
                        if existing_option:
                            modifier_option = existing_option
                            print(f"      Using existing ModifierOption: {modifier_option.name} - {modifier_option.price}₸")
                        else:
                            modifier_option = ModifierOption(
                                name=option_data['name'],
                                modifier_category_id=modifier_category.id,
                                price=option_data['price']
                            )
                            self.db_sess.add(modifier_option)
                            self.db_sess.flush()  # Get the ID
                            print(f"      Created ModifierOption: {modifier_option.name} - {modifier_option.price}₸")
                        
                        # Check if FoodModifierOption relationship already exists
                        existing_relationship = self.db_sess.query(FoodModifierOption).filter(
                            FoodModifierOption.food_id == food.id,
                            FoodModifierOption.modifier_option_id == modifier_option.id
                        ).first()
                        
                        if not existing_relationship:
                            # Create FoodModifierOption relationship
                            food_modifier_option = FoodModifierOption(
                                food_id=food.id,
                                modifier_option_id=modifier_option.id
                            )
                            self.db_sess.add(food_modifier_option)
                            print(f"        Created FoodModifierOption relationship")
                        else:
                            print(f"        Using existing FoodModifierOption relationship")
        
        self.db_sess.commit()
        print("Food types and foods loaded successfully.")

    def load(self, clear_all=False):
        """Main loading method
        
        Args:
            clear_all (bool): If True, clears all data including modifiers. 
                            If False, preserves existing modifiers.
        """
        try:
            print("Starting menu data loading...")
            
            if clear_all:
                self._drop_everything()
            else:
                self._drop_everything_except_modifiers()
            
            self._load_food_types_and_foods()
            print("Menu data loading completed successfully!")
            
        except Exception as e:
            print(f"Error loading menu data: {e}")
            self.db_sess.rollback()
            raise
        finally:
            self.db_sess.close()


if __name__ == '__main__':
    loader = MenuJsonLoader()
    loader.load()
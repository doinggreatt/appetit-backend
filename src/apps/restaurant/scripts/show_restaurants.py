#!/usr/bin/env python3
"""
Script to display all restaurants
"""

import sys
import os
sys.path.append('/app/src')

from apps.restaurant.models import Restaurant
from config import db_settings
from sqlalchemy.orm import sessionmaker


def show_restaurants():
    """Display all restaurants"""
    print("🏪 APPETIT RESTAURANTS")
    print("=" * 80)
    
    SessionLocal = sessionmaker(db_settings.sync_engine, expire_on_commit=False)
    session = SessionLocal()
    
    try:
        restaurants = session.query(Restaurant).all()
        
        if not restaurants:
            print("No restaurants found in the database.")
            return
        
        for i, restaurant in enumerate(restaurants, 1):
            print(f"\n{i}. 🏪 {restaurant.name}")
            print(f"   📍 Coordinates: {restaurant.lat}, {restaurant.lon}")
            print(f"   🗺️  Google Maps: https://maps.google.com/?q={restaurant.lat},{restaurant.lon}")
            print("-" * 80)
        
        print(f"\n📊 Total restaurants: {len(restaurants)}")
        
    except Exception as e:
        print(f"❌ Error displaying restaurants: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    show_restaurants()

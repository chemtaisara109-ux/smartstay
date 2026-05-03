#!/usr/bin/env python3
"""
SmartStay Setup Script
Creates sample data for testing the booking system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_enhanced import User
from models.listing import Property
from database import init_db

def create_sample_data():
    """Create sample users and properties for testing"""

    print("🚀 Setting up SmartStay sample data...")

    # Create sample host
    try:
        host = User.create(
            username='samplehost',
            full_name='Sample Host',
            email='host@smartstay.com',
            password='Password123',
            role='host',
            phone='+1234567890',
            property_name='Sample Villa',
            location='Nairobi, Kenya'
        )
        print(f"✅ Created host: {host.full_name} (ID: {host.id})")
        host_id = host.id
    except Exception as e:
        print(f"Host already exists or error: {e}")
        # Find existing host
        existing_host = User.find_by_email('host@smartstay.com')
        if existing_host:
            host_id = existing_host.id
        else:
            print("❌ Could not create or find host")
            return

    # Create sample guest
    try:
        guest = User.create(
            username='sampleguest',
            full_name='Sample Guest',
            email='guest@smartstay.com',
            password='Password123',
            role='guest'
        )
        print(f"✅ Created guest: {guest.full_name} (ID: {guest.id})")
    except Exception as e:
        print(f"Guest already exists or error: {e}")

    # Create sample properties
    properties_data = [
        {
            'title': 'Cozy Apartment in Westlands',
            'location': 'Westlands, Nairobi',
            'price': 150.00,
            'max_guests': 2,
            'description': 'A beautiful 1-bedroom apartment in the heart of Westlands. Perfect for couples or business travelers.'
        },
        {
            'title': 'Luxury Villa with Garden',
            'location': 'Karen, Nairobi',
            'price': 300.00,
            'max_guests': 6,
            'description': 'Spacious 3-bedroom villa with private garden, swimming pool, and modern amenities.'
        },
        {
            'title': 'Budget Room in Koinange Street',
            'location': 'Koinange Street, Nairobi',
            'price': 50.00,
            'max_guests': 1,
            'description': 'Clean and affordable single room, perfect for budget travelers.'
        },
        {
            'title': 'Beach House in Mombasa',
            'location': 'Mombasa, Kenya',
            'price': 200.00,
            'max_guests': 4,
            'description': 'Stunning beachfront property with ocean views and direct beach access.'
        }
    ]

    for prop_data in properties_data:
        try:
            property = Property.create(
                host_id=host_id,
                title=prop_data['title'],
                location=prop_data['location'],
                price=prop_data['price'],
                max_guests=prop_data['max_guests'],
                description=prop_data['description']
            )
            print(f"✅ Created property: {property.title} (ID: {property.id})")
        except Exception as e:
            print(f"Property '{prop_data['title']}' already exists or error: {e}")

    print("\n🎉 Setup complete!")
    print("\nSample login credentials:")
    print("Host: host@smartstay.com / Password123")
    print("Guest: guest@smartstay.com / Password123")
    print("\nVisit http://localhost:5000 to start using SmartStay!")

if __name__ == '__main__':
    init_db()
    create_sample_data()
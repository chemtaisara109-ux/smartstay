#!/usr/bin/env python3
"""
Test script for user registration and login API
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_register():
    """Test user registration"""
    print("Testing user registration...")

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123'
    }

    response = requests.post(f'{BASE_URL}/api/register', json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login():
    """Test user login"""
    print("Testing user login...")

    data = {
        'email': 'test@example.com',
        'password': 'TestPass123'
    }

    response = requests.post(f'{BASE_URL}/api/login', json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == '__main__':
    test_register()
    test_login()
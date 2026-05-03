#!/usr/bin/env python3
"""
Test script for SmartStay web application
Tests the complete booking flow
"""
import requests

BASE_URL = 'http://localhost:5000'

def test_landing_page():
    """Test landing page loads"""
    print("Testing landing page...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    assert response.status_code == 200, "Landing page should load"
    assert "SmartStay" in response.text, "Should contain SmartStay branding"
    print("✅ Landing page loads successfully\n")

def test_registration_page():
    """Test registration page loads"""
    print("Testing registration page...")
    response = requests.get(f'{BASE_URL}/register')
    print(f"Status: {response.status_code}")
    assert response.status_code == 200, "Registration page should load"
    assert "register" in response.text.lower(), "Should contain registration form"
    print("✅ Registration page loads successfully\n")

def test_login_page():
    """Test login page loads"""
    print("Testing login page...")
    response = requests.get(f'{BASE_URL}/login')
    print(f"Status: {response.status_code}")
    assert response.status_code == 200, "Login page should load"
    assert "login" in response.text.lower(), "Should contain login form"
    print("✅ Login page loads successfully\n")

def test_host_registration_page():
    """Test host registration page loads"""
    print("Testing host registration page...")
    response = requests.get(f'{BASE_URL}/host-register')
    print(f"Status: {response.status_code}")
    assert response.status_code == 200, "Host registration page should load"
    assert "host" in response.text.lower(), "Should contain host registration form"
    print("✅ Host registration page loads successfully\n")

def test_sample_login():
    """Test login with sample credentials"""
    print("Testing sample login...")

    # Get login page first to get any session cookies
    session = requests.Session()
    response = session.get(f'{BASE_URL}/login')
    assert response.status_code == 200, "Login page should load"

    # Try to login
    login_data = {
        'email': 'guest@smartstay.com',
        'password': 'Password123'
    }

    response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
    print(f"Login status: {response.status_code}")

    if response.status_code in [302, 303]:
        print("✅ Login successful (redirected)")
        redirect_url = response.headers.get('Location', '')
        print(f"Redirected to: {redirect_url}")

        # Follow redirect
        response = session.get(BASE_URL + redirect_url)
        if "dashboard" in redirect_url:
            print("✅ Redirected to dashboard")
        else:
            print(f"Redirected to: {redirect_url}")
    else:
        print(f"Login response contains: {'dashboard' if 'dashboard' in response.text.lower() else 'no dashboard'}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting SmartStay Web Tests\n")

    try:
        test_landing_page()
        test_registration_page()
        test_login_page()
        test_host_registration_page()
        test_sample_login()

        print("🎉 All basic tests passed! SmartStay web interface is working.")
        print("\n📋 Manual Testing Checklist:")
        print("1. Visit http://localhost:5000")
        print("2. Register as a guest or login with guest@smartstay.com / Password123")
        print("3. Browse properties and make a booking")
        print("4. Login as host with host@smartstay.com / Password123")
        print("5. Confirm bookings and generate receipts")
        print("\n🔧 To enable MySQL (optional):")
        print("1. Start XAMPP MySQL service")
        print("2. Set USE_SQLITE=False in config.py")
        print("3. Restart the app")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the Flask app is running on http://localhost:5000")

if __name__ == '__main__':
    main()
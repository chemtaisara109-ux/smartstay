#!/usr/bin/env python3
"""
Authentication API Testing Script
Tests registration and login endpoints
"""

import requests
import json
from datetime import datetime

# Configuration
API_URL = 'http://127.0.0.1:5000'
HEADERS = {'Content-Type': 'application/json'}

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")


def print_info(text):
    """Print info message"""
    print(f"{YELLOW}ℹ️  {text}{RESET}")


def print_json(data, label="Response"):
    """Pretty print JSON data"""
    print(f"\n{label}:")
    print(json.dumps(data, indent=2))


def test_registration():
    """Test user registration endpoint"""
    print_header("Test 1: User Registration")

    # Test data
    test_user = {
        'username': f'testuser_{datetime.now().timestamp():.0f}',
        'email': f'test_{datetime.now().timestamp():.0f}@example.com',
        'password': 'SecurePass123'
    }

    print_info(f"Registering new user: {test_user['username']}")
    print_info(f"Email: {test_user['email']}")

    try:
        response = requests.post(
            f'{API_URL}/register',
            json=test_user,
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 201:
            print_success("Registration successful!")
            return test_user
        else:
            print_error(f"Registration failed: {response.json().get('error')}")
            return None

    except Exception as e:
        print_error(f"Exception: {e}")
        return None


def test_duplicate_registration(user):
    """Test duplicate email registration"""
    print_header("Test 2: Duplicate Email Registration")

    if not user:
        print_error("No user data from previous test")
        return

    print_info(f"Attempting to register with existing email: {user['email']}")

    try:
        response = requests.post(
            f'{API_URL}/register',
            json={
                'username': 'anotheruser',
                'email': user['email'],  # Same email
                'password': 'AnotherPass123'
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 409:
            print_success("Correctly rejected duplicate email!")
        else:
            print_error("Should have returned 409 Conflict")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_invalid_email():
    """Test invalid email format"""
    print_header("Test 3: Invalid Email Format")

    print_info("Attempting registration with invalid email format")

    try:
        response = requests.post(
            f'{API_URL}/register',
            json={
                'username': 'testuser',
                'email': 'not-an-email',  # Invalid format
                'password': 'ValidPass123'
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 400:
            print_success("Correctly rejected invalid email!")
        else:
            print_error("Should have returned 400 Bad Request")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_weak_password():
    """Test weak password validation"""
    print_header("Test 4: Weak Password")

    print_info("Attempting registration with weak password (too short)")

    try:
        response = requests.post(
            f'{API_URL}/register',
            json={
                'username': 'weakpass',
                'email': f'weak_{datetime.now().timestamp():.0f}@example.com',
                'password': 'Short1'  # Too short, no uppercase, etc.
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 400:
            print_success("Correctly rejected weak password!")
        else:
            print_error("Should have returned 400 Bad Request")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_login_success(user):
    """Test successful login"""
    print_header("Test 5: Successful Login")

    if not user:
        print_error("No user data from registration test")
        return None

    print_info(f"Logging in with email: {user['email']}")

    try:
        response = requests.post(
            f'{API_URL}/login',
            json={
                'email': user['email'],
                'password': user['password']
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 200:
            print_success("Login successful!")
            data = response.json()
            if 'access_token' in data:
                print_success(f"JWT Token received: {data['access_token'][:50]}...")
            return data.get('access_token')
        else:
            print_error(f"Login failed: {response.json().get('error')}")
            return None

    except Exception as e:
        print_error(f"Exception: {e}")
        return None


def test_login_invalid_password(user):
    """Test login with wrong password"""
    print_header("Test 6: Login with Invalid Password")

    if not user:
        print_error("No user data from registration test")
        return

    print_info(f"Attempting login with wrong password")

    try:
        response = requests.post(
            f'{API_URL}/login',
            json={
                'email': user['email'],
                'password': 'WrongPassword123'
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 401:
            print_success("Correctly rejected invalid password!")
        else:
            print_error("Should have returned 401 Unauthorized")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_login_nonexistent_email():
    """Test login with non-existent email"""
    print_header("Test 7: Login with Non-existent Email")

    print_info("Attempting login with non-existent email")

    try:
        response = requests.post(
            f'{API_URL}/login',
            json={
                'email': f'nonexistent_{datetime.now().timestamp():.0f}@example.com',
                'password': 'SomePass123'
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 401:
            print_success("Correctly rejected non-existent email!")
        else:
            print_error("Should have returned 401 Unauthorized")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_missing_fields():
    """Test missing required fields"""
    print_header("Test 8: Missing Required Fields")

    print_info("Attempting registration without email field")

    try:
        response = requests.post(
            f'{API_URL}/register',
            json={
                'username': 'testuser',
                # Missing 'email'
                'password': 'ValidPass123'
            },
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 400:
            print_success("Correctly rejected missing field!")
        else:
            print_error("Should have returned 400 Bad Request")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_empty_request():
    """Test empty request body"""
    print_header("Test 9: Empty Request Body")

    print_info("Attempting registration with empty request body")

    try:
        response = requests.post(
            f'{API_URL}/register',
            json={},
            headers=HEADERS
        )

        print_json(response.json(), f"HTTP {response.status_code}")

        if response.status_code == 400:
            print_success("Correctly rejected empty request!")
        else:
            print_error("Should have returned 400 Bad Request")

    except Exception as e:
        print_error(f"Exception: {e}")


def test_sample_accounts():
    """Test login with pre-loaded sample accounts"""
    print_header("Test 10: Sample Pre-loaded Accounts")

    sample_accounts = [
        {
            'email': 'guest@example.com',
            'password': 'password123',
            'name': 'Guest Account'
        },
        {
            'email': 'host@example.com',
            'password': 'password123',
            'name': 'Host Account'
        }
    ]

    for account in sample_accounts:
        print_info(f"Testing {account['name']}: {account['email']}")

        try:
            response = requests.post(
                f'{API_URL}/login',
                json={
                    'email': account['email'],
                    'password': account['password']
                },
                headers=HEADERS
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"✓ {account['name']} login successful")
                print(f"  User: {data['user']['username']}")
                print(f"  Token: {data['access_token'][:40]}...\n")
            else:
                print_error(f"✗ {account['name']} login failed")

        except Exception as e:
            print_error(f"Exception: {e}")


def main():
    """Run all tests"""
    print(f"\n{BLUE}{'*'*60}")
    print(f"  SmartStay Authentication API Test Suite")
    print(f"  API URL: {API_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'*'*60}{RESET}")

    try:
        # Test 1: Registration
        registered_user = test_registration()

        # Test 2-4: Registration edge cases
        test_duplicate_registration(registered_user)
        test_invalid_email()
        test_weak_password()

        # Test 5-7: Login tests
        token = test_login_success(registered_user)
        test_login_invalid_password(registered_user)
        test_login_nonexistent_email()

        # Test 8-9: Validation tests
        test_missing_fields()
        test_empty_request()

        # Test 10: Pre-loaded sample accounts
        test_sample_accounts()

        # Summary
        print_header("Test Summary")
        print_success("All tests completed!")
        print_info("Check results above for details")

    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API!")
        print_info(f"Make sure Flask server is running on {API_URL}")
        print_info("Run: python app.py")

    except Exception as e:
        print_error(f"Unexpected error: {e}")

    print(f"\n{BLUE}{'='*60}{RESET}\n")


if __name__ == '__main__':
    main()

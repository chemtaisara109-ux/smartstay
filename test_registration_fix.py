"""
Test script to verify the registration duplicate checking functionality
"""
import sys
import sqlite3
import pymysql
from models.user import User
from database import get_db_connection, get_placeholder

print("\n" + "=" * 70)
print("🧪 TESTING REGISTRATION DUPLICATE CHECKING")
print("=" * 70 + "\n")

# Test data
test_username = "testuser_" + str(int(__import__('time').time()))
test_email = f"test_{test_username}@example.com"
test_password = "TestPassword123"

print(f"📝 Test Data:")
print(f"   Username: {test_username}")
print(f"   Email: {test_email}")
print(f"   Password: {test_password}\n")

# Test 1: Register a new user successfully
print("Test 1️⃣: Register a new user")
print("-" * 70)
result = User.create(test_username, test_email, test_password)

if result['success']:
    print(f"✅ User registered successfully!")
    print(f"   User ID: {result['user'].id}")
    print(f"   Username: {result['user'].username}")
    print(f"   Email: {result['user'].email}\n")
else:
    print(f"❌ Registration failed: {result['error']}\n")
    sys.exit(1)

# Test 2: Try to register with the same username
print("Test 2️⃣: Try to register with the same username")
print("-" * 70)
result2 = User.create(test_username, f"different_{test_email}", test_password)

if not result2['success'] and 'Username already taken' in result2['error']:
    print(f"✅ Correctly blocked duplicate username!")
    print(f"   Error message: {result2['error']}\n")
else:
    print(f"❌ Duplicate username check failed!\n")
    sys.exit(1)

# Test 3: Try to register with the same email
print("Test 3️⃣: Try to register with the same email")
print("-" * 70)
result3 = User.create(f"different_{test_username}", test_email, test_password)

if not result3['success'] and 'Email already registered' in result3['error']:
    print(f"✅ Correctly blocked duplicate email!")
    print(f"   Error message: {result3['error']}\n")
else:
    print(f"❌ Duplicate email check failed!\n")
    sys.exit(1)

# Test 4: Verify find_by_username works
print("Test 4️⃣: Verify find_by_username method")
print("-" * 70)
found_user = User.find_by_username(test_username)

if found_user and found_user.username == test_username:
    print(f"✅ Successfully found user by username!")
    print(f"   Username: {found_user.username}")
    print(f"   Email: {found_user.email}\n")
else:
    print(f"❌ find_by_username failed!\n")
    sys.exit(1)

# Test 5: Verify find_by_email works
print("Test 5️⃣: Verify find_by_email method")
print("-" * 70)
found_user_email = User.find_by_email(test_email)

if found_user_email and found_user_email.email == test_email:
    print(f"✅ Successfully found user by email!")
    print(f"   Username: {found_user_email.username}")
    print(f"   Email: {found_user_email.email}\n")
else:
    print(f"❌ find_by_email failed!\n")
    sys.exit(1)

print("=" * 70)
print("✅ ALL TESTS PASSED! Registration duplicate checking is working correctly.")
print("=" * 70 + "\n")

print("📋 Summary of Changes:")
print("   • User.create() now checks for duplicate usernames BEFORE inserting")
print("   • User.create() now checks for duplicate emails BEFORE inserting")
print("   • IntegrityError exceptions are caught and handled gracefully")
print("   • User-friendly error messages are returned instead of crashing")
print("   • Added User.find_by_username() method for username lookups")
print("   • Auth routes now handle the new response format properly")
print("   • Both API and form-based registration properly validate duplicates\n")

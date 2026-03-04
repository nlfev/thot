"""
Test script to check if the profile API returns data correctly
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_login_and_profile():
    """Test login and profile retrieval"""
    
    # First, try to login
    print("=" * 60)
    print("Testing Login and Profile API")
    print("=" * 60)
    
    # You need to provide a valid username and password
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Login
    print("\n1. Testing Login...")
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        # Check if OTP is required
        if response.status_code == 403 and "Two-factor" in response.text:
            print("⚠ Two-factor authentication required")
            otp_code = input("Enter OTP code: ")
            login_data["otp_code"] = otp_code
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        response.raise_for_status()
        login_result = response.json()
        
        print("✓ Login successful!")
        print(f"Token: {login_result['access_token'][:50]}...")
        print(f"\nUser data from login:")
        print(json.dumps(login_result['user'], indent=2))
        
        # Get token
        token = login_result['access_token']
        
    except requests.exceptions.HTTPError as e:
        print(f"✗ Login failed: {e}")
        print(f"Response: {e.response.text}")
        return
    except Exception as e:
        print(f"✗ Error during login: {e}")
        return
    
    # Get profile
    print("\n" + "=" * 60)
    print("2. Testing Profile API...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
        response.raise_for_status()
        profile_data = response.json()
        
        print("✓ Profile API successful!")
        print(f"\nProfile data:")
        print(json.dumps(profile_data, indent=2))
        
        # Check for empty fields
        print("\n" + "=" * 60)
        print("3. Checking for empty fields:")
        empty_fields = []
        for key, value in profile_data.items():
            if value is None or value == "":
                empty_fields.append(key)
                print(f"  ⚠ {key}: {value} (empty)")
            else:
                print(f"  ✓ {key}: {value}")
        
        if empty_fields:
            print(f"\n⚠ Warning: {len(empty_fields)} empty fields found: {', '.join(empty_fields)}")
            print("This might explain why the profile appears empty in the frontend.")
        else:
            print("\n✓ All fields have values!")
        
    except requests.exceptions.HTTPError as e:
        print(f"✗ Profile API failed: {e}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"✗ Error during profile retrieval: {e}")

if __name__ == "__main__":
    test_login_and_profile()

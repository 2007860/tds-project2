"""Test the quiz endpoint with the demo quiz."""
import requests
import json
import sys

# Configuration
API_ENDPOINT = "http://localhost:8000/quiz"  # Change if deployed
STUDENT_EMAIL = "your.email@example.com"  # Update with your email
STUDENT_SECRET = "your_secret_string"  # Update with your secret

# Demo quiz URL
DEMO_URL = "https://tds-llm-analysis.s-anand.net/demo"


def test_endpoint():
    """Test the endpoint with the demo quiz."""
    
    payload = {
        "email": STUDENT_EMAIL,
        "secret": STUDENT_SECRET,
        "url": DEMO_URL
    }
    
    print("=" * 60)
    print("Testing Quiz Endpoint")
    print("=" * 60)
    print(f"Endpoint: {API_ENDPOINT}")
    print(f"Email: {STUDENT_EMAIL}")
    print(f"Quiz URL: {DEMO_URL}")
    print("=" * 60)
    
    try:
        print("\nSending POST request...")
        response = requests.post(API_ENDPOINT, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✓ SUCCESS: Endpoint accepted the request!")
            print("Check the server logs to see quiz solving progress.")
        elif response.status_code == 403:
            print("\n✗ ERROR: Invalid secret or email")
        elif response.status_code == 400:
            print("\n✗ ERROR: Invalid request format")
        else:
            print(f"\n✗ ERROR: Unexpected status code {response.status_code}")
        
        return response.status_code == 200
        
    except requests.ConnectionError:
        print("\n✗ ERROR: Could not connect to endpoint")
        print("Make sure the server is running: python app.py")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


def test_invalid_secret():
    """Test with invalid secret (should return 403)."""
    
    payload = {
        "email": STUDENT_EMAIL,
        "secret": "wrong_secret",
        "url": DEMO_URL
    }
    
    print("\n" + "=" * 60)
    print("Testing Invalid Secret (should return 403)")
    print("=" * 60)
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, timeout=10)
        
        if response.status_code == 403:
            print("✓ SUCCESS: Correctly rejected invalid secret")
            return True
        else:
            print(f"✗ ERROR: Expected 403, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False


def test_invalid_json():
    """Test with invalid JSON (should return 400)."""
    
    print("\n" + "=" * 60)
    print("Testing Invalid JSON (should return 400)")
    print("=" * 60)
    
    try:
        response = requests.post(
            API_ENDPOINT,
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✓ SUCCESS: Correctly rejected invalid JSON")
            return True
        else:
            print(f"✗ ERROR: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False


if __name__ == "__main__":
    print("LLM Quiz Endpoint Test")
    print("\nMake sure to update STUDENT_EMAIL and STUDENT_SECRET in this file!")
    print("Also ensure the server is running: python app.py\n")
    
    # Run tests
    results = []
    
    results.append(("Valid request", test_endpoint()))
    results.append(("Invalid secret", test_invalid_secret()))
    results.append(("Invalid JSON", test_invalid_json()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    sys.exit(0 if passed == total else 1)

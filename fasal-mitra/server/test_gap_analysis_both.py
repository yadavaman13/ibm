"""
Test both Gap Analysis scenarios
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("="*70)
print("🌾 TESTING BOTH GAP ANALYSIS SCENARIOS")
print("="*70)

# Test Scenario 1: Post-Harvest (Actual Yield Known)
print("\n" + "="*70)
print("📊 SCENARIO 1: POST-HARVEST ANALYSIS (Farmer knows actual yield)")
print("="*70)

post_harvest_payload = {
    "crop": "Wheat",
    "state": "Punjab",
    "season": "Rabi",
    "actual_yield": 2.1
}

print("\nRequest:")
print(json.dumps(post_harvest_payload, indent=2))

response1 = requests.post(f"{BASE_URL}/yield/gap-analysis", json=post_harvest_payload)
print(f"\nStatus Code: {response1.status_code}")

if response1.status_code == 200:
    result1 = response1.json()
    data1 = result1['data']
    print(f"\n✅ Analysis Type: {data1['analysis_type']}")
    print(f"   Actual Yield: {data1['actual_yield']} tons/hectare")
    print(f"   Potential Yield: {data1['potential_yield']} tons/hectare")
    print(f"   Gap: {data1['gap_percentage']}%")
    print(f"   Performance: {data1['performance_level']}")
    print(f"\n   Top Recommendations:")
    for i, rec in enumerate(data1['improvement_steps'][:3], 1):
        print(f"   {i}. {rec}")
else:
    print(f"❌ Error: {response1.text}")

# Test Scenario 2: Pre-Harvest (Predict from inputs)
print("\n" + "="*70)
print("🌱 SCENARIO 2: PRE-HARVEST PLANNING (Farmer planning next season)")
print("="*70)

pre_harvest_payload = {
    "crop": "Wheat",
    "state": "Punjab",
    "season": "Rabi",
    "area": 50,
    "fertilizer": 20000,
    "pesticide": 300
}

print("\nRequest:")
print(json.dumps(pre_harvest_payload, indent=2))

response2 = requests.post(f"{BASE_URL}/yield/gap-analysis", json=pre_harvest_payload)
print(f"\nStatus Code: {response2.status_code}")

if response2.status_code == 200:
    result2 = response2.json()
    data2 = result2['data']
    print(f"\n✅ Analysis Type: {data2['analysis_type']}")
    print(f"   Predicted Yield: {data2['predicted_yield']} tons/hectare")
    print(f"   Potential Yield: {data2['potential_yield']} tons/hectare")
    print(f"   Gap: {data2['gap_percentage']}%")
    print(f"   Performance: {data2['performance_level']}")
    print(f"\n   Top Recommendations:")
    for i, rec in enumerate(data2['improvement_steps'][:3], 1):
        print(f"   {i}. {rec}")
else:
    print(f"❌ Error: {response2.text}")

# Test Error Case: Missing both required fields
print("\n" + "="*70)
print("❌ ERROR CASE: Missing both actual_yield and farming inputs")
print("="*70)

error_payload = {
    "crop": "Wheat",
    "state": "Punjab",
    "season": "Rabi"
}

print("\nRequest:")
print(json.dumps(error_payload, indent=2))

response3 = requests.post(f"{BASE_URL}/yield/gap-analysis", json=error_payload)
print(f"\nStatus Code: {response3.status_code}")
print(f"Response: {response3.json()}")

print("\n" + "="*70)
print("🎉 BOTH SCENARIOS TESTED!")
print("="*70)

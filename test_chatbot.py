"""Test chatbot functionality directly"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.farmer_helper_bot import FarmerHelperBot

print("=" * 60)
print("Testing FarmerHelperBot")
print("=" * 60)

# Initialize bot
bot = FarmerHelperBot()
print(f"\nBot enabled: {bot.enabled}")
print(f"Bot API key configured: {bool(bot.api_key and len(bot.api_key) > 10)}")

if not bot.enabled:
    print(f"Initialization error: {bot.initialization_error}")
    sys.exit(1)

# Test simple question
print("\n" + "=" * 60)
print("Testing simple question...")
print("=" * 60)

question = "How to detect wheat diseases?"
print(f"\nQuestion: {question}")

try:
    response = bot.chat_with_farmer(question, [])
    print(f"\nResponse: {response}")
    print("\n✅ TEST PASSED!")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

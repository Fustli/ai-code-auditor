#!/usr/bin/env python3
"""
Simple test script to verify Gemini API key is working
Usage: python test_gemini.py YOUR_API_KEY
"""

import sys
import google.generativeai as genai

def test_gemini_api(api_key: str):
    """Test if the Gemini API key is valid and working"""
    
    print(f"🔑 Testing Gemini API key: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    # Validate format
    if not api_key.startswith("AIza"):
        print("❌ ERROR: API key should start with 'AIza'")
        print(f"   Your key starts with: {api_key[:4]}")
        return False
    
    print("✓ API key format looks correct")
    
    # Try to configure
    try:
        genai.configure(api_key=api_key)
        print("✓ API key configured successfully")
    except Exception as e:
        print(f"❌ Failed to configure API: {e}")
        return False
    
    # List available models first
    print("\n📋 Checking available models...")
    try:
        models = list(genai.list_models())
        if not models:
            print("⚠️  No models found. API might not be enabled.")
            print("\n🔧 ACTION REQUIRED:")
            print("   Enable the Generative Language API at:")
            print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
            return False
        
        print(f"✓ Found {len(models)} available models:")
        generate_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                generate_models.append(m.name)
                print(f"  • {m.name}")
        
        if not generate_models:
            print("\n❌ No models support generateContent method")
            return False
        
        # Use the first available model
        model_name = generate_models[0]
        print(f"\n🎯 Using model: {model_name}")
        
    except Exception as e:
        print(f"❌ Failed to list models: {e}")
        print("\n🔧 ACTION REQUIRED:")
        print("   Enable the Generative Language API at:")
        print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
        return False
    
    # Try to create a model
    try:
        model = genai.GenerativeModel(model_name)
        print("✓ Model created successfully")
    except Exception as e:
        print(f"❌ Failed to create model: {e}")
        return False
    
    # Try a simple generation
    try:
        print("\n📤 Sending test request...")
        response = model.generate_content("Say 'Hello, I am working!' in exactly those words.")
        print(f"📥 Response received: {response.text}")
        print("\n✅ SUCCESS! Your Gemini API key is working correctly!")
        return True
    except Exception as e:
        print(f"\n❌ API call failed: {e}")
        print("\n🔍 Common issues:")
        print("   1. API key might not be enabled yet (try waiting a few minutes)")
        print("   2. API key might be restricted to specific APIs")
        print("   3. You might need to enable the Generative Language API at:")
        print("      https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_gemini.py YOUR_API_KEY")
        print("\nExample:")
        print("  python test_gemini.py AIzaSyD-9tNy_1234567890abcdefghijklmnop")
        print("\nGet your API key at: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    api_key = sys.argv[1].strip()
    success = test_gemini_api(api_key)
    sys.exit(0 if success else 1)

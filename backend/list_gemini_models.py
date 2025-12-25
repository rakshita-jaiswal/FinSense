"""List available Gemini models for the API key."""
import google.generativeai as genai
from config import settings

# Configure with API key
genai.configure(api_key=settings.gemini_api_key)

print("=" * 60)
print("AVAILABLE GEMINI MODELS")
print("=" * 60)

try:
    # List all available models
    models = genai.list_models()
    
    print("\nAll available models:")
    for model in models:
        print(f"\n  Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported methods: {model.supported_generation_methods}")
    
    print("\n" + "=" * 60)
    print("Models that support 'generateContent':")
    print("=" * 60)
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n  ✓ {model.name}")
            print(f"    Display: {model.display_name}")
    
except Exception as e:
    print(f"\nError listing models: {e}")
    print("\nThis might indicate an issue with the API key.")
    print("Please verify your API key at: https://makersuite.google.com/app/apikey")
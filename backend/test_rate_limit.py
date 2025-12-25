"""Test Gemini API rate limits to find the actual limit."""
import asyncio
import time
from datetime import datetime
import google.generativeai as genai
from config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

async def test_rate_limit(num_requests=10, delay_between_requests=0):
    """Test how many requests we can make per minute."""
    print("=" * 60)
    print(f"TESTING GEMINI API RATE LIMIT")
    print(f"Target: {num_requests} requests")
    print(f"Delay between requests: {delay_between_requests}s")
    print("=" * 60)
    
    successful_requests = 0
    failed_requests = 0
    start_time = time.time()
    
    for i in range(1, num_requests + 1):
        try:
            print(f"\n[Request {i}/{num_requests}] Sending at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}...")
            
            response = model.generate_content("Say 'OK' in one word.")
            
            if response.text:
                successful_requests += 1
                print(f"  [OK] Success: {response.text.strip()}")
            
            # Add delay if specified
            if delay_between_requests > 0 and i < num_requests:
                await asyncio.sleep(delay_between_requests)
                
        except Exception as e:
            failed_requests += 1
            error_msg = str(e)
            print(f"  [FAIL] Failed: {error_msg[:100]}...")
            
            # Check if it's a rate limit error
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"\n  [RATE LIMIT HIT at request {i}]")
                # Extract retry delay if available
                if "retry in" in error_msg.lower():
                    import re
                    match = re.search(r'retry in (\d+\.?\d*)', error_msg.lower())
                    if match:
                        retry_delay = float(match.group(1))
                        print(f"  Suggested retry delay: {retry_delay}s")
                break
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Total requests attempted: {num_requests}")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Time elapsed: {elapsed_time:.2f}s")
    print(f"Requests per minute: {(successful_requests / elapsed_time * 60):.1f}")
    
    if successful_requests == num_requests:
        print(f"\n[SUCCESS] All {num_requests} requests completed!")
    else:
        print(f"\n[RATE LIMIT] Hit limit at {successful_requests} requests")
        print(f"  Actual limit appears to be: {successful_requests} requests per minute")
    
    return successful_requests, failed_requests

async def main():
    """Run rate limit tests."""
    print("\n" + "=" * 60)
    print("GEMINI API RATE LIMIT TESTING")
    print("=" * 60)
    
    # Test 1: Try 10 requests with no delay
    print("\n\nTEST 1: 10 requests with no delay")
    print("-" * 60)
    success1, fail1 = await test_rate_limit(num_requests=10, delay_between_requests=0)
    
    # If we hit the limit, wait before next test
    if fail1 > 0:
        print("\n\nWaiting 65 seconds before next test...")
        await asyncio.sleep(65)
    
    # Test 2: Try 10 requests with 6 second delay (10 requests per minute)
    print("\n\nTEST 2: 10 requests with 6s delay between each")
    print("-" * 60)
    success2, fail2 = await test_rate_limit(num_requests=10, delay_between_requests=6)
    
    # Final summary
    print("\n\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Test 1 (no delay): {success1}/{10} successful")
    print(f"Test 2 (6s delay): {success2}/{10} successful")
    
    if success1 >= 10:
        print("\n[CONCLUSION] Can handle 10+ requests per minute")
    elif success2 >= 10:
        print(f"\n[CONCLUSION] Can handle 10 requests per minute with 6s delay")
    else:
        print(f"\n[CONCLUSION] Rate limit is approximately {success1} requests per minute")

if __name__ == "__main__":
    asyncio.run(main())
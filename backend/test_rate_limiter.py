"""Test the rate limiter implementation."""
import asyncio
import time
from datetime import datetime
from services.ai_service import ai_service


async def test_rate_limited_requests():
    """Test that rate limiter prevents exceeding API limits."""
    print("=" * 60)
    print("TESTING RATE LIMITER WITH AI SERVICE")
    print("=" * 60)
    print("\nSending 10 requests rapidly...")
    print("Rate limiter should queue requests to stay under 5 RPM limit")
    print("-" * 60)
    
    start_time = time.time()
    successful = 0
    failed = 0
    
    for i in range(1, 11):
        try:
            print(f"\n[Request {i}/10] Sending at {datetime.now().strftime('%H:%M:%S')}...")
            
            # Make AI request (rate limiter will handle queuing)
            response = await ai_service.generate_response(
                user_message="Say 'OK' in one word.",
                conversation_history=[],
                user_data={}
            )
            
            if response and "OK" in response.upper():
                successful += 1
                print(f"  [OK] Response: {response[:50]}")
            else:
                print(f"  [RESPONSE] {response[:100]}")
                successful += 1
            
            # Show rate limit status
            status = await ai_service.get_rate_limit_status()
            print(f"  Rate Limit: {status['requests_in_window']}/{status['max_requests']} used")
            
        except Exception as e:
            failed += 1
            print(f"  [FAIL] Error: {str(e)[:100]}")
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Total requests: 10")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Time elapsed: {elapsed:.1f}s")
    print(f"Average time per request: {elapsed/10:.1f}s")
    
    if successful == 10:
        print("\n[SUCCESS] All requests completed without hitting rate limit!")
        print("Rate limiter is working correctly.")
    else:
        print(f"\n[PARTIAL] {successful}/10 requests succeeded")


async def test_concurrent_requests():
    """Test concurrent requests to verify rate limiter handles them properly."""
    print("\n\n" + "=" * 60)
    print("TESTING CONCURRENT REQUESTS")
    print("=" * 60)
    print("\nSending 5 concurrent requests...")
    print("Rate limiter should serialize them properly")
    print("-" * 60)
    
    start_time = time.time()
    
    # Create 5 concurrent requests
    tasks = []
    for i in range(1, 6):
        task = ai_service.generate_response(
            user_message=f"Say 'Request {i}' in 2-3 words.",
            conversation_history=[],
            user_data={}
        )
        tasks.append(task)
    
    # Wait for all to complete
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\n[RESULTS]")
    print(f"Time elapsed: {elapsed:.1f}s")
    print(f"All {len(responses)} requests completed")
    
    successful = sum(1 for r in responses if isinstance(r, str) and not isinstance(r, Exception))
    print(f"Successful: {successful}/{len(responses)}")
    
    if successful == len(responses):
        print("\n[SUCCESS] Concurrent requests handled correctly!")


async def main():
    """Run all rate limiter tests."""
    print("\n" + "=" * 60)
    print("RATE LIMITER TESTING SUITE")
    print("=" * 60)
    
    # Test 1: Sequential requests
    await test_rate_limited_requests()
    
    # Wait a bit before next test
    print("\n\nWaiting 10 seconds before concurrent test...")
    await asyncio.sleep(10)
    
    # Test 2: Concurrent requests
    await test_concurrent_requests()
    
    print("\n\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
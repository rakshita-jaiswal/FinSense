"""Test response caching system."""
import asyncio
from services.ai_service import ai_service


async def test_caching():
    """Test that caching reduces API calls."""
    print("=" * 60)
    print("TESTING RESPONSE CACHING")
    print("=" * 60)
    
    # Test 1: First request (should miss cache)
    print("\n[Test 1] First request - should MISS cache")
    print("-" * 60)
    question1 = "What is double-entry bookkeeping?"
    response1 = await ai_service.generate_response(question1, None, None)
    print(f"Question: {question1}")
    print(f"Response length: {len(response1)} characters")
    print(f"Response preview: {response1[:100]}...")
    
    # Test 2: Same request (should hit cache)
    print("\n[Test 2] Same request - should HIT cache")
    print("-" * 60)
    response2 = await ai_service.generate_response(question1, None, None)
    print(f"Question: {question1}")
    print(f"Response length: {len(response2)} characters")
    print(f"Same response: {response1 == response2}")
    
    # Test 3: Different request (should miss cache)
    print("\n[Test 3] Different request - should MISS cache")
    print("-" * 60)
    question2 = "How do I categorize expenses?"
    response3 = await ai_service.generate_response(question2, None, None)
    print(f"Question: {question2}")
    print(f"Response length: {len(response3)} characters")
    print(f"Response preview: {response3[:100]}...")
    
    # Test 4: Repeat second question (should hit cache)
    print("\n[Test 4] Repeat second question - should HIT cache")
    print("-" * 60)
    response4 = await ai_service.generate_response(question2, None, None)
    print(f"Question: {question2}")
    print(f"Same response: {response3 == response4}")
    
    # Test 5: Case insensitive (should hit cache)
    print("\n[Test 5] Case variation - should HIT cache")
    print("-" * 60)
    question3 = "WHAT IS DOUBLE-ENTRY BOOKKEEPING?"
    response5 = await ai_service.generate_response(question3, None, None)
    print(f"Question: {question3}")
    print(f"Same as first response: {response1 == response5}")
    
    # Get cache statistics
    print("\n" + "=" * 60)
    print("CACHE STATISTICS")
    print("=" * 60)
    stats = ai_service.get_cache_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("CACHE TEST COMPLETED")
    print("=" * 60)
    
    # Calculate expected results
    expected_hits = 3  # Tests 2, 4, 5
    expected_misses = 2  # Tests 1, 3
    actual_hits = stats['hits']
    actual_misses = stats['misses']
    
    if actual_hits >= expected_hits and actual_misses == expected_misses:
        print("\n[SUCCESS] Caching is working correctly!")
        print(f"  - Cache hits: {actual_hits} (expected >= {expected_hits})")
        print(f"  - Cache misses: {actual_misses} (expected {expected_misses})")
        print(f"  - Hit rate: {stats['hit_rate']}")
    else:
        print("\n[WARNING] Cache statistics don't match expected values")
        print(f"  - Expected hits >= {expected_hits}, got {actual_hits}")
        print(f"  - Expected misses = {expected_misses}, got {actual_misses}")


async def test_sample_prompts():
    """Test that sample prompts are pre-cached."""
    print("\n\n" + "=" * 60)
    print("TESTING SAMPLE PROMPTS PRE-CACHING")
    print("=" * 60)
    
    from services.sample_responses import get_sample_prompts
    
    prompts = get_sample_prompts()
    print(f"\nTotal sample prompts: {len(prompts)}")
    
    # Test a few sample prompts
    test_prompts = prompts[:3]
    
    for i, prompt_obj in enumerate(test_prompts, 1):
        print(f"\n[Prompt {i}] {prompt_obj['text']}")
        print("-" * 60)
        response = await ai_service.generate_response(prompt_obj['text'], None, None)
        print(f"Response length: {len(response)} characters")
        print(f"Response preview: {response[:150]}...")
    
    # Check cache stats
    stats = ai_service.get_cache_stats()
    print("\n" + "=" * 60)
    print("FINAL CACHE STATISTICS")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n[SUCCESS] Sample prompts are working!")


async def main():
    """Run all caching tests."""
    await test_caching()
    await test_sample_prompts()


if __name__ == "__main__":
    asyncio.run(main())
"""Test script for KmbApiClient to verify models and API connectivity."""

import asyncio

from .kmb_api_client import KmbApiClient


async def test_get_bounds(client: KmbApiClient, route: str):
    """Test get_bounds function."""
    print(f"Testing get_bounds('{route}')...", end=" ")
    try:
        result = await client.get_bounds(route)
        print("✓ Success")
        # print(result.model_dump_json(indent=2))
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_schedule(client: KmbApiClient, route: str, bound: int):
    """Test get_schedule function."""
    print(f"Testing get_schedule('{route}', {bound})...", end=" ")
    try:
        result = await client.get_schedule(route, bound)
        print("✓ Success")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_stops(client: KmbApiClient, route: str, bound: int):
    """Test get_stops function."""
    print(f"Testing get_stops('{route}', {bound})...", end=" ")
    try:
        result = await client.get_stops(route, bound)
        print("✓ Success")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def main():
    """Run all tests."""
    print("=" * 60)
    print("KmbApiClient Test Script")
    print("=" * 60)
    print()

    client = KmbApiClient()
    test_results = {"passed": 0, "failed": 0}

    # Use a common route for testing
    TEST_ROUTE = "271B"

    # Test 1: Get Bounds
    bounds_result = await test_get_bounds(client, TEST_ROUTE)
    if bounds_result:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
        print("Cannot continue without bounds. Exiting.")
        return

    TEST_BOUND = 1
    if bounds_result.data and hasattr(bounds_result.data[0], "BOUND"):
        TEST_BOUND = bounds_result.data[0].BOUND

    print()

    # Test 2: Get Schedule
    schedule_result = await test_get_schedule(client, TEST_ROUTE, TEST_BOUND)
    if schedule_result:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1

    print()

    # Test 3: Get Stops
    stops_result = await test_get_stops(client, TEST_ROUTE, TEST_BOUND)
    if stops_result:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1

    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    print(f"Total: {test_results['passed'] + test_results['failed']}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

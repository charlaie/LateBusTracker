"""Simple test script to verify all KmbApi functions work without errors."""

import asyncio
from typing import Literal

from kmb_api import KmbApi


async def test_get_route_list(api: KmbApi):
    """Test get_route_list_ function."""
    print("Testing get_route_list_()...", end=" ")
    try:
        result = await api.get_route_list_()
        print(f"✓ Success - Got {len(result.data)} routes")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_route(
    api: KmbApi,
    route: str,
    direction: Literal["outbound", "inbound"],
    service_type: int,
):
    """Test get_route function."""
    print(f"Testing get_route('{route}', '{direction}', {service_type})...", end=" ")
    try:
        result = await api.get_route(route, direction, service_type)
        print(f"✓ Success - Route: {result.data.route}")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_stop_list(api: KmbApi):
    """Test get_stop_list function."""
    print("Testing get_stop_list()...", end=" ")
    try:
        result = await api.get_stop_list()
        print(f"✓ Success - Got {len(result.data)} stops")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_stop(api: KmbApi, stop_id: str):
    """Test get_stop function."""
    print(f"Testing get_stop('{stop_id}')...", end=" ")
    try:
        result = await api.get_stop(stop_id)
        print(f"✓ Success - Stop: {result.data.name_en}")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_route_stop_list(api: KmbApi):
    """Test get_route_stop_list function."""
    print("Testing get_route_stop_list()...", end=" ")
    try:
        result = await api.get_route_stop_list()
        print(f"✓ Success - Got {len(result.data)} route-stop entries")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_route_stop(
    api: KmbApi,
    route: str,
    direction: Literal["outbound", "inbound"],
    service_type: int,
):
    """Test get_route_stop function."""
    print(
        f"Testing get_route_stop('{route}', '{direction}', {service_type})...", end=" "
    )
    try:
        result = await api.get_route_stop(route, direction, service_type)
        print(f"✓ Success - Route: {result.data[0].route}, Stop: {result.data[0].stop}")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_eta(api: KmbApi, stop_id: str, route: str, service_type: int):
    """Test get_eta function."""
    print(f"Testing get_eta('{stop_id}', '{route}', {service_type})...", end=" ")
    try:
        result = await api.get_eta(stop_id, route, service_type)
        print(f"✓ Success - Got {len(result.data)} ETA entries")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_stop_eta(api: KmbApi, stop_id: str):
    """Test get_stop_eta function."""
    print(f"Testing get_stop_eta('{stop_id}')...", end=" ")
    try:
        result = await api.get_stop_eta(stop_id)
        print(f"✓ Success - Got {len(result.data)} ETA entries")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def test_get_route_eta(api: KmbApi, route: str, service_type: int):
    """Test get_route_eta function."""
    print(f"Testing get_route_eta('{route}', {service_type})...", end=" ")
    try:
        result = await api.get_route_eta(route, service_type)
        print(f"✓ Success - Got {len(result.data)} ETA entries")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


async def main():
    """Run all tests."""
    print("=" * 60)
    print("KmbApi Test Script")
    print("=" * 60)
    print()

    api = KmbApi()
    test_results = {"passed": 0, "failed": 0}

    # Test 1: Get route list (needed for other tests)
    print("1. Testing list endpoints...")
    route_list = await test_get_route_list(api)
    if route_list:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
        print("Cannot continue without route list. Exiting.")
        return

    stop_list = await test_get_stop_list(api)
    if stop_list:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1

    route_stop_list = await test_get_route_stop_list(api)
    if route_stop_list:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1

    print()

    # Test 2: Get specific route (use first route from list)
    print("2. Testing specific route endpoints...")
    if route_list and route_list.data:
        first_route = route_list.data[0]
        route_result = await test_get_route(
            api, first_route.route, "outbound", int(first_route.service_type)
        )
        if route_result:
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1

        # Test route-stop with same route
        route_stop_result = await test_get_route_stop(
            api, first_route.route, "outbound", int(first_route.service_type)
        )
        if route_stop_result:
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
    else:
        print("Skipping route tests - no routes available")

    print()

    # Test 3: Get specific stop (use first stop from list)
    print("3. Testing specific stop endpoints...")
    if stop_list and stop_list.data:
        first_stop = stop_list.data[0]
        stop_result = await test_get_stop(api, first_stop.stop)
        if stop_result:
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
    else:
        print("Skipping stop tests - no stops available")

    print()

    # Test 4: Get ETA (use route-stop data if available)
    print("4. Testing ETA endpoints...")
    if route_stop_list and route_stop_list.data:
        # Find a route-stop entry to use for ETA tests
        first_route_stop = route_stop_list.data[0]

        # Test get_eta
        eta_result = await test_get_eta(
            api,
            first_route_stop.stop,
            first_route_stop.route,
            int(first_route_stop.service_type),
        )
        if eta_result:
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1

        # Test get_stop_eta
        stop_eta_result = await test_get_stop_eta(api, first_route_stop.stop)
        if stop_eta_result:
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1

        # Test get_route_eta
        route_eta_result = await test_get_route_eta(
            api, first_route_stop.route, int(first_route_stop.service_type)
        )
        if route_eta_result:
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
    else:
        print("Skipping ETA tests - no route-stop data available")

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

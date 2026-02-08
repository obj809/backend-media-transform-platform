#!/usr/bin/env python3
"""Script to test all API endpoints."""

import httpx

BASE_URL = "http://localhost:8000"


def test_all_endpoints():
    with httpx.Client(base_url=BASE_URL) as client:
        # GET /
        print("GET /")
        response = client.get("/")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        print()


if __name__ == "__main__":
    test_all_endpoints()

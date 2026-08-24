import json
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"


def main():
    print(f"Sending GET request to: {API_URL}")

    try:
        response = requests.get(API_URL, timeout=20)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Fail clearly if unsuccessful
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        print(f"Status code: {response.status_code}")
        return

    print(f"Status code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

    # Parse JSON
    payload = response.json()

    # Determine top-level structure
    top_level_type = type(payload).__name__
    print(f"Top-level type: {top_level_type}")

    if isinstance(payload, list):
        print(f"Number of records: {len(payload)}")
        sample_record = payload[0] if len(payload) > 0 else None
    elif isinstance(payload, dict):
        print(f"Top-level keys: {list(payload.keys())}")
        # Try to find a list inside the dict (common API pattern)
        list_fields = [k for k, v in payload.items() if isinstance(v, list)]
        if list_fields:
            first_list_key = list_fields[0]
            print(f"Number of records (in '{first_list_key}'): {len(payload[first_list_key])}")
            sample_record = payload[first_list_key][0] if payload[first_list_key] else payload
        else:
            print("No list found inside the object; treating whole object as one record.")
            sample_record = payload
    else:
        sample_record = payload

    print("\nSample record:")
    print(json.dumps(sample_record, indent=2, ensure_ascii=False))

    # Save raw response as JSON
    output_path = Path("data/raw/api_snapshot.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    retrieved_at_utc = datetime.now(timezone.utc).isoformat()
    print(f"\nSaved response to: {output_path}")
    print(f"retrieved_at_utc: {retrieved_at_utc}")


if __name__ == "__main__":
    main()

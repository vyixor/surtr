import requests
from typing import Optional, Dict, Any

API_URL = "http://screenbot.cu.ma/api.php"
DEFAULT_TIMEOUT = 30 # seconds


def post_json(session: requests.Session, payload: Dict[str, Any], url: str = API_URL,
              timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict[str, Any]]:
    """
    POST JSON to the API with timeout and unified error handling.
    Returns parsed JSON as dict on success, or None on failure.
    """
    try:
        resp = session.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()  # raise for 4xx/5xx
    except requests.exceptions.RequestException as e:
        #print(f"[network error] request failed for payload {payload!r}: {e}")
        return None

    try:
        data = resp.json()
    except ValueError as e:
        #print(f"[parse error] failed to decode JSON response: {e}")
        return None

    if not isinstance(data, dict):
        #print(f"[type error] expected JSON object but got: {type(data).__name__}")
        return None

    return data


def validate_activation(appid: str, gmail: str, url: str = API_URL,
                        timeout: int = DEFAULT_TIMEOUT) -> bool:
    payload = {'appid': appid, 'gmail': gmail, 'type': 'validate'}
    with requests.Session() as s:
        result = post_json(s, payload, url=url, timeout=timeout)

    if not result:
        # network/parse error already printed
        return False

    status = result.get('status')
    total_rows = result.get('total_rows')  # may be None if missing
    #print(result)
    if status == 'success' and isinstance(total_rows, int) and total_rows > 0:
        return True

    # Print friendly debug info
    #print(f"[validation failed] server response: {result}")
    return False


def check_update(sutrversion: str, url: str = API_URL,
                 timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict[str, Any]]:
    payload = {'type': 'updatecheck', 'sutrversion': sutrversion}
    with requests.Session() as s:
        result = post_json(s, payload, url=url, timeout=timeout)

    if not result:
        return None

    if result.get('status') != 'success':
        #print(f"[update check] server returned non-success status: {result}")
        return None

    data = result.get('data')
    if not data:
        #print("[update check] no update data returned.")
        return None

    # Assume data is a list and first item is latest update info
    latest_update = data[0] if isinstance(data, list) and data else None
    return latest_update

"""
if __name__ == "__main__":
    # Example usage
    appid = '1111-2222-1111-3333-4444'
    gmail = 'test@gmail.com'

    if validate_activation(appid, gmail):
        print("Valid activation key!")
    else:
        print("Invalid key or request failed.")

    latest = check_update('pro')
    if latest:
        print("Latest update info:", type(latest))
    else:
        print("Could not retrieve update information.")



outputs:
license check = Valid activation key!
update = Latest update info: {'id': 2, 'downloadfile': 'https://file/pro/updatefile.exe', 'version': '4.55', 'date': 'saturday 25,2025', 'sutrversion': 'pro'}

    
"""
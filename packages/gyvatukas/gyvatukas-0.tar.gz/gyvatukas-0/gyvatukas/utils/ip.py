import requests


def _get_ipinfo_io() -> dict:
    result = requests.get(url="https://ipinfo.io/json")
    result_json = result.json()
    result_json.pop("readme")
    return result_json


def _get_ifconfig_me() -> str:
    result = requests.get(url="https://ifconfig.me")
    return result.text


def get_external_ip_v4() -> str:
    """Calls https://ipinfo.io/json."""
    return _get_ipinfo_io()["ip"]


def get_ip_v4_meta() -> dict:
    """Calls https://ipinfo.io/json."""
    return _get_ipinfo_io()

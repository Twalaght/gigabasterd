#!/usr/bin/env python3
""" Simple script to cycle through connected servers in a Gluetun instance. """
import json
import logging

from requests import get, put

with open("/cycle/valid_servers.json") as f:
    hostnames = json.loads(f.read())

def cycle_gluetun() -> None:
    """ Fetch current Gluetun config, and swap to the next VPN host. """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
    )

    response = get("http://localhost:8000/v1/vpn/settings")
    response.raise_for_status()

    # Use the first item in the list as a failsafe, otherwise find the next sequential item
    new_hostname = hostnames[0]
    if current_hostname := response.json().get("provider").get("server_selection").get("hostnames"):
        current_hostname = current_hostname[0]
        current_index = hostnames.index(current_hostname)
        new_hostname = hostnames[(current_index + 1) % len(hostnames)]

    headers = {"content-type": "application/json"}
    payload = {"provider": {"server_selection": {"hostnames": [new_hostname]}}}

    logging.warning(f"Cycling '{current_hostname}' -> '{new_hostname}'")
    response = put("http://localhost:8000/v1/vpn/settings", json=payload, headers=headers)
    response.raise_for_status()


if __name__ == "__main__":
    cycle_gluetun()

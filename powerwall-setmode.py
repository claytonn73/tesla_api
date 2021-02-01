##############################################################################
# Python script to set mode and backup server percentages
# This might be used with automation such as Home Assistant to change
# modes to charge the battery at cheap rate electricity times
##############################################################################

import json
import requests
import time
import asyncio
import sys
import argparse
from enum import Enum
from tesla_api import TeslaApiClient
from tesla_api.energy import PowerwallMode


class PowerwallReserved(Enum):
    # Reserved Percentage for different Powerwall modes
    AUTONOMOUS = 0
    SELF_CONSUMPTION = 0
    BACKUP = 100


def getopts(argv):
    parser = argparse.ArgumentParser(
        description='Set Powerwall operating mode')
    parser.add_argument('-m', '--mode', required=True, type=PowerwallMode,
                        choices=PowerwallMode, help='Desired operating mode for powerwall')
    args = parser.parse_args()

    return args


async def save_token(token):
    with open("/data/homeassistant/.homeassistant/tokens.json", 'w') as file:
        file.write(token)


def get_token(file):
    try:
        token = open("/data/homeassistant/.homeassistant/" + file).read()
        return token
    except OSError:
        print("Unable to read token file")
        sys.exit(2)


async def main(desiredmode):

    accesstokens = get_token("tokens.json")

    client = TeslaApiClient(token=accesstokens, on_new_token=save_token)

    await client.authenticate()

    # Get the current operating mode
    energy_sites = await client.list_energy_sites()
    opmode = PowerwallMode(await energy_sites[0].get_operating_mode())

    # If the current operating mode is not as desired then set mode and reserved percentage
    if opmode != desiredmode:
        print("Setting mode to {} from {} and backup reserve percentage to {}"
              .format(desiredmode.value, opmode.value, PowerwallReserved[desiredmode.name].value))
        await energy_sites[0].set_operating_mode(desiredmode)
        await energy_sites[0].set_backup_reserve_percent(PowerwallReserved[desiredmode.name].value)
    else:
        print("Current operating mode is already {} ".format(desiredmode.value))

    await client.close()

args = getopts(sys.argv[1:])

asyncio.run(main(args.mode))

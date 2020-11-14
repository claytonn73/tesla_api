##############################################################################
# Python script to set mode and backup server percentages
# This might be used with automation such as Home Assistant to change
# modes to charge the battery at cheap rate electricity times
##############################################################################

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
    parser = argparse.ArgumentParser(description='Set Powerwall operating mode')
    parser.add_argument('-e', '--email', required=True, help='Powerwall customer email')
    parser.add_argument('-p', '--password', required=True, help='Powerwall customer password')
    parser.add_argument('-m', '--mode', required=True, type=PowerwallMode,
                        choices=PowerwallMode, help='Desired operating mode for powerwall')
    args = parser.parse_args()

    return args


async def main(email, password, desiredmode):

    client = TeslaApiClient(email, password)
    try:
        await client.authenticate()
    except:
        print("Authentication failed")
        await client.close()
        sys.exit(2)

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

asyncio.run(main(args.email, args.password, args.mode))

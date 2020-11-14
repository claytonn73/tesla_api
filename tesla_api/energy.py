##############################################################################
# Class to manage a Powerwall (tested on one Powerwall 2) via the Tesla API
##############################################################################
# MIT License
#
# Copyright (c) 2019 S.W. Moore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import date, datetime, time
from typing import Optional, Union
from .const import (
                   PowerwallMode,
                   HistoryType,
                   HistoryPeriod,
                   EnergySites,
                   LiveStatus,
                   SiteInfo,
                   SiteInfoUserSettings,
                   SiteInfoComponents,
                   TouSettings,
                   HistoryData,
                   SelfConsumptionTimeSeries,
                   TESLA_API_PERIOD,
                   TESLA_API_KIND,
                   TESLA_API_END_DATE,
                   TESLA_API_URL_ENERGY_SITES,
                   TESLA_API_URL_SITE_INFO,
                   TESLA_API_URL_LIVE_STATUS,
                   TESLA_API_URL_CALENDAR_HISTORY,
                   TESLA_API_URL_OPERATION,
                   TESLA_API_URL_BACKUP,
)


class Energy:
    def __init__(self, api_client, energy_site_id):
        self._api_client = api_client
        self._energy_site_id = energy_site_id

    @property
    def site_id(self):
        return self._energy_site_id

    async def get_energy_site_info(self):
        return await self._api_client.get('{}/{}/{}'.format(
            TESLA_API_URL_ENERGY_SITES,
            self._energy_site_id,
            TESLA_API_URL_SITE_INFO))

    async def print_energy_site_info(self):
        info = await self.get_energy_site_info()
        for data in SiteInfo:
            if data.name == SiteInfo.USER_SETTINGS.name:
                for settings in SiteInfoUserSettings:
                    print(settings.value, info[data.value][settings.value])
            elif data.name == SiteInfo.COMPONENTS.name:
                for components in SiteInfoComponents:
                    print(components.value, info[data.value][components.value])
            elif data.name == SiteInfo.TOU_SETTINGS.name:
                for settings in TouSettings:
                    print(settings.value, info[data.value][settings.value])
            else:
                print(data.value, info[data.value])

    # Helper functions for get_energy_site_info
    async def get_backup_reserve_percent(self):
        info = await self.get_energy_site_info()
        return int(info[EnergySites.BACKUP_RESERVE_PERCENT.value])

    async def get_operating_mode(self):
        info = await self.get_energy_site_info()
        return info[EnergySites.DEFAULT_REAL_MODE.value]

    async def get_version(self):
        info = await self.get_energy_site_info()
        return info[EnergySites.VERSION.value]

    async def get_battery_count(self):
        info = await self.get_energy_site_info()
        return int(info[EnergySites.BATTERY_COUNT.value])

    async def get_energy_site_calendar_history_data(
            self, kind=HistoryType.ENERGY.value, period=HistoryPeriod.DAY.value,
            end_date: Optional[Union[str, date]] = None) -> dict:
        """Return historical energy data.

        Args:
            kind: [power, energy, self_consumption]
            period: Amount of time to include in report. One of day, week, month, year,
                and lifetime. When kind is 'power', this parameter is ignored, and the
                period is always 'day'.
            end_date: A date/datetime object, or a str in ISO 8601 format
                (e.g. 2019-12-23T17:39:18.546Z). The response report interval ends at this
                datetime and starts at the beginning of the given period. For example,
                with datetime(year=2020, month=5, day=1), this gets all data for May 1st.
                Defaults to the current time.
        """
        params = {TESLA_API_KIND: kind, TESLA_API_PERIOD: period}

        if isinstance(end_date, date):
            if not isinstance(end_date, datetime):
                end_date = datetime.combine(end_date, time(23, 59, 59))
            elif end_date.hour == 0 and end_date.minute == 0:
                # If the datetime object's time is 00:00 then the API returns nothing.
                # We adjust by adding 23:59, so it's possible to use
                # datetime(year=2020, month=5, day=2) and it gets the data for
                # May 2, 2020 as expected.
                end_date = end_date.replace(hour=23, minute=59, second=59)
            end_date = end_date.isoformat()

        if end_date is not None:
            params[TESLA_API_END_DATE] = end_date

        return await self._api_client.get('{}/{}/{}'.format(
            TESLA_API_URL_ENERGY_SITES,
            self._energy_site_id,
            TESLA_API_URL_CALENDAR_HISTORY),
            params=params)

    # Helper functions for get_energy_site_calendar_history_data
    async def get_energy_site_power_history(self):
        history = await self.get_energy_site_calendar_history_data(kind=HistoryType.POWER.value)
        return history

    async def get_energy_site_energy_history(self, period=HistoryPeriod.DAY.value):
        history = await self.get_energy_site_calendar_history_data(kind=HistoryType.ENERGY.value, period=period)
        return history

    async def get_energy_site_self_consumption_history(self, period=HistoryPeriod.DAY.value):
        history = await self.get_energy_site_calendar_history_data(kind=HistoryType.SELF_CONSUMPTION.value,
                                                                   period=period)
        timestamp = history[HistoryData.TIME_SERIES.value][0][SelfConsumptionTimeSeries.TIMESTAMP.value]
        solar_percent = int(history[HistoryData.TIME_SERIES.value][0][SelfConsumptionTimeSeries.SOLAR_PERCENT.value])
        battery_percent = int(history[HistoryData.TIME_SERIES.value][0][SelfConsumptionTimeSeries.BATTERY_PERCENT.value])
        return timestamp, solar_percent, battery_percent

    # Live Status Information
    async def get_energy_site_live_status(self):
        return await self._api_client.get('{}/{}/{}'.format(
            TESLA_API_URL_ENERGY_SITES,
            self._energy_site_id,
            TESLA_API_URL_LIVE_STATUS))

    async def print_energy_site_live_status(self):
        info = await self.get_energy_site_live_status()
        for data in LiveStatus:
            if data.name == LiveStatus.ENERGY_LEFT.name:
                print(data.value, int(info[data.value]))
            elif data.name == LiveStatus.PERCENTAGE_CHARGED.name:
                print(data.value, int(info[data.value]))
            else:
                print(data.value, info[data.value])

    # Helper functions for get_energy_site_live_status
    async def get_energy_site_live_status_percentage_charged(self):
        status = await self.get_energy_site_live_status()
        return int(status[LiveStatus.PERCENTAGE_CHARGED.value])

    async def get_energy_site_live_status_energy_left(self):
        status = await self.get_energy_site_live_status()
        return int(status[LiveStatus.ENERGY_LEFT.value])

    async def get_energy_site_live_status_total_pack_energy(self):
        status = await self.get_energy_site_live_status()
        return int(status[LiveStatus.TOTAL_PACK_ENERGY.value])

    async def get_solar_power(self):
        status = await self.get_energy_site_live_status()
        return int(status[LiveStatus.SOLAR_POWER.value])

    # Setting of the backup_reserve_percent
    async def set_backup_reserve_percent(self, backup_reserve_percent):
        assert 0 <= backup_reserve_percent <= 100
        return await self._api_client.post(
            endpoint='{}/{}/{}'.format(
                TESLA_API_URL_ENERGY_SITES,
                self._energy_site_id,
                TESLA_API_URL_BACKUP),
            data={EnergySites.BACKUP_RESERVE_PERCENT.value: backup_reserve_percent}
        )

    # Setting the operating mode of the Powerwall
    # Mode uses the PowerwallMode Enum
    async def set_operating_mode(self, mode):
        return await self._api_client.post(
            endpoint='{}/{}/{}'.format(
                TESLA_API_URL_ENERGY_SITES,
                self._energy_site_id,
                TESLA_API_URL_OPERATION),
            data={EnergySites.DEFAULT_REAL_MODE.value: mode.value}
        )

    # helper functions for set_operating_mode
    async def set_operating_mode_self_consumption(self):
        return await self.set_operating_mode(PowerwallMode.SELF_CONSUMPTION)

    async def set_operating_mode_backup(self):
        return await self.set_operating_mode(PowerwallMode.BACKUP)

    async def set_operating_mode_autonomous(self):
        return await self.set_operating_mode(PowerwallMode.AUTONOMOUS)

import asyncio
import json
from datetime import datetime, timedelta

import aiohttp

from .exceptions import ApiError, AuthenticationError, VehicleUnavailableError
from .vehicle import Vehicle
from .energy import Energy
from .const import (
    EnergySites,
    TESLA_API_TOKEN_URL,
    TESLA_API_URL,
    OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET,
    TESLA_API_URL_PRODUCTS,
    TESLA_API_URL_VEHICLES,
)


class TeslaApiClient:
    callback_update = None  # Called when vehicle's state has been updated.
    callback_wake_up = None  # Called when attempting to wake a vehicle.
    timeout = 30  # Default timeout for operations such as Vehicle.wake_up().

    def __init__(self, email=None, password=None, token=None, on_new_token=None):
        """Creates client from provided credentials.

        If token is not provided, or is no longer valid, then a new token will
        be fetched if email and password are provided.

        If on_new_token is provided, it will be called with the newly created token.
        This should be used to save the token, both after initial login and after an
        automatic token renewal. The token is returned as a string and can be passed
        directly into this constructor.
        """
        assert token is not None or (email is not None and password is not None)
        self._email = email
        self._password = password
        self._token = json.loads(token) if token else None
        self._new_token_callback = on_new_token
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()

    async def _get_token(self, data):
        request_data = {
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET
        }
        request_data.update(data)

        async with self._session.post(TESLA_API_TOKEN_URL, data=request_data) as resp:
            response_json = await resp.json()
            if resp.status == 401:
                raise AuthenticationError(response_json)

        # Send token to application via callback.
        if self._new_token_callback:
            asyncio.create_task(self._new_token_callback(json.dumps(response_json)))

        return response_json

    async def _get_new_token(self):
        return await self._get_token({'grant_type': 'password', 'email': self._email,
                                      'password': self._password, })

    async def _refresh_token(self, refresh_token):
        return await self._get_token({'grant_type': 'refresh_token',
                                      'refresh_token': refresh_token})

    async def authenticate(self):
        if not self._token:
            self._token = await self._get_new_token()

        expiry_time = timedelta(seconds=self._token['expires_in'])
        expiration_date = datetime.fromtimestamp(self._token['created_at']) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self._token = await self._refresh_token(self._token['refresh_token'])

    def _get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._token['access_token'])
        }

    async def get(self, endpoint, params=None):
        await self.authenticate()
        url = '{}/{}'.format(TESLA_API_URL, endpoint)

        async with self._session.get(url, headers=self._get_headers(), params=params) as resp:
            response_json = await resp.json()

        if 'error' in response_json:
            if 'vehicle unavailable' in response_json['error']:
                raise VehicleUnavailableError()
            raise ApiError(response_json['error'])

        return response_json['response']

    async def post(self, endpoint, data=None):
        await self.authenticate()
        url = '{}/{}'.format(TESLA_API_URL, endpoint)

        async with self._session.post(url, headers=self._get_headers(), json=data) as resp:
            response_json = await resp.json()

        if 'error' in response_json:
            if 'vehicle unavailable' in response_json['error']:
                raise VehicleUnavailableError()
            raise ApiError(response_json['error'])

        return response_json['response']

    async def list_vehicles(self):
        return [Vehicle(self, vehicle) for vehicle in await self.get(TESLA_API_URL_VEHICLES)]

    async def list_energy_sites(self):
        return [Energy(self, product[EnergySites.ENERGY_SITE_ID.value]) for
                product in await self.get(TESLA_API_URL_PRODUCTS) if EnergySites.ENERGY_SITE_ID.value in product]

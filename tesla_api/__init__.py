import asyncio
import json
import time
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
    TESLA_API_OAUTH2_URL,
)


class TeslaApiClient:
    callback_update = None  # Called when vehicle's state has been updated.
    callback_wake_up = None  # Called when attempting to wake a vehicle.
    timeout = 30  # Default timeout for operations such as Vehicle.wake_up().

    def __init__(self, token=None, on_new_token=None):
        """Creates client from provided credentials.

        If token is not provided, or is no longer valid, then a new token will
        be fetched if email and password are provided.

        If on_new_token is provided, it will be called with the newly created token.
        This should be used to save the token, both after initial login and after an
        automatic token renewal. The token is returned as a string and can be passed
        directly into this constructor.
        """
        assert token is not None
        self._token = json.loads(token) if token else None
        self._new_token_callback = on_new_token
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()

    def _get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._token["authentication_token"]['access_token'])
        }

    def check_token_expiration(self):

        # Check whether current token is close to expiration with less than 1 hour remaining
        expiration_time = self._token["authentication_token"]['created_at'] +\
                          self._token["authentication_token"]['expires_in'] -\
                          int(time.time())
        if expiration_time > 3600:
            return False
        else:
            return True

    async def get_access_token(self, refresh_token):
        # Obtain new shortlived oauth access token using stored refresh token
        headers = {"Requested-With": "com.teslamotors.tesla"}
        payload = {
            "grant_type": "refresh_token",
            "client_id": "ownerapi",
            "client_secret": OAUTH_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "scope": "openid email offline_access",
        }
        async with self._session.post(url=TESLA_API_OAUTH2_URL, headers=headers, json=payload) as response:
            response_json = await response.json()
            if response.status == 200:
                return response_json["access_token"]

    async def get_authentication_token(self, access_token):
        # Use shortlived access token to obtain the long lived access token
        headers = {"authorization": "bearer " + access_token}
        payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET,
        }
        async with self._session.post(url=TESLA_API_TOKEN_URL, headers=headers, json=payload) as response:
            response_json = await response.json()
            if response.status == 200:
                return response_json

    async def refresh_token(self):
        # Get tokens from the token file which contains both oauth and authentication tokens
        if self.check_token_expiration() is True:

            access_token = await self.get_access_token(self._token["oauth_token"]["refresh_token"])

            if access_token is not None:
                new_token = await self.get_authentication_token(access_token)

            if new_token is not None:
                self._token["authentication_token"] = new_token

    async def authenticate(self):
        if self.check_token_expiration() is True:
            await self.refresh_token()
            # Send token to application via callback.
            if self._new_token_callback:
                asyncio.create_task(self._new_token_callback(json.dumps(self._token)))
        return True

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

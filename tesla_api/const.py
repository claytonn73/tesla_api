from enum import Enum

TESLA_API_BASE_URL = 'https://owner-api.teslamotors.com/'
TESLA_API_AUTH_URL = 'https://auth.tesla.com/'
TESLA_API_OAUTH2_URL = TESLA_API_AUTH_URL + 'oauth2/v3/token'
TESLA_API_OAUTH2_AUTH_URL = TESLA_API_AUTH_URL + 'oauth2/v3/authorize'
TESLA_API_REDIRECT_URL = TESLA_API_AUTH_URL + 'void/callback'
TESLA_API_TOKEN_URL = TESLA_API_BASE_URL + 'oauth/token'
TESLA_API_URL = TESLA_API_BASE_URL + 'api/1'
TESLA_API_URL_VEHICLES = 'vehicles'
TESLA_API_URL_PRODUCTS = 'products'
TESLA_API_URL_SITE_INFO = 'site_info'
TESLA_API_URL_LIVE_STATUS = 'live_status'
TESLA_API_URL_CALENDAR_HISTORY = 'calendar_history'
TESLA_API_URL_ENERGY_SITES = 'energy_sites'
TESLA_API_URL_OPERATION = 'operation'
TESLA_API_URL_BACKUP = 'backup'

OAUTH_CLIENT_ID = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
OAUTH_CLIENT_SECRET = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
OAUTH_OWNERAPI = 'ownerapi'
OAUTH_SCOPE = 'openid email offline_access'
OAUTH_TOKEN_FILE = 'oauth_token_file.json'
TOKEN_FILE = 'token_file.json'

TESLA_API_PERIOD = 'period'
TESLA_API_KIND = 'kind'
TESLA_API_END_DATE = 'end_date'


class SiteInfo(Enum):
    ID = 'id'
    SITE_NAME = 'site_name'
    BACKUP_RESERVE_PERCENT = 'backup_reserve_percent'
    DEFAULT_REAL_MODE = 'default_real_mode'
    INSTALLATION_DATE = 'installation_date'
    VERSION = 'version'
    BATTERY_COUNT = 'battery_count'
    USER_SETTINGS = 'user_settings'
    COMPONENTS = 'components'
    TOU_SETTINGS = 'tou_settings'
    NAMEPLATE_POWER = 'nameplate_power'
    NAMEPLATE_ENERGY = 'nameplate_energy'
    INSTALLATION_TIME_ZONE = 'installation_time_zone'


class SiteInfoUserSettings(Enum):
    STORM_MODE_ENABLED = 'storm_mode_enabled'
    SYNC_GRID_ALERT_ENABLED = 'sync_grid_alert_enabled'
    BREAKER_ALERT_ENABLED = 'breaker_alert_enabled'


class SiteInfoComponents(Enum):
    SOLAR = 'solar'
    SOLAR_TYPE = 'solar_type'
    BATTERY = 'battery'
    GRID = 'grid'
    BACKUP = 'backup'
    GATEWAY = 'gateway'
    LOAD_METER = 'load_meter'
    TOU_CAPABLE = 'tou_capable'
    STORM_MODE_CAPABLE = 'storm_mode_capable'
    FLEX_ENERGY_REQUEST_CAPABLE = 'flex_energy_request_capable'
    CAR_CHARGING_DATA_SUPPORTED = 'car_charging_data_supported'
    OFF_GRID_VEHICLE_CHARGING_RESERVE_SUPPORTED = 'off_grid_vehicle_charging_reserve_supported'
    VEHICLE_CHARGING_PERFORMANCE_VIEW_ENABLED = 'vehicle_charging_performance_view_enabled'
    VEHICLE_CHARGING_SOLAR_OFFSET_VIEW_ENABLED = 'vehicle_charging_solar_offset_view_enabled'
    BATTERY_SOLAR_OFFSET_VIEW_ENABLED = 'battery_solar_offset_view_enabled'
    BATTERY_TYPE = 'battery_type'
    CONFIGURABLE = 'configurable'
    GRID_SERVICES_ENABLED = 'grid_services_enabled'


class TouSettings(Enum):
    OPTIMISATION_STRATEGY = 'optimization_strategy'
    SCHEDULE = 'schedule'


class TouSchedule(Enum):
    TARGET = 'target'
    WEEK_DAYS = 'week_days'
    START_SECONDS = 'start_seconds'
    END_SECONDS = 'end_seconds'


class EnergySites(Enum):
    VERSION = 'version'
    ENERGY_SITE_ID = 'energy_site_id'
    DEFAULT_REAL_MODE = 'default_real_mode'
    BACKUP_RESERVE_PERCENT = 'backup_reserve_percent'
    RESOURCE_TYPE = 'resource_type'
    SITE_NAME = 'site_name'
    ID = 'id'
    GATEWAY_ID = 'gateway_id'
    ASSET_SITE_ID = 'asset_site_id'
    ENERGY_LEFT = 'energy_left'
    TOTAL_PACK_ENERGY = 'total_pack_energy'
    PERCENTAGE_CHARGED = 'percentage_charged'
    BATTERY_TYPE = 'battery_type'
    BACKUP_CAPABLE = 'backup_capable'
    BATTERY_POWER = 'battery_power'
    SYNC_GRID_ALERT_ENABLED = 'sync_grid_alert_enabled'
    BREAKER_ALERT_ENABLED = 'breaker_alert_enabled'
    COMPONENTS = 'components'


class EnergySiteComponents(Enum):
    BATTERY = 'battery'
    BATTERY_TYPE = 'battery_type'
    SOLAR = 'solar'
    SOLAR_TYPE = 'solar_type'
    GRID = 'grid'
    LOAD_METER = 'load_meter'
    MARKET_TYPE = 'market_type'


class LiveStatus(Enum):
    TOTAL_PACK_ENERGY = 'total_pack_energy'
    ENERGY_LEFT = 'energy_left'
    PERCENTAGE_CHARGED = 'percentage_charged'
    SOLAR_POWER = 'solar_power'
    BATTERY_POWER = 'battery_power'
    LOAD_POWER = 'load_power'
    GRID_POWER = 'grid_power'
    GENERATOR_POWER = 'generator_power'
    GRID_SERVICES_POWER = 'grid_services_power'
    GRID_STATUS = 'grid_status'
    GRID_SERVICES_ACTIVE = 'grid_services_active'
    BACKUP_CAPABLE = 'backup_capable'
    STORM_MODE_ACTIVE = 'storm_mode_active'
    TIMESTAMP = 'timestamp'


class HistoryType(Enum):
    # Supported History Types
    POWER = 'power'
    ENERGY = 'energy'
    SELF_CONSUMPTION = 'self_consumption'


class HistoryPeriod(Enum):
    # Supported History Periods
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'
    LIFETIME = 'lifetime'


class HistoryData(Enum):
    SERIAL_NUMBER = 'serial_number'
    PERIOD = 'period'
    INSTALLATION_TIME_ZONE = 'installation_time_zone'
    TIME_SERIES = 'time_series'


class PowerTimeSeries(Enum):
    TIMESTAMP = 'timestamp'
    SOLAR_POWER = 'solar_power'
    BATTERY_POWER = 'battery_power'
    GRID_POWER = 'grid_power'
    GRID_SERVICES_POWER = 'grid_services_power'
    GENERATORY_POWER = 'generator_power'


class SelfConsumptionTimeSeries(Enum):
    TIMESTAMP = 'timestamp'
    SOLAR_PERCENT = 'solar'
    BATTERY_PERCENT = 'battery'


class EnergyTimeSeries(Enum):
    TIMESTAMP = 'timestamp'
    SOLAR_EXPORTED = 'solar_energy_exported'
    GENERATOR_EXPORTED = 'generator_energy_exported'
    BATTERY_EXPORTED = 'battery_energy_exported'
    GRID_SERVICES_IMPORTED = 'grid_services_energy_imported'
    GRID_SERVICES_EXPORTED = 'grid_services_energy_exported'
    GRID_EXPORTED_FROM_SOLAR = 'grid_energy_exported_from_solar'
    GRID_EXPORTED_FROM_GENERATOR = 'grid_energy_exported_from_generator'
    GRID_EXPORTED_FROM_BATTERY = 'grid_energy_exported_from_battery'
    GRID_IMPORTED = 'grid_energy_imported'
    BATTERY_IMPORTED_FROM_GRID = 'battery_energy_imported_from_grid'
    BATTERY_IMPORTED_FROM_SOLAR = 'battery_energy_imported_from_solar'
    BATTERY_IMPORTED_FROM_GENERATOR = 'battery_energy_imported_from_generator'
    CONSUMER_IMPORTED_FROM_GRID = 'consumer_energy_imported_from_grid'
    CONSUMER_IMPORTED_FROM_SOLAR = 'consumer_energy_imported_from_solar'
    CONSUMER_IMPORTED_FROM_BATTERY = 'consumer_energy_imported_from_battery'
    CONSUMER_IMPORTED_FROM_GENERATOR = 'consumer_energy_imported_from_generator'


class PowerwallMode(Enum):
    # Supported Powerwall modes
    #   mode = 'self_consumption' = 'self-powered' on app
    #   mode = 'backup' = 'backup-only' on app
    #   mode = 'autonomous' = 'Advanced - Time-based control' on app
    # Note: setting 'backup' mode causes my Powerwall 2 to charge at 3.4kW
    AUTONOMOUS = 'autonomous'
    BACKUP = 'backup'
    SELF_CONSUMPTION = 'self_consumption'

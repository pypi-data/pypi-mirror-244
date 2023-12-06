from logger_local.LoggerComponentEnum import LoggerComponentEnum


class LocationLocalConstants:
    LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 113
    LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'location local python package'
    OBJECT_FOR_LOGGER_CODE = {
        'component_id': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': 'tal.g@circ.zone'
    }

    OBJECT_FOR_LOGGER_TEST = {
        'component_id': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'developer_email': 'tal.g@circ.zone'
    }

    UNKNOWN_LOCATION_ID = 0
    DEFAULT_NEGIHBORHOOD_NAME = None
    DEFAULT_COUNTY_NAME = None
    DEFAULT_REGION_NAME = None
    '''Cannot be None because it would result in mysql.connector.errors.IntegrityError: 1048 (23000):
    Column 'state_name' cannot be null'''
    DEFAULT_STATE_NAME = 'UNKNOWN'
    DEFAULT_COUNTRY_NAME = 'UNKNOWN'    # Cannot be None because `name` is an index
    DEFAULT_ADDRESS_LOCAL_LANGUAGE = None
    DEFAULT_ADDRESS_ENGLISH = None
    DEFAULT_POSTAL_CODE = None
    DEFAULT_PLUS_CODE = None
    DEFAULT_COORDINATE = {'latitude': 0.0, 'longitude': 0.0}
    LOCATION_SCHEMA_NAME = 'location'
    LOCATION_TABLE_NAME = 'location_table'
    LOCATION_VIEW_NAME = 'location_view'
    COUNTRY_TABLE_NAME = 'country_table'
    COUNTRY_ML_TABLE_NAME = 'country_ml_table'
    COUNTRY_ML_VIEW_NAME = 'country_ml_view'
    COUNTY_TABLE_NAME = 'county_table'
    COUNTY_ML_TABLE_NAME = 'county_ml_table'
    COUNTY_ML_VIEW_NAME = 'county_ml_view'
    NEIGHBORHOOD_TABLE_NAME = 'neighborhood_table'
    NEIGHBORHOOD_ML_TABLE_NAME = 'neighborhood_ml_table'
    NEIGHBORHOOD_ML_VIEW_NAME = 'neighborhood_ml_view'
    REGION_TABLE_NAME = 'region_table'
    REGION_ML_TABLE_NAME = 'region_ml_table'
    REGION_ML_VIEW_NAME = 'region_ml_view'
    STATE_TABLE_NAME = 'state_table'
    STATE_ML_TABLE_NAME = 'state_ml_table'
    STATE_ML_VIEW_NAME = 'state_ml_view'



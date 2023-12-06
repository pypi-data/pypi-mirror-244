from typing import Dict
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from dotenv import load_dotenv  # noqa: E402
load_dotenv()                   # noqa: E402
try:
    # When running from this package
    from neighborhood import Neighborhood
    from county import County
    from region import Region
    from state import State
    from country import Country
except Exception:
    # When importing this module from another package
    from location_local.neighborhood import Neighborhood
    from location_local.county import County
    from location_local.region import Region
    from location_local.state import State
    from location_local.country import Country

from circles_local_database_python.generic_crud import GenericCRUD   # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402

LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 113
LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'location/src/location.py'


object_to_insert = {
    'component_id': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

user_context = UserContext().login_using_user_identification_and_password()


class LocationLocal(GenericCRUD):
    def __init__(self):
        logger.start()

        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    def get_location_ids(self, neighborhood_name: str, county_name: str, region_name: str,
                         state_name: str, country_name: str) -> tuple([list[int], int, int, int, int]):
        logger.start(object={'neighborhood_name': neighborhood_name, 'county_name': county_name,
                     'region_name': region_name, 'state_name': state_name, 'country_name': country_name})

        neighborhood_ids = Neighborhood.get_neighborhood_ids_by_neighborhood_name(neighborhood_name)
        county_ids = County.get_county_ids_by_county_name_state_id(county_name)
        region_ids = Region.get_region_ids_by_region_name(region_name)
        state_ids = State.get_state_ids_by_state_name(state_name)
        country_id = Country.get_country_id_by_country_name(country_name)

        logger.end(object={"neighborhood_ids": neighborhood_ids, "county_ids": county_ids, "region_ids": region_ids,
                           "state_ids": state_ids, "country_id": country_id})
        return (neighborhood_ids, county_ids, region_ids, state_ids, country_id)

    def insert(
            self, data: Dict[str, any],
            lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),
            is_approved: bool = True, new_country_data: Dict[str, any] = None) -> int:
        logger.start(object={'data': data, 'lang_code': lang_code,
                     'is_approved': is_approved, 'new_country_data': new_country_data})
        (neighborhood_id, county_id, region_id, state_id, country_id) = self._check_details_and_insert_if_not_exist(
            data["coordinate"],
            (data["neighborhood"],
             data["county"],
             data["region"],
             data["state"],
             data["country"]),
            lang_code, is_approved, new_country_data)

        insert_location_sql = "INSERT INTO location_table (coordinate, address_local_language, address_english," \
            " neighborhood_id, county_id, region_id, state_id, country_id, postal_code, plus_code, is_approved)" \
            " VALUES (POINT(%s, %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(
            insert_location_sql,
            (data["coordinate"]["latitude"],
             data["coordinate"]["longitude"],
             data["address_local_language"],
             data["address_english"],
             neighborhood_id, county_id, region_id, state_id, country_id, data["postal_code"],
             data["plus_code"],
             is_approved))
        self.connector.commit()

        location_id = self.cursor.lastrowid()

        logger.end(object={'location_id': location_id})
        return location_id

    def update(self, location_id: int, data: Dict[str, any], lang_code: LangCode = "en", is_approved: bool = True):
        logger.start(object={'location_id': location_id, 'data': data,
                     'lang_code': lang_code, 'is_approved': is_approved})
        (neighborhood_id, county_id, region_id, state_id, country_id) = self._check_details_and_insert_if_not_exist(
            data["coordinate"], (data["neighborhood"], data["county"], data["region"], data["state"], data["country"]),
            lang_code, is_approved)

        update_location_sql = "UPDATE location_table SET coordinate = POINT(%s, %s), address_local_language = %s, " \
            "address_english = %s, neighborhood_id = %s, county_id = %s, region_id = %s, state_id = %s," \
            " country_id = %s, postal_code = %s, plus_code = %s, is_approved = %s WHERE location_id = %s"
        self.cursor.execute(
            update_location_sql,
            (data["coordinate"]["latitude"],
             data["coordinate"]["longitude"],
             data["address_local_language"],
             data["address_english"],
             neighborhood_id, county_id, region_id, state_id, country_id, data["postal_code"],
             data["plus_code"],
             is_approved,
             location_id))
        self.connector.commit()
        logger.end()

    def read(self, location_id: int) -> tuple([Dict[str, float], str, str, str, str, str, str, str, str, str]):
        logger.start(object={'location_id': location_id})

        select_location_sql = '''SELECT ST_X(l.coordinate), ST_Y(l.coordinate), l.address_local_language, l.address_english,
                            n.title, c.title, r.title, s.state_name, co.name, l.postal_code, l.plus_code 
                            FROM location_view l 
                            JOIN neighborhood_ml_table n ON n.neighborhood_id = l.neighborhood_id
                            JOIN county_ml_table c ON c.county_id = l.county_id
                            JOIN region_ml_table r ON r.region_id = l.region_id
                            JOIN state_ml_table s ON s.state_id = l.state_id 
                            JOIN country_table co ON co.country_id = l.country_id 
                            WHERE l.location_id = %s LIMIT 1'''
        self.cursor.execute(select_location_sql, (location_id,))
        result = None
        coordinate = None
        result = self.cursor.fetchone()
        if result is None:
            logger.end(object={"result": result})
            return None

        (latitude, longitude, address_local_language, address_english, neighborhood,
         county, region, state, country, postal_code, plus_code) = result
        coordinate = {"latitude": latitude, "longitude": longitude}

        logger.end(object={"address_local_language": address_local_language, "address_english": address_english,
                           "neighborhood": neighborhood, "county": county, "region": region, "state": state,
                           "country": country, "postal_code": postal_code, "plus_code": plus_code})
        return (coordinate, address_local_language, address_english, neighborhood, county, region,
                state, country, postal_code, plus_code)

    def delete(self, location_id: int):
        logger.start(object={'location_id': location_id})

        update_location_sql = "UPDATE location_table SET end_timestamp = NOW() WHERE location_id = %s"
        self.cursor.execute(update_location_sql, (location_id,))

        self.connector.commit()
        logger.end()

    def _check_details_and_insert_if_not_exist(
            self, coordinate: Dict[str, float],
            location_details: tuple([str, str, str, str, str]),
            lang_code: LangCode = 'en', is_approved: bool = False, new_country_data: Dict[str, any] = None) -> tuple(
            [int, int, int, int, int]):
        logger.start(object={'coordinate': coordinate, 'location_details': location_details,
                     'lang_code': lang_code, 'new_country_data': new_country_data})
        (neighborhood_name, county_name, region_name, state_name, country_name) = location_details
        ids = self.get_location_ids(
            neighborhood_name, county_name, region_name, state_name, country_name)
        if ids is None:
            return None
        (neighborhood_ids, county_ids, region_ids, state_ids, country_id) = ids

        if neighborhood_ids == []:
            neighborhood_object = Neighborhood()
            neighborhood_id = neighborhood_object.insert(
                coordinate, neighborhood_name, lang_code, is_approved)
        else:
            neighborhood_id = neighborhood_ids[0]
        if county_ids == []:
            county_object = County()
            county_id = county_object.insert(coordinate, county_name, lang_code, is_approved)
        else:
            county_id = county_ids[0]
        if region_ids == []:
            region_object = Region()
            region_id = region_object.insert(coordinate, region_name, lang_code, is_approved)
        else:
            region_id = region_ids[0]
        if state_ids == []:
            state_object = State()
            state_id = state_object.insert(coordinate, state_name, lang_code)
        else:
            state_id = state_ids[0]
        # I commented the follwing lines because I don't want to insert a new country
        # if country_id == None:
            # country_object = Country()
            # country_id = country_object.insert(coordinate, country_name, lang_code, is_approved, new_country_data)
        logger.end(object={'neighborhood_id': neighborhood_id, 'county_id': county_id,
                   'region_id': region_id, 'state_id': state_id, 'country_id': country_id})
        return (neighborhood_id, county_id, region_id, state_id, country_id)

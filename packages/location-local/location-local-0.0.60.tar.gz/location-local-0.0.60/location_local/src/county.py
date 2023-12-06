from typing import Dict
try:
    # When running from this package
    from location_local_constants import LocationLocalConstants
except Exception:
    # When importing this module from another package
    from location_local.location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402


logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class County(GenericCRUD):
    def __init__(self):
        logger.start()

        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    def insert(
            self, coordinate: Dict[str, float],
            county: str, lang_code: LangCode, title_approved: bool = False, state_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'county': county,
                     'lang_code': lang_code, 'title_approved': title_approved, 'state_id': state_id})
        insert_county_sql = "INSERT INTO county_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_county_sql, (coordinate["latitude"], coordinate["longitude"]))
        county_id = self.cursor.lastrowid()
        insert_county_ml_sql = "INSERT INTO county_ml_table (county_id, lang_code," \
            " title, title_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_county_ml_sql, (county_id,
                            lang_code, county, title_approved))
        self.connector.commit()
        logger.end(object={'county_id': county_id})
        return county_id

    @staticmethod
    def get_county_ids_by_county_name_state_id(county_name: str, state_id: int = None) -> list[int]:
        logger.start(object={'county_name': county_name, 'state_id': state_id})

        connector = Connector.connect("location")
        cursor = connector.cursor()

        # TODO: Add this logic to GenericCRUDML so others will enjoy it
        if county_name is None:
            select_county_ml_sql = "SELECT county_id FROM county_ml_view WHERE title IS NULL"
            cursor.execute(select_county_ml_sql)
        else:
            select_county_ml_sql = "SELECT county_id FROM county_ml_view WHERE title = %s"
            cursor.execute(select_county_ml_sql, (county_name,))
        county_rows = cursor.fetchall()
        county_ids = []
        for county_row in county_rows:
            county_ids.append(county_row[0])

        logger.end(object={'county_ids': county_ids})
        return county_ids
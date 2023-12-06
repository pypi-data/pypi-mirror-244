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


class Region(GenericCRUD):
    def __init__(self):
        logger.start()

        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    def insert(
            self, coordinate: Dict[str, float],
            region: str, lang_code: LangCode, title_approved: bool = False, country_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'region': region,
                     'lang_code': lang_code, 'title_approved': title_approved, 'country_id': country_id})
        insert_region_sql = "INSERT INTO region_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_region_sql, (coordinate["latitude"], coordinate["longitude"]))
        region_id = self.cursor.lastrowid()
        insert_region_ml_sql = "INSERT INTO region_ml_table (region_id, lang_code, title, title_approved)" \
            " VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_region_ml_sql, (region_id,
                            lang_code, region, title_approved))
        self.connector.commit()
        logger.end(object={'region_id': region_id})
        return region_id

    @staticmethod
    def get_region_ids_by_region_name(region_name: str, country_id: int = None) -> list[int]:
        logger.start(object={'region_name': region_name, 'country_id': country_id})

        connector = Connector.connect("location")
        cursor = connector.cursor()

        if (region_name is None):
            select_region_ml_sql = "SELECT region_id FROM region_ml_view WHERE title IS NULL"
            cursor.execute(select_region_ml_sql)
        else:
            select_region_ml_sql = "SELECT region_id FROM region_ml_view WHERE title = %s"
            cursor.execute(select_region_ml_sql, (region_name,))
        region_rows = cursor.fetchall()
        region_ids = []
        for region_row in region_rows:
            region_ids.append(region_row[0])

        logger.end(object={'region_ids': region_ids})
        return region_ids

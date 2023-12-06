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


class Neighborhood(GenericCRUD):
    def __init__(self):
        logger.start()

        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    def insert(
            self, coordinate: Dict[str, float],
            neighborhood: str, lang_code: LangCode, title_approved: bool = False, city_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'neighborhood': neighborhood,
                     'lang_code': lang_code, 'title_approved': title_approved, 'city_id': city_id})
        insert_neighborhood_sql = "INSERT INTO neighborhood_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_neighborhood_sql, (coordinate["latitude"], coordinate["longitude"]))
        neighborhood_id = self.cursor.lastrowid()
        insert_neighborhood_ml_sql = "INSERT INTO neighborhood_ml_table (neighborhood_id, lang_code," \
            " title, title_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_neighborhood_ml_sql, (neighborhood_id,
                            lang_code, neighborhood, title_approved))
        self.connector.commit()
        logger.end(object={'neighborhood_id': neighborhood_id})
        return neighborhood_id

    @staticmethod
    def get_neighborhood_ids_by_neighborhood_name(neighborhood_name: str, city_id: int = None) -> list[int]:
        logger.start(object={'neighborhood_name': neighborhood_name, 'city_id': city_id})

        connector = Connector.connect("location")
        cursor = connector.cursor()

        # TODO: Add this logic to GenericCRUDML so others will enjoy it
        if neighborhood_name is None:
            select_neighborhood_ml_sql = "SELECT neighborhood_id FROM neighborhood_ml_view WHERE title IS NULL"
            cursor.execute(select_neighborhood_ml_sql)
        else:
            select_neighborhood_ml_sql = "SELECT neighborhood_id FROM neighborhood_ml_view WHERE title = %s"
            cursor.execute(select_neighborhood_ml_sql, (neighborhood_name,))
        neighborhood_rows = cursor.fetchall()
        neighborhood_ids = []
        for neighborhood_row in neighborhood_rows:
            neighborhood_ids.append(neighborhood_row[0])

        logger.end(object={'neighborhood_ids': neighborhood_ids})
        return neighborhood_ids
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


class State(GenericCRUD):
    def __init__(self):
        logger.start()

        self.connector = Connector.connect("location")
        self.cursor = self.connector.cursor()

        logger.end()

    def insert(
            self, coordinate: Dict[str, float],
            state: str, lang_code: LangCode, state_name_approved: bool = False, country_id: int = None) -> int:
        logger.start(object={'coordinate': coordinate, 'state': state,
                     'lang_code': lang_code, 'state_name_approved': state_name_approved, 'country_id': country_id})
        insert_state_sql = "INSERT INTO state_table (coordinate) VALUES (POINT(%s, %s))"
        self.cursor.execute(
            insert_state_sql, (coordinate["latitude"], coordinate["longitude"]))
        state_id = self.cursor.lastrowid()
        insert_state_ml_sql = "INSERT INTO state_ml_table (state_id, lang_code, state_name," \
            " state_name_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(
            insert_state_ml_sql, (state_id, lang_code, state, state_name_approved))
        self.connector.commit()
        logger.end(object={'state_id': state_id})
        return state_id

    @staticmethod
    def get_state_ids_by_state_name(state_name: str, country_id: int = None) -> list[int]:
        logger.start(object={'state_name': state_name, 'country_id': country_id})

        connector = Connector.connect("location")
        cursor = connector.cursor()

        select_state_ml_sql = "SELECT state_id FROM state_ml_view WHERE state_name = %s"
        cursor.execute(select_state_ml_sql, (state_name,))
        state_rows = cursor.fetchall()
        state_ids = []
        for state_row in state_rows:
            state_ids.append(state_row[0])

        logger.end(object={'state_ids': state_ids})
        return state_ids

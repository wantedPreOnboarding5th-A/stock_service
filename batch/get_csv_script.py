from batch.excel_helper import excel_handler
from batch.repository import sync_with_db


def get_csv_and_save():
    loaded_data = excel_handler.get_all_data_sets()
    sync_with_db(**loaded_data)

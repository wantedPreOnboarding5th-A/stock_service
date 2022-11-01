import logging
import pandas as pd
from batch.configs.csv_schema import CustomBaseModel
from batch.configs.config import EXCEL_DATA_SCHEMA_MAP_LIST
from pydantic import ValidationError
import os

logger = logging.getLogger()

absolute_path = os.path.dirname(__file__)
relative_path = "data/"
full_path = os.path.join(absolute_path, relative_path)


class ExcelHandler:
    def __init__(self):
        self.excel_file_schema_map_list = EXCEL_DATA_SCHEMA_MAP_LIST
        self.root_dir = full_path

    def _read_excel(self, filename: str) -> list[list[str]]:
        try:
            file_fullpath = f"{self.root_dir}/{filename}"
            dataframe = pd.read_excel(file_fullpath)
            return dataframe.values.tolist()
        except FileNotFoundError as e:
            # 파일이 존재하지 않는 경우, 해당 파일 읽지 않음
            logger.error(
                f"Can not find file from {file_fullpath}. Excel Handler will stop batch!!"
            )
            raise e

    def _validate_data_with_schema(self, data: list[str], schema: CustomBaseModel):
        try:
            fields_names = schema.get_fields_name_list()
            mapped_data = dict(zip(fields_names, data))
            validated_data = schema(**mapped_data)  # 조건 충족하지 않을 경우 ValidationError 발생
            return validated_data.dict()
        except ValidationError as e:
            return None

    def _parse_data_list(self, data_list: list, schema: CustomBaseModel):
        parsed = []
        for data in data_list:
            validated_data = self._validate_data_with_schema(data, schema)
            if validated_data != None:
                parsed.append(validated_data)
        return parsed

    def parse_data_to_dict_list(
        self, filename: str, schema: CustomBaseModel
    ) -> list[dict]:
        data_list = self._read_excel(filename)
        return self._parse_data_list(data_list, schema) if len(data_list) else []

    def get_all_data_sets(self) -> dict:
        data_dict = dict()
        for schema_map in self.excel_file_schema_map_list:
            data_dict[schema_map["name"]] = self.parse_data_to_dict_list(
                filename=schema_map["filename"], schema=schema_map["schema"]
            )
        return data_dict


excel_handler = ExcelHandler()

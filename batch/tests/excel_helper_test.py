from batch.excel_helper import ExcelHandler

excel_handler = ExcelHandler()


def test_read_excel_and_validate():
    sut = excel_handler.get_all_data_sets()
    assert isinstance(sut, dict)

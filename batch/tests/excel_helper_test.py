import pytest
from batch.excel_helper import ExcelHandler
from batch.csv_schema import (
    AccountBasicInfoSchema,
    AccountAssetInfoSchema,
    AssetGroupInfoSchema,
)

excel_handler = ExcelHandler()

account_basic_info_test_set = [
    {"account_number": "5736692368320", "investment_principal": "1911386"},
    {"account_number": "1573538006848", "investment_principal": "1744732"},
    {"account_number": "8699709932280", "investment_principal": "1454737"},
    {"account_number": "1623177400337", "investment_principal": "1482996"},
    {"account_number": "5961683984108", "investment_principal": "1247757"},
    {"account_number": "7564548104802", "investment_principal": "1075758"},
    {"account_number": "5608672867775", "investment_principal": "1621094"},
]

asset_group_info_test_set = [
    {"name": "미국S&P500", "isin_number": "KR7360750004", "group": "미국 주식"},
    {"name": "미국나스닥바이오", "isin_number": "KR7203780002", "group": "미국섹터 주식"},
    {"name": "선진국MSCI World", "isin_number": "KR7251350005", "group": "선진국 주식"},
    {"name": "일본니케이225", "isin_number": "KR7241180009", "group": "선진국 주식"},
    {"name": "현금", "isin_number": "CASH", "group": "채권 / 현금"},
]

account_asset_info_test_set = [
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7360750004",
        "current_price": "8585",
        "amount": "21",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7133690008",
        "current_price": "14459",
        "amount": "13",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7203780002",
        "current_price": "12707",
        "amount": "12",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7200020006",
        "current_price": "7195",
        "amount": "8",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7251350005",
        "current_price": "14210",
        "amount": "7",
    },
]

invalid_account_basic_info_test_set = [
    {
        "account_number": "12345",
        "investment_principal": "1911386",
    },  # 계좌번호는 12자리 또는 13자리 여야함
    {
        "account_number": "5608672867775",
        "investment_principal": "-2",
    },  # 투자원금은 음수가 될수 없음
    {
        "account_number": "8699709_93228",
        "investment_principal": "1454,737",
    },  # 계좌번호, 투자원금은 숫자로만 이루어져야함
]

invalid_asset_group_info_test_set = [
    {
        "name": "미국S&P500",
        "isin_number": "KR736075000",
        "group": "미국 주식",
    },  # isin은 12자리거나 CASH 여야함
    {"name": "현금", "isin_number": "CASH1", "group": "채권 / 현금"},  # isin은 12자리거나 CASH 여야함
]

invalid_account_asset_info_test_set = [
    {
        "user_name": "류" * 21,  # 이름은 최대 20글자임
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7360750004",
        "current_price": "8585",
        "amount": "21",
    },
    {
        "user_name": "류영길",
        "brokerage": "디" * 21,  # 증권사명은 최대 20글자임
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7133690008",
        "current_price": "14459",
        "amount": "13",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692_68320",  # 계좌번호는 숫자로만 이루어져야함
        "account_name": "계좌1",
        "isin_number": "KR7360750004",
        "current_price": "8585",
        "amount": "21",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "73669236",  # 계좌번호는 12 또는 13자리여야함
        "account_name": "계좌1",
        "isin_number": "KR713369000",  # isin은 12자리거나 CASH 여야함
        "current_price": "14459",
        "amount": "13",
    },
    {
        "user_name": "류영길",
        "brokerage": "디셈버증권",
        "number": "5736692368320",
        "account_name": "계좌1",
        "isin_number": "KR7251350005",
        "current_price": "14210",
        "amount": "-1",  # 보유 수량은 0보다 커야함
    },
]


def test_read_excel_and_validate():
    sut = excel_handler.get_all_data_sets()
    assert isinstance(sut, dict)


@pytest.mark.parametrize(
    "test_input",
    [
        [invalid_account_basic_info_test_set, AccountBasicInfoSchema],
        [invalid_asset_group_info_test_set, AssetGroupInfoSchema],
        [invalid_account_asset_info_test_set, AccountAssetInfoSchema],
    ],
)
def test_excel_schema_validators(test_input):
    parsed_test_data = map(lambda x: list(x.values()), test_input[0])
    sut = excel_handler._parse_data_list(parsed_test_data, test_input[1])
    assert len(sut) == 0

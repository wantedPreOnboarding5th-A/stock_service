import logging

from invest.models import Account, Stock, InvestInfo
from invest.serializers import AccountSerializer, StockSerializer, InvestInfoSerializer
from user.serializers import UserSerializer
from stock_service.utils.dict_helper import (
    make_hashtable,
    make_hashtable_by_multi_keys,
    sperate_hsashtable_by_keys,
    merge_hashtable_by_key,
    change_key_name,
)
from django.db.models import QuerySet, CharField
from stock_service.models import BaseModel
from user.models import User as CustomUser
from django.db.models.functions import Concat


logger = logging.getLogger()

# AccountBasicInfoSchema account_number, investment_principal -> account


def get_account_orm_from_csv_data(
    basic_data: list[dict],
    asset_data: list[dict],
    user_hasttable: dict,
) -> tuple[list[Account]]:
    # basic_data는 AccountBasicInfoSchema로 valdation 을 했다고 가정합니다
    # asset_data는 AccountAssetInfoSchema valdation 을 했다고 가정합니다

    basic_data_hashtable = make_hashtable("account_number", basic_data)
    asset_data_hashtable = make_hashtable("number", asset_data)

    data_hashtable = merge_hashtable_by_key(basic_data_hashtable, asset_data_hashtable)

    account_number_list = list(data_hashtable.keys())
    update_target = AccountSerializer(
        Account.objects.filter(number__in=account_number_list), many=True
    ).data

    update_account_number_list = list(map(lambda x: x["number"], update_target))

    # create할 대상과 update 대상 분리
    update_hashtable, create_hashtable = sperate_hsashtable_by_keys(
        data_hashtable, update_account_number_list
    )

    create_orm_list = []
    update_orm_list = []
    for origin_data in update_target:
        account_number = str(origin_data["number"])
        update_data = update_hashtable[account_number]
        origin_data = change_key_name(origin_data, "user", "user_id")
        # TODO: data mapping
        update_orm_list.append(
            Account(
                **{
                    **origin_data,
                    "number": update_data["account_number"],
                    "investment_principal": update_data["investment_principal"],
                }
            )
        )

    for data in create_hashtable.values():
        user_name = data["user_name"]
        create_orm_list.append(
            Account(
                **{
                    "user": CustomUser(**user_hasttable[user_name]),
                    "number": data["account_number"],
                    "brokerage": data["brokerage"],
                    "name": data["account_name"],
                    "investment_principal": data["investment_principal"],
                }
            )
        )

    return create_orm_list, update_orm_list


def get_stock_orm_from_csv_data(
    asset_group_info_data: list[dict],
) -> tuple[list[Stock]]:
    # data는 AccountBasicInfoSchema로 valdation 을 했다고 가정합니다
    data_hashed_by_isin_number = make_hashtable("isin_number", asset_group_info_data)
    isin_number_list = list(data_hashed_by_isin_number.keys())

    update_target_query = Stock.objects.filter(isin_number__in=isin_number_list)
    update_target = StockSerializer(update_target_query, many=True).data
    update_isin_number_list = list(map(lambda x: x["isin_number"], update_target))

    # create할 대상과 update 대상 분리
    update_hashtable, create_hashtable = sperate_hsashtable_by_keys(
        data_hashed_by_isin_number, update_isin_number_list
    )

    update_orm_list = []
    create_orm_list = []

    for data in update_target:
        isin_number = str(data["isin_number"])
        update_data = update_hashtable[isin_number]
        update_orm_list.append(
            Stock(
                id=data["id"],
                name=update_data["name"],
                isin_number=update_data["isin_number"],
                group=update_data["group"],
            )
        )

    for data in create_hashtable.values():
        create_orm_list.append(
            Stock(
                name=data["name"],
                isin_number=data["isin_number"],
                group=data["group"],
            )
        )

    return create_orm_list, update_orm_list


def get_account_isin_number(asset_data: dict) -> str:
    account_number = asset_data["number"]
    isin_number = asset_data["isin_number"]
    return f"{account_number}_{isin_number}"


def get_account_and_stock_from_invest_info(
    account_number: str,
    isin_number: str,
    stock_hashtable: dict,
    account_hashtable: dict,
) -> tuple:
    try:
        stock = stock_hashtable[isin_number]
        account = account_hashtable[account_number]
        return account, stock
    except Exception as e:
        raise e


def parse_create_invest_info_data_to_orm(
    invest_info: dict, stock_hashtable: dict, account_hashtable: dict
):
    account_number = invest_info["number"]
    isin_number = invest_info["isin_number"]
    account, stock = get_account_and_stock_from_invest_info(
        account_number,
        isin_number,
        stock_hashtable,
        account_hashtable,
    )
    account = change_key_name(account, "user", "user_id")
    return InvestInfo(
        stock=Stock(**stock),
        account=Account(**account),
        amount=invest_info["amount"],
        current_price=invest_info["current_price"],
        account_isin_number=f"{account_number}_{isin_number}",
    )


def parse_update_invest_info_data_to_orm(
    origin_data: dict,
    update_hashtable: dict,
    stock_hashtable: dict,
    account_hashtable: dict,
):
    account_isin_number = origin_data["account_isin_number"]
    account_number, isin_number = (
        account_isin_number.split("_")[0],
        account_isin_number.split("_")[1],
    )
    account, stock = get_account_and_stock_from_invest_info(
        account_number, isin_number, stock_hashtable, account_hashtable
    )

    update_data = update_hashtable[account_isin_number]
    account = change_key_name(account, "user", "user_id")
    # id, 계좌, 주식 데이터는 업데이트 하지 않음 투자금액과 현재가격만 update
    return InvestInfo(
        id=origin_data["id"],
        stock_id=stock["id"],
        account_id=account["id"],
        amount=update_data["amount"],
        current_price=update_data["current_price"],
        account_isin_number=account_isin_number,
    )


def get_invest_info_orm_from_csv_data(
    asset_data: list[dict],
    account_hashtable: dict,
    stock_hashtable: dict,
):
    # account를 update, create 후 데이터를 가져와야 합니다
    # asset_data는 AccountAssetInfoSchema valdation 을 했다고 가정합니다
    data_hashtable = make_hashtable_by_multi_keys(["number", "isin_number"], asset_data)
    account_isin_number_list = list(
        map(
            lambda x: get_account_isin_number(x),
            asset_data,
        )
    )
    update_target = InvestInfoSerializer(
        InvestInfo.objects.filter(account_isin_number__in=account_isin_number_list),
        many=True,
    ).data
    update_account_isin_number_list = list(map(lambda x: x["account_isin_number"], update_target))
    update_hashtable, create_hashtable = sperate_hsashtable_by_keys(
        data_hashtable, update_account_isin_number_list
    )

    update_orm_list = []
    create_orm_list = []
    for origin_data in update_target:
        update_orm_list.append(
            parse_update_invest_info_data_to_orm(
                origin_data,
                update_hashtable,
                stock_hashtable,
                account_hashtable,
            )
        )

    for invest_info in create_hashtable.values():
        create_orm_list.append(
            parse_create_invest_info_data_to_orm(invest_info, stock_hashtable, account_hashtable)
        )

    return create_orm_list, update_orm_list


def _get_db_data_hashtable(query: QuerySet, key_name: str, serilizer):
    data_list = serilizer(query, many=True).data
    return make_hashtable(key_name, data_list)


def _get_user_hashtable(account_asset: list[dict]):
    user_names = set(map(lambda x: x["user_name"], account_asset))
    query = CustomUser.objects.filter(name__in=user_names)
    return _get_db_data_hashtable(query, "name", UserSerializer)


def _get_stock_hashtable(account_asset: list[dict]):
    stok_number = set(map(lambda x: x["isin_number"], account_asset))
    query = Stock.objects.filter(isin_number__in=stok_number)
    return _get_db_data_hashtable(query, "isin_number", StockSerializer)


def _get_account_hashtable(account_asset: list[dict]):
    account_number = set(map(lambda x: x["number"], account_asset))
    query = Account.objects.filter(number__in=account_number)
    return _get_db_data_hashtable(query, "number", AccountSerializer)


def _upsert_data(
    model, update_data: list[Stock], create_data: list[Stock], update_fields: list[str]
):
    if update_data:
        model.objects.bulk_update(update_data, update_fields)
    if create_data:
        model.objects.bulk_create(create_data)


def sync_with_db(account_asset: list[dict], account_basic: list[dict], asset_group: list[dict]):
    user_hashtable = _get_user_hashtable(account_asset)

    create_stock_list, update_stock_list = get_stock_orm_from_csv_data(asset_group)
    _upsert_data(Stock, update_stock_list, create_stock_list, ["name", "isin_number", "group"])

    create_account_list, update_account_list = get_account_orm_from_csv_data(
        account_basic, account_asset, user_hashtable
    )
    _upsert_data(
        Account,
        update_account_list,
        create_account_list,
        ["brokerage", "name", "investment_principal"],
    )

    account_hashtable = _get_account_hashtable(account_asset)
    stock_hashtable = _get_stock_hashtable(account_asset)
    create_invest_list, update_invest_list = get_invest_info_orm_from_csv_data(
        account_asset, account_hashtable, stock_hashtable
    )
    _upsert_data(
        InvestInfo,
        update_invest_list,
        create_invest_list,
        ["amount", "current_price"],
    )

    return

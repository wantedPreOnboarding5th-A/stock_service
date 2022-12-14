import logging

from invest.models import Account, Stock, InvestInfo
from invest.serializers import AccountSerializer, StockSerializer, InvestInfoSerializer
from user.serializers import UserSerializer
from stock_service.utils.list_helper import map_single_item
from stock_service.utils.dict_helper import (
    make_hashtable,
    make_hashtable_by_multi_keys,
    sperate_hsashtable_by_keys,
    merge_hashtable_by_key,
    change_key_name,
)
from django.db.models import QuerySet
from stock_service.models import BaseModel
from user.models import User as CustomUser


logger = logging.getLogger()


def _upsert_data(
    model: BaseModel,
    update_data: list[Stock],
    create_data: list[Stock],
    update_fields: list[str],
):
    if update_data:
        model.objects.bulk_update(update_data, update_fields)
    if create_data:
        model.objects.bulk_create(create_data)



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


class AccountRepo:
    def parse_create_dict_lst_to_orm_lst(
        self, create_data: list[dict], user_hasttable: dict
    ) -> list[Account]:
        create_orm_list = []
        for data in create_data:
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
        return create_orm_list

    def parse_update_dict_lst_to_orm_lst(
        self, update_target: list[dict], update_hashtable: dict
    ) -> list[Account]:
        update_orm_list = []
        for origin_data in update_target:
            account_number = str(origin_data["number"])
            update_data = update_hashtable[account_number]
            origin_data = change_key_name(origin_data, "user", "user_id")
            update_orm_list.append(
                Account(
                    **{
                        **origin_data,
                        "number": update_data["account_number"],
                        "investment_principal": update_data["investment_principal"],
                    }
                )
            )
        return update_orm_list

    def get_account_orm_from_csv_data(
        self,
        basic_data: list[dict],
        asset_data: list[dict],
        user_hasttable: dict,
    ) -> tuple[list[Account]]:
        # basic_data??? AccountBasicInfoSchema??? valdation ??? ????????? ???????????????
        # asset_data??? AccountAssetInfoSchema valdation ??? ????????? ???????????????

        basic_data_hashtable = make_hashtable("account_number", basic_data)
        asset_data_hashtable = make_hashtable("number", asset_data)
        data_hashtable = merge_hashtable_by_key(
            basic_data_hashtable, asset_data_hashtable
        )

        account_number_list = list(data_hashtable.keys())
        update_target = AccountSerializer(
            Account.objects.filter(number__in=account_number_list), many=True
        ).data

        # update_account_number_list = list(map(lambda x: x["number"], update_target))
        update_account_number_list = map_single_item(update_target, "number")
        # create??? ????????? update ?????? ??????
        update_hashtable, create_hashtable = sperate_hsashtable_by_keys(
            data_hashtable, update_account_number_list
        )

        create_orm_list = self.parse_create_dict_lst_to_orm_lst(
            create_hashtable.values(), user_hasttable
        )
        update_orm_list = self.parse_update_dict_lst_to_orm_lst(
            update_target, update_hashtable
        )
        return create_orm_list, update_orm_list

    def bulk_upsert_with_csv_data(
        self,
        basic_data: list[dict],
        asset_data: list[dict],
        user_hashtable: dict,
    ) -> None:
        create_account_list, update_account_list = self.get_account_orm_from_csv_data(
            basic_data, asset_data, user_hashtable
        )
        _upsert_data(
            Account,
            update_account_list,
            create_account_list,
            ["brokerage", "name", "investment_principal"],
        )


class StockRepo:
    def find_by_isin_number(self, isin_numbers: list[int]):
        return StockSerializer(
            Stock.objects.filter(isin_number__in=isin_numbers), many=True
        ).data

    def parse_create_dict_lst_to_orm_lst(self, create_data: list[dict]):
        create_orm_list = []
        for data in create_data:
            create_orm_list.append(
                Stock(
                    name=data["name"],
                    isin_number=data["isin_number"],
                    group=data["group"],
                )
            )
        return create_orm_list

    def parse_update_dict_lst_to_orm_lst(
        self, update_target: list[dict], update_hashtable: dict
    ) -> list[Stock]:
        update_orm_list = []
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
        return update_orm_list

    def get_stock_orm_from_csv_data(
        self,
        asset_group_info_data: list[dict],
    ) -> tuple[list[Stock]]:
        # data??? AccountBasicInfoSchema??? valdation ??? ????????? ???????????????
        data_hashed_by_isin_number = make_hashtable(
            "isin_number", asset_group_info_data
        )
        isin_number_list = list(data_hashed_by_isin_number.keys())
        update_target = self.find_by_isin_number(isin_number_list)
        update_isin_number_list = map_single_item(update_target, "isin_number")

        # create??? ????????? update ?????? ??????
        update_hashtable, create_hashtable = sperate_hsashtable_by_keys(
            data_hashed_by_isin_number, update_isin_number_list
        )

        update_orm_list = self.parse_update_dict_lst_to_orm_lst(
            update_target, update_hashtable
        )
        create_orm_list = self.parse_create_dict_lst_to_orm_lst(
            create_hashtable.values()
        )
        return create_orm_list, update_orm_list

    def bulk_upsert_with_csv_data(self, asset_group_info_data: list[dict]):
        create_stock_list, update_stock_list = self.get_stock_orm_from_csv_data(
            asset_group_info_data
        )
        _upsert_data(
            Stock,
            update_stock_list,
            create_stock_list,
            ["name", "isin_number", "group"],
        )


class InvestInfoRepo:
    def find_by_account_isin_number(
        self, account_isin_numbers: list[int]
    ) -> list[dict]:
        return InvestInfoSerializer(
            InvestInfo.objects.filter(account_isin_number__in=account_isin_numbers),
            many=True,
        ).data

    def get_account_isin_number(self, asset_data: dict) -> str:
        account_number = asset_data["number"]
        isin_number = asset_data["isin_number"]
        return f"{account_number}_{isin_number}"

    def get_account_and_stock_from_invest_info(
        self,
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
        self, invest_info: dict, stock_hashtable: dict, account_hashtable: dict
    ):
        account_number = invest_info["number"]
        isin_number = invest_info["isin_number"]
        account, stock = self.get_account_and_stock_from_invest_info(
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
        self,
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
        account, stock = self.get_account_and_stock_from_invest_info(
            account_number, isin_number, stock_hashtable, account_hashtable
        )

        update_data = update_hashtable[account_isin_number]
        account = change_key_name(account, "user", "user_id")
        # id, ??????, ?????? ???????????? ???????????? ?????? ?????? ??????????????? ??????????????? update
        return InvestInfo(
            id=origin_data["id"],
            stock_id=stock["id"],
            account_id=account["id"],
            amount=update_data["amount"],
            current_price=update_data["current_price"],
            account_isin_number=account_isin_number,
        )

    def get_update_orm_list(
        self,
        update_target: list[dict],
        update_hashtable: dict,
        stock_hashtable: dict,
        account_hashtable: dict,
    ) -> list[InvestInfo]:
        update_orm_list = []
        for origin_data in update_target:
            update_orm_list.append(
                self.parse_update_invest_info_data_to_orm(
                    origin_data,
                    update_hashtable,
                    stock_hashtable,
                    account_hashtable,
                )
            )
        return update_orm_list

    def get_create_orm_list(
        self, create_data: list[dict], stock_hashtable: dict, account_hashtable: dict
    ) -> list[InvestInfo]:
        create_orm_list = []
        for invest_info in create_data:
            create_orm_list.append(
                self.parse_create_invest_info_data_to_orm(
                    invest_info, stock_hashtable, account_hashtable
                )
            )
        return create_orm_list

    def get_invest_info_orm_from_csv_data(
        self,
        asset_data: list[dict],
        account_hashtable: dict,
        stock_hashtable: dict,
    ):
        # account??? update, create ??? ???????????? ???????????? ?????????
        # asset_data??? AccountAssetInfoSchema valdation ??? ????????? ???????????????
        data_hashtable = make_hashtable_by_multi_keys(
            ["number", "isin_number"], asset_data
        )
        account_isin_number_list = list(
            map(
                lambda x: self.get_account_isin_number(x),
                asset_data,
            )
        )
        update_target = self.find_by_account_isin_number(account_isin_number_list)
        update_account_isin_number_list = map_single_item(
            update_target, "account_isin_number"
        )
        update_hashtable, create_hashtable = sperate_hsashtable_by_keys(
            data_hashtable, update_account_isin_number_list
        )

        update_orm_list = self.get_update_orm_list(
            update_target, update_hashtable, stock_hashtable, account_hashtable
        )
        create_orm_list = self.get_create_orm_list(
            create_hashtable.values(), stock_hashtable, account_hashtable
        )
        return create_orm_list, update_orm_list

    def bulk_upsert_with_csv_data(
        self, account_asset: list[dict], account_hashtable: dict, stock_hashtable: dict
    ):
        create_invest_list, update_invest_list = self.get_invest_info_orm_from_csv_data(
            account_asset, account_hashtable, stock_hashtable
        )
        _upsert_data(
            InvestInfo,
            update_invest_list,
            create_invest_list,
            ["amount", "current_price"],
        )


def sync_with_db(
    account_asset: list[dict], account_basic: list[dict], asset_group: list[dict]
):
    # NOTE: ?????? ????????? account, stock??? ?????? ????????? stock -> account -> invest_info ????????? upsert ?????????
    user_hashtable = _get_user_hashtable(account_asset)
    StockRepo().bulk_upsert_with_csv_data(asset_group)
    AccountRepo().bulk_upsert_with_csv_data(
        account_basic, account_asset, user_hashtable
    )

    account_hashtable = _get_account_hashtable(account_asset)
    stock_hashtable = _get_stock_hashtable(account_asset)

    InvestInfoRepo().bulk_upsert_with_csv_data(
        account_asset, account_hashtable, stock_hashtable
    )
    return

from batch.configs.csv_schema import (
    AccountBasicInfoSchema,
    AccountAssetInfoSchema,
    AssetGroupInfoSchema,
)

EXCEL_DATA_SCHEMA_MAP_LIST = [
    {
        "name": "account_asset",
        "filename": "account_asset_info_set.xlsx",
        "schema": AccountAssetInfoSchema,
    },
    {
        "name": "account_basic",
        "filename": "account_basic_info_set.xlsx",
        "schema": AccountBasicInfoSchema,
    },
    {
        "name": "asset_group",
        "filename": "asset_group_info_set.xlsx",
        "schema": AssetGroupInfoSchema,
    },
]

# EXCEL_DATA_SCHEMA_MAP_LIST = [
#     {
#         "name": "account_asset",
#         "filename": "1.xlsx",
#         "schema": AccountAssetInfoSchema,
#     },
#     {
#         "name": "account_basic",
#         "filename": "2.xlsx",
#         "schema": AccountBasicInfoSchema,
#     },
#     {
#         "name": "asset_group",
#         "filename": "asset_group_info_set.xlsx",
#         "schema": AssetGroupIngoSchema,
#     },
# ]

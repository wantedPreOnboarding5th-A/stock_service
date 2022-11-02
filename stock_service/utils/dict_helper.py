import copy


def change_key_name(dict_data: dict, target_key: str, change_key: str):
    copy_data = copy.deepcopy(dict_data)
    data = copy_data[target_key]
    del copy_data[target_key]
    copy_data[change_key] = data
    return copy_data


def make_hashtable(hash_key: str, data: list[dict]) -> dict:
    # data의 element 는 반드시 hash_key를 가지고 있어야함
    # data의 element의 hash_key의 value는 중복되지 않아야함 (중복될 경우, 나중에 있는 값으로 덮어씌워짐)
    hash_table = dict()
    for record in data:
        hash_table[record[hash_key]] = record

    return hash_table


def make_hashtable_by_multi_keys(
    hash_keys: list[str], data: list[dict], seperate_str: str = "_"
) -> dict:
    # data의 element 는 반드시 hash_key를 가지고 있어야함
    # data의 element의 hash_key의 value는 중복되지 않아야함 (중복될 경우, 나중에 있는 값으로 덮어씌워짐)
    hash_table = dict()

    for record in data:
        hash_key = seperate_str.join(list(map(lambda k: record[k], hash_keys)))
        hash_table[hash_key] = record
    return hash_table


def merge_hashtable_by_key(hashtable1: dict, hashtable2: dict) -> dict:
    # 순서가 바뀔수 있음
    merged_keys = set(hashtable1.keys()) | set(hashtable2.keys())
    result = dict()
    for key in merged_keys:
        result[key] = {**hashtable1.get(key, dict()), **hashtable2.get(key, dict())}

    return result


def sperate_hsashtable_by_keys(hashtable: dict, included_key: list):
    included = dict()
    excluded = dict()
    for key in hashtable.keys():
        if key in included_key:
            included[key] = hashtable[key]
        else:
            excluded[key] = hashtable[key]

    return included, excluded

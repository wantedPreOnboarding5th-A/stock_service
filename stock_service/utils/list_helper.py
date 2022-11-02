def map_single_item(dict_lst: list[dict], key_name: str):
    return list(map(lambda x: x[key_name], dict_lst))

from batch.fake_provider.fake_models import (
    CustomBaseModel,
    User,
    Stock,
    Account,
    InvestInfo,
)
from batch.fake_provider.fake_exceptions import NotFoundError


class FakeRepoBase:
    def __init__(self, model: CustomBaseModel) -> None:
        self.in_memory_db = dict()
        self.model = model

    def create(self, params: dict):
        data = self.model(**params)  # validation함, 문제 있을 시 raise Exception 해줌
        self.in_memory_db[str(params["id"])] = params

    def get(self, data_id: int):
        return self.in_memory_db.get(str(data_id), None)

    def update(self, data_id: int, params: dict):
        update_target = self.get(data_id)
        data_id_str = str(data_id)
        if update_target != None:
            for field in params.keys():
                self.in_memory_db[data_id_str][field] = params[field]
        else:
            raise NotFoundError

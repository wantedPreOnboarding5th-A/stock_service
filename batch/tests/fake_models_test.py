import pytest
from batch.fake_provider.fake_models import Stock
from datetime import datetime
from pydantic import ValidationError


_base_model_input = {
    "id": 1,
    "name": "a" * 20,
    "isin_number": "1" * 12,
    "group": "g" * 20,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


@pytest.mark.parametrize(
    "test_input",
    [
        {**_base_model_input, "name": "a" * 21},
        {**_base_model_input, "isin_number": "1" * 11},
        {**_base_model_input, "group": "g" * 22},
    ],
)
def test_validators(test_input):
    with pytest.raises(ValidationError):
        Stock(**test_input)

import pytest
from batch.excel_helper import excel_handler
from batch.repository import sync_with_db
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_sync_db():
    sut = sync_with_db(**excel_handler.get_all_data_sets())
    return sut

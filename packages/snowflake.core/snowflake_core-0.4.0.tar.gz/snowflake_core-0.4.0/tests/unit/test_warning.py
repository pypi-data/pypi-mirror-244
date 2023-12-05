
from contextlib import suppress
from unittest.mock import MagicMock, patch

import pytest

from snowflake.core import Root
from snowflake.core._internal.utils import WARNING_TEXT


@pytest.fixture(scope="function")
def root_for_warn():
    with patch("warnings.warn") as warn_mock:
        root = Root(MagicMock())
        yield warn_mock, root


def test_warn_compute_pools(root_for_warn):
    warn_mock, root = root_for_warn
    _ = root.compute_pools
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_warn_warehouse(root_for_warn):
    warn_mock, root = root_for_warn
    _ = root.warehouses
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_warn_database(root_for_warn):
    warn_mock, root = root_for_warn
    _ = root.databases
    warn_mock.assert_not_called()
    with suppress(Exception):
        _ = root.databases.create(database=None)
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_warn_schemas(root_for_warn):
    warn_mock, root = root_for_warn
    _ = root.databases["d"].schemas["s"]
    warn_mock.assert_not_called()
    with suppress(Exception):
        _ = root.databases["a"].schemas.create(schema=None)
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_warn_service(root_for_warn):
    warn_mock, root = root_for_warn
    schema = root.databases["d"].schemas["s"]
    _ = schema.services
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_warn_table(root_for_warn):
    warn_mock, root = root_for_warn
    schema = root.databases["d"].schemas["s"]
    _ = schema.tables
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_warn_image_repositories(root_for_warn):
    warn_mock, root = root_for_warn
    schema = root.databases["d"].schemas["s"]
    _ = schema.image_repositories
    warn_mock.assert_called_once_with(WARNING_TEXT, stacklevel=0)


def test_not_warn_tasks(root_for_warn):
    warn_mock, root = root_for_warn
    schema = root.databases["d"].schemas["s"]
    t = schema.tasks["t"]
    with suppress(Exception):
        t.fetch()
    warn_mock.assert_not_called()

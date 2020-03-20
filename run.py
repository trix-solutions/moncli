from importlib import import_module

from moncli import MondayClient, enums
from moncli.entities import column_value as cv

from tests import entities_board_tests as test
test.test_should_create_an_item()
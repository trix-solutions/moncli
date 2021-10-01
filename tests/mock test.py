import json

from unittest.mock import patch
from nose.tools import eq_, raises

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t
from moncli.models import MondayModel



def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_timezone_value_to_world_clock_type():

    # Arrange
    timezone_type = WorldClockModel(id='some_id', name='some_name', raw_data={'timezone': 'America/Phoenix'})

    # Act
    timezone_value = timezone_type.to_primitive()

    # Assert
    eq_(timezone_value,{'timezone': 'America/Phoenix'})

@raises(t.ValidationError)
def test_should_fail_when_to_primitive_raises_a_validation_error_when_passed_a_str_timezone_that_is_invalid_to_world_clock_type():

    # Arrange
    timezone_type = WorldClockModel(id='some_id', name='some_name', raw_data={'timezone': 'Invalid/Timezone'})

    # Act
    timezone_type.validate()

class WorldClockModel(MondayModel):
    timezone = t.WorldClockType(title='Time Zone Column 1')
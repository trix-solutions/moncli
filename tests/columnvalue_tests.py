from nose.tools import ok_, raises

from moncli import columnvalue
from moncli.columnvalue import create_column_value
from moncli.enums import ColumnType

@raises(columnvalue.InvalidColumnValueType)
def test_should_fail_for_non_writeable_column_type():

    # Arrange
    column_type = ColumnType.auto_number

    # Act
    create_column_value('test_id', column_type, 'should fail')
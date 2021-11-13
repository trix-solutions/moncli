import json
from nose.tools import eq_

from moncli import column_value as cv
from moncli.enums import ColumnType

def test_should_suceed_when_to_native_returns_list_when_passing_api_data_to_sub_item_value():

    # Arrange
    
    id = 'subitem_1'
    title = 'SubItem'
    column_type = ColumnType.subitems
    value =  json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act 
    
    format = column_value.value

    # Assert

    eq_(format,[123456789])

import json
from schematics.exceptions import ConversionError, DataError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.entities.column_value.objects import PersonOrTeam
from moncli.enums import ColumnType, PeopleKind
from moncli.models import MondayModel
from moncli.types import PeopleType


def test_should_succeed_when_to_native_returns_a_list_when_passing_in_peoplevalue_value_with_api_data_and_max_allowed_is_not_1():

    # Arrange
    id = "people_1"
    title = 'Assignee'
    column_type = ColumnType.people
    value = {'personsAndTeams': [
        {'id': 13435, 'kind': 'person'}, {'id': 11234, 'kind': 'person'}]}
    value = json.dumps(value)
    settings_str = json.dumps({'max_people_allowed': 0})
    people_value = en.cv.create_column_value(column_type,id=id,title=title,value=value,settings_str=settings_str)

    # Act
    people_type = PeopleType(title='Assignee')
    value = people_type.to_native(people_value)

    # Assert
    eq_(value[0].id, 13435)
    eq_(value[1].kind, PeopleKind.person)

def test_should_suceed_when_to_native_returns_a_personorteam_when_passing_in_a_peoplevalue_with_api_data_and_max_allowed_is_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=1)

    # Act
    value = people_type.to_native(en.cv.PersonOrTeam(id=12345,kind=PeopleKind.person))

    # Assert
    eq_(value.id, 12345)
    eq_(value.kind, PeopleKind.person)

def test_should_suceed_when_to_native_returns_an_empty_list_when_passed_a_none_and_max_allowed_is_not_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=2)

    # Act
    value = people_type.to_native(None)

    # Assert
    eq_(value,[])


def test_should_suceed_when_to_native_returns_an_none_when_passed_none_and_max_allowed_is_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=1)

    # Act
    value = people_type.to_native(None)

    # Assert
    eq_(value,None)

def test_should_suceed_when_to_native_returns_a_list_of_personorteam_values_when_passed_a_list_containing_valid_import_dict_int_and_str_values_and_max_allowed_is_not_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=2)
    people_list = [{'id': 13435, 'kind': 'person'}, {'id': 11234, 'kind': 'person'}]

    # Act
    value = people_type.to_native(people_list)
    format = value[0]

    # Assert
    eq_(format.id,13435)
    eq_(format.kind,PeopleKind.person)

def test_should_suceed_when_to_native_returns_a_list_of_personorteam_values_when_passed_a_list_containing_valid_import_dict_int_and_str_values_and_max_allowed_is_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=1)
    people_list = {'id': 13435, 'kind': 'person'}

    # Act
    format = people_type.to_native(people_list)

    # Assert
    eq_(format.id,13435)
    eq_(format.kind,PeopleKind.person)


@raises(ConversionError)
def test_should_suceed_when_to_native_raises_a_conversionerror_when_passed_a_list_containing_invalid_import_dict_and_or_str_values_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=1)

    # Act
    people_type.to_native(['invalid number'])


def test_should_suceed_when_to_primitive_returns_an_empty_dict_when_passed_in_a_none_and_max_allowed_is_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=1)

    # Act
    value = people_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_suceed_when_to_primitive_returns_an_empty_dict_when_passed_an_empty_list_and_max_allowed_is_not_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=2)

    # Act
    value = people_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_suceed_when_to_primitive_returns_export_dict_when_passed_in_a_list_of_personorteam_values_and_max_allowed_is_not_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=2)

    # Act
    value = people_type.to_primitive([12345,98765])
    value1 = value['personsAndTeams'][0]


    # Assert
    eq_(value1['id'],12345)
    eq_(value1['kind'],PeopleKind.person.name)


def test_should_suceed_when_to_primitive_returns_export_dict_when_passed_a_personorteam_value_and_max_allowed_is_1_to_people_type():
    
    # Arrange
    people_type = PeopleType(title='Assignee',max_allowed=1)

    # Act
    value = people_type.to_primitive(PersonOrTeam(12345,PeopleKind.person))
    value1 = value['personsAndTeams'][0]


    # Assert
    eq_(value1['id'],12345)
    eq_(value1['kind'],PeopleKind.person.name)


@raises(DataError)
def test_should_suceed_when_validate_people_raises_validationerror_when_passed_a_list_of_personorteam_values_with_len_greater_than_1_and_max_value_is_1_to_people_type():

    # Arrange
    class TestModel(MondayModel):
        people_value = PeopleType(title='People',max_allowed=1)
    model =  TestModel(id='item_id', name='Item Name')

    person_list = [PersonOrTeam(id=13435,kind=PeopleKind.person),PersonOrTeam(id=11234,kind=PeopleKind.person)]
    model.people_value = person_list

    # Assert
    model.validate() 
   
    
@raises(DataError)
def test_should_suceed_when_validate_people_raises_validateerror_when_passed_a_list_of_personorteam_values_with_len_greater_than_max_allowed_and_max_allowed_is_between_two_and_three_to_people_type():
    
    # Arrange
    class TestModel(MondayModel):
        people_value = PeopleType(title='People',max_allowed=3)
    model =  TestModel(id='item_id', name='Item Name')

    id = [12235,12432,12342,12312,123122,321,2131]

    person_list = [PersonOrTeam(id=value,kind=PeopleKind.person) for value in id]
    model.people_value = person_list

    # Assert
    model.validate()



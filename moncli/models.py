import importlib, json, pickle

from schematics.exceptions import DataError
from schematics.models import Model

class MondayModel(Model):

    def __init__(self, item = None, raw_data: dict = {}, id: str = None, name: str = None, board = None, **kwargs):
        
        self._item = item
        self._board = board
        self._module = self.__module__
        self._class = self.__class__.__name__
        self._original_values = {}

        if not (item or board) and not (id and name):
            raise TypeError('Input item, board, or id and name parameters are required.')

        self.id = id
        self.name = name
        if item:
            self.id = item.id
            self.name = item.name

        def get_key(field_type):
            try:
                return field_type.metadata['title']
            except:
                try:
                    return field_type.metadata['id']
                except:
                    return None

        for field, field_type in self._fields.items():
            if not (item or board):
                continue                
            key = get_key(field_type)
            if not key:
                print('Field {} contains no configured column ID or title.'.format(field))
                continue
            try:
                column_values = item.column_values
                value = column_values[key]
                raw_data[field] = value
                self._original_values[field] = pickle.dumps(value.value)
            except:
                columns = board.columns
                column = columns[key]
                field_type.metadata['id'] = column.id
                field_type.metadata['title'] = column.title
                settings = json.loads(column.settings_str)
                for k, v in settings.items():
                    field_type.metadata[k] = v
                self._original_values[field] = pickle.dumps(field_type.default)
                
        super().__init__(raw_data=raw_data, **kwargs)  


    @property
    def item(self):
        return self._item

    def __repr__(self):
        return str(self.__dict__)

    def to_primitive(self, diff_only = False, role = None, app_data = None, **kwargs):        
        base_dict = super().to_primitive(role=role, app_data=app_data, **kwargs)
        result = {}

        def value_changed(value, other):
            return value != other

        for field, value in base_dict.items():
            model_field = self._fields[field]
            if model_field.is_readonly:
                continue      
            if not value:
                value = model_field.null_value
            new_value = pickle.dumps(getattr(self, field))
            if diff_only and not value_changed(new_value, self._original_values[field]):
                continue
            try:
                result[model_field.metadata['id']] = value
            except:
                result[field] = value

        return result

    def get_metadata(self, field: str, key: str):
        try:
            field_obj = self._fields[field]
        except KeyError:
            raise KeyError('Model does not contain field: ({}).'.format(field))
        try:
            return field_obj.metadata[key]
        except KeyError:
            raise KeyError('Model field does not contain metadata key: ({}).'.format(key))
        

    def save(self, group = None, archive: bool = False):
        if not self._item and not self._board:
            raise TypeError('Unable to save model without monday.com item/board information.')

        if self._board and not self.name:
            raise TypeError('Unable to save new model as item without a name.')
        
        try:
            self.validate()
        except DataError as ex:
            raise ex

        column_values = self.to_primitive(diff_only=True)
        if self._item:
            if column_values:
                self._item = self._item.change_multiple_column_values(column_values, get_column_values=True)
            if group:
                self._item = self._item.move_to_group(group.id, get_column_values=True)
        elif self._board:
            kwargs = {}
            if column_values:
                kwargs['column_values'] = column_values
            if group:
                self._item = self._board.add_item(self.name, get_column_values=True, group_id=group.id, **kwargs)
            else:
                self._item = self._board.add_item(self.name, get_column_values=True, **kwargs)
            self.id = self._item.id
        if archive:
            self._item.archive()
        return self
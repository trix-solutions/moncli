import importlib, json, pickle

from schematics.exceptions import DataError
from schematics.models import Model

class MondayModel(Model):

    def __init__(self, item = None, raw_data: dict = None, id: str = None, name: str = None, board = None, *args, **kwargs):
        
        self._item = item
        self._board = board
        self._module = self.__module__
        self._class = self.__class__.__name__
        self._original_values = {}

        has_original = False

        if item:
            self.id = item.id
            self.name = item.name
            raw_data = {}
            column_values = item.column_values
            # When loading column values to the model fields,
            for field, field_type in self._fields.items():
                # First give title a try, as it is best known.
                try:
                    raw_data[field] = column_values[field_type.metadata['title']]
                except:
                    # If that doesn't work, then see if there is an ID.
                    try:
                        raw_data[field] = column_values[field_type.metadata['id']]
                    except:
                        # Otherwise, it's not work the trouble...
                        continue
            has_original = True
        elif raw_data:
            self.id = raw_data.pop('id', None)
            self.name = raw_data.pop('name', None)
        elif (name and id):
            self.id = id
            self.name = name        
        else:
            raise TypeError('Input item, raw data, or id and name are required.')
                
        super(MondayModel, self).__init__(raw_data=raw_data)
        
        if board:
            columns = board.columns
            for field, field_type in self._fields.items():
                try:
                    column = columns[field_type.metadata['title']]
                except:
                    try:
                        column = columns[field_type.metadata['id']]
                    except:
                        continue
                field_type.original_value = None  # Clear out any stale original values.
                field_type.metadata['id'] = column.id
                field_type.metadata['title'] = column.title
                settings = json.loads(column.settings_str)
                for k, v in settings.items():
                    field_type.metadata[k] = v

        for field, _type in self._fields.items():
            if has_original:
                self._original_values[field] = pickle.dumps(getattr(self, field))
            else:
                self._original_values[field] = pickle.dumps(_type.default)


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
        elif self._board and column_values:
            if group:
                self._item = self._board.add_item(self.name, get_column_values=True, group_id=group.id, column_values=column_values)
            else:
                self._item = self._board.add_item(self.name, get_column_values=True, column_values=column_values)
        if archive:
            self._item.archive()
        return getattr(importlib.import_module(self._module), self._class)(self._item)
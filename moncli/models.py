import importlib, json

from schematics.exceptions import DataError
from schematics.models import Model

from .entities import Item, Board, Group

class MondayModel(Model):

    def __init__(self, item: Item = None, raw_data: dict = None, board: Board = None, *args, **kwargs):
        
        self._item = item
        self._board = board
        self._module = self.__module__
        self._class = self.__class__.__name__

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
        elif raw_data:
            self.id = raw_data.pop('id', None)
            self.name = raw_data.pop('name', None)
        
        else:
            raise MondayModelError('Input item or raw data is required.')
                
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
                field_type.metadata['id'] = column.id
                field_type.metadata['title'] = column.title
                settings = json.loads(column.settings_str)
                for k, v in settings.items():
                    field_type.metadata[k] = v


    @property
    def item(self):
        return self._item

    def to_primitive(self, diff_only = False, role = None, app_data = None, **kwargs):        
        base_dict = super().to_primitive(role=role, app_data=app_data, **kwargs)
        result = {}

        for field, value in base_dict.items():
            model_field = self._fields[field]
            if diff_only and not model_field.value_changed(value):
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
            raise MondayModelError('Model does not contain field: ({}).'.format(field))
        try:
            return field_obj.metadata[key]
        except KeyError:
            raise MondayModelError('Model field does not contain metadata key: ({}).'.format(key))
        

    def save(self, group: Group = None):
        if not self._item and not self._board:
            raise MondayModelError('Unable to save model without monday.com item/board information.')

        if self._board and not self.name:
            raise MondayModelError('Unable to save new model as item without a name.')
        
        try:
            self.validate()
        except DataError as ex:
            raise MondayModelError(ex.messages)

        column_values = self.to_primitive(diff_only=True)
        if self._item:
            self._item = self._item.change_multiple_column_values(column_values, get_column_values=True)
            if group:
                self._item = self._item.move_to_group(group.id, get_column_values=True)
        elif self._board:
            if group:
                self._item = self._board.add_item(self.name, get_column_values=True, group_id=group.id, column_values=column_values)
            else:
                self._item = self._board.add_item(self.name, get_column_values=True, column_values=column_values)
        return getattr(importlib.import_module(self._module), self._class)(self._item)


    def __repr__(self):
        return str(self.to_primitive())


class MondayModelError(Exception):
    def __init__(self, message):
        super(MondayModelError, self).__init__(message)
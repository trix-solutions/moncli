import importlib

from schematics.exceptions import DataError
from schematics.models import Model

from .entities import Item

class MondayModel(Model):

    def __init__(self, item: Item = None, raw_data: dict = None, *args, **kwargs):
        
        self._item = item
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
        

    def save(self):
        if not self._item:
            raise MondayModelError('Unable to save model without monday.com item information.')
        
        try:
            self.validate()
        except DataError as ex:
            raise MondayModelError(ex.messages)

        column_values = self.to_primitive(diff_only=True)
        self._item = self._item.change_multiple_column_values(column_values, get_column_values=True)
        return getattr(importlib.import_module(self._module), self._class)(self._item)

    def __repr__(self):
        return str(self.to_primitive())


class MondayModelError(Exception):
    def __init__(self, message):
        super(MondayModelError, self).__init__(message)
from schematics.models import Model

from .entities import Item

class MondayModel(Model):

    def __init__(self, item: Item, *args, **kwargs):
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
                
        super(MondayModel, self).__init__(raw_data=raw_data)
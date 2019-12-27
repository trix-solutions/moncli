from schematics.models import Model
from schematics.types import StringType

class ColumnValue(Model):

    id = StringType(required=True)
    title = StringType()
    text = StringType()
    value = StringType()
    additional_info = StringType()


    def __repr__(self):
        return str(self.to_primitive())


    def format(self):
        return self.to_primitive()
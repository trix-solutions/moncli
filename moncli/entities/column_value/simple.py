from .base import ColumnValue

class DateValue(ColumnValue):
    """A date column value."""

    def format(self):
        """Format for column value update."""
        pass
        

class DropdownValue(ColumnValue):
    """A dropdown column value."""

    def format(self):
        """Format for column value update."""
        pass


class EmailValue(ColumnValue):
    """An email column value."""

    def format(self):
        """Format for column value update."""
        pass

class LinkValue(ColumnValue):
    """A link column value."""

    def format(self):
        """Format for column value update."""
        pass


class LongTextValue(ColumnValue):
    """A long text column value."""
    
    def format(self):
        """Format for column value update."""
        pass

class NumberValue(ColumnValue):
    """A number column value."""

    def format(self):
        """Format for column value update."""
        pass

    def __isfloat(self, value):
        """Is the value a float."""
        try:
            float(value)
        except ValueError:
            return False
        return True
  
    def __isint(self, value):
        """Is the value an int."""
        try:
            a = float(value)
            b = int(a)
        except ValueError:
            return False
        return a == b


class PeopleValue(ColumnValue):
    """A people column value."""
    
    def format(self):
        """Format for column value update."""
        pass


class PhoneValue(ColumnValue):
    """A phone column value."""

    def format(self):
        """Format for column value update."""
        pass


class StatusValue(ColumnValue):
    """A status column value."""

    def format(self):
        """Format for column value update."""
        pass


class TextValue(ColumnValue):
    """A text column value."""

    def format(self):
        """Format for column value update."""
        pass

from numbers import Number


class Entry_Value:
    """TODO"""
    type_id = None
    label = None

    def __init__(self, value):
        if not isinstance(value, Number):
            raise TypeError('value parameter {0} is not a Number'.format(value))
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_type(self):
        """ Return type of the value, as a string. By default, if `type_id` is
            not overrided, the type is the class name as lowercase
        """
        if self.type_id is not None:
            return self.type_id
        return self.__class__.__name__.lower()

    def get_label(self):
        """ Return label of the value, as a string. By default, if `label` is
            not overrided, the type is the class name, ith _ replaced by spaces
            and with title case
        """
        if self.label is not None:
            return self.label
        return self.__class__.__name__.replace('_', ' ').title()

    def get_value(self):
        return self.value


class Expense(Entry_Value):
    """TODO"""

    def __init__(self, value):
        value = -abs(value)
        super().__init__(value)


class Credit(Entry_Value):
    """TODO"""

    def __init__(self, value):
        value = abs(value)
        super().__init__(value)

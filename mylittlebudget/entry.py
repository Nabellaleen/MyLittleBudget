from mylittlebudget.core import User
from mylittlebudget.entry_value import Entry_Value


class Entry:
    """docstring for Entry"""
    def __init__(self, name, category, date, value, owner, users, count=1):
        self.name = name
        self.category = category
        self.date = date
        if not isinstance(value, Entry_Value):
            raise TypeError('value parameter ({0}) is not an Entry_Value'
                .format(value))
        self.value = value
        self.count = count
        if not isinstance(owner, User):
            raise TypeError('owner parameter ({0}) is not a User')
        self.owner = owner
        self.users = users

    def __str__(self):
        entry_type = self.value.get_label()
        entry_type_str = '{0:%Y-%m-%d} - {1} in {2}'.format(self.date,
                                                            entry_type,
                                                            self.category)
        if self.count > 1:
            entry_item_str = self.__get_multi_count_entry_item_str()
        else:
            entry_item_str = self.__get_single_count_entry_item_str()
        entry_owner_str = 'Owner : {0}'.format(self.owner)
        users_str = [str(user) for user in self.users]
        entry_users_str = 'Users : ' + ', '.join(users_str)
        return '{0}: {1} - {2} - {3}'.format(entry_type_str, entry_item_str,
                                             entry_owner_str, entry_users_str)

    def __get_multi_count_entry_item_str(self):
        return '{0} {1} at {2:n}€'.format(self.count,
                                          self.name,
                                          abs(self.value.get_value()))

    def __get_single_count_entry_item_str(self):
        return '{0} at {1:n}€'.format(self.name,
                                      abs(self.value.get_value()))

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from numbers import Number

from bottle import run
from datetime import datetime

from mylittlebudget.web import index


class User:
    """TODO"""
    def __init__(self, name, share_index):
        self.name = name
        self.share_index = share_index

    def __str__(self):
        return 'User({0}, {1})'.format(self.name, self.share_index)


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


class Credit(object):
    """docstring for Credit"""

    def __init__(self, value):
        value = abs(value)
        super().__init__(value)


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


class Account:
    """TODO"""
    _entries = []

    session = None

    def __init__(self, name, users, categories=None):
        self.name = name
        self.users = users
        self.categories = {}
        if categories:
            self.categories = {category.name: category
                               for category in categories}

    def get_multi_share_index(self, users):
        return sum([user.share_index for user in users])

    def add_expense(self, name, category, value, users=None,
                    date=datetime.today()):
        # TODO : generify this check with a decorator
        if not self.session:
            raise Exception('add_expense action need an opened session')

        new_category = self.get_category(category)
        if not new_category:
            exception_message = '{0} not previously defined in {1}'.format(
                category, self)
            raise Exception(exception_message)
        new_users = users if users is not None else self.users
        owner = self.session.user
        new_entry = Entry(name, new_category, date, value, owner, new_users)
        self._entries.append(new_entry)

    def get_expenses(self):
        return [entry for entry in self._entries if isinstance(entry.value,
                                                               Expense)]

    def get_expenses_by_user(self, date_min=None, date_max=None):
        return self.get_entries_by_user(entry_filter=[Expense],
                                        date_min=date_min, date_max=date_max)

    def get_entries_by_user(self, entry_filter=[],
                            date_min=None, date_max=None):
        expenses = []
        for entry in self._entries:
            if entry_filter and entry.value.__class__ not in entry_filter:
                continue
            expense = {'entry': entry,
                       'parts': {},
                       'owners': {},
                       'totals': {}}
            expenses.append(expense)
            entry_value = entry.value.get_value()
            total_share_index = self.get_multi_share_index(entry.users)
            for user in self.users:
                # Compute user share
                user_share = 0
                if user in entry.users:
                    user_share = entry_value * user.share_index / total_share_index
                expense['parts'][user.name] = user_share
                # Compute owners contribution
                owner_value = 0
                if user is entry.owner:
                    owner_value = entry_value
                expense['owners'][user.name] = owner_value
                # Compute users totals
                expense['totals'][user.name] = owner_value - user_share
        return expenses

    def add_category(self, category):
        self.categories[category.name] = category

    def get_category(self, category):
        if isinstance(category, Category):
            # TODO : optimize with directly searching the object in the values
            return self.categories.get(category.name)
        elif isinstance(category, str):
            return self.categories.get(category)
        else:
            raise Exception('Not handled parameter : {0}'.format(category))

    def get_user(self, user_name):
        for user in self.users:
            if user.name is user_name:
                return user
        else:
            return None

    def open_session(self, user_name):
        if self.session:
            raise Exception('A session is already opened')
        # Check credentials
        user = self.get_user(user_name)
        if not user:
            # Login error
            raise ValueError('Unknown user : {0}'.format(user_name))
        # Process to login
        self.session = User_Session(user)

    def close_session(self):
        self.session = None

    def __str__(self):
        return '{0} account'.format(self.name)


class User_Session:

    def __init__(self, user):
        self.user = user


class Category:
    """docstring for Category"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'category {0}'.format(self.name)


def total_sum(x, y):
    try:
        return x + y
    except TypeError:
        x = x if isinstance(x, Number) else 0
        y = y if isinstance(y, Number) else 0
        return x + y


def get_formated_elements(users_cols, elements):
    for user in users_cols:
        element = elements.get(user) or 0
        if element:
            yield '{0:.2f}'.format(element)
        else:
            yield ''


def main():
    categories_names = ['Vehicle', 'Food']
    categories = {name: Category(name=name) for name in categories_names}

    vehicle_category = categories['Vehicle']
    food_category = categories['Food']
    beauty_category = Category(name='Beauty')
    ######################
    # Remove in final test
    categories[beauty_category.name] = beauty_category
    ######################

    users_dict = [{'name': 'Héloïse', 'share_index': 1300},
                  {'name': 'Florian', 'share_index': 2300}]
    users = [User(**user) for user in users_dict]
    current_account = Account(name='household',
                              users=users,
                              categories=categories.values())

    current_account.open_session('Florian')

    current_account.add_expense(name='Fuel', category=vehicle_category,
                                value=Expense(22))
    current_account.add_expense(name='Restaurant', category=food_category,
                                value=Expense(14))
    current_account.add_expense(name='Milk', category='Food',
                                value=Expense(4), users=users[:1])
    current_account.add_expense(name='Bread', category=food_category,
                                value=Expense(1), users=users[1:2])
    current_account.add_expense(name='Soap', category=beauty_category,
                                value=Expense(12))

    current_expenses = current_account.get_expenses()
    for expense in current_expenses:
        print(expense)

    from prettytable import PrettyTable
    standard_col = ['Expenses', 'Date']
    users_cols = [user.name for user in current_account.users]
    users_parts_labels = ['{0} part'.format(user) for user in users_cols]
    owners_labels = ['{0} expense'.format(user) for user in users_cols]
    users_totals_labels = ['{0} total'.format(user) for user in users_cols]
    expenses_table = PrettyTable(standard_col + users_parts_labels +
                                 owners_labels + users_totals_labels)
    total_parts_row = [0 for u in users_cols]
    total_owners_row = [0 for u in users_cols]
    total_totals_row = [0 for u in users_cols]
    current_expenses_by_user = current_account.get_expenses_by_user()
    # from pprint import pprint; pprint(current_expenses_by_user)
    for expense in current_expenses_by_user:
        entry = expense['entry']
        parts = expense['parts']
        owners = expense['owners']
        users_totals = expense['totals']
        # Standard columns
        standard_row = [entry.name, entry.date]
        # Parts columns
        users_row = [part for part in get_formated_elements(users_cols, parts)]
        # Owners columns
        owners_row = [abs(owners.get(user)) or '' for user in users_cols]
        # Users totals columns
        users_totals_row = [total for total in get_formated_elements(users_cols,
                                                                     users_totals)]
        # Create row
        expenses_table.add_row(standard_row + users_row +
                               owners_row + users_totals_row)
        # Compute totals
        total_parts_row = [total_sum(x, y) for x, y in zip(total_parts_row,
                                                           users_row)]
        total_owners_row = [total_sum(x, y) for x, y in zip(total_owners_row,
                                                            owners_row)]
    empty_row = ['' for i in expenses_table.field_names]
    expenses_table.add_row(empty_row)
    total_label_row = ['Total', '']
    expenses_table.add_row(total_label_row + total_parts_row +
                           total_owners_row + total_totals_row)

    print(expenses_table)

    # run(host='localhost', port=8080)

if __name__ == '__main__':
    main()

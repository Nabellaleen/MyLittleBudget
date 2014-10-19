#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bottle import run
from datetime import datetime

from mylittlebudget.web import index


class User:
    """TODO"""
    def __init__(self, name):
        self.name = name


class Entry:
    """docstring for Entry"""
    def __init__(self, name, category, date, value, count):
        if value == 0:
            raise Exception('Value cannot be zero')
        self.name = name
        self.category = category
        self.date = date
        self.value = value
        self.count = count

    def __str__(self):
        entry_type = 'Expense' if self.is_expense() else 'Credit'
        entry_type_str = '{0:%Y-%m-%d} - {1} in {2}'.format(self.date,
                                                            entry_type,
                                                            self.category)
        if self.count > 1:
            entry_item_str = '{0} {1} at {2:n}€'.format(self.count,
                                                        self.name,
                                                        abs(self.value))
        else:
            entry_item_str = '{0} at {1:n}€'.format(self.name,
                                                    abs(self.value))
        return '{0}: {1}'.format(entry_type_str, entry_item_str)

    def is_expense(self):
        return self.value < 0

    def is_credit(self):
        return self.value > 0


class Account:
    """TODO"""
    _entries = []

    def __init__(self, name, users, categories=None):
        self.name = name
        self.users = users
        self.categories = {}
        if categories:
            self.categories = {category.name: category
                               for category in categories}

    def add_expense(self, name, category, total, date=datetime.today(),
                    count=1):
        new_category = self.get_category(category)
        if not new_category:
            exception_message = '{0} not previously defined in {1}'.format(
                category, self)
            raise Exception(exception_message)
        new_total = total if total < 0 else -total
        new_entry = Entry(name, new_category, date, new_total, count)
        self._entries.append(new_entry)

    def get_expenses(self):
        return [entry for entry in self._entries if entry.is_expense()]

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

    def __str__(self):
        return '{0} account'.format(self.name)


class Category(object):
    """docstring for Category"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'category {0}'.format(self.name)


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

    user_names = ['Héloïse', 'Florian']
    users = [User(name=name) for name in user_names]
    current_account = Account(name='household',
                              users=users,
                              categories=categories.values())
    current_account.add_expense(name='Fuel', category=vehicle_category,
                                total=22)
    current_account.add_expense(name='Restaurant', category=food_category,
                                total=14)
    current_account.add_expense(name='Milk', category='Food',
                                total=4, count=4)
    current_account.add_expense(name='Bread', category=food_category,
                                total=1, count=2)
    current_account.add_expense(name='Soap', category=beauty_category,
                                total=12, count=2)

    current_expenses = current_account.get_expenses()
    for expense in current_expenses:
        print(expense)

    # run(host='localhost', port=8080)

if __name__ == '__main__':
    main()

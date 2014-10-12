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
        # TODO : manage value equals to zero
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

    def __init__(self, name, users):
        self.name = name
        self.users = users

    def add_expense(self, name, category, value, date=datetime.today(), count=1):
        new_value = value if value < 0 else -value
        new_entry = Entry(name, category, date, new_value, count)
        self._entries.append(new_entry)

    def get_expenses(self):
        return [entry for entry in self._entries if entry.is_expense()]


def main():
    user_names = ['Héloïse', 'Florian']
    users = [User(name=name) for name in user_names]
    current_account = Account(name='household',
                              users=users)
    current_account.add_expense(name='Fuel', category='Vehicle',
                                value=22)
    current_account.add_expense(name='Restaurant', category='Food',
                                value=14)
    current_account.add_expense(name='Milk', category='Food',
                                value=4, count=4)
    current_account.add_expense(name='Bread', category='Food',
                                value=1, count=2)

    current_expenses = current_account.get_expenses()
    for expense in current_expenses:
        print(expense)

    # run(host='localhost', port=8080)

if __name__ == '__main__':
    main()

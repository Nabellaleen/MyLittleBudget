#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from numbers import Number

from bottle import run

from mylittlebudget.web import index
from mylittlebudget.category import Category
from mylittlebudget.user import User
from mylittlebudget.account import Account
from mylittlebudget.entry_value import Expense


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
        total_totals_row = [total_sum(x, y) for x, y in zip(total_totals_row,
                                                            users_totals_row)]
    empty_row = ['' for i in expenses_table.field_names]
    expenses_table.add_row(empty_row)
    total_label_row = ['Total', '']
    expenses_table.add_row(total_label_row + total_parts_row +
                           total_owners_row + total_totals_row)

    print(expenses_table)

    # run(host='localhost', port=8080)

if __name__ == '__main__':
    main()

from datetime import datetime

from mylittlebudget.entry import Entry
from mylittlebudget.entry_value import Expense
from mylittlebudget.category import Category
from mylittlebudget.session import User_Session


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

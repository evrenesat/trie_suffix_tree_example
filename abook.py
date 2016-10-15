# -*-  coding: utf-8 -*-
"""

"""
from collections import defaultdict

from debe import DeBe, TrieIndex


class Person:
    """
    Person(name='foo', group='bar', phones=['123','345'])
    Person(surname='foo', groups=['bar','baz'], phone='123')
    """

    def __init__(self, **kwargs):
        self.pk = None
        self.data = {
            'name': '',
            'last_name': '',
            'address_set': [],
            'email_set': [],
            'phone_set': [],
            'group_set': [],
        }
        self.add(**kwargs)

    def __repr__(self):
        return '%s %s' % (self.data['name'], self.data['email_set'])

    def add(self, **kwargs):
        """
        handles assignment of multiple or singular properties
        """
        for param in ['address', 'email', 'phone', 'group']:
            if param in kwargs:
                self.data["%s_set" % param].append(kwargs.pop(param))
        self.data.update(kwargs)


class AddressBook(DeBe):
    def __init__(self):
        self.groups = defaultdict(list)
        super(AddressBook, self).__init__(['group_set', 'email_set', 'name', 'last_name'])
        self.indexes['email_set'] = TrieIndex(use_suffix=True)

    def add(self, person, pk=None):
        super(AddressBook, self).add(person, pk)
        for group in person.data['group_set']:
            self.groups[group].append(person.pk)

    def create_person(self, **kwargs):
        person = Person(**kwargs)
        self.add(person)
        return person

    def group(self, name):
        self.groups.setdefault(name, {})

# -*-  coding: utf-8 -*-
"""

"""
from collections import defaultdict

from debe import DeBe


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

    def get_groups(self):
        return self.data['group_set']

    def add(self, **kwargs):
        """
        Handles assignment of multiple or singular properties

        Keyword Args:
            name (str): Person's name
            last_name (str): Person's last name
            email (str): Person's email
            address (str): Person's address
            phone (str): Person's phone
            group (str): Person's group
            email_set (list): Update Person's email_set
            address_set (list): Update Person's address_set
            phone_set (list): Update Person's phone_set
            group_set (list): Update Person's group_set
        """
        for key, val in kwargs.items():
            if key in ['name', 'last_name']:
                self.data[key] = val
            else:
                key_set = '%s_set' % key
                if key_set in self.data:
                    key, val = key_set, [val]
                self.data[key] = list(set(self.data[key] + val))


class AddressBook(DeBe):
    def __init__(self):
        """

        """
        self.groups = defaultdict(list)
        super(AddressBook, self).__init__(
            prefix_index=['group_set', 'address_set', 'name', 'last_name'],
            suffix_index=['email_set'])

    def add(self, person, pk=None):
        """
        Add a Person to address book.

        Args:
            person (Person): Person object.
            pk (str, optional): Primary key for person.
        """
        super(AddressBook, self).add(person, pk)
        for group in person.data['group_set']:
            self.groups[group].append(person.pk)

    def create_person(self, **kwargs):
        """
        Shortcut method for creating a Person object with given parameters,
        then adding it to address book.

        Keyword Args:
            See Person object.
        Returns:
            Person: Just created Person object
        """
        person = Person(**kwargs)
        self.add(person)
        return person

    def add_group(self, name):
        """Creates a group, but explicit
        group creation is not required.

        Args:
            name(str): Name of group
        """
        self.groups.setdefault(name, {})

    def list_groups(self):
        """
        Returns:
            list: List of group names
        """
        return list(self.groups.keys())

    def get_group(self, name):
        """
        Group
        Args:
            name (str): name of group
        Returns:
            generator: Members (Person) of given group
        """
        return self._get_objects_by_ids(self.groups[name]) if self.groups[name] else []

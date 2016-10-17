# -*-  coding: utf-8 -*-
"""
"""
from abook import AddressBook, Person

person1_data = {
    'email': 'eeo@goomail.com',
    'name': 'person',
    'last_name': 'last1',
    'address': 'address 1',
    'phone': '5550555',
    'group_set': ['family', 'friend']
}
person1_additional_email = 'mail2@person1.com'

person2_data = {
    'email_set': ['foomail@foomale.com', 'bar@bazmail.com'],
    'name': 'person',
    'last_name': 'last2',
    'address': 'address 1',
    'phone_set': ['0011010000110010'],
    'group': 'work'
}


class Test:
    def test_add_find_persons(self):
        # create address book
        ab = AddressBook()
        # create person
        p1 = Person(**person1_data)
        # add a mail to person
        p1.add(email=person1_additional_email)
        # add person to address book
        ab.add(p1)
        # create and add a person to address book
        p2 = ab.create_person(**person2_data)

        # find person  by last name
        results = list(ab.find_by(last_name=person1_data['last_name']))
        assert 1 == len(results)
        assert p1 == results[0]

        # since their first names are same,
        # just first name is not enough to find one we are looking for
        assert 2 == len(list(ab.find_by(name='person')))
        results = list(ab.find_by(name=person1_data['name'], last_name=person1_data['last_name']))
        assert 1 == len(results)
        assert p1 == results[0]
        assert person1_data['email'] in results[0].data['email_set']
        assert person1_additional_email in results[0].data['email_set']

        # substring search on multiple mails of a Person
        assert p2 == list(ab.find_by(email='male'))[0]
        assert p2 == list(ab.find_by(email='baz'))[0]

    def test_groups(self):
        ab = AddressBook()
        ab.add_group('FooGroup')
        assert 'FooGroup' == ab.list_groups()[0]
        p1 = ab.create_person(**person1_data)
        p2 = ab.create_person(**person2_data)
        assert 'FooGroup' in ab.list_groups()
        assert person2_data['group'] in ab.list_groups()
        # find person by group
        assert p2 == list(ab.get_group(person2_data['group']))[0]
        # no body in this group
        assert not ab.get_group('FooGroup')

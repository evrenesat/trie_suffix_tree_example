# -*-  coding: utf-8 -*-
"""
"""
from pprint import pprint

from abook import AddressBook


class Test:
    def test_add_person(self):
        ab = AddressBook()

        p1 = ab.create_person(name='esat', email='eeo@goomail.com', group='family')
        p1.add(email='e2@roobar.com')
        p2 = ab.create_person(name='fooz',
                              email_set=['foomail@foomale.com',
                                         'bar@bazmail.com'],
                              group_set=['friend', 'work'])

        results = list(ab.find_by(name='esat'))
        assert 1 == len(results)
        p1_from_ab = results[0]
        assert p1 == p1_from_ab
        assert 'eeo@goomail.com' in p1_from_ab.data['email_set']
        assert 'e2@roobar.com' in p1_from_ab.data['email_set']
        p0 = ab.create_person(name='esata', email='e1', group='family')
        pprint(ab.indexes['email'].idx)
        assert p2 == list(ab.find_by(email='male'))[0]
        assert p2 == list(ab.find_by(email='baz'))[0]
        assert p2 == list(ab.find_by(name='fo'))[0]


    def test_groups(self):
        ab = AddressBook()
        p1 = ab.create_person(name='esat', email='e1', group='family')
        p1.add(email='e2')
        p2 = ab.create_person(name='foo', group_set=['friend', 'work'])
        p3 = ab.create_person(name='Buzz', last_name='lightyear', group_set=['friend', 'work'])
        p1_from_ab = list(ab.find_by(name='esat'))[0]
        assert p1 == p1_from_ab
        assert 'e1' in p1_from_ab.data['email_set']
        assert 'e2' in p1_from_ab.data['email_set']
        assert p2 == list(ab.find_by(name='fo'))[0]

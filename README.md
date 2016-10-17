**An AddressBook library using simple Trie / Suffix Trie indexes**

This project contains a simple in-memory DB implementation using Python data types.
This is just an example project, which is not suitable for any production need.
For production please use one of the followings:
 * https://github.com/pytries/DAWG
 * https://github.com/s-yata/marisa-trie
    


***Usage***

```python

In [1]: from abook import AddressBook

In [2]: ab = AddressBook()

In [3]: p1 = ab.create_person(name='foo', last_name='bar', group='work')

In [4]: p2 = ab.create_person(name='fee', last_name='bin', email='mail@ma.co',  group_set=['work', 'friend'])

In [5]: list(ab.find_by(name='fee'))
Out[5]: [fee ['mail@ma.co']]

# Explicitly create a Person object
In [7]: from abook import Person

In [8]: p3=Person(name='p3', address_set=['ad1','adr2'], group='family')

# add a proprety
In [9]: p3.add(email='p3@p3.com')

# then add it to address book
In [10]: ab.add(p3)
```
***Prefix and substring searches***

By using Trie indexes, all fields supports prefix matching.
 We only use [Suffix tire indexing][1] on  email field, 
 so we can search with substring of an email
 [1]: https://github.com/evrenesat/trie_suffix_tree_example/blob/master/debe.py#L29

```python

# find_by method works for all fields (name, last_name, email, address, phone)
# But only "email" field supports substring matching
In [11]: list(ab.find_by(email='co')) # we need to convert result generator to list
Out[11]: [fee ['mail@ma.co'], p3 ['p3@p3.com']]

# get list of existing groups
In [12]: ab.list_groups()
Out[12]: ['work', 'family', 'friend']

# get members of a group
In [13]: ab.get_group('work')
Out[13]: <generator object <genexpr> at 0x11047d370>

In [14]: list(ab.get_group('work'))
Out[14]: [foo [], fee ['mail@ma.co']]

# we can explicity create a group but it's not required
In [15]: ab.add_group('foo')

In [16]: ab.list_groups()
Out[16]: ['work', 'family', 'friend', 'foo']


```

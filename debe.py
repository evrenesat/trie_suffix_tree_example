# -*-  coding: utf-8 -*-
"""
"""
from uuid import uuid4


class TrieIndex(object):
    def __init__(self, use_suffix=False):
        """
        A super simple Trie or Suffix Trie index.

        Args:
            use_suffix(bool): Set True if you need substring matching on this index.
        """
        self.idx = dict(vals=list())
        self.add = self._suffix_add if use_suffix else self._prefix_add

    def add(self, key, val):
        """
        According to `use_suffix` parameter,
        replaced by _prefix_add or _suffix_add at init.

        Args:
            key: Any object with a string representation
            val: Value to be indexed according to key
        """
        pass

    def _suffix_add(self, key, val):
        """
        adds all suffixes of the key to index using prefix_add
        """
        key = str(key)
        for i in range(len(key)):
            self._prefix_add(key[-i - 1:], val)

    def _prefix_add(self, key, val):
        """
        creates a trie index for given `key`,
        adds `val` to `vals` list of each level along the way
        """
        idx = self.idx
        for word in str(key).lower():
            for letter in word:
                idx = idx.setdefault(letter, dict(vals=list()))
            idx['vals'].append(val)

    def find(self, key):
        idx = self.idx
        for letter in str(key).lower():
            if letter in idx:
                idx = idx[letter]
            else:
                return False
        else:
            return idx['vals']


class DeBe(object):
    def __init__(self, prefix_index=None, suffix_index=None):
        """
        An in-memory DB that supports prefix and substring (suffix)
        matching.

        Args:
            prefix_index(list): List of fields to be indexed for prefix matching
            suffix_index(list): List of fields to be indexed for substring matching

        """
        self.object_by_pk = {}
        self.indexes = {}
        self._create_indexes(prefix_index or [], suffix_index or [])

    def _create_indexes(self, prefix, suffix):
        for field in prefix:
            self.indexes[field] = TrieIndex()
        for field in suffix:
            self.indexes[field] = TrieIndex(use_suffix=True)

    def add(self, obj, pk=None):
        """
        Add an object to database
        Args:
            obj: Any object that has a "data" dict with fields to be indexed.
            pk(str, optional): Optional primary key

        Returns:
            object
        """
        obj.pk = pk or uuid4().hex
        self.object_by_pk[obj.pk] = obj
        self._handle_indexing(obj)
        return obj

    def _handle_indexing(self, object):
        for field in self.indexes:
            if field.endswith('_set'):
                for field_item in object.data[field]:
                    self.indexes[field].add(field_item, object.pk)
            else:
                self.indexes[field].add(object.data[field], object.pk)

    def get(self, pk):
        """
        Get the object by its primary key

        Args:
            pk (str): Primary key of requested object

        Returns:
            Requested object.
        """
        return self.object_by_pk[pk]

    def _get_objects_by_ids(self, pk_list):
        """returns a generator that yields a result object in each turn"""
        return (self.object_by_pk[pk] for pk in pk_list)

    def find_by(self, **kwargs):
        """
         Fields that defined in "indexed_fields"
          can be used for filtering.
         All filters will be ANDed together.

        Args:
            **kwargs: Filter parameters

        Returns:
            generator: Objects matching to given filters
        """
        results = []
        for key, val in kwargs.items():
            index_name = key if key in self.indexes else "%s_set" % key
            if index_name not in self.indexes:
                print("%s field does not indexed, please try searching on following fields:" % key)
                print("\t".join([f.replace('_set', '') for f in self.indexes]))
            results.append(set(self.indexes[index_name].find(val)))
        return self._get_objects_by_ids(set.intersection(*results))

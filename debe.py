# -*-  coding: utf-8 -*-
"""
"""
from collections import defaultdict
from uuid import uuid4


class TrieIndex(object):
    def __init__(self, use_suffix=False):
        self.idx = dict(vals=list())
        self.add = self.suffix_add if use_suffix else self.prefix_add

    def suffix_add(self, key, val):
        key = str(key)
        for i in range(len(key)):
            self.prefix_add(key[-i - 1:], val)

    def prefix_add(self, key, val):
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
    def __init__(self, indexed_fields=None):
        self.object_by_pk = dict()
        self.indexes = defaultdict(TrieIndex)
        self.indexed_fields = indexed_fields

    def add(self, obj, pk=None):
        obj.pk = pk or uuid4().hex
        self.object_by_pk[obj.pk] = obj
        self._handle_indexing(obj)

    def _handle_indexing(self, object):
        for field in self.indexed_fields:
            if field.endswith('_set'):
                for field_item in object.data[field]:
                    self.indexes[field].add(field_item, object.pk)
            else:
                self.indexes[field].add(object.data[field], object.pk)

    def _get_objects_by_ids(self, pk_list):
        """returns a generator that yields a result object in each turn"""
        return (self.object_by_pk[pk] for pk in pk_list)

    def find_by(self, **kwargs):
        results = []
        for key, val in kwargs.items():
            k_set = key if key in self.indexed_fields else "%s_set" % key
            if k_set not in self.indexed_fields:
                print("%s field does not indexed, please try searching on following fields:" % key)
                print("\t".join([f.replace('_set', '') for f in self.indexed_fields]))
            results.append(set(self.indexes[k_set].find(val)))
        return self._get_objects_by_ids(set.intersection(*results))

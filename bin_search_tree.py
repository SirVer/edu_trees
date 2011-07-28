#!/usr/bin/env python
# encoding: utf-8

"""
Implementation of a binary search tree
"""

from functools import total_ordering
import random

@total_ordering
class Node(object):
    def __init__(self, key, parent = None, l = None, r = None):
        self.key = key
        self.parent = parent
        self.l = l
        self.r = r

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.key == other.key

    def __repr__(self):
        return "Node(%r,%s,%s,%s)" % (self.key,
            self.parent.key if self.parent else None,
            self.l.key if self.l else None,
            self.r.key if self.r else None)


class BinarySearchTree(object):
    def __init__(self, iter = []):
        self._root = None

        for i in iter:
            self.insert(i)

    # Search a node
    def _search(self, node, key):
        if node is None: return None
        if node.key == key: return node
        return self._search(node.l, key) if key < node.key else \
               self._search(node.r, key)

    # Inserting
    def insert(self, k):
        self._root = self._insert(self._root, k)
        return self._root

    def _insert(self, node, key):
        if node is None: return Node(key)

        if key <= node.key:
            node.l = self._insert(node.l, key)
            node.l.parent = node
        else:
            node.r = self._insert(node.r, key)
            node.r.parent = node
        return node

    # Deleting
    def delete(self, k):
        n = self._search(self._root, k)
        if not n: return

        self._delete_node(n)


    def _delete_leaf(self, n):
        if n.parent.l == n:
            n.parent.l = None
        else:
            n.parent.r = None

    def _delete_node_with_one_child(self, n):
        child = n.l or n.r

        if n.parent.l == n:
            n.parent.l = child
        if n.parent.r == n:
            n.parent.r = child
        child.parent = n.parent

    def _biggest_succ(self, node):
        if node.r:
            return self._biggest_succ(node.r)
        return node

    def _smallest_succ(self, node):
        if node.l:
            return self._smallest_succ(node.l)
        return node

    def _delete_node_with_two_childs(self, n):
        child = self._smallest_succ(n.r) if random.choice((0,1)) == 0 \
                else self._biggest_succ(n.l)

        n.key = child.key
        self._delete_node(child)

    def _delete_node(self, n):
        if n.l is None and n.r is None:
            self._delete_leaf(n)
        elif n.l is None or n.r is None:
            self._delete_node_with_one_child(n)
        else:
            self._delete_node_with_two_childs(n)


    def __iter__(self):
        def _do_yields(node):
            if node.l:
                for k in _do_yields(node.l):
                    yield k
            yield node.key
            if node.r:
                for k in _do_yields(node.r):
                    yield k

        if self._root:
            for k in _do_yields(self._root):
                yield k

    def plot(self, fn):
        import pydot
        import os.path

        df = pydot.Dot(bgcolor="#ffffff00")

        def _add_dummy_node(node, appendix):
            dn = str(node.key) + appendix
            df.add_node(pydot.Node(dn, label="", shape="point", color="white"))
            df.add_edge(pydot.Edge(node.key, dn, color="#cecece"))

        def _plot_node(node):
            df.add_node(pydot.Node(node.key, color="#cecece", fontcolor="#cecece"))
            if node.l:
                _plot_node(node.l)
                df.add_edge(pydot.Edge(node.key, node.l.key, color="#cecece"))
            else:
                _add_dummy_node(node, '_l')

            if node.r:
                _plot_node(node.r)
                df.add_edge(pydot.Edge(node.key, node.r.key, color="#cecece"))
            else:
                _add_dummy_node(node, '_r')

        if self._root:
            _plot_node(self._root)

        ft = os.path.splitext(fn)[1].replace(".","_")
        df.__getattribute__("write"+ ft)(fn)


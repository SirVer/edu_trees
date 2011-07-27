#!/usr/bin/env python
# encoding: utf-8

"""
Implementation of a binary search tree
"""

from functools import total_ordering
import random

import pydot

@total_ordering
class Node(object):
    def __init__(self, key, data, parent = None, child_left = None, child_right = None):
        self.key = key
        self.data = data
        self._parent = parent
        self._l = child_left
        self._r = child_right

    def replace_with(self, n):
        self.key = n.key
        self.data = n.data

    def l():
        """The left (smaller) child"""
        def fget(self):
            return self._l
        def fset(self, value):
            if value is not None:
                value._parent = self
            self._l = value
        return locals()
    l = property(**l())

    def r():
        """The right (bigger) child"""
        def fget(self):
            return self._r
        def fset(self, value):
            if value is not None:
                value._parent = self
            self._r = value
        return locals()
    r = property(**r())

    def parent():
        """The parent of this node"""
        def fget(self):
            return self._parent
        def fset(self, value):
            self._parent = value
        return locals()
    parent = property(**parent())

    @property
    def grandparent(self):
        if self._parent:
            return self._parent._parent

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.key == other.key

    def __repr__(self):
        return "Node(%s,%s)" % (self.key, self.data)


class BinarySearchTree(object):
    def __init__(self):
        self._root = None

# TODO: deleting
    def insert(self, k, v = None):
        self._root = self._insert(self._root, Node(k,v))
        return self._root

    def _biggest_child(self, node):
        if node.r:
            return self._biggest_child(node.r)
        return node

    def _smallest_child(self, node):
        if node.l:
            return self._smallest_child(node.l)
        return node

    def _insert(self, node, data):
        if node is None:
            return data

        if data <= node:
            node.l = self._insert(node.l, data)
        else:
            node.r = self._insert(node.r, data)

        return node

    def _delete_leaf(self, n):
        if n.parent._l == n:
            n.parent._l = None
        else:
            n.parent._r = None
        n._parent = None

    def _delete_node_with_one_child(self, n):
        child = n._l or n._r
        n.replace_with(child)
        n.l = child.l
        n.r = child.r

    def _delete_node_with_two_childs(self, n):
        child = self._smallest_child(n.r) if random.choice((0,1)) == 0 \
                else self._biggest_child(n.l)

        n.replace_with(child)
        self._delete_node(child)

    def _delete_node(self, n):
        if n.l is None and n.r is None:
            self._delete_leaf(n)
        elif n.l is None or n.r is None:
            self._delete_node_with_one_child(n)
        else:
            self._delete_node_with_two_childs(n)

    def delete(self, k):
        n = self.search(k)
        if not n: return

        self._delete_node(n)


    def search(self, k):
        cur = self._root
        while 1:
            if not cur: return None
            if k < cur.key:
                cur = cur.l
            elif k > cur.key:
                cur = cur.r
            else:
                return cur

    def __iter__(self):
        def _do_yields(node):
            if node.l:
                for k in _do_yields(node.l):
                    yield k
            yield node
            if node.r:
                for k in _do_yields(node.r):
                    yield k

        if self._root:
            for k in _do_yields(self._root):
                yield k


    def plot(self, fn):
        df = pydot.Dot()

        def _add_dummy_node(node, appendix):
            dn = str(node.key) + appendix
            df.add_node(pydot.Node(dn, label="", shape="point", color="green"))
            df.add_edge(pydot.Edge(node.key, dn))

        def _plot_node(node):
            df.add_node(pydot.Node(node.key))
            if node.l:
                _plot_node(node.l)
                df.add_edge(pydot.Edge(node.key, node.l.key))
            else:
                _add_dummy_node(node, '_l')

            if node.r:
                _plot_node(node.r)
                df.add_edge(pydot.Edge(node.key, node.r.key))
            else:
                _add_dummy_node(node, '_r')

        if self._root:
            _plot_node(self._root)

        df.write_pdf(fn)
        df.write_dot(fn + '.dot')

def blah():
    k = BinarySearchTree()
    maxn = 20
    vals = range(maxn)
    random.shuffle(vals)

    for v in vals: k.insert(v)

    dv = range(0,maxn,2)

    vals = list(v.key for v in k)
    print "vals: %s" % (vals)

    k.plot("blah_orig.pdf")

    return k, dv








#!/usr/bin/env python
# encoding: utf-8


from bin_search_tree import Node, BinarySearchTree

import pydot

class AVLNode(Node):
    def __init__(self, key, parent = None, l = None, r = None):
        Node.__init__(self, key, parent, l, r)

    @property
    def pydot_node(self):
        height = '<font point-size="9">%i</font><br />' % (self.height)
        balance = '<font point-size="8" '
        if abs(self.height_balance) > 1:
            balance += 'color="red"'
        else:
            balance += 'color="green"'

        balance += '>%s</font>' % self.height_balance
        return pydot.Node(self.key, color="#cecece", fontcolor="#cecece", label =
"""<%s<br />%s%s>""" % (self.key, height, balance))

    @property
    def height_balance(self):
        r = 0 if self.r is None else self.r.height
        l = 0 if self.l is None else self.l.height
        return l - r

    @property
    def height(self):
        return 1 + max(
            0 if self.l is None else self.l.height,
            0 if self.r is None else self.r.height
        )


class AVLTree(BinarySearchTree):

    def __init__(self, iter = []):
        BinarySearchTree.__init__(self, iter, AVLNode)


    def insert(self, key):
        if not self._root:
            self._root = self._node_klass(key)
        else:
            self._insert(self._root, key)
        return self._root

    def _insert(self, node, key):
        assert(node)

        if key <= node.key:
            if node.l is None:
                node.l = self._node_klass(key, node)
            else:
                self._insert(node.l, key)
        else:
            if node.r is None:
                node.r = self._node_klass(key, node)
            else:
                self._insert(node.r, key)

        if node:
            if abs(node.height_balance) > 1:
                self._rebalance(node)

        return node


    def _rebalance(self, P):
        assert(abs(P.height_balance) == 2)
        if P.height_balance == 2: # left subtree > right subtree
            L = P.l
            assert abs(L.height_balance) == 1, "%s" % L.height_balance
            if L.height_balance == 1:
                self._right_rotate(P)
                #self._right_rotate(L)
            else:
                self._left_rotate(L)
                self._right_rotate(P)
            return L
        else: # right subtree > left subtree
            R = P.r
            assert abs(R.height_balance) == 1, "%s" % R.height_balance
            if R.height_balance == -1:
                self._left_rotate(P)
                #self._left_rotate(R)
            else:
                self._right_rotate(R)
                self._left_rotate(P)
            return R




    def _left_rotate(self, P):
        R = P.r
        GP = P.parent
        B = R.l

        # Link P as new l of R
        P.parent = R; R.l = P

        # Link R as new child of GP
        R.parent = GP
        if GP:
            if GP.l == P:
                GP.l = R
            else:
                GP.r = R
        else: # No grandparent -> P was the root
            self._root = R

        # Link P as new parent of R.l
        P.r = B;
        if B:
            B.parent = P

    def _right_rotate(self, P):
        L = P.l
        GP = P.parent
        B = L.r

        # Link P as new r of L
        P.parent = L; L.r = P

        # Link L as new child of GP
        L.parent = GP
        if GP:
            if GP.l == P:
                GP.l = L
            else:
                GP.r = L
        else: # No grandparent -> P was the root
            self._root = L

        # Link P as new parent of L.r
        P.l = B
        if B:
            B.parent = P



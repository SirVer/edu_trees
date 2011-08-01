#!/usr/bin/env python
# encoding: utf-8

import pydot

from bin_search_tree import Node, BinarySearchTree

class AVLNode(Node):
    def __init__(self, key, parent = None, l = None, r = None):
        Node.__init__(self, key, parent, l, r)
        self.height = 1

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

class AVLTree(BinarySearchTree):
    def __init__(self, iter = []):
        BinarySearchTree.__init__(self, iter, AVLNode)

    # Inserting
    def _just_inserted(self, node):
        par = node.parent
        while par:
            self._update_height(par)
            if abs(par.height_balance) > 1:
                self._rebalance(par)
                break
            par = par.parent

        return node

    # Deleting: rebalance tree if necessary
    def _delete_leaf(self, n):
        par = n.parent
        BinarySearchTree._delete_leaf(self, n)
        self._rebalance_till_root(par)

    def _delete_node_with_one_child(self, n):
        par = n.parent
        BinarySearchTree._delete_node_with_one_child(self, n)
        self._rebalance_till_root(par)

    # Rebalancing:
    def _update_height(self, node):
        """Returns True if the height has changed"""
        old_height = node.height
        node.height = 1 + max(
            node.l.height if node.l else 0,
            node.r.height if node.r else 0,
        )
        return node.height != old_height

    def _rebalance_till_root(self, node):
        while node and self._update_height(node):
            node = node.parent if abs(node.height_balance) <= 1 else self._rebalance(node)

    def _rebalance(self, P):
        assert(abs(P.height_balance) == 2)
        if P.height_balance == 2: # left subtree > right subtree
            L = P.l
            #assert abs(L.height_balance) == 1, "%s" % L.height_balance
            if L.height_balance >= 0:
                self._right_rotate(P)
            else:
                self._left_rotate(L)
                self._right_rotate(P)
            return L.parent
        else: # right subtree > left subtree
            R = P.r
            #assert abs(R.height_balance) == 1, "%s" % R.height_balance
            if R.height_balance <= 0:
                self._left_rotate(P)
            else:
                self._right_rotate(R)
                self._left_rotate(P)
            return R.parent

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

        self._update_height(P)
        self._update_height(R)
        self._rebalance_till_root(R.parent)

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

        self._update_height(P)
        self._update_height(L)
        self._rebalance_till_root(L.parent)


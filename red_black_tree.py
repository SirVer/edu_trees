#!/usr/bin/env python
# encoding: utf-8

import pydot

from bin_search_tree import Node, BinarySearchTree

RED, BLACK = 0,1
class RedBlackNode(Node):
    def __init__(self, key, parent = None, l = None, r = None):
        Node.__init__(self, key, parent, l, r)
        self.color = BLACK

    @property
    def pydot_node(self):
        color = "red" if self.color is RED else "black"
        return pydot.Node(self.key, color=color, fontcolor="#cecece")

    @property
    def sibling(self):
        if not self.parent: return None
        if self.parent.l == self:
            return self.parent.r
        return self.parent.l

class RedBlackTree(BinarySearchTree):
    def __init__(self, iter = []):
        BinarySearchTree.__init__(self, iter, RedBlackNode)

    # Insertion, taken straight from Wikipedias page
    def _just_inserted(self, node):
        node.color = RED

        self._handle_insert_case1(node)

    def _handle_insert_case1(self, node):
        if node.parent is None:
            node.color = BLACK
        else:
            self._handle_insert_case2(node)

    def _handle_insert_case2(self, node):
        if node.parent.color is RED:
            self._handle_insert_case3(node)

    def _handle_insert_case3(self, node):
        uncle = node.parent.sibling
        if uncle and uncle.color is RED:
            uncle.color = BLACK
            node.parent.color = BLACK
            gp = node.parent.parent
            gp.color = RED
            self._handle_insert_case1(gp)
        else:
            self._handle_insert_case4(node)

    def _handle_insert_case4(self, node):
        gp = node.parent.parent
        par = node.parent

        if (gp.l == par and par.r == node):
            self._left_rotate(par)
            node = par
        elif (gp.r == par and par.l == node):
            self._right_rotate(par)
            node = par
        self._handle_insert_case5(node)

    def _handle_insert_case5(self, node):
        par = node.parent
        gp = par.parent

        par.color = BLACK
        gp.color = RED
        if gp.l == par and par.l == node:
            self._right_rotate(gp)
        else:
            self._left_rotate(gp)


    # Deleting
    def _delete_leaf(self, n):
        if n.color is RED: # simple case
            BinarySearchTree._delete_leaf(self, n)
        else:
            self._delete_case1(n)
            BinarySearchTree._delete_leaf(self, n)

    def _delete_node_with_one_child(self, M):
        C = M.l or M.r
        assert(M.color is BLACK)
        if C.color is RED:
            C.color = BLACK
        BinarySearchTree._delete_node_with_one_child(self, M)

    def _delete_case1(self, n):
        if n.parent is not None:
            self._delete_case2(n)
    def _delete_case2(self, n):
        s = n.sibling
        if s and s.color is RED:
            n.parent.color = RED
            s.color = BLACK
            if n.parent.l == n:
                self._left_rotate(n.parent)
            else:
                self._right_rotate(n.parent)
        self._delete_case3(n)
    def _delete_case3(self, n):
        s = n.sibling

        if (n.parent.color is BLACK and
            (s is None or s.color is BLACK) and
            (s.l is None or s.l.color is BLACK) and
            (s.r is None or s.r.color is BLACK)):
                assert(s)
                s.color = RED
                self._delete_case1(n.parent)
        else:
            self._delete_case4(n)
    def _delete_case4(self, n):
        s = n.sibling

        if (n.parent.color is RED and
            (s is None or s.color is BLACK) and
            (s.l is None or s.l.color is BLACK) and
            (s.r is None or s.r.color is BLACK)):
                assert(s)
                s.color = RED
                n.parent.color = BLACK
        else:
            self._delete_case5(n)
    def _delete_case5(self, n):
        s = n.sibling
        if (s is None or s.color == BLACK):
            if (n is n.parent.l and
                (s.r is None or s.r.color is BLACK) and
                (s.l is not None and s.l.color is RED)):
                    assert(s)
                    s.color = RED
                    s.l.color = BLACK
                    self._right_rotate(s)
            elif (n is n.parent.r and
                (s.l is None or s.l.color is BLACK) and
                (s.r is not None and s.r.color is RED)):
                    assert(s)
                    s.color = RED
                    s.r.color = BLACK
                    self._left_rotate(s)
        self._delete_case6(n)
    def _delete_case6(self, n):
        s = n.sibling

        assert(s)
        s.color = n.parent.color
        n.parent.color = BLACK

        if n is n.parent.l:
            s.r.color = BLACK
            self._left_rotate(n.parent)
        else:
            s.l.color = BLACK
            self._right_rotate(n.parent)







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
            self._root.color = BLACK

        # Link P as new parent of R.l
        P.r = B;
        if B:
            B.parent = P

    # Rotation
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
            self._root.color = BLACK

        # Link P as new parent of L.r
        P.l = B
        if B:
            B.parent = P

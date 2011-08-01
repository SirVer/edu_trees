#!/usr/bin/env python
# encoding: utf-8

import unittest
from nose.tools import *

import os, sys
sys.path.append(os.path.dirname(__file__) + os.path.sep + '..')

from bin_search_tree import BinarySearchTree
from avl_tree import AVLTree
from red_black_tree import RedBlackTree

import random

class _BaseForBinarySearchTree(object):
    def test_sorting(self):
        vals = range(10000)
        random.shuffle(vals)

        for v in vals: self.t.insert(v)

        assert_equal(sorted(vals), list(self.t))

    def test_deleting(self):
        maxn = 10000
        vals = range(maxn)
        random.shuffle(vals)
        delete_vals = [ random.randint(0,maxn-1) for i in range(maxn // 3) ]

        for v in vals: self.t.insert(v)

        for v in delete_vals:
            self.t.delete(v)

        assert_equal(sorted(set(vals) - set(delete_vals)), list(self.t))

class TestBinarySearchTree(_BaseForBinarySearchTree, unittest.TestCase):
    def setUp(self):
        self.t = BinarySearchTree()

class TestAVLTree(_BaseForBinarySearchTree, unittest.TestCase):
    def setUp(self):
        self.t = AVLTree()

class TestRedBlackTree(_BaseForBinarySearchTree, unittest.TestCase):
    def setUp(self):
        self.t = RedBlackTree()

if __name__ == '__main__':
   unittest.main()
   # k = TestBinarySearchTree()
   # unittest.TextTestRunner().run(k)


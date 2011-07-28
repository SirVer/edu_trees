#!/usr/bin/env python
# encoding: utf-8

import unittest
from nose.tools import *

import os, sys
sys.path.append(os.path.dirname(__file__) + os.path.sep + '..')

from bin_search_tree import BinarySearchTree
import random

class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.t = BinarySearchTree()

    def test_sorting(self):
        vals = range(100)
        random.shuffle(vals)

        for v in vals: self.t.insert(v)

        assert_equal(sorted(vals), list(self.t))

    def test_deleting(self):
        maxn = 1000
        vals = range(maxn)
        random.shuffle(vals)

        for v in vals: self.t.insert(v)

        for v in range(0,maxn,2):
            self.t.delete(v)

        assert_equal(range(1,maxn,2), list(self.t))

if __name__ == '__main__':
   unittest.main()
   # k = TestBinarySearchTree()
   # unittest.TextTestRunner().run(k)


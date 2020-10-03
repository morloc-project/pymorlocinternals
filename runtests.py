#!/usr/bin/env python3

from pymorlocinternals.main import (mlc_serialize, mlc_deserialize) 
from pymorlocinternals.types import *
import unittest

class TestAll(unittest.TestCase):
    def test_primitives(self):
        self.assertEqual(mlc_serialize(42, mlc_int), "42")
        self.assertEqual(mlc_serialize(-42, mlc_int), "-42")
        self.assertEqual(mlc_serialize(-42, mlc_float), "-42")

if __name__ == "__main__":
    unittest.main()

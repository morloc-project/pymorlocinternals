#!/usr/bin/env python3

from pymorlocinternals.main import mlc_serialize, mlc_deserialize
from pymorlocinternals.types import *
import unittest

# FIXME: For now tests will only cover serialization of correctly typed data.
# The reason is that the json library I use for all deserialization does not
# consider my morloc types. Eventually I will replace it with a solution
# written in custom C++ with full type checking (like in the rmorlocinternals
# package for R).

class PersonObj:
  def __init__(self, name, age):
    self.name = name 
    self.age = age 

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class TestAll(unittest.TestCase):
    def test_int(self):
        self.assertEqual(mlc_serialize(42, mlc_int), "42")
        self.assertEqual(mlc_serialize(0, mlc_int), "0")
        self.assertEqual(mlc_serialize(-42, mlc_int), "-42")
        self.assertEqual(mlc_deserialize("-42", mlc_int), -42)
        self.assertEqual(mlc_deserialize("0", mlc_int), 0)
        self.assertEqual(mlc_deserialize("42", mlc_int), 42)

    def test_float(self):
        self.assertEqual(mlc_serialize(4.2, mlc_float), "4.2")
        self.assertEqual(mlc_serialize(0, mlc_float), "0")
        self.assertEqual(mlc_serialize(-4.2, mlc_float), "-4.2")
        self.assertEqual(mlc_deserialize("-4.2", mlc_float), -4.2)
        self.assertEqual(mlc_deserialize("0", mlc_float), 0)
        self.assertEqual(mlc_deserialize("4.2", mlc_float), 4.2)

    def test_string(self):
        # serialization
        self.assertEqual(mlc_serialize("", mlc_str), '""')
        self.assertEqual(mlc_serialize("42", mlc_str), '"42"')
        self.assertEqual(mlc_serialize("true", mlc_str), '"true"')
        self.assertEqual(mlc_serialize("yolo", mlc_str), '"yolo"')
        self.assertEqual(
            mlc_serialize("""bad"'strin{g}""", mlc_str), '''"bad\\"'strin{g}"'''
        )
        # deserialization
        self.assertEqual(mlc_deserialize('""', mlc_str), "")
        self.assertEqual(mlc_deserialize('"42"', mlc_str), "42")
        self.assertEqual(mlc_deserialize('"true"', mlc_str), "true")
        self.assertEqual(mlc_deserialize('"yolo"', mlc_str), "yolo")
        self.assertEqual(
            mlc_deserialize('''"bad\\"'strin{g}"''', mlc_str), """bad"'strin{g}"""
        )

    def test_bool(self):
        self.assertEqual(mlc_serialize(True, mlc_bool), "true")
        self.assertEqual(mlc_serialize(False, mlc_bool), "false")
        self.assertEqual(mlc_deserialize("true", mlc_bool), True)
        self.assertEqual(mlc_deserialize("false", mlc_bool), False)

    def test_list(self):
        # serialization
        self.assertEqual(mlc_serialize([1, 2, 3], mlc_list(mlc_int)), "[1,2,3]")
        self.assertEqual(
            mlc_serialize(["1", "2", "3"], mlc_list(mlc_str)), '["1","2","3"]'
        )
        self.assertEqual(
            mlc_serialize([[1, 2], [2, 3], [3, 4]], mlc_list(mlc_list(mlc_int))),
            "[[1,2],[2,3],[3,4]]",
        )
        # deserialization
        self.assertEqual(mlc_deserialize('[1, 2, 3]', mlc_list(mlc_int)), [1,2,3])
        self.assertEqual(
            mlc_deserialize('["1", "2", "3"]', mlc_list(mlc_str)), ["1","2","3"]
        )
        self.assertEqual(
            mlc_deserialize('[[1, 2], [2, 3], [3, 4]]', mlc_list(mlc_list(mlc_int))),
            [[1,2],[2,3],[3,4]],
        )

    def test_tuple(self):
        # serialization
        self.assertEqual(mlc_serialize((1, 2, "3"), mlc_tuple(mlc_int,mlc_int,mlc_str)), '[1,2,"3"]')
        self.assertEqual(
            mlc_serialize(([1, 2], "foo"), mlc_tuple(mlc_list(mlc_int), mlc_str)),
            '[[1,2],"foo"]',
        )
        # deserialization
        self.assertEqual(mlc_deserialize('[1,2,"3"]', mlc_tuple(mlc_int,mlc_int,mlc_str)), (1, 2, "3"))
        self.assertEqual(
            mlc_deserialize('[[1,2],"foo"]', mlc_tuple(mlc_list(mlc_int), mlc_str)),
            ([1, 2], "foo"),
        )

    def test_object(self):
        person = PersonObj(name="Alice", age=4)

        # serialization
        self.assertEqual(
            mlc_serialize(person, schema=mlc_object(PersonObj, name=mlc_str, age=mlc_int)),
            '{"name":"Alice","age":4}',
        )
        # deserialization
        self.assertEqual(
            mlc_deserialize('{"name":"Alice","age":4}', mlc_object(PersonObj, name=mlc_str, age=mlc_int)),
            person
        )

if __name__ == "__main__":
    unittest.main()

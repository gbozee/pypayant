from collections import OrderedDict
import unittest
from unittest import TestCase
import json
try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

# class GraphqlQueryTestCase(TestCase):
#     def test_simple_api(self):
#         api = GraphQLClient("http://localhost:3000",)
#         api.query({"query"})
def convert(val, remove_inner=False):
    # new_val = OrderedDict(val)
    new_val = val
    new_string = json.dumps(new_val).replace('\\', '')
    for x in new_val.keys():
        new_string = new_string.replace(json.dumps(x), x)
    if remove_inner:
        return new_string.replace('\\','')
    return new_string

def convert_list(val):
    result = {}
    for key, value in val.items():
        if type(value) == list:
            result.update({key:[convert(v, True) for v in value]})
        elif type(value) == dict:
            result.update({key:convert(value)})
        else:
            result.update({key: json.dumps(value)})
    return convert(result).replace('["',"[").replace('"]',"]").replace('"{', '{').replace('}"',"}")

class Testing(TestCase):
    def test_is_valid1(self):
        self.assertEqual(convert_list(dict(name="shola")),'{name: "shola"}')

    def test_is_valid2(self):
        self.assertEqual(convert_list({'name':"dotun","age":33}),'{name: "dotun", age: 33}')

    def test_is_valid3(self):
        self.assertEqual(convert_list({
            'item':[{
                'name': 'Biola',
                'age': 23
            }]
        }), '{item: [{age: 23, name: "Biola"}]}')

    def test_is_valid4(self):
        self.assertEqual(convert_list({
            'item':{
                'name': 'holla'
            }
        }),'{item: {name: "holla"}}')

    def test_is_valid5(self):
        self.assertEqual(convert_list({
            'item':{
                'name':'holla'
            },
            'list':[{
                'name':'hallo'
            },],
            "name":"jolly"
        }),'{item: {name: "holla"}, list: [{name: "hallo"}], name: "jolly"}')
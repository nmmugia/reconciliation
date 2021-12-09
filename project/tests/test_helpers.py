# tests/helpers.py
import unittest
import io

from project.server.main.helpers import CompareTwoDict, ConvertCSVtoDict, wrapper, SuggestPossibilities
from werkzeug import FileStorage
from base import BaseTestCase

class TestHelpers(BaseTestCase):
    def test_compare_two_dict(self):
        """
        Test CompareTwoDict function
        """
        d1 = {"1": {"TransactionID": 1, "TransactionAmount": 5000}}
        d2 = {"1": {"TransactionID": 1, "TransactionAmount": 5000}}
        self.assertEqual(CompareTwoDict(d1, d2), {'matches': [],'matching_records': 1,'total_records': 1,'unmatched_data': {},'unmatched_records': 0})
    
    def test_convert_csv_to_dict(self):
        """
        Test ConvertCSVtoDict function
        """
        csv_file = FileStorage(filename='test.csv', content_type='text/csv', stream=io.BytesIO(b"""TransactionID,TransactionAmount\n1,100"""))
        self.assertEqual(ConvertCSVtoDict(csv_file), {'1_100': {'TransactionID': '1', 'TransactionAmount': '100', 'total_exist': 1}, 'duplicate_data': 0,'header': ['TransactionID', 'TransactionAmount'],'total_data': 1})

    def test_suggest_possibilities(self):
        """
        Test SuggestPossibilities function
        """
        dict1 = {'matches': [],'matching_records': 1,'total_records': 1,'unmatched_data': {"1": {"TransactionID": 1, "TransactionAmount": 500}},'unmatched_records': 1}
        dict2 = {'matches': [],'matching_records': 1,'total_records': 1,'unmatched_data': {"1": {"TransactionID": 1, "TransactionAmount": 600}},'unmatched_records': 1}
        self.assertEqual(SuggestPossibilities(dict1, dict2, ["TransactionID", "TransactionAmount"]), ({'matches': [], 'matching_records': 1, 'total_records': 1, 'unmatched_data': {'1': {'TransactionID': 1, 'TransactionAmount': 500, 'points': 0}}, 'unmatched_records': 1}, {'matches': [], 'matching_records': 1, 'total_records': 1, 'unmatched_data': {'1': {'TransactionID': 1, 'TransactionAmount': 600, 'points': 0}}, 'unmatched_records': 1}))

if __name__ == "__main__":
    unittest.main()

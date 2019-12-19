#! /usr/bin/env python3
import unittest
import builtins
import os
import logging
import requests
from mock import patch, mock_open, call, MagicMock
from reporting.report import who_in_space, csv_reporting

TEST_OBJ1 = {"people":[{"name": "Tom", "age": 10}, {"name": "Tom", "age": 14}]}

TEST_OBJ2 = {"people": [{"name": "Christina Koch", "craft": "ISS"}, {"name": "Alexander Skvortsov", "craft": "ISS"}]}

class TestInventoryTracker(unittest.TestCase):
    """
    unittest for report.py file.
    """

    @patch('reporting.report.csv_reporting')
    @patch('requests.get')
    def test_who_in_space(self,mock_get,mock_csv_report):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = TEST_OBJ1
        who_in_space('http://api.open-notify.org/astros.json')

        mock_get.assert_called_once_with('http://api.open-notify.org/astros.json')

    @patch('reporting.report.csv_reporting')
    @patch('requests.get')
    def test_who_in_space_invalid(self,mock_get, mock_csv_report):
        mock_get.return_value.status_code = 400
        with self.assertRaises(Exception):
            who_in_space('http://api.open-notify.org/astros.json')
        mock_csv_report.return_value = None
        mock_get.assert_called_once_with('http://api.open-notify.org/astros.json')

    def test_who_in_space_invalid2(self):
        with self.assertRaises(Exception):
            who_in_space('abc')

    def test_csv_reporting_empty(self):
        output = csv_reporting([])
        self.assertEqual(output,None)

    def test_csv_reporting_keyerror(self):
        with self.assertRaises(KeyError):
            csv_reporting(['abc'])


    @patch("logging.error")
    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_csv_reporting_wrong_data(self,mock_writer,mock_file, mock_logging):
        with self.assertRaises(TypeError):
             csv_reporting({"people":[1,2,3]})
             mock_file.assert_called_once_with('report.csv','w')
             mock_logging.assert_called_once_with("Expected a dictionary, got a {}".format(type(item)))


    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_csv_write_out(self, mock_writer,mock_file):
        csv_reporting(TEST_OBJ2)
        mock_file.assert_called_once_with('report.csv','w')
        mock_writer.return_value.writerow.call_count = 3
        #mock_writer.return_value.writerow.assert_has_calls([call(TEST_OBJ2["people"][0].keys()),call(TEST_OBJ2["people"][0].values()),call(TEST_OBJ2["people"][1].values())])


if __name__ == '__main__':
    unittest.main()

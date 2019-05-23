import os
from unittest import TestCase
from ..phone_autocomplete import install_db, phone_autocomplete


def _gen_phones():
    phones = ['380973456789', '380971234567', '380633456789', '380971234567']
    for phone in phones:
        yield phone


class TestAutocomplete(TestCase):
    def setUp(self):
        self.DB_NAME = 'test_users.db'
        install_db(_gen_phones, self.DB_NAME)

    def tearDown(self):
        os.remove(self.DB_NAME)

    def test_two_phones(self):
        expected = ['380971234567', '380971234567']
        res = phone_autocomplete('380971234567', self.DB_NAME)
        self.assertEqual(expected, res)

    def test_all_phones(self):
        expected = 4
        res = len(phone_autocomplete('380', self.DB_NAME))
        self.assertEqual(expected, res)

    def test_operator_63(self):
        expected = ['380633456789']
        res = phone_autocomplete('38063', self.DB_NAME)
        self.assertEqual(expected, res)

    def test_len_number(self):
        expected = []
        res = phone_autocomplete('3809712345671', self.DB_NAME)
        self.assertEqual(expected, res)

    def test_string(self):
        expected = []
        res = phone_autocomplete('38097samsung', self.DB_NAME)
        self.assertEqual(expected, res)

    def test_symbol(self):
        expected = []
        res = phone_autocomplete('38O97', self.DB_NAME)
        self.assertEqual(expected, res)

    def test_country_code(self):
        expected = []
        res = phone_autocomplete('20', self.DB_NAME)
        self.assertEqual(expected, res)
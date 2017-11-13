import unittest
import tempfile
from unittest import TestCase
import process
import os

import app

class FacedateTestCase(TestCase):
    def setUp(self):
        app.testing = True
        self.db = app.db
        self.client = app.app.test_client()

    def testShouldBeAbleToVisitHomePage(self):
        rv = self.visitHomePage()
        assert b'Get started' in rv.data


    def visitHomePage(self):
        return self.client.get('/', follow_redirects = False)

if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python
# TimeStamperTest.py -- Unit Tests for TimeStamper
#
# Copyright (C) 2013 Juha Autero <jautero@iki.fi>
#

import unittest
import TimeStamper

class TimeStamperUnitTest(unittest.TestCase):
    """TimeStamper unit tests"""
    def test_create(self):
        teststamper=TimeStamper.Stamper()

if __name__ == '__main__':
    unittest.main()
        
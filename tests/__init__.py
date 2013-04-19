# -*- coding: utf-8 -*-
"""
    __init__

    Description goes here...

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest

from .test_international import TestInternationalShipping
from .test_api import TestAPI


def suite():
    '''
    Test Suite
    '''
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    )
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(
            TestInternationalShipping
        )
    )
    return suite

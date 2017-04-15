# coding=utf-8
"""
malpy.__main__ Tets
"""
from __future__ import print_function

from nose.tools import assert_equal

from malpy.__main__ import call, main


class TestMalPy(object):
    """Tests the main call method and argument/options parser.

    """
    def test_bad_arg(self):
        assert_equal(127, main(argv='malpy -r'.split()))

    def test_help(self):
        assert_equal(0, main(argv='malpy -h'.split()))

    def test_call(self):
        assert_equal(0, call(None, ['basic.mal']))

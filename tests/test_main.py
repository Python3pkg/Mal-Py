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
    def test_no_arg(self):
        assert_equal(127, main())

    def test_bad_arg(self):
        assert_equal(127, main(argv='malpy -r'.split()))

    def test_help(self):
        assert_equal(0, main(argv='malpy -h'.split()))

    def test_call(self):
        assert_equal(0, call(None, ['basic.mal']))

    def test_call_err(self):
        assert_equal(0, call(None, ['error.mal']))

    def test_call_m(self):
        assert_equal(0, call([("-m", "")], ['basic.mal']))
        assert_equal(0, call([("-m",
                               " ".join(map(str, range(64))))],
                             ['basic.mal']))
        assert_equal(0, call([("-m",
                               " ".join(map(str, range(10))))],
                             ['basic.mal']))
        assert_equal(1, call([("-m", "test_bad_literal")],
                             ['basic.mal']))

    def test_call_memory(self):
        assert_equal(0, call([("--memory", "")], ['basic.mal']))
        assert_equal(0, call([("--memory",
                               " ".join(map(str, range(64))))],
                             ['basic.mal']))
        assert_equal(0, call([("--memory",
                               " ".join(map(str, range(10))))],
                             ['basic.mal']))
        assert_equal(1, call([("--memory", "test_bad_literal")],
                             ['basic.mal']))

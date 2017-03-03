# coding=utf-8
"""
malpy.actionrunner.ActionRunner Tests
"""
from __future__ import print_function
from nose.tools import assert_equal

import malpy.actionrunner
import malpy.parser

PARSER = malpy.parser.Parser()
RUNNER = malpy.actionrunner.ActionRunner(dict([]))


class TestMalActionRunner(object):
    """
    Tests the action runner class for consistency in the public facing API.
    """
    def setup(self):
        """
        Resets the memory, registers and program counter before each test.
        :return: None
        """
        RUNNER.reset()

    def test_reset(self):
        """
        validate reset works properly.
        :return: None
        """
        test_program = PARSER.parse("MOVEI V63, R0\nEND\n")
        RUNNER.run(test_program, [0 for _ in range(64)])
        assert_equal(RUNNER.registers[0], 63)
        RUNNER.reset()
        assert_equal(RUNNER.registers[0], 0)

    def test_run(self):
        """
        validate runner works proper with no JIT actions
        :return: None 
        """

        instrs = PARSER.parse(
                "MOVEI V63, R0\n"
                "LOAD R1, R0\n"
                "STORE R1, R0\n"
                "MOVE R1, R0\n"
                "ADD R2, R1, R0\n"
                "INC R2\n"
                "SUB R2, R1, R0\n"
                "DEC R2\n"
                "MUL R2, R1, R0\n"
                "DIV R2, R1, R0\n"
                "BLT R2, R1, L13\n"
                "BGT R2, R1, L13\n"
                "BEQ R2, R1, L13\n"
                "BR L3\n"
                "END\n "
        )
        mem = RUNNER.run(instrs, [0 for _ in range(64)])
        assert_equal(len(mem), 64)
        assert_equal(mem, [0 for _ in range(64)])
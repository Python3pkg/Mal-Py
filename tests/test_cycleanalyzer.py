# coding=utf-8
"""
malpy.cycleanalyzer.CycleAnalyzer Tests
"""


from nose.tools import assert_equal

import malpy.cycleanalyzer
import malpy.parser

PARSER = malpy.parser.Parser()
RUNNER = malpy.cycleanalyzer.CycleAnalyzer()


class TestMalCycleAnalyzer(object):
    """Tests the parser class for consistency in the public facing API.

    """
    def test_reset(self):
        """validate reset works properly.

            Returns: None

        """
        test_program = PARSER.parse("MOVEI V63, R0\nEND\n")
        RUNNER.run(test_program, [0] * 64)
        assert_equal(RUNNER.registers[0], 63)
        RUNNER.reset()
        assert_equal(RUNNER.registers[0], 0)
        valc = 0
        for i in range(80):
            valc ^= RUNNER.state_table[64*i]
        assert_equal(RUNNER.curr_state, valc)
        assert_equal(RUNNER.states, dict([]))

    def test_run(self):
        """validate runner works proper with Cycle checking JIT actions

            Returns: None

        """
        loop_instr = PARSER.parse("BR L1\nBR L0\nEND\n")
        mem = RUNNER.run(loop_instr, [0]*64)
        assert_equal(len(mem), 4)

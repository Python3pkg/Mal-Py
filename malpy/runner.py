# coding=utf-8
"""
Mal Runtime environment.
"""
import collections

import malpy.parser

Flags = collections.namedtuple('Flags', ('halt',
                                         'div_by_zero',
                                         'out_of_bounds',
                                         'bad_operand'))


class Runner:
    """
    This is a runtime environment.
    It sets memory on instantiation and zeros the registers.
    """
    def __init__(self):
        self.memory = None
        self.flags = Flags(False, False, False, False)
        self.registers = [0 for _ in range(16)]
        self.program_counter = 0
        self.evaluate = {
            'MOVE': self._move,
            'MOVEI': self._movei,
            'LOAD': self._load,
            'STORE': self._store,
            'ADD': self._add,
            'INC': self._inc,
            'SUB': self._sub,
            'DEC': self._dec,
            'MUL': self._mul,
            'DIV': self._div,
            'BEQ': self._beq,
            'BLT': self._blt,
            'BGT': self._bgt,
            'BR': self._br,
            'END': self._end
        }

    def run(self, program, memory):
        """
        Runs an instruction set on a loaded memory and cleared register
        :param program: Either the instruction list or text.
                        It will be parsed if it is text.
        :param memory: The memory contents on which to run the program.
        :return: Memory contents
        """
        inst = []
        self.memory = memory
        if isinstance(program, str):
            p = malpy.parser.Parser()
            inst = p.parse(program)
        elif isinstance(program, list):
            inst = program

        while not any([self.flags.halt, self.flags.div_by_zero,
                       self.flags.out_of_bounds, self.flags.bad_operand]):
            if self.program_counter > len(inst):
                self.flags.out_of_bounds = True
            else:
                opcode, operands = inst[self.program_counter]
                self.evaluate[opcode](operands)
                self.program_counter += 1

        self.registers = [0 for _ in range(16)]
        if not any([self.flags.div_by_zero,
                    self.flags.out_of_bounds,
                    self.flags.bad_operand]):
            return self.memory
        else:
            return [self.flags.div_by_zero,
                    self.flags.out_of_bounds,
                    self.flags.bad_operand]

    def _move(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R'):
            self.registers[int(ops[1][1:], 16)] = \
                self.registers[int(ops[0][1:], 16)]
        else:
            self.flags.bad_operand = True

    def _movei(self, ops):
        if ops[0].startswith('V') and ops[1].startswith('R'):
            self.registers[int(ops[1][1:], 16)] = int(ops[0][1:])
        else:
            self.flags.bad_operand = True

    def _load(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R'):
            self.registers[int(ops[1][1:], 16)] = \
                self.memory[self.registers[int(ops[0][1:], 16)]]
        else:
            self.flags.bad_operand = True

    def _store(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R'):
            self.memory[self.registers[int(ops[1][1:], 16)]] = \
                self.registers[int(ops[0][1:], 16)]
        else:
            self.flags.bad_operand = True

    def _add(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('R'):
            self.registers[int(ops[2][1:], 16)] = \
                self.registers[int(ops[0][1:], 16)] + \
                self.registers[int(ops[1][1:], 16)]
        else:
            self.flags.bad_operand = True

    def _inc(self, ops):
        if ops[0].startswith('R'):
            self.registers[int(ops[0][1:], 16)] += 1
        else:
            self.flags.bad_operand = True

    def _sub(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('R'):
            self.registers[int(ops[2][1:], 16)] = \
                self.registers[int(ops[0][1:], 16)] - \
                self.registers[int(ops[1][1:], 16)]
        else:
            self.flags.bad_operand = True

    def _dec(self, ops):
        if ops[0].startswith('R'):
            self.registers[int(ops[0][1:], 16)] -= 1
        else:
            self.flags.bad_operand = True

    def _mul(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('R'):
            self.registers[int(ops[2][1:], 16)] = \
                self.registers[int(ops[0][1:], 16)] * \
                self.registers[int(ops[1][1:], 16)]
        else:
            self.flags.bad_operand = True

    def _div(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('R'):
            self.registers[int(ops[2][1:], 16)] = \
                int(self.registers[int(ops[0][1:], 16)] //
                    self.registers[int(ops[1][1:], 16)])
        else:
            self.flags.bad_operand = True

    def _bgt(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('L'):
            if self.registers[int(ops[0][1:], 16)] > \
              self.registers[int(ops[1][1:], 16)]:
                self.program_counter = int(ops[2][1:])
        else:
            self.flags.bad_operand = True

    def _blt(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('L'):
            if self.registers[int(ops[0][1:], 16)] < \
              self.registers[int(ops[1][1:], 16)]:
                self.program_counter = int(ops[2][1:]) - 1
        else:
            self.flags.bad_operand = True

    def _beq(self, ops):
        if ops[0].startswith('R') and ops[1].startswith('R') and \
                ops[2].startswith('L'):
            if self.registers[int(ops[0][1:], 16)] == \
              self.registers[int(ops[1][1:], 16)]:
                self.program_counter = int(ops[2][1:]) - 1
        else:
            self.flags.bad_operand = True

    def _br(self, ops):
        if ops[0].startswith('L'):
            self.program_counter = int(ops[0][1:]) - 1
        else:
            self.flags.bad_operand = True

    def _end(self, _):
        self.flags.halt = True

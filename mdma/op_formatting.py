from __future__ import annotations
import os
import json
from enum import Enum
from typing import NamedTuple, Dict, List


class OpFormat(NamedTuple):
    """A representation of an operation's formatting, including format (one of R, I, or J), data segment names/sizes,
    and the order the fields are in the human-readable/human entered instruction

    :param format_type_char: Character representing the format type. Either R, I, or J
    :param fields: A mapping of the format's fields to the number of bits it uses
    :param syntax: the fields in the order they appear in the human-readable instruction string
    """

    format_type_char: str
    fields: Dict[str, int]
    syntax: List[str]

    @staticmethod
    def from_32bit_binary_string(binary_string: str) -> OpFormat:
        """Parses the 'op' bits and 'func' bits of a 32-bit binary string and uses them to parse the operation format.

        :param binary_string: the binary string to be parsed.
        :returns: The (pre-defined) OpFormat
        """
        op_bits = binary_string[:6]
        func_bits = binary_string[26:]
        return OpFormat.from_op_and_func(op_bits, func_bits)

    @staticmethod
    def from_instruction_str(instr_str: str) -> OpFormat:
        """Determines the values of the 'op' and 'func' bits of the given instruction and uses them to
        parse the operation format.

        :param instr_str: the human-readable instruction string to be parsed
        :returns: The (pre-defined) OpFormat
        """
        if instr_str in codes['op'].values():
            op_bits = next((bin_str for bin_str, op_name in codes['op'].items() if op_name == instr_str))
            func_bits = None
        else:  # This is a special operation with a func code
            op_bits = '000000'
            func_bits = next((bin_str for bin_str, func_name in codes['func'].items() if func_name == instr_str), None)
        return OpFormat.from_op_and_func(op_bits=op_bits, func_bits=func_bits)

    @staticmethod
    def from_op_and_func(op_bits: str, func_bits: str = None) -> OpFormat:
        """Parses the operation format of a 32-bit binary string based off of the 6 operation digits
        (and/or the 6 function digits) in a 32-bit binary machine code string.

        :param op_bits: the 6 bits defining the instruction's operation
        :param func_bits: the 6 bits defining the instruction's function, if needed
        :returns: The (pre-defined) OpFormat
        """
        if op_bits == '000000':
            if not func_bits:
                raise Exception(f'Op bits (000000) indicate this is a special R-type operation'
                                f'but function bits were not provided')
            if func_bits in ["000000", "000100", "000011", "000111", "000010", "000110"]:  # A shifting operation
                return s_format
            else:
                return r_format
        elif op_bits in ['000010', '000011']:
            return j_format
        else:  # Anything not specified is assumed to be an I format operation
            return i_format


# Represents R format operations
r_format = OpFormat(
    format_type_char="R",
    fields={'op': 6, 'rs': 5, 'rt': 5, 'rd': 5,'shamt': 5,'func':6},
    syntax=["func", "rd", "rs", "rt"]
)

# Represents I format operations
i_format = OpFormat(
    format_type_char="I",
    fields={'op': 6, 'rs': 5, 'rt': 5, 'immediate': 16},
    syntax=["op", "rt", "rs", "immediate"]
)

# Represents J format operations
j_format = OpFormat(
    format_type_char="J",
    fields={'op': 6, 'target': 26},
    syntax=["op", "target"]
)

# Represent shift operations - similar to R format, but syntax is slightly different
s_format = OpFormat(
    format_type_char="R",
    fields={'op': 6, 'rs': 5, 'rt': 5, 'rd': 5,'shamt': 5,'func':6},
    syntax=["func", "rs", "rt", "shamt"]
)

_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'func_and_opcodes.json')
with open(_path, 'r') as yf:
    codes = json.load(yf)


class Registers(Enum):
    """An enum representing the different register names/numbers in MIPS"""

    zero = 0
    at = 1
    v0 = 2
    v1 = 3 
    a0 = 4
    a1 = 5
    a2 = 6
    a3 = 7
    t0 = 8
    t1 = 9
    t2 = 10
    t3 = 11
    t4 = 12
    t5 = 13
    t6 = 14
    t7 = 15
    s0 = 16
    s1 = 17
    s2 = 18
    s3 = 19
    s4 = 20
    s5 = 21
    s6 = 22
    s7 = 23
    t8 = 24
    t9 = 25
    gp = 28
    sp = 29
    fp = 30
    ra = 31

    def __str__(self) -> str:
        return '$' + self.name

    @staticmethod
    def register_num(register_name: str) -> int:
        """Parses the operation format of a 32-bit binary string based off of the 6 operation digits
        (and/or the 6 function digits) in a 32-bit binary machine code string.

        :param register_name: the human-readable name of the register. Both $[register name] and $[register number]
                are acceptable
        :returns: The register number corresponding to the register name given
        """
        if register_name.startswith('$'):
            register_name = register_name[1:]
        if register_name.isdigit():  # Register name with number e.g. $4 which is a0
            return Registers(int(register_name)).value
        else:
            return Registers[register_name].value

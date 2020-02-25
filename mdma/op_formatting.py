import os
import json
from enum import Enum
from typing import NamedTuple, Dict, List


class OpFormat(NamedTuple):
    format: str
    fields: Dict[str, int]
    syntax: List[str]

    @staticmethod
    def from_binary_string(binary_string):
        op_digits = binary_string[:6]
        if op_digits in ['000000']:
            func_digits = binary_string[26:]
            if func_digits in ["000000", "000100", "000011", "000111", "000010", "000110"]:  # A shifting operation
                return _s_format
            else:
                return _r_format
        elif op_digits in ['000010', '000011']:
            return _j_format
        else:  # Anything not specified is assumed to be an I format operation
            return _i_format
        

_r_format = OpFormat(format="R", 
                     fields={'op': 6, 'rs': 5, 'rt': 5, 'rd': 5,'shamt': 5,'func':6}, 
                     syntax=["func", "rd", "rs", "rt"])
_i_format = OpFormat(format="I",
                     fields={'op': 6, 'rs': 5, 'rt': 5, 'immediate': 16},
                     syntax=["op", "rt", "rs", "immediate"])
_j_format = OpFormat(format="J",
                     fields={'op': 6, 'target': 26},
                     syntax=["op", "target"])
_s_format = OpFormat(format="R",  # SHIFT FORMAT
                     fields={'op': 6, 'rs': 5, 'rt': 5, 'rd': 5,'shamt': 5,'func':6},
                     syntax=["func", "rs", "rt", "shamt"])

path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path, 'func_and_opcodes.json')
with open(path, 'r') as yf:
    codes = json.load(yf)


class Registers(Enum):
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

    def __str__(self):
        return '$' + self.name

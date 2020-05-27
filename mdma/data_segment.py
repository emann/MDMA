import math
from typing import Optional, Sized

from .op_formatting import codes, Registers


class DataSegment:
    """An object representation of a segment of data in a machine code binary string

    Parses the decimal value and either the binary string or the human-readable string, depending on input. If
    creating a data segment from a human-readable string, the number of bits contained in the segment MUST be passed
    in as well. len(DataSegment) returns the number of bits in the data segment, and str(Datasegment) returns the
    human readable representation whether it is an opcode, register number, or integer immediate.

    :param name: The name of the data segment (e.g. "op", "rs")
    :param bin_str: A string of the data segment's bits.
    :param num_bits: The number of bits in the data segment
    :param decimal: The decimal representation of the binary string. Converted from two's complement when needed
    :param human_readable: A human readable representation of the data
    """

    def __init__(self, name: str, bin_str: Optional[str] = None, instr_str: Optional[str] = None, num_bits: Optional[int] = None):
        self.name = name
        self.bin_str = bin_str
        self.instr_str = instr_str
        if self.instr_str:
            if not num_bits:  # Number of bits was not specified
                raise ValueError("Instruction string given but number of bits was not specified")
        elif self.bin_str:  # The binary string was given
            num_bits = len(self.bin_str)
        else:
            raise ValueError("Neither binary string nor instruction string were specified")
        self.num_bits: int = num_bits
        self._parse()

    def __len__(self) -> int:
        return self.num_bits

    def __str__(self) -> str:
        return self.human_readable

    def _parse(self):
        if self.bin_str:
            self.decimal = self._parse_decimal()
            self.human_readable = self._parse_human_readable()
        else:
            self.human_readable = self.instr_str
            self.bin_str = self._parse_bin_str()
            self.decimal = self._parse_decimal()

    def _parse_decimal(self) -> int:
        """Parses the data segment's decimal value, determining if it needs to be converted from two's complement form.

        :returns: The decimal value of this data segment
        """
        if self.bin_str is None:
            raise ValueError("Can't parse decimal value from None-valued binary string")
        if self.name in ['offset', 'immediate']:
            return _int_from_twos_comp(self.bin_str)
        else:
            return int(self.bin_str, 2)

    def _parse_human_readable(self) -> str:
        """Parses the data into its human readable form.

        :returns: The human-readable representation of the data.
        """
        if self.name in ['op', 'func']:
            return codes[self.name][self.bin_str]
        elif self.name in ['rs', 'rt', 'rd', 'src1', 'src2']:
            return str(Registers(self.decimal))
        elif self.name == 'target':  # Upper four of program counter are assumed to be 0000
            return '0x' + hex(int(f'0000{self.bin_str}00', 2))[2:].zfill(8)
        else:
            return str(self.decimal)

    def _parse_bin_str(self) -> str:
        """Parses the binary string representation of a human-readable instruction string

        :returns: The encoded binary string representing the instruction string provided.
        """
        if self.instr_str is None:
            raise ValueError("Can't parse binary string from None-value instruction string")
        if self.name in ['op', 'func']:
            bin_str = next((bin_str for bin_str, op_name in codes[self.name].items() if op_name == self.instr_str), None)
            if bin_str is None:
                raise Exception(f'UNKNOWN OPERATION: {self.instr_str}')
            return bin_str
        elif self.instr_str.startswith('$'):
            return bin(Registers.register_num(self.instr_str))[2:].zfill(5)
        elif self.name == 'target':
            # First four come from PC (usually 0000) and last two are 00
            return bin(int(self.instr_str, 16))[2:].zfill(32)[4:30]
        else:  # Assumed to be an immediate/offset value
            return _twos_comp_from_int(int(self.instr_str), self.num_bits)


def _int_from_twos_comp(twos_comp_binary_str: str) -> int:
    """Converts a binary string in two's complement format into its decimal value.

    :param twos_comp_binary_str: the binary string (in two's compliment form) to be converted
    :returns: The (converted) decimal representation of the input string
    """
    bits = len(twos_comp_binary_str)
    bin_str = int(twos_comp_binary_str, 2)
    if (bin_str & (1 << (bits - 1))) != 0:  # if sign bit is set
        bin_str = bin_str - (1 << bits)  # compute negative value
    return bin_str


def _twos_comp_from_int(val: int, num_bits: int) -> str:
    """Converts an integer value into a binary string in two's complement format.

    :param val: The integer value to be converted
    :param num_bits: The number of bits available to store the value in
    :returns: The binary string in two's complement format representing the input value
    """
    if val != 0 and num_bits < math.ceil(math.log(abs(val), 2)):
        raise ValueError(f'Value ({val}) too large to fit in {num_bits} bits')
    val_is_negative = val < 0
    sign_bit: str = str(int(val_is_negative))
    if val_is_negative:
        val += (1 << num_bits)
    bin_str = bin(val)[2:]
    sign_extend = sign_bit*(num_bits - len(bin_str))
    bin_str = sign_extend + bin_str
    return bin_str
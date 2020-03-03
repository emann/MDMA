import math

from .op_formatting import codes, Registers


class DataSegment:
    """An object representation of a segment of data in a machine code string

        The decimal value and human readable string are automatically generated on instantiation.
        len(DataSegment) returns the number of bits in the data segment, and str(Datasegment) returns a human readable
        representation whether it is an opcode, register number, or decimal immediate.

        Attributes:
            name (str): The name of the data segment (e.g. "op", "rs")
            bin_str (str): A string of the data segment's bits.
            num_bits (int): The number of bits in the data segment
            decimal (int): The decimal representation of the binary string. Converted from two's complement when needed
            human_readable (str): A human readable representation of the data

        """

    def __init__(self, name: str, bin_str: str = None, instr_str: str = None, num_bits: int = None):
        self.name = name
        self.bin_str = bin_str
        self.instr_str = instr_str
        self.num_bits = num_bits if num_bits else len(self.bin_str)
        self._parse()

    def __len__(self):
        return self.num_bits

    def __str__(self):
        return self.human_readable

    def _parse(self):
        if self.bin_str:
            self.decimal = self._parse_decimal()
            self.human_readable = self._parse_human_readable()
        else:
            self.human_readable = self.instr_str
            self.bin_str = self._parse_bin_str()
            self.decimal = self._parse_decimal()

    def _int_from_twos_comp(self) -> int:
        """Converts the data segment's binary string from two's complement into its decimal value.

            Returns:
                The (converted) decimal representation of the input string

            """
        bits = len(self.bin_str)
        bin_str = int(self.bin_str, 2)
        if (bin_str & (1 << (bits - 1))) != 0:  # if sign bit is set
            bin_str = bin_str - (1 << bits)  # compute negative value
        return bin_str

    def _twos_comp_from_int(self, val) -> str:
        if self.num_bits > math.ceil(math.log(val, 2)):
            raise Exception
        val
        if self.decimal < 0:
            val += (1 << self.num_bits)
        return bin(val)[2:]

    def _parse_decimal(self) -> int:
        """Parses the data segment's decimal value, determining if it needs to be converted from two's complement form.

            Returns:
                The decimal value of this data segment

            """
        if self.name in ['offset', 'immediate']:
            return self._int_from_twos_comp()
        else:
            return int(self.bin_str, 2)

    def _parse_human_readable(self) -> str:
        """Parses the data into its human readable form.

            Returns:
                The human-readable representation of the data.

            """
        if self.name in ['op', 'func']:
            return codes[self.name][self.bin_str]
        elif self.name in ['rs', 'rt', 'rd', 'src1', 'src2']:
            return str(Registers(self.decimal))
        else:
            return str(self.decimal)

    def _parse_bin_str(self) -> str:
        """Parses the binary string representation of a human-readable instruction string"""
        if self.name in ['op', 'func']:
            bin_str = next((bin_str for bin_str, op_name in codes[self.name].items() if op_name == self.instr_str), None)
            if bin_str is None:
                raise Exception
            return bin_str
        elif self.instr_str in [str(r) for r in Registers]:
            return bin(Registers.register_num(self.human_readable))[2:].zfill(5)
        else:
            return self._twos_comp_from_int(int(self.instr_str))

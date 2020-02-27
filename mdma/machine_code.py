from typing import List
from .op_formatting import OpFormat, codes, Registers


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

    def __init__(self, name: str, bin_str: str):
        self.name = name
        self.bin_str = bin_str
        self.num_bits = len(bin_str)
        self.decimal = self._parse_decimal()
        self.human_readable = self._parse_human_readable()

    def __len__(self):
        return self.num_bits

    def __str__(self):
        return self.human_readable

    def _twos_comp(self) -> int:
        """Converts the data segment's binary string from two's complement into its decimal value.

            Returns:
                The (converted) decimal representation of the input string

            """
        bits = len(self.bin_str)
        bin_str = int(self.bin_str, 2)
        if (bin_str & (1 << (bits - 1))) != 0:  # if sign bit is set
            bin_str = bin_str - (1 << bits)         # compute negative value
        return bin_str
    
    def _parse_decimal(self) -> int:
        """Parses the data segment's decimal value, determining if it needs to be converted from two's complement form.

            Returns:
                The decimal value of this data segment

            """
        if self.name in ['offset', 'immediate']:
            return self._twos_comp()
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


class MachineCode:
    """An object representation of decoded 32-bit machine code.

        The decimal value and human readable string are automatically generated on instantiation.
        len(DataSegment) returns the number of bits in the data segment, and str(Datasegment) returns a human readable
        representation whether it is an opcode, register number, or decimal immediate.

        Attributes:
            hex_str (str): The input machine code (32-bit hex string) to be decoded. 0x is automatically added and spaces are removed, if necessary.
            bin_str (str): A string containing the binary representation of the machine code.
            op_format (OpFormat): A named tuple representing the operation's formatting
            data_segments (List[DataSegment]): A list of the machine code's data segments, in their order in the binary.
            ordered_data_segments (List[DataSegment]): A list of the meaningful data segments in the order they are displayed in a human-readable string

        """

    def __init__(self, hex_str):
        self.hex_str = hex_str.replace(' ', '')
        if not self.hex_str.startswith('0x'):
            self.hex_str = '0x' + self.hex_str
        self.bin_str = bin(int(self.hex_str, 16))[2:].zfill(32)
        self.op_format: OpFormat = None
        self.data_segments: List[DataSegment] = []
        self.ordered_data_segments: List[DataSegment] = []
        self.decode()

    def __str__(self):
        return ' '.join([str(d) for d in self.ordered_data_segments])

    def decode(self) -> None:
        """Decodes the machine code"""
        self.op_format = OpFormat.from_binary_string(self.bin_str)
        start = 0
        for section_name, bits in self.op_format.fields.items():
            end = start + bits
            bin_str = self.bin_str[start:end]
            self.data_segments.append(DataSegment(section_name, bin_str))
            start = end
        critical_segments = [d for d in self.data_segments if d.name in self.op_format.syntax]
        self.ordered_data_segments = list(sorted(critical_segments, key=lambda d: self.op_format.syntax.index(d.name)))

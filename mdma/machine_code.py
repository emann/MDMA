from typing import List
from .op_formatting import OpFormat
from .data_segment import DataSegment


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

    def __init__(self, hex_str: str):
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
        self.op_format = OpFormat.from_32bit_binary_string(self.bin_str)
        start = 0
        for section_name, bits in self.op_format.fields.items():
            end = start + bits
            bin_str = self.bin_str[start:end]
            self.data_segments.append(DataSegment(section_name, bin_str))
            start = end
        critical_segments = [d for d in self.data_segments if d.name in self.op_format.syntax]
        self.ordered_data_segments = list(sorted(critical_segments, key=lambda d: self.op_format.syntax.index(d.name)))

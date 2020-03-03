from typing import List

from mdma.op_formatting import OpFormat
from mdma.data_segment import DataSegment


class MIPSInstruction:
    """An object representation of a MIPS instruction, including its human-readable string as well as encoded hex and binary.

        Only accepts keyword arguments for hex, binary, or instruction string. The other two are automatically en/decoded.

        Attributes:
            instruction_str (str): The human-readable instruction string
            hex_str (str): The hex string representation of the encoded instruction
            bin_str (str): The encoded 32-bit binary string
            op_format (OpFormat): A named tuple representing the operation's formatting
            data_segments (List[DataSegment]): A list of the machine code's data segments, in their order in the binary.
            ordered_data_segments (List[DataSegment]): A list of the meaningful data segments in the order they are displayed in a human-readable string

        """

    def __init__(self, *, hex_str: str = None, bin_str: str = None, instruction_str: str = None):
        self.instruction_str: str = instruction_str
        self.hex_str: str = hex_str
        self.bin_str: str = bin_str
        self.op_format: OpFormat = None
        self.data_segments: List[DataSegment] = []
        self.ordered_data_segments: List[DataSegment] = []
        self._decode_or_encode()

    def __str__(self):
        return self.instruction_str

    def __index__(self):
        return int(self.hex_str, 16)

    def _decode_or_encode(self):
        if self.instruction_str is not None:  # The instruction string has been given
            self._encode()
        elif self.bin_str is not None:  # the binary string has been given
            self.hex_str = hex((int(self.bin_str, 2)))
            self._decode()
        else:
            self.hex_str = self.hex_str.replace(' ', '')
            if not self.hex_str.startswith('0x'):
                self.hex_str = '0x' + self.hex_str
            self.bin_str = bin(int(self.hex_str, 16))[2:].zfill(32)
            self._decode()

    def _decode(self) -> None:
        """Decodes the machine code"""
        self.op_format = OpFormat.from_32bit_binary_string(self.bin_str)
        start = 0
        for segment_name, bits in self.op_format.fields.items():
            end = start + bits
            bin_str = self.bin_str[start:end]
            self.data_segments.append(DataSegment(segment_name, bin_str))
            start = end
        critical_segments = [d for d in self.data_segments if d.name in self.op_format.syntax]
        self.ordered_data_segments = list(sorted(critical_segments, key=lambda d: self.op_format.syntax.index(d.name)))
        self.instruction_str = ' '.join([str(d) for d in self.ordered_data_segments])

    def _encode(self):
        """Encodes the instruction string"""
        instruction_params = self.instruction_str.split()
        instruction = instruction_params[0]
        data_segments = {}
        self.op_format = OpFormat.from_instruction_str(instruction)

        # Making a dictionary of data segments using the syntax of the OpFormat and the instruction string
        for segment_name, instr_str in zip(self.op_format.syntax, instruction_params):
            num_bits = self.op_format.fields[segment_name]
            data_segments[segment_name] = DataSegment(name=segment_name, instr_str=instr_str, num_bits=num_bits)
        self.ordered_data_segments = data_segments.values()

        # Constructing the binary string from the OpFormats's fields and the data segment dictionary
        self.bin_str = ''
        for segment_name in self.op_format.fields:
            if segment_name in data_segments:
                segment_bits = data_segments[segment_name].bin_str
            else:  # segments not actually in use should just be zeroes
                segment_bits = '0'*self.op_format.fields[segment_name]
            self.data_segments.append(DataSegment(name=segment_name, bin_str=segment_bits))
            self.bin_str += segment_bits
        self.hex_str = '0x' + hex(int(self.bin_str, 2))[2:].zfill(8)  # Padding to 8 hex digits
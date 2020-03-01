from .op_formatting import OpFormat
from .data_segment import DataSegment


class MIPSInstruction:
    """An object representation of an encoded MIPS instruction string.

        The hex and binary strings are automatically encoded on instantiation.

        Attributes:
            instruction_str (str): The instruction string to be encoded
            hex_str (str): the hex string representation of the encoded instruction
            bin_str (str): the encoded 32-bit binary string
            op_format (OpFormat): A named tuple representing the operation's formatting

        """

    def __init__(self, instruction_str: str):
        self.instruction_str: str = instruction_str
        self.hex_str: str = None
        self.bin_str: str = None
        self.op_format: OpFormat = None
        self.encode()

    def encode(self):
        """Encodes the instruction string"""
        instruction_params = self.instruction_str.split()
        instruction = instruction_params[0]
        data_segments = {}
        self.op_format = OpFormat.from_instruction_str(instruction)

        # Making a dictionary of data segments using the syntax of the OpFormat and the instruction string
        for segment_name, instr_str in zip(self.op_format.syntax, instruction_params):
            num_bits = self.op_format.fields[segment_name]
            data_segments[segment_name] = DataSegment(name=segment_name, instr_str=instr_str, num_bits=num_bits)
        self.bin_str = ''

        # Constructing the binary string from the OpFormats's fields and the data segment dictionary
        for segment_name in self.op_format.fields:
            if segment_name in data_segments:
                self.bin_str += data_segments[segment_name].bin_str
            else:  # segments not actually in use should just be zeroes
                self.bin_str += '0'*self.op_format.fields[segment_name]
        self.hex_str = hex(int(self.bin_str, 2))

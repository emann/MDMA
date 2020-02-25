from typing import List
from .op_formatting import OpFormat, codes, Registers


class DataSegment:
    def __init__(self, name: str, num_bits: str, bin_str: str):
        self.name = name
        self.num_bits = num_bits
        self.bin_str = bin_str
        self.decimal = self.parse_decimal()
        self.human_readable = self.parse_human_readable()

    def __len__(self):
        return self.num_bits

    def __str__(self):
        return self.human_readable

    @staticmethod
    def _twos_comp(val):
        bits = len(val)
        val = int(val,2)
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val
    
    def parse_decimal(self):
        if self.name in ['offset', 'immediate']:
            return self._twos_comp(self.bin_str)
        else:
            return int(self.bin_str, 2)

    def parse_human_readable(self):
        if self.name in ['op', 'func']:
            return codes[self.name][self.bin_str]
        elif self.name in ['rs', 'rt', 'rd', 'src1', 'src2']:
            return str(Registers(self.decimal))
        else:
            return str(self.decimal)


class MachineCode:
    def __init__(self, hex_str):
        self.hex_str = hex_str
        if not self.hex_str.startswith('0x'):
            self.hex_str = '0x' + self.hex_str
        self.bin_str = bin(int(self.hex_str, 16))[2:].zfill(32)
        self.operation: str = None
        self.op_format: OpFormat = None
        self.data_segments: List[DataSegment] = []
        self.ordered_data_segments: List[DataSegment] = []
        self.decode()

    def __str__(self):
        return ' '.join([str(d) for d in self.ordered_data_segments])

    def __getattr__(self, attr):
        pass

    def decode(self):
        self.op_format = OpFormat.from_binary_string(self.bin_str)
        start=0
        for section_name, bits in self.op_format.fields.items():
            end = start + bits
            bin_str = self.bin_str[start:end]
            self.data_segments.append(DataSegment(section_name, bits, bin_str))
            start = end
        critical_segments = [d for d in self.data_segments if d.name in self.op_format.syntax]
        self.ordered_data_segments = list(sorted(critical_segments, key=lambda d: self.op_format.syntax.index(d.name)))

import pytest

from mdma.data_segment import DataSegment

instr_input_and_expected = [('op', 'addi', 6, '001000'),
                            ('func', 'xor', 6, '100110'),
                            ('immediate', 77, 16, '0000000001001101'),
                            ('offset', -77, 16, '1111111110110011'),
                            ('rd', '$v0', 5, '00010'),
                            ('src1', '$2', 5, '00010')]

bin_input_and_expected = [('op', '001000', 'addi'),
                          ('func', '100110', 'xor'),
                          ('immediate', '0000000001001101', 77),
                          ('offset', '1111111110110011', -77),
                          ('rd', '00010', '$v0'),
                          ('src1', '00010', '$s')]


@pytest.mark.parametrize('segment_name, instr_str, num_bits, expected_bin_str', instr_input_and_expected)
def test_data_segment_from_instr_str(segment_name, instr_str, num_bits, expected_bin_str):
    d = DataSegment(name=segment_name, instr_str=instr_str, num_bits=num_bits)
    assert str(d) == instr_str
    assert len(d) == num_bits
    assert d.bin_str == expected_bin_str


@pytest.mark.parametrize('segment_name, bin_str, expected_instr_str', bin_input_and_expected)
def test_data_segment_from_instr_str(segment_name, bin_str, expected_instr_str):
    d = DataSegment(name=segment_name, bin_str=bin_str)
    assert str(d) == expected_instr_str

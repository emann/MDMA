import pytest
from mdma.op_formatting import OpFormat, r_format, i_format, j_format, s_format


instr_str_and_expected_format = [('add', r_format),
                                 ('addi', i_format),
                                 ('j', j_format),
                                 ('sll', s_format)]

op_and_func_bits_and_expected_format = [('000000', '100000', r_format),
                                        ('001000', '123456', i_format),
                                        ('000010', '123456', j_format),
                                        ('000000', '000000', s_format)]


@pytest.mark.parametrize("instr_str, expected_op_format", instr_str_and_expected_format)
def test_from_instruction_str(instr_str, expected_op_format):
    op_format = OpFormat.from_instruction_str(instr_str)
    assert op_format == expected_op_format


@pytest.mark.parametrize("op_bits, func_bits, expected_op_format", op_and_func_bits_and_expected_format)
def test_from_op_and_func_bits(op_bits, func_bits, expected_op_format):
    op_format = OpFormat.from_op_and_func(op_bits, func_bits)
    assert op_format == expected_op_format

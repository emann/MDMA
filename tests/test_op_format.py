import pytest
from mdma.op_formatting import OpFormat, _r_format, _i_format, _j_format, _s_format


instr_str_and_expected_format = [('add', _r_format),
                                 ('addi', _i_format),
                                 ('j', _j_format),
                                 ('sll', _s_format)]

op_and_func_bits_and_expected_format = [('000000', '100000', _r_format),
                                        ('001000', '123456', _i_format),
                                        ('000010', '123456', _j_format),
                                        ('000000', '000000', _s_format)]


@pytest.mark.parametrize("instr_str, expected_op_format", instr_str_and_expected_format)
def test_from_instruction_str(instr_str, expected_op_format):
    op_format = OpFormat.from_instruction_str(instr_str)
    assert op_format == expected_op_format


@pytest.mark.parametrize("op_bits, func_bits, expected_op_format", op_and_func_bits_and_expected_format)
def test_from_op_and_func_bits(op_bits, func_bits, expected_op_format):
    op_format = OpFormat.from_op_and_func(op_bits, func_bits)
    assert op_format == expected_op_format

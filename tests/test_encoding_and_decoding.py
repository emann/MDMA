import pytest

from mdma.mips_instruction import MIPSInstruction

# ToDo: Add j format test once j format support is better
instr_str_and_expected_hex = [("sll $zero $zero 0", '0x00000000'),
                              ("add $t0 $t1 $t2", "0x012a4020"),
                              ("addi $a0 $s3 -77", "0x2264ffb3"),
                              ("addi $a0 $s3 77", "0x2264004d"),
                              ("j 0x00c40ab0", "0x083102ac")]


@pytest.mark.parametrize("instr_str, expected_hex", instr_str_and_expected_hex)
def test_encoding(instr_str, expected_hex):
    """Test one of each type of instruction, and ensure they are correctly encoded"""
    mi = MIPSInstruction(instruction_str=instr_str)
    assert str(mi) == instr_str
    assert mi.hex_str == expected_hex
    expected_binary = bin(int(expected_hex, 16))[2:].zfill(32)
    assert mi.bin_str == expected_binary
    encoded_str_decoded = MIPSInstruction(hex_str=mi.hex_str)
    assert str(encoded_str_decoded) == instr_str


@pytest.mark.parametrize("expected_instr_str, hex_str", instr_str_and_expected_hex)
def test_encoding(expected_instr_str, hex_str):
    """Test one of each type of instruction, and ensure they are correctly decoded"""
    mi = MIPSInstruction(hex_str=hex_str)
    assert mi.hex_str == hex_str
    expected_binary = bin(int(hex_str, 16))[2:].zfill(32)
    assert mi.bin_str == expected_binary
    assert str(mi) == expected_instr_str
    decoded_str_encoded = MIPSInstruction(instruction_str=mi.instruction_str)
    assert decoded_str_encoded.hex_str == hex_str

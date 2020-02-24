import binascii
import json

def twos_comp(val):
    bits = len(val)
    val = int(val,2)
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

with open('func_and_opcodes.json', 'r') as yf:
    codes = json.load(yf)
    opcodes = codes['opcodes']
    func_codes = codes['func_codes']

while True:
    print('=======')
    mc_hex = input("Machine code: ").replace(' ', '')
    if mc_hex.startswith('0x'):
        mc_hex = mc_hex[2:]
    mc_binary = bin(int(mc_hex, 16))[2:].zfill(32)
    print("Binary: ", mc_binary)
    if mc_binary.startswith('000000'):  # Special Operation
        fields = ['op', 'rs', 'rt', 'rd','shamt','func']
        binary = [mc_binary[:6], mc_binary[6:11], mc_binary[11:16], mc_binary[16:21], mc_binary[21:26], mc_binary[26:32]]
        decimal = [int(bb, 2) for bb in binary]
    elif any((mc_binary.startswith(c) for c in ['000010', '000011'])):  # J or JAL
        fields = ['op', 'target']
        binary = [mc_binary[:6], mc_binary[6:]]
        decimal = [int(bb, 2) for bb in binary]
        decimal[-1] = twos_comp(binary[-1])
    elif any((mc_binary.startswith(c) for c in ['000100', '000101'])):  # BEQ or BNE
        fields = ['op', 'src1', 'src2', 'offset']
        binary = [mc_binary[:6], mc_binary[6:11], mc_binary[11:16], mc_binary[16:]]
        decimal = [int(bb, 2) for bb in binary]
        decimal[-1] = twos_comp(binary[-1])
    else:
        fields = ['op', 'rs', 'rt', 'immediate']
        binary = [mc_binary[:6], mc_binary[6:11], mc_binary[11:16], mc_binary[16:]]
        decimal = [int(bb, 2) for bb in binary]
        decimal[-1] = twos_comp(binary[-1])
    if binary[0] == '000000':  # This is a special opcode with a func code
        op = func_codes[binary[5]]
    else:  # standard opcode
        op = opcodes[binary[0]]
    print('-----')
    print("OPERATION:", op)
    print('Section\tdecimal\tbinary')
    for i in range(len(fields)):
        print(f'{fields[i]}\t{decimal[i]}\t{binary[i]}')
    print('=======')
    print()

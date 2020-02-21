import binascii

known_opcodes = {2: 'J', 3: 'JAL', 4: 'BEQ', 5: 'BNE'}
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
    elif any((mc_binary.startswith(c) for c in ['000100', '000101'])):  # BEQ or BNE
        fields = ['op', 'src1', 'src2', 'offset']
        binary = [mc_binary[:6], mc_binary[6:11], mc_binary[11:16], mc_binary[16:]]
        decimal = [int(bb, 2) for bb in binary]
    else:
        fields = ['op', 'rs', 'rt', 'immediate']
        binary = [mc_binary[:6], mc_binary[6:11], mc_binary[11:16], mc_binary[16:]]
        decimal = [int(bb, 2) for bb in binary]
    if decimal[0] in known_opcodes:
        fields[0] = f'{fields[0]}: {known_opcodes[decimal[0]]}'
    print('Section\tdecimal\tbinary')
    for i in range(len(fields)):
        print(f'{fields[i]}\t{decimal[i]}\t{binary[i]}')
    print('=======')
    print()

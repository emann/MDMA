import binascii

known_opcodes = {2: 'J', 3: 'JAL', 4: 'BEQ', 5: 'BNE'}
while True:
    print('=======')
    mc = input("Machine code: ").replace(' ', '')
    if mc.startswith('0x'):
        mc = mc[2:]
    mc = bin(int(mc, 16))[2:].zfill(32)
    print("Binary: ", mc)
    if mc.startswith('000000'):
        n = ['op', 'rs', 'rt', 'rd','shamt','func']
        b = [mc[:6], mc[6:11], mc[11:16], mc[16:21], mc[21:26], mc[26:32]]
        d = [int(bb, 2) for bb in b]
    elif any((mc.startswith(c) for c in ['000010', '000011'])):  # J or JAL
        n = ['op', 'target']
        b = [mc[:6], mc[6:]]
        d = [int(bb, 2) for bb in b]
    elif any((mc.startswith(c) for c in ['000100', '000101'])):  # BEQ or BNE
        n = ['op', 'src1', 'src2', 'offset']
        b = [mc[:6], mc[6:11], mc[11:16], mc[16:]]
        d = [int(bb, 2) for bb in b]
    else:
        n = ['op', 'rs', 'rt', 'immediate']
        b = [mc[:6], mc[6:11], mc[11:16], mc[16:]]
        d = [int(bb, 2) for bb in b]
    if d[0] in known_opcodes:
        n[0] = f'{n[0]}: {known_opcodes[d[0]]}'
    print('Section\tdecimal\tbinary')
    for i in range(len(n)):
        print(f'{n[i]}\t{d[i]}\t{b[i]}')
    print('=======')
    print()

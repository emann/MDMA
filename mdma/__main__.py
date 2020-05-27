from typing import Optional

from .mips_instruction import MIPSInstruction
from prettytable import PrettyTable
from argparse import ArgumentParser


def decode(hex_str: str, verbose: bool=False) -> None:
    """Decodes the hex string and prints the machine code, binary, and decoded instruction string

    :param hex_str: the 32-bit hex machine code to be decoded
    :param verbose: if True, the value of each data segment is printed in a table as well
    """
    print('=======')
    print('Machine Code:', hex_str)
    mc = MIPSInstruction(hex_str=hex_str)
    print("Binary:", mc.bin_str)
    if verbose:
        t = PrettyTable(['SECTION', 'DECIMAL', 'BINARY', 'DECODED'])
        for d in mc.data_segments:
            t.add_row([d.name, d.decimal, d.bin_str, d.human_readable])
        print(t)
    print("DECODED:", str(mc))
    print('=======\n')


def encode(instr_str: str, verbose: bool=False) -> None:
    """Encodes the instruction string and prints the instruction string as well as the encoded machine code and binary

    :param hex_str: the human readable instruction string to be encoded
    :param verbose: if True, the value of each data segment is printed in a table as well
    """
    print('=======')
    print('Instruction String:', instr_str)
    mc = MIPSInstruction(instruction_str=instr_str)
    if verbose:
        t = PrettyTable(['SECTION', 'DECIMAL', 'BINARY', 'ENCODED'])
        for d in mc.data_segments:
            t.add_row([d.name, d.decimal, d.bin_str, d.human_readable])
        print(t)
    print("Binary:", mc.bin_str)
    print("ENCODED:", mc.hex_str)
    print('=======\n')


def interactive_loop(operation: Optional[str]=None, verbose: bool=False) -> None:
    """The loop that drives "interactive mode" - user enters an operation (if one wasn't specified when starting) and an
    input and the result is printed.

    :param operation: Operation to be used by default (Optional)
    :param verbose: passes verbose=True to the encode and decode functions
    """
    print('Type \"exit\" to exit')
    while True:
        input_str = input('>>>')
        if input_str in ['', 'exit']:
            break
        if not operation:
            if not input_str.startswith(('encode', 'decode')):
                print('INVALID OPERATION. Format: {encode, decode} input (e.g. decode 0x00000000)')
            operation = input_str[:6]
            input_str = input_str[7:]
        if operation == 'decode':
            decode(input_str, verbose)
        elif operation == 'encode':
            encode(input_str, verbose)
        else:
            print('INVALID OPERATION. Format: {encode, decode} input (e.g. decode 0x00000000)')


parser = ArgumentParser(description='Decode machine code or Encode MIPS Assembly Language')
parser.add_argument('mode', type=str, nargs='?', choices={"encode", "decode"})
parser.add_argument('input_str', type=str, nargs='?')
parser.add_argument('-i', '--interactive', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if args.interactive:
    interactive_loop(getattr(args, 'mode'), args.verbose)
elif args.mode:
    if not args.input_str:
        parser.error(f'Must supply an input string to {args.mode}.')
    if args.mode == 'decode':
        decode(args.input_str, args.verbose)
    if args.mode == 'encode':
        encode(args.input_str, args.verbose)
else:
    interactive_loop(verbose=args.verbose)

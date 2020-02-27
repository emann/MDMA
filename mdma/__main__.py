from .machine_code import MachineCode
from prettytable import PrettyTable
from argparse import ArgumentParser


def decode(hex_str, verbose=False):
    print('=======')
    print('Machine Code:', hex_str)
    mc = MachineCode(hex_str)
    print("Binary:", mc.bin_str)
    if verbose:
        t = PrettyTable(['SECTION', 'DECIMAL', 'BINARY', 'DECODED'])
        for d in mc.data_segments:
            t.add_row([d.name, d.decimal, d.bin_str, d.human_readable])
        print(t)
    print("DECODED:", str(mc))
    print('=======\n')
    return True


def interactive_loop(operation=None, verbose=False):
    print('Type \"exit\" to exit')
    while True:
        input_str = input('>>>')
        if input_str in ['', 'exit']:
            break
        if not operation:
            if not input_str.startswith(('encode', 'decode')):
                print()
            operation = input_str[:6]
            input_str = input_str[7:]
        if operation == 'decode':
            decode(input_str, verbose)
        elif operation == 'encode':
            print('Encoding MIPS instructions is not supported yet.')
        else:
            print()


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
        print('Encoding is not supported yet.')
else:
    parser.error('encode or decode must be specified if interactive mode (-i) is not specified.')

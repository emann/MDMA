from .machine_code import MachineCode
from prettytable import PrettyTable


def _loop_func():
    print('=======')
    hex_str = input("Machine Code: ").replace(' ', '')
    if hex_str == 'exit':
        return False
    mc = MachineCode(hex_str)
    print("Binary:", mc.bin_str)
    t = PrettyTable(['SECTION', 'DECIMAL', 'BINARY', 'DECODED'])
    for d in mc.data_segments:
        t.add_row([d.name, d.decimal, d.bin_str, d.human_readable])
    print(t)
    print("DECODED:", str(mc))
    print('=======\n')
    return True


while _loop_func():
    pass

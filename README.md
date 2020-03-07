# MDMA

### (M)achine code (D)ecoding/encoding for (M)ips (A)ssembly language
A python package for decoding machine code and encoding human-readable instruction strings for use with the [MIPS Assembly Language](https://en.wikipedia.org/wiki/MIPS_architecture). 

## Installation

Installation with pip coming soon.

## Usage
### Interactive
When ran as a module, you can either decode/encode one instruction at a time:
```bash
python -m mdma encode "add $t2 $s1 $v0"  # Prints the encoded binary and machine code
python -m mdma decode 0x02225020         # Prints the decoded binary and human-readable instruction string
````

Or, MDMA can be also be ran interactively if no operation/input is specified:
```
python -m mdma
Type "exit" to exit
>>>encode sll $0 $0 0  # Prints the encoded binary and machine code
>>>decode 0x00000000   # Prints the decoded binary and human-readable instruction string
```

You can also specify an operation to be used in interactive mode using the `-i` or `--interactive` argument:
```
python -m mdma encode -i 
Type "exit" to exit
>>>sll $0 $0 0  # Prints the encoded binary and machine code
```
```
python -m mdma decode -i 
Type "exit" to exit
>>>0x00000000  # Prints the decoded binary and human-readable string
```
If you wish to see a nicely-formatted table of the data segments, with binary and parsed values for each, use the `-v` or `--verbose` argument.

### As a package
Creating a MIPSInstruction object from either an instruction string, binary string, or hex string automatically decode/encodes the other two.

```python
from mdma import MIPSInstruction

from_instr = MIPSInstruction(instruction_str='j 0x002cd3ff')
from_bin = MIPSInstruction(bin_str='00001000000010110011010011111111')
from_hex = MIPSInstruction(hex_str='0x080b34ff')

#These all print the same three values
for mips_instr in [from_instr, from_bin, from_hex]:
    print(mips_instr)           # str(MIPSInstruction) returns the instruction string 
    print(mips_instr.hex_str)
    print(mips_instr.bin_str)
```
You can also access an instruction's data segments (a list of `DataSegment` objects) and its Operation Format (an `OpFormat` object).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
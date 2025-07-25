# pyiostream
A C++ approach to I/O in Python with OStream &lt;&lt; and manipulators &lt;&lt; endl;


## Quick Overview:
```python
from pyiostream import OStream, endl, Hex

cout = OStream()

cout << "Hello World!" << endl;
cout << "1+1 = " << 1+1 << endl;
cout << "hex(1+1) = " << Hex << 1+1 << "\n" << endl;
```

## Installation
The Wizard `pip` will guide you through the package installation process.

Run `pip install .` inside the same folder containing the `setup.cfg` file.

## Note:
Main goal of the project now is to implement basic IOStream like functionality with basic manipulators. Custom IOManipulators can be made, however, the implementation with OStream will likely change; So only use predefined IOManipulators to avoid breaking.

## Future goals/ ideas:
- Implementing float and integer conversion using decimal.Decimal -- where the default output is to "Round as taught in school", and convert floats to Decimal automatically by Decimal(str(some_float)),
- Support basic terminal output control sequences for changing color, moving cursor, etc. + in addition, supporting cross-platform functionality with Windows Console host (cmd.exe) native api.

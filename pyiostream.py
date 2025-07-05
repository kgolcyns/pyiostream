# pyiostream.py
import sys


"""Main Classes"""

class OStream:

    def __init__(self, output=None):
        self.output = sys.stdout if output is None else output
        self.format = ''

    def __lshift__(self, argument):
        """The special method which Python calls when you use
        the << operator and the left-hand operand is an OStream."""

        if isinstance(argument, IOManipulator):
            argument(self)
        else:
            try:
                output_str = (self.format % argument) if self.format else str(argument)
                self.output.write(output_str)
            finally:
                self.format = ''

        return self


class IOManipulator:

    def __init__(self, function=None):
        self.function = function

    def __call__(self, stream: OStream):
        self.function(stream)


"""Builtin IOManipulators"""

'''Stream operating Manipulators'''
@IOManipulator
def endl(stream: OStream):
    """Add new line and flush output stream."""
    stream.output.write('\n')
    stream.output.flush()

@IOManipulator
def flush(stream: OStream):
    stream.output.flush()

'''Type Conversion Manipulators'''
@IOManipulator
def Hex(stream: OStream):
    """Sets uppercase hex format specifier, with prefix 0x (x is lowercase)."""
    stream.format = '0x%X'

@IOManipulator
def Str(stream: OStream):  # Redundant, but for show
    stream.format = '%s'

@IOManipulator
def Repr(stream: OStream):
    stream.format = '%r'


"""Testing and Examples"""
def test_example():
    """Example of using."""
    cout = OStream()

    cout << "The average of " << 1 << " and " << 3 << " is: " << (1+3)/2 << endl;
    cout << "Decimal " << 269 << " in hexadecimal is: " << Hex << 269 << endl;

    cout << "repr(" << cout << ")=" << Repr << cout << endl;

    cout << "Flushing Toilet..." << flush << "...Complete!" << endl;
    cout << "Exiting Test\n" << endl;


if __name__ == '__main__':
    test_example()

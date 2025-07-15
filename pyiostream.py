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



"""REPL Helpers"""

# Suppress echoing of OStream objects in REPL
def _displayhook(value):
    """
    In REPL OStream objects echo unwanted repr, change displayhook
    to exclude OStream objects, so they behave like None when echoed.
    """
    if isinstance(value, OStream):
        return None
    else:
        _displayhook_bak(value)

_displayhook_bak = sys.displayhook
sys.displayhook = _displayhook


cout = OStream()

# no inspection see:
# https://gist.github.com/pylover/7870c235867cf22817ac5b096defb768
# ref from: https://stackoverflow.com/questions/39847884/can-i-get-pycharm-to-suppress-a-particular-warning-on-a-single-line


"""Testing and Examples"""
def test_example():
    """Example of using."""
    cout = OStream()  # noqa noinspection PyShadowingNames

    cout << "The average of " << 1 << " and " << 3 << " is: " << (1+3)/2 << endl;
    cout << "Decimal " << 269 << " in hexadecimal is: " << Hex << 269 << endl;

    cout << "repr(" << cout << ")=" << Repr << cout << endl;

    cout << "Flushing Toilet..." << flush << "...Complete!" << endl;
    cout << "Exiting Test\n" << endl;


if __name__ == '__main__':
    test_example()

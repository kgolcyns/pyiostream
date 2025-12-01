# pyiostream.py
from __future__ import annotations

import decimal
decimal.getcontext().rounding=decimal.ROUND_HALF_UP  #TODO: implement preserving context, later
import sys
from collections.abc import Callable
from io import IOBase
from typing import Optional

"""Main Classes"""

class OStream:
    DEFAULT_FORMAT: str = ''
    DEFAULT_PREFIX: str = ''
    DEFAULT_SUFFIX: str = ''
    DEFAULT_PREPROCESSOR: Optional[Callable] = None
    DEFAULT_POSTPROCESSOR: Optional[Callable] = None

    def __init__(self, output: Optional[IOBase] = None):
        self.output: IOBase = sys.stdout if output is None else output

        # Declare and Initialize formatters (pycharm complains despite reset_formatters() being called)
        # <editor-fold desc="formatters redeclaration for nagging linter">
        self.format: str = ''  # format specifier passed to format() built in.
        self.prefix: str = ''
        self.suffix: str = ''
        self.preprocessor: Optional[Callable] = None  # optional function to be called the argument object before passed to format()
        self.postprocessor: Optional[Callable] = None  # optional function to be called on the output of format()
        # </editor-fold>
        self._reset_formatters()

    def __lshift__(self, argument):
        """The special method which Python calls when you use
        the << operator and the left-hand operand is an OStream."""

        if isinstance(argument, IOManipulator):
            argument(self)
        else:
            try:
                if callable(self.preprocessor):
                    argument = self.preprocessor(argument)

                output_str = format(argument, self.format)

                if callable(self.postprocessor):
                    output_str = self.postprocessor(output_str)

                output_str = f'{self.prefix}{output_str}{self.suffix}'
                #output_str = (self.format % argument) if self.format else str(argument)
                self.output.write(output_str)
            finally:
                self._reset_formatters()

        return self

    def _reset_formatters(self):
        """
        Resets all formatting attributes to their normal/Default value;
        Called after a format and write has been made. Not typically necessary or useful for users to call this;
        set DEFAULT_... can be changed to allow formatters to persist between write indefinitely.
        (IOManipulators still have priority for individual calls)
        """
        self.format = self.DEFAULT_FORMAT
        self.prefix = self.DEFAULT_PREFIX
        self.suffix = self.DEFAULT_SUFFIX
        self.preprocessor = self.DEFAULT_PREPROCESSOR
        self.postprocessor = self.DEFAULT_POSTPROCESSOR  # Callable, input 1 str, output 1 str

    def restore_default_formatters(self):
        """Restores the default values of the formatters to that of the OStream class.
        Note: Remember to call _reset_formatters() to take immediate effect."""
        del self.DEFAULT_FORMAT
        del self.DEFAULT_PREFIX
        del self.DEFAULT_SUFFIX
        del self.DEFAULT_PREPROCESSOR
        del self.DEFAULT_POSTPROCESSOR

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
    stream.format = 'X'
    stream.prefix = '0x'

@IOManipulator
def Str(stream: OStream):  # Redundant, but for show
    stream.preprocessor = str  # to be consistent with repr

@IOManipulator
def Repr(stream: OStream):
    stream.preprocessor = repr


# Rounding Stuff
# TODO: Convert this to subclass of IOManipulator notation, instead of wrapper notation
def _convert_and_round(number, ndigits):
    if not isinstance(number, decimal.Decimal):
        number = decimal.Decimal(str(number))
    return round(number, ndigits)

def Round(ndigits=0):
    # NOTE: when ndigits=None, Decimal.__round__() does not obey the rounding context,
    @IOManipulator
    def RoundManipulator(stream: OStream):
        stream.preprocessor = lambda number: _convert_and_round(number, ndigits)

    return RoundManipulator


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
        return _displayhook_bak(value)

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

def test_rounding():
    n = 2.55
    cout << n << " rounded to the nearest tenth should be 2.6" << endl;
    cout << "\tBut stupid rounding makes it 2.5 --> " << round(n, 1) << endl;
    cout << "\nWith pyiostream's improved Round(...) IOManipulator, "
    cout << "\nFloating point like numbers are rounded: 'As Taught in School':\n\t"
    cout << "2.6 --> " << Round(1) << n<< '\n' << endl;

if __name__ == '__main__':
    test_example()
    test_rounding()

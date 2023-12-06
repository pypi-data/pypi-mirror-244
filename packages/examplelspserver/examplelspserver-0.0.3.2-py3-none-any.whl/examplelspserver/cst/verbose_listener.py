"""Verbose Error Listener for ANTLR"""
__author__ = 'sgu'

#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys

from antlr4.Recognizer import Recognizer
from antlr4.Token import Token
# antlr
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import RecognitionException


class VerboseListener(ErrorListener):
    def __init__(self):
        self._symbol = ''
        super().__init__()

    @property
    def symbol(self):
        return self._symbol

    def test(self, msg: str = "bar"):
        print(msg)

    def syntaxError(self, recognizer: Recognizer, offendingSymbol: Token, line: int, column: int, msg: str, e: RecognitionException = None):
        stack = recognizer.getRuleInvocationStack()
        stack.reverse()

        self._symbol = offendingSymbol.text

        print("ERROR: when parsing line %d column %d: %s\n" % (line, column, msg), file=sys.stderr)
        # Alternative
        # raise Exception("ERROR: when parsing line %d column %d: %s\n" % (line, column, msg))

        print("rule stack: ", str(stack), file=sys.stderr)
        print("line", line, ":", column, "at", offendingSymbol, ":", msg, file=sys.stderr)

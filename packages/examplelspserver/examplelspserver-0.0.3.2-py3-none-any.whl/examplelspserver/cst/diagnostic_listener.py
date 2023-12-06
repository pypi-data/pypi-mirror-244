"""DiagnosticListener module."""

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

# util imports
import logging
from typing import List

# antlr4
from antlr4.error.ErrorListener import ErrorListener
from antlr4.Recognizer import Recognizer
from antlr4.Token import Token
from antlr4.error.Errors import RecognitionException

# pygls
# Deprecated from 0.13
# from pygls.lsp.types import (Diagnostic, Range, Position)
# Migrating to pygls v1.0
# https://pygls.readthedocs.io/en/latest/pages/migrating-to-v1.html
from lsprotocol.types import (Diagnostic, Range, Position)

# debug
logging.basicConfig(level=logging.DEBUG)


class DiagnosticListener(ErrorListener):
    def __init__(self):
        self.diagnostics: List[Diagnostic] = []
        super().__init__()

    logger = logging.getLogger(__name__)
    # Enables printing ATN state info to terminal.
    show_debug_output: bool = False

    # reset the listener's state
    def reset(self):
        self.diagnostics = []

    def syntaxError(self, recognizer: Recognizer, offendingSymbol: Token, line: int, column: int, msg: str,
                    e: RecognitionException = None):
        self.diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(
                        line=line - 1,
                        character=column - 1),
                    end=Position(
                        line=line - 1,
                        character=column)
                ),
                message=msg
            )
        )

        if self.show_debug_output and self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('ERROR: when parsing line %d column %d: %s\n' % (line, column, msg))
        # dev alternatives
        # print('ERROR: when parsing line %d column %d: %s\n' % (line, column, msg), file=sys.stderr)
        # raise Exception("ERROR: when parsing line %d column %d: %s\n" % (line, column, msg))

"""computeTokenIndex module."""

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

# utils
import logging
from dataclasses import dataclass
from typing import List, Optional, Any

# antlr4
from antlr4 import TerminalNode, Token, BufferedTokenStream
from antlr4.tree.Tree import ParseTree, ErrorNodeImpl
from antlr4.ParserRuleContext import ParserRuleContext

# debug
logger = logging.getLogger(__name__)
logger.disabled = True


@dataclass
class CaretPosition:
    line: int
    column: int


@dataclass
class TokenPosition:
    index: int
    context: ParserRuleContext
    text: str


def compute_token_index_of_terminal_node(terminalNode: TerminalNode, caretPosition: CaretPosition) -> Optional[Any]:
    start = terminalNode.symbol.column
    stop = terminalNode.symbol.column + len(terminalNode.getText())
    if terminalNode.symbol.line == caretPosition.line and start <= caretPosition.column <= stop:
        return terminalNode.symbol.tokenIndex
    else:
        return None


def compute_token_index_of_child_node(parser_rule_context: ParserRuleContext, caretPosition: CaretPosition) -> Optional[int]:
    i = 0
    while i < parser_rule_context.getChildCount():
        index = compute_token_index(parser_rule_context.getChild(i), caretPosition)
        if index is not None:
            return index
        i += 1
    return None


def compute_token_index(parseTree: ParseTree, caretPosition: CaretPosition) -> int:
    if isinstance(parseTree, TerminalNode):
        return compute_token_index_of_terminal_node(parseTree, caretPosition)
    else:
        parser_rule_context: ParserRuleContext = parseTree
        return compute_token_index_of_child_node(parser_rule_context, caretPosition)


def position_of_token(token: Token, text: str, caretPosition: CaretPosition, identifier_token_types: List[int],
                      parseTree: ParseTree):
    start = token.column
    stop = token.column + len(text)
    logger.info(
        'token.line: %s == caretPosition.line: %s = %s, start: %s <= caretPosition.column: %s <= stop: %s = %s, '
        'token.column: %s , len(text): %s, text: %s, index: %s',
        token.line, caretPosition.line, token.line == caretPosition.line, start, caretPosition.column, stop,
        start <= caretPosition.column <= stop, token.column, len(text), text, token.tokenIndex)
    if token.line == caretPosition.line and start <= caretPosition.column <= stop:
        index = token.tokenIndex
        if token.type in identifier_token_types:
            index -= 1

        # TODO check to choose complete token text or substring
        # result: TokenPosition = tokenPosition(index, parseTree, text)
        parser_rule_context: ParserRuleContext = parseTree
        # TODO check for error nodes
        text = text[0: caretPosition.column - start] if not isinstance(parseTree, ErrorNodeImpl) else ''
        result: TokenPosition = TokenPosition(index, parser_rule_context, text)

        logger.info('position_of_token return result = %s', result)
        return result
    else:
        logger.info('position_of_token return None')
        return None


def compute_token_position_of_terminal(terminalNode: TerminalNode, tokenStream: BufferedTokenStream,
                                       caretPosition: CaretPosition, identifier_token_types: List[int]):
    token: Token = terminalNode.symbol
    text: str = terminalNode.getText()
    logger.info('compute_token_position_of_terminal')
    return position_of_token(token, text, caretPosition, identifier_token_types, terminalNode)


def compute_token_position_of_child_node(parser_rule_context: ParserRuleContext, tokens: BufferedTokenStream,
                                         caretPosition: CaretPosition, identifier_token_types: List[int]):
    logger.info('start: %s > caret: %s = %s, stop: %s < caret: %s = %s', parser_rule_context.start.line,
                caretPosition.line, parser_rule_context.start.line > caretPosition.line, parser_rule_context.stop.line,
                caretPosition.line, parser_rule_context.stop.line < caretPosition.line)
    logger.info('parser_rule_context.start is not None = %s, parser_rule-_context.stop is not None = %s',
                parser_rule_context.start is not None, parser_rule_context.stop is not None)
    if (parser_rule_context.start is not None and parser_rule_context.start.line > caretPosition.line) or (
            parser_rule_context.stop is not None and parser_rule_context.stop.line < caretPosition.line):
        logger.info('return None\n')
        return None
    i = 0
    logger.info('parser_rule_context.getChildCount() = %s', parser_rule_context.getChildCount())
    while i < parser_rule_context.getChildCount():
        position = compute_token_position(parser_rule_context.getChild(i), tokens, caretPosition, identifier_token_types)
        logger.info('Child compute_token_position = %s', position)
        if position is not None:
            logger.info('return position = %s\n', position)
            return position
        i += 1
    logger.info('parser_rule_context.start is not None = %s, parser_rule_context.stop is not None = %s',
                parser_rule_context.start is not None, parser_rule_context.stop is not None)
    if parser_rule_context.start is not None and parser_rule_context.stop is not None:
        logger.info('parser_rule_context.start.tokenIndex: %s <= parser_rule_context.stop.tokenIndex: %s = %s',
                    parser_rule_context.start.tokenIndex, parser_rule_context.stop.tokenIndex,
                    parser_rule_context.start.tokenIndex <= parser_rule_context.stop.tokenIndex)
        i = parser_rule_context.start.tokenIndex
        logger.info('while parser_rule_context start.tokenIndex: %s, stop.tokenIndex: %s',
                    parser_rule_context.start.tokenIndex, parser_rule_context.stop.tokenIndex)
        while i <= parser_rule_context.stop.tokenIndex:
            pos = position_of_token(tokens.tokens[i], tokens.tokens[i].text, caretPosition, identifier_token_types,
                                    parser_rule_context)
            logger.info('position_of_token = %s', pos)
            if pos:
                logger.info('return position = %s\n', pos)
                return pos
            i += 1
    logger.info('final return None\n')
    return None


def compute_token_position(parseTree: ParseTree, tokens: BufferedTokenStream, caretPosition: CaretPosition,
                           identifier_token_types: List[int] = []) -> Optional[TokenPosition]:
    if isinstance(parseTree, TerminalNode):
        return compute_token_position_of_terminal(parseTree, tokens, caretPosition, identifier_token_types)
    else:
        parser_rule_context: ParserRuleContext = parseTree
        return compute_token_position_of_child_node(parser_rule_context, tokens, caretPosition, identifier_token_types)

"""exampleLSPServer package."""

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

############################################################################
############################################################################

# util imports
import asyncio
import logging
import re
import time
import uuid
from typing import List, Optional

# antlr4
from antlr4 import CommonTokenStream, InputStream, Token
from antlr4.IntervalSet import IntervalSet

# pygls
# Deprecated from 0.13
# from pygls.lsp.methods import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE,
# TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL)
# from pygls.lsp.types import (CompletionItem, CompletionList, CompletionOptions, CompletionParams,
# ConfigurationItem, ConfigurationParams, Diagnostic, DidChangeTextDocumentParams,
#                              DidCloseTextDocumentParams, DidOpenTextDocumentParams, MessageType, Position, Range,
#                              Registration, RegistrationParams, SemanticTokens,
#                              SemanticTokensLegend, SemanticTokensParams, Unregistration, UnregistrationParams)
# from pygls.lsp.types.basic_structures import (WorkDoneProgressBegin, WorkDoneProgressEnd, WorkDoneProgressReport)
#
# Migrating to pygls v1.0
# https://pygls.readthedocs.io/en/latest/pages/migrating-to-v1.html
from lsprotocol.types import (
    CompletionItem, CompletionList, CompletionOptions, CompletionParams, ConfigurationItem, ConfigurationParams, Diagnostic, DidChangeTextDocumentParams, DidCloseTextDocumentParams, DidOpenTextDocumentParams, DidSaveTextDocumentParams, MessageType,
    Registration, RegistrationParams, SemanticTokens, SemanticTokensLegend, SemanticTokensParams, TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL, Unregistration, UnregistrationParams, WorkDoneProgressBegin, WorkDoneProgressEnd, WorkDoneProgressReport
)
from pygls.server import LanguageServer
from pygls.workspace import Document

# antlr4-c3
from codeCompletionCore.CodeCompletionCore import CandidatesCollection, CodeCompletionCore

# user relative imports
from examplelspserver.utils.compute_token_index import CaretPosition, TokenPosition, compute_token_position
from examplelspserver.utils.suggest_variables import suggest_variables
from examplelspserver.cst.diagnostic_listener import DiagnosticListener
from examplelspserver.cst.symbol_table_visitor import SymbolTableVisitor
from examplelspserver.gen.python.exampleDsl.exampleDslLexer import exampleDslLexer
from examplelspserver.gen.python.exampleDsl.exampleDslParser import exampleDslParser

# debug import
# from pprint import pprint
# python path hacking / DO NOT USE for live code
# if not os.path.join(sys.path[0], 'example-dsl', 'lspExampleServer') in sys.path:
#     sys.path.append(os.path.join( sys.path[0], 'example-dsl', 'lspExampleServer') )
# pprint(sys.path)

COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1


class ExampleLSPServer(LanguageServer):
    CMD_COUNT_DOWN_BLOCKING = 'countDownBlocking'
    CMD_COUNT_DOWN_NON_BLOCKING = 'countDownNonBlocking'
    CMD_PROGRESS = 'progress'
    CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    CMD_SHOW_CONFIGURATION_ASYNC = 'showConfigurationAsync'
    CMD_SHOW_CONFIGURATION_CALLBACK = 'showConfigurationCallback'
    CMD_SHOW_CONFIGURATION_THREAD = 'showConfigurationThread'
    CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    CONFIGURATION_SECTION = 'ODslExampleServer'

    def __init__(self, *args):
        super().__init__(*args)
        # set ErrorListener
        self.error_listener: DiagnosticListener = DiagnosticListener()
        # set empty input stream
        input_stream: InputStream = InputStream(str())

        # set lexer
        self.lexer: exampleDslLexer = exampleDslLexer(input_stream)
        # set ErrorListener for diagnostics
        self.lexer.removeErrorListeners()
        self.lexer.addErrorListener(self.error_listener)

        # set token stream pipe between lexer and parser
        self.tokenStream: CommonTokenStream = CommonTokenStream(self.lexer)

        # set parser
        self.parser: exampleDslParser = exampleDslParser(self.tokenStream)
        # set ErrorListener for diagnostics
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(self.error_listener)


example_server = ExampleLSPServer('pygls-odsl-example-prototype', 'v0.1')

logger = logging.getLogger(__name__)


def _validate(ls: ExampleLSPServer, params):
    # msg to debug console
    # TODO setup debug logger
    # ls.show_message_log( 'Validating file...' )

    # get file content for lexer input stream
    text_doc: Document = ls.workspace.get_document(params.text_document.uri)
    source: str = text_doc.source
    # validate format if source is determined
    diagnostics: List[Diagnostic] = _validate_format(ls, source) if source is not None else []
    # return diagnostics
    ls.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_format(ls: ExampleLSPServer, source: str):
    """Validates file format."""
    # get input stream of characters for lexer
    input_stream: InputStream = InputStream(source)

    # set the input stream and reset the lexer/parser/listener
    ls.error_listener.reset()
    ls.lexer.inputStream = input_stream
    ls.tokenStream = CommonTokenStream(ls.lexer)
    ls.parser.setInputStream(ls.tokenStream)

    try:
        # launch parser by invoking top-level rule
        ls.parser.stat()
    except OSError as err:
        # TODO add exception
        msg = err.filename.msg

        ls.error_listener.diagnostics.append(msg)

    # return diagnostics
    return ls.error_listener.diagnostics


def get_symbol_name_at_position(uri, position):
    logger.info('uri: %s\n', uri, 'position: %s\n', position)


def lookup_symbol(uri, name):
    logger.info('uri: %s\n', uri, 'name: %s\n', name)


@example_server.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[',']))
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""

    # set input stream of characters for lexer
    text_doc: Document = example_server.workspace.get_document(params.text_document.uri)
    source: str = text_doc.source
    input_stream: InputStream = InputStream(source)

    # reset the lexer/parser
    example_server.error_listener.reset()
    example_server.lexer.inputStream = input_stream
    example_server.tokenStream = CommonTokenStream(example_server.lexer)
    example_server.parser.setInputStream(example_server.tokenStream)

    # launches parser by invoking top-level rule
    Top_levelContext = exampleDslParser.StatContext
    parseTree: Top_levelContext = example_server.parser.stat()

    # get token index under caret position
    # params.position.line + 1 as lsp line counts from 0 and antlr4 line counts from 1
    tokenIndex: TokenPosition = compute_token_position(
        parseTree, example_server.tokenStream,
        CaretPosition(
            params.position.line + 1,
            params.position.character
        )
    )

    # set emtpy return list
    completion_list: CompletionList = CompletionList(is_incomplete=False, items=[])

    # return if no index could be determined
    if tokenIndex is None:
        # TODO add exception
        return completion_list

    # launch c3 core with parser
    core: CodeCompletionCore = CodeCompletionCore(example_server.parser)

    core.ignoredTokens = {Token.EPSILON}
    core.preferredRules = {exampleDslParser.RULE_variableRef, exampleDslParser.RULE_functionRef}

    # get completion candidates
    candidates: CandidatesCollection = core.collectCandidates(tokenIndex.index)

    if any(
            rule in candidates.rules for rule in
            [exampleDslParser.RULE_variableRef, exampleDslParser.RULE_functionRef]
    ):

        symbol_table_visitor: SymbolTableVisitor = SymbolTableVisitor('completions')

        symbol_table = symbol_table_visitor.visit(parseTree)

        variables = suggest_variables(symbol_table, tokenIndex)

        for variable in variables:
            completion_list.items.append(CompletionItem(label=variable))

    # get labels of completion candidates to return
    labels_list: List[str] = []
    for key, valueList in candidates.tokens.items():
        completion_list.items.append(
            CompletionItem(
                label=IntervalSet.elementName(
                    IntervalSet, example_server.parser.literalNames,
                    example_server.parser.symbolicNames, key
                )
            )
        )

    # return completion candidates labels
    return completion_list


# @odsl_server.thread()
@example_server.command(ExampleLSPServer.CMD_COUNT_DOWN_BLOCKING)
def count_down_10_seconds_blocking(ls, *args):
    """Starts counting down and showing message synchronously.
    It will `block` the main thread, which can be tested by trying to show
    completion items.
    """
    for i in range(COUNT_DOWN_START_IN_SECONDS):
        ls.show_message(f'Counting down... {COUNT_DOWN_START_IN_SECONDS - i}')
        time.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


@example_server.command(ExampleLSPServer.CMD_COUNT_DOWN_NON_BLOCKING)
async def count_down_10_seconds_non_blocking(ls, *args):
    """Starts counting down and showing message asynchronously.
    It won't `block` the main thread, which can be tested by trying to show
    completion items.
    """
    for i in range(COUNT_DOWN_START_IN_SECONDS):
        ls.show_message(f'Counting down... {COUNT_DOWN_START_IN_SECONDS - i}')
        await asyncio.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


@example_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate(ls, params)


@example_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: ExampleLSPServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message('Text Document Did Close')


@example_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(server: ExampleLSPServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""

    # set input stream of characters for lexer
    text_doc: Document = example_server.workspace.get_document(params.text_document.uri)
    source: str = text_doc.source
    input_stream: InputStream = InputStream(source)

    # reset the lexer/parser
    example_server.error_listener.reset()
    example_server.lexer.inputStream = input_stream
    example_server.tokenStream = CommonTokenStream(example_server.lexer)
    example_server.parser.setInputStream(example_server.tokenStream)

    Top_levelContext = exampleDslParser.StatContext
    parseTree: Top_levelContext = example_server.parser.stat()

    # TODO

    server.show_message('Text Document Did Save')


@example_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message('Text Document Did Open')
    _validate(ls, params)


@example_server.feature(
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    SemanticTokensLegend(token_types=["operator"], token_modifiers=[])
)
def semantic_tokens(ls: ExampleLSPServer, params: SemanticTokensParams):
    """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
    for details on how semantic tokens are encoded."""

    TOKENS = re.compile('".*"(?=:)')

    uri = params.text_document.uri
    doc = ls.workspace.get_document(uri)

    last_line = 0
    last_start = 0

    data = []

    for lineno, line in enumerate(doc.lines):
        last_start = 0

        for match in TOKENS.finditer(line):
            start, end = match.span()
            data += [(lineno - last_line), (start - last_start), (end - start), 0, 0]

            last_line = lineno
            last_start = start

    return SemanticTokens(data=data)


@example_server.command(ExampleLSPServer.CMD_PROGRESS)
async def progress(ls: ExampleLSPServer, *args):
    """Create and start the progress on the client."""
    token = 'token'
    # Create
    await ls.progress.create_async(token)
    # Begin
    ls.progress.begin(token, WorkDoneProgressBegin(title='Indexing', percentage=0))
    # Report
    for i in range(1, 10):
        ls.progress.report(token, WorkDoneProgressReport(message=f'{i * 10}%', percentage=i * 10), )
        await asyncio.sleep(2)
    # End
    ls.progress.end(token, WorkDoneProgressEnd(message='Finished'))


@example_server.command(ExampleLSPServer.CMD_REGISTER_COMPLETIONS)
async def register_completions(ls: ExampleLSPServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams(
        registrations=[Registration(
            id=str(uuid.uuid4()), method=TEXT_DOCUMENT_COMPLETION,
            register_options={"triggerCharacters": "[':']"}
        )]
    )
    response = await ls.register_capability_async(params)
    if response is None:
        ls.show_message('Successfully registered completions method')
    else:
        ls.show_message('Error happened during completions registration.', MessageType.Error)


@example_server.command(ExampleLSPServer.CMD_SHOW_CONFIGURATION_ASYNC)
async def show_configuration_async(ls: ExampleLSPServer, *args):
    """Gets exampleConfiguration from the client settings using coroutines."""
    try:
        config = await ls.get_configuration_async(
            ConfigurationParams(
                items=[ConfigurationItem(scope_uri='', section=ExampleLSPServer.CONFIGURATION_SECTION)]
            )
        )

        example_config = config[0].get('exampleConfiguration')

        ls.show_message(f'odslServer.exampleConfiguration value: {example_config}')

    except Exception as e:
        ls.show_message_log(f'Error ocurred: {e}')


@example_server.command(ExampleLSPServer.CMD_SHOW_CONFIGURATION_CALLBACK)
def show_configuration_callback(ls: ExampleLSPServer, *args):
    """Gets exampleConfiguration from the client settings using callback."""

    def _config_callback(config):
        try:
            example_config = config[0].get('exampleConfiguration')

            ls.show_message(f'odslServer.exampleConfiguration value: {example_config}')

        except Exception as e:
            ls.show_message_log(f'Error occurred: {e}')

    ls.get_configuration(
        ConfigurationParams(
            items=[ConfigurationItem(scope_uri='', section=ExampleLSPServer.CONFIGURATION_SECTION)]
        ),
        _config_callback
    )


@example_server.thread()
@example_server.command(ExampleLSPServer.CMD_SHOW_CONFIGURATION_THREAD)
def show_configuration_thread(ls: ExampleLSPServer, *args):
    """Gets exampleConfiguration from the client settings using thread pool."""
    try:
        config = ls.get_configuration(
            ConfigurationParams(
                items=[ConfigurationItem(scope_uri='', section=ExampleLSPServer.CONFIGURATION_SECTION)]
            )
        ).result(2)

        example_config = config[0].get('exampleConfiguration')

        ls.show_message(f'odslServer.exampleConfiguration value: {example_config}')

    except Exception as e:
        ls.show_message_log(f'Error occurred: {e}')


@example_server.command(ExampleLSPServer.CMD_UNREGISTER_COMPLETIONS)
async def unregister_completions(ls: ExampleLSPServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(
        unregisterations=[Unregistration(id=str(uuid.uuid4()), method=TEXT_DOCUMENT_COMPLETION)]
    )
    response = await ls.unregister_capability_async(params)
    if response is None:
        ls.show_message('Successfully unregistered completions method')
    else:
        ls.show_message('Error happened during completions unregistration.', MessageType.Error)

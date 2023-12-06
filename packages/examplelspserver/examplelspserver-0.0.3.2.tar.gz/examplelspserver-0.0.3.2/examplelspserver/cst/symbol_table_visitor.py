"""SymbolTableVisitor module."""

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
from typing import TypeVar, Generic, Dict, Optional, Callable, Any

# antlr4
from antlr4.tree.Tree import ParseTree

# user relative imports
from ..symboltable.symbol_table import ScopedSymbol, SymbolTable, P, T, VariableSymbol, RoutineSymbol, SymbolTableOptions
from ..gen.python.exampleDsl.exampleDslParser import exampleDslParser
from ..gen.python.exampleDsl.exampleDslVisitor import exampleDslVisitor


class SymbolTableVisitor(exampleDslVisitor, Generic[T]):
    _symbolTable: SymbolTable

    def __init__(self, name: str = '', ):
        super().__init__()
        self._symbolTable = SymbolTable(name, SymbolTableOptions(False))
        # TODO scope marker
        # self._scope = self._symbolTable.addNewSymbolOfType( ScopedSymbol, None )
        self._scope = None

    @property
    def symbolTable(self) -> SymbolTable:
        return self._symbolTable

    def defaultResult(self) -> SymbolTable:
        return self._symbolTable

    def visitAssignStat(self, ctx: exampleDslParser.AssignStatContext):
        self._symbolTable.add_new_symbol_of_type(VariableSymbol, self._scope, ctx.ID().getText())
        return self.visitChildren(ctx)

    # def visitFuncExpr(self, ctx: exampleDslParser.FuncExprContext):
    #     return self.withScope( ctx, RoutineSymbol, lambda: self.visitChildren( ctx ), ctx.ID().getText() )

    def withScope(self, tree: ParseTree, t: type, action: Callable, *my_args: P.args or None, **my_kwargs: P.kwargs or None) -> T:
        scope = self._symbolTable.add_new_symbol_of_type(t, self._scope, *my_args, **my_kwargs)
        scope.context = tree
        self._scope = scope
        try:
            return action()
        finally:
            self._scope = scope.parent()

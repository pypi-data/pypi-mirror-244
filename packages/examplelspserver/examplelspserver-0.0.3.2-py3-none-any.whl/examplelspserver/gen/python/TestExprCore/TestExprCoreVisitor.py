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

# Generated from TestExprCore.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .TestExprCoreParser import TestExprCoreParser
else:
    from TestExprCoreParser import TestExprCoreParser

# This class defines a complete generic visitor for a parse tree produced by TestExprCoreParser.

class TestExprCoreVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TestExprCoreParser#expression.
    def visitExpression(self, ctx:TestExprCoreParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#assignment.
    def visitAssignment(self, ctx:TestExprCoreParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#simpleExpression.
    def visitSimpleExpression(self, ctx:TestExprCoreParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#variableRef.
    def visitVariableRef(self, ctx:TestExprCoreParser.VariableRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#functionRef.
    def visitFunctionRef(self, ctx:TestExprCoreParser.FunctionRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#identifier.
    def visitIdentifier(self, ctx:TestExprCoreParser.IdentifierContext):
        return self.visitChildren(ctx)



del TestExprCoreParser
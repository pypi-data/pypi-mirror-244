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

# This class defines a complete listener for a parse tree produced by TestExprCoreParser.
class TestExprCoreListener(ParseTreeListener):

    # Enter a parse tree produced by TestExprCoreParser#expression.
    def enterExpression(self, ctx:TestExprCoreParser.ExpressionContext):
        pass

    # Exit a parse tree produced by TestExprCoreParser#expression.
    def exitExpression(self, ctx:TestExprCoreParser.ExpressionContext):
        pass


    # Enter a parse tree produced by TestExprCoreParser#assignment.
    def enterAssignment(self, ctx:TestExprCoreParser.AssignmentContext):
        pass

    # Exit a parse tree produced by TestExprCoreParser#assignment.
    def exitAssignment(self, ctx:TestExprCoreParser.AssignmentContext):
        pass


    # Enter a parse tree produced by TestExprCoreParser#simpleExpression.
    def enterSimpleExpression(self, ctx:TestExprCoreParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by TestExprCoreParser#simpleExpression.
    def exitSimpleExpression(self, ctx:TestExprCoreParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by TestExprCoreParser#variableRef.
    def enterVariableRef(self, ctx:TestExprCoreParser.VariableRefContext):
        pass

    # Exit a parse tree produced by TestExprCoreParser#variableRef.
    def exitVariableRef(self, ctx:TestExprCoreParser.VariableRefContext):
        pass


    # Enter a parse tree produced by TestExprCoreParser#functionRef.
    def enterFunctionRef(self, ctx:TestExprCoreParser.FunctionRefContext):
        pass

    # Exit a parse tree produced by TestExprCoreParser#functionRef.
    def exitFunctionRef(self, ctx:TestExprCoreParser.FunctionRefContext):
        pass


    # Enter a parse tree produced by TestExprCoreParser#identifier.
    def enterIdentifier(self, ctx:TestExprCoreParser.IdentifierContext):
        pass

    # Exit a parse tree produced by TestExprCoreParser#identifier.
    def exitIdentifier(self, ctx:TestExprCoreParser.IdentifierContext):
        pass



del TestExprCoreParser
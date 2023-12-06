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

# Generated from exampleDsl.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .exampleDslParser import exampleDslParser
else:
    from exampleDslParser import exampleDslParser

# This class defines a complete listener for a parse tree produced by exampleDslParser.
class exampleDslListener(ParseTreeListener):

    # Enter a parse tree produced by exampleDslParser#startProg.
    def enterStartProg(self, ctx:exampleDslParser.StartProgContext):
        pass

    # Exit a parse tree produced by exampleDslParser#startProg.
    def exitStartProg(self, ctx:exampleDslParser.StartProgContext):
        pass


    # Enter a parse tree produced by exampleDslParser#printExprStat.
    def enterPrintExprStat(self, ctx:exampleDslParser.PrintExprStatContext):
        pass

    # Exit a parse tree produced by exampleDslParser#printExprStat.
    def exitPrintExprStat(self, ctx:exampleDslParser.PrintExprStatContext):
        pass


    # Enter a parse tree produced by exampleDslParser#assignStat.
    def enterAssignStat(self, ctx:exampleDslParser.AssignStatContext):
        pass

    # Exit a parse tree produced by exampleDslParser#assignStat.
    def exitAssignStat(self, ctx:exampleDslParser.AssignStatContext):
        pass


    # Enter a parse tree produced by exampleDslParser#blankStat.
    def enterBlankStat(self, ctx:exampleDslParser.BlankStatContext):
        pass

    # Exit a parse tree produced by exampleDslParser#blankStat.
    def exitBlankStat(self, ctx:exampleDslParser.BlankStatContext):
        pass


    # Enter a parse tree produced by exampleDslParser#addSubExpr.
    def enterAddSubExpr(self, ctx:exampleDslParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by exampleDslParser#addSubExpr.
    def exitAddSubExpr(self, ctx:exampleDslParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by exampleDslParser#funRef.
    def enterFunRef(self, ctx:exampleDslParser.FunRefContext):
        pass

    # Exit a parse tree produced by exampleDslParser#funRef.
    def exitFunRef(self, ctx:exampleDslParser.FunRefContext):
        pass


    # Enter a parse tree produced by exampleDslParser#numberExpr.
    def enterNumberExpr(self, ctx:exampleDslParser.NumberExprContext):
        pass

    # Exit a parse tree produced by exampleDslParser#numberExpr.
    def exitNumberExpr(self, ctx:exampleDslParser.NumberExprContext):
        pass


    # Enter a parse tree produced by exampleDslParser#parensExpr.
    def enterParensExpr(self, ctx:exampleDslParser.ParensExprContext):
        pass

    # Exit a parse tree produced by exampleDslParser#parensExpr.
    def exitParensExpr(self, ctx:exampleDslParser.ParensExprContext):
        pass


    # Enter a parse tree produced by exampleDslParser#mulDivExpr.
    def enterMulDivExpr(self, ctx:exampleDslParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by exampleDslParser#mulDivExpr.
    def exitMulDivExpr(self, ctx:exampleDslParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by exampleDslParser#idRef.
    def enterIdRef(self, ctx:exampleDslParser.IdRefContext):
        pass

    # Exit a parse tree produced by exampleDslParser#idRef.
    def exitIdRef(self, ctx:exampleDslParser.IdRefContext):
        pass


    # Enter a parse tree produced by exampleDslParser#argList.
    def enterArgList(self, ctx:exampleDslParser.ArgListContext):
        pass

    # Exit a parse tree produced by exampleDslParser#argList.
    def exitArgList(self, ctx:exampleDslParser.ArgListContext):
        pass


    # Enter a parse tree produced by exampleDslParser#varExpr.
    def enterVarExpr(self, ctx:exampleDslParser.VarExprContext):
        pass

    # Exit a parse tree produced by exampleDslParser#varExpr.
    def exitVarExpr(self, ctx:exampleDslParser.VarExprContext):
        pass


    # Enter a parse tree produced by exampleDslParser#funcExpr.
    def enterFuncExpr(self, ctx:exampleDslParser.FuncExprContext):
        pass

    # Exit a parse tree produced by exampleDslParser#funcExpr.
    def exitFuncExpr(self, ctx:exampleDslParser.FuncExprContext):
        pass



del exampleDslParser
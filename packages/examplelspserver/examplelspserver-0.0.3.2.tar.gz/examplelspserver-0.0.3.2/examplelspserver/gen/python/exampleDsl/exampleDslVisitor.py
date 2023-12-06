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

# This class defines a complete generic visitor for a parse tree produced by exampleDslParser.

class exampleDslVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by exampleDslParser#startProg.
    def visitStartProg(self, ctx:exampleDslParser.StartProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#printExprStat.
    def visitPrintExprStat(self, ctx:exampleDslParser.PrintExprStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#assignStat.
    def visitAssignStat(self, ctx:exampleDslParser.AssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#blankStat.
    def visitBlankStat(self, ctx:exampleDslParser.BlankStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#addSubExpr.
    def visitAddSubExpr(self, ctx:exampleDslParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#funRef.
    def visitFunRef(self, ctx:exampleDslParser.FunRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#numberExpr.
    def visitNumberExpr(self, ctx:exampleDslParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#parensExpr.
    def visitParensExpr(self, ctx:exampleDslParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#mulDivExpr.
    def visitMulDivExpr(self, ctx:exampleDslParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#idRef.
    def visitIdRef(self, ctx:exampleDslParser.IdRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#argList.
    def visitArgList(self, ctx:exampleDslParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#varExpr.
    def visitVarExpr(self, ctx:exampleDslParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#funcExpr.
    def visitFuncExpr(self, ctx:exampleDslParser.FuncExprContext):
        return self.visitChildren(ctx)



del exampleDslParser
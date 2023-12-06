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
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,12,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,5,
        0,14,8,0,10,0,12,0,17,9,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,
        1,28,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,38,8,2,1,2,1,2,1,2,
        1,2,1,2,1,2,5,2,46,8,2,10,2,12,2,49,9,2,1,3,1,3,1,3,5,3,54,8,3,10,
        3,12,3,57,9,3,1,4,1,4,1,5,1,5,1,5,3,5,64,8,5,1,5,1,5,1,5,0,1,4,6,
        0,2,4,6,8,10,0,2,1,0,1,2,1,0,3,4,71,0,15,1,0,0,0,2,27,1,0,0,0,4,
        37,1,0,0,0,6,50,1,0,0,0,8,58,1,0,0,0,10,60,1,0,0,0,12,14,3,2,1,0,
        13,12,1,0,0,0,14,17,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,1,1,0,
        0,0,17,15,1,0,0,0,18,19,3,4,2,0,19,20,5,12,0,0,20,28,1,0,0,0,21,
        22,5,10,0,0,22,23,5,7,0,0,23,24,3,4,2,0,24,25,5,12,0,0,25,28,1,0,
        0,0,26,28,5,12,0,0,27,18,1,0,0,0,27,21,1,0,0,0,27,26,1,0,0,0,28,
        3,1,0,0,0,29,30,6,2,-1,0,30,31,5,5,0,0,31,32,3,4,2,0,32,33,5,6,0,
        0,33,38,1,0,0,0,34,38,5,11,0,0,35,38,3,10,5,0,36,38,3,8,4,0,37,29,
        1,0,0,0,37,34,1,0,0,0,37,35,1,0,0,0,37,36,1,0,0,0,38,47,1,0,0,0,
        39,40,10,6,0,0,40,41,7,0,0,0,41,46,3,4,2,7,42,43,10,5,0,0,43,44,
        7,1,0,0,44,46,3,4,2,6,45,39,1,0,0,0,45,42,1,0,0,0,46,49,1,0,0,0,
        47,45,1,0,0,0,47,48,1,0,0,0,48,5,1,0,0,0,49,47,1,0,0,0,50,55,3,4,
        2,0,51,52,5,8,0,0,52,54,3,4,2,0,53,51,1,0,0,0,54,57,1,0,0,0,55,53,
        1,0,0,0,55,56,1,0,0,0,56,7,1,0,0,0,57,55,1,0,0,0,58,59,5,10,0,0,
        59,9,1,0,0,0,60,61,5,10,0,0,61,63,5,5,0,0,62,64,3,6,3,0,63,62,1,
        0,0,0,63,64,1,0,0,0,64,65,1,0,0,0,65,66,5,6,0,0,66,11,1,0,0,0,7,
        15,27,37,45,47,55,63
    ]

class exampleDslParser ( Parser ):

    grammarFileName = "exampleDsl.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'*'", "'/'", "'+'", "'-'", "'('", "')'", 
                     "'='", "','" ]

    symbolicNames = [ "<INVALID>", "OP_MUL", "OP_DIV", "OP_ADD", "OP_SUB", 
                      "PAR_L", "PAR_R", "EQUAL", "SEP", "WS", "ID", "NUM", 
                      "NEWLINE" ]

    RULE_prog = 0
    RULE_stat = 1
    RULE_expr = 2
    RULE_exprList = 3
    RULE_variableRef = 4
    RULE_functionRef = 5

    ruleNames =  [ "prog", "stat", "expr", "exprList", "variableRef", "functionRef" ]

    EOF = Token.EOF
    OP_MUL=1
    OP_DIV=2
    OP_ADD=3
    OP_SUB=4
    PAR_L=5
    PAR_R=6
    EQUAL=7
    SEP=8
    WS=9
    ID=10
    NUM=11
    NEWLINE=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return exampleDslParser.RULE_prog

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StartProgContext(ProgContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ProgContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(exampleDslParser.StatContext)
            else:
                return self.getTypedRuleContext(exampleDslParser.StatContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStartProg" ):
                listener.enterStartProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStartProg" ):
                listener.exitStartProg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStartProg" ):
                return visitor.visitStartProg(self)
            else:
                return visitor.visitChildren(self)



    def prog(self):

        localctx = exampleDslParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            localctx = exampleDslParser.StartProgContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 7200) != 0):
                self.state = 12
                self.stat()
                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return exampleDslParser.RULE_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PrintExprStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(exampleDslParser.ExprContext,0)

        def NEWLINE(self):
            return self.getToken(exampleDslParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintExprStat" ):
                listener.enterPrintExprStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintExprStat" ):
                listener.exitPrintExprStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintExprStat" ):
                return visitor.visitPrintExprStat(self)
            else:
                return visitor.visitChildren(self)


    class BlankStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEWLINE(self):
            return self.getToken(exampleDslParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlankStat" ):
                listener.enterBlankStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlankStat" ):
                listener.exitBlankStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlankStat" ):
                return visitor.visitBlankStat(self)
            else:
                return visitor.visitChildren(self)


    class AssignStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(exampleDslParser.ID, 0)
        def EQUAL(self):
            return self.getToken(exampleDslParser.EQUAL, 0)
        def expr(self):
            return self.getTypedRuleContext(exampleDslParser.ExprContext,0)

        def NEWLINE(self):
            return self.getToken(exampleDslParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStat" ):
                listener.enterAssignStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStat" ):
                listener.exitAssignStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStat" ):
                return visitor.visitAssignStat(self)
            else:
                return visitor.visitChildren(self)



    def stat(self):

        localctx = exampleDslParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stat)
        try:
            self.state = 27
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = exampleDslParser.PrintExprStatContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self.expr(0)
                self.state = 19
                self.match(exampleDslParser.NEWLINE)
                pass

            elif la_ == 2:
                localctx = exampleDslParser.AssignStatContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self.match(exampleDslParser.ID)
                self.state = 22
                self.match(exampleDslParser.EQUAL)
                self.state = 23
                self.expr(0)
                self.state = 24
                self.match(exampleDslParser.NEWLINE)
                pass

            elif la_ == 3:
                localctx = exampleDslParser.BlankStatContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 26
                self.match(exampleDslParser.NEWLINE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return exampleDslParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AddSubExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(exampleDslParser.ExprContext)
            else:
                return self.getTypedRuleContext(exampleDslParser.ExprContext,i)

        def OP_ADD(self):
            return self.getToken(exampleDslParser.OP_ADD, 0)
        def OP_SUB(self):
            return self.getToken(exampleDslParser.OP_SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSubExpr" ):
                listener.enterAddSubExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSubExpr" ):
                listener.exitAddSubExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddSubExpr" ):
                return visitor.visitAddSubExpr(self)
            else:
                return visitor.visitChildren(self)


    class FunRefContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionRef(self):
            return self.getTypedRuleContext(exampleDslParser.FunctionRefContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunRef" ):
                listener.enterFunRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunRef" ):
                listener.exitFunRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunRef" ):
                return visitor.visitFunRef(self)
            else:
                return visitor.visitChildren(self)


    class NumberExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprContext
            super().__init__(parser)
            self.value = None # Token
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(exampleDslParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberExpr" ):
                listener.enterNumberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberExpr" ):
                listener.exitNumberExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberExpr" ):
                return visitor.visitNumberExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParensExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PAR_L(self):
            return self.getToken(exampleDslParser.PAR_L, 0)
        def expr(self):
            return self.getTypedRuleContext(exampleDslParser.ExprContext,0)

        def PAR_R(self):
            return self.getToken(exampleDslParser.PAR_R, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParensExpr" ):
                listener.enterParensExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParensExpr" ):
                listener.exitParensExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParensExpr" ):
                return visitor.visitParensExpr(self)
            else:
                return visitor.visitChildren(self)


    class MulDivExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(exampleDslParser.ExprContext)
            else:
                return self.getTypedRuleContext(exampleDslParser.ExprContext,i)

        def OP_MUL(self):
            return self.getToken(exampleDslParser.OP_MUL, 0)
        def OP_DIV(self):
            return self.getToken(exampleDslParser.OP_DIV, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDivExpr" ):
                listener.enterMulDivExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDivExpr" ):
                listener.exitMulDivExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulDivExpr" ):
                return visitor.visitMulDivExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdRefContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variableRef(self):
            return self.getTypedRuleContext(exampleDslParser.VariableRefContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdRef" ):
                listener.enterIdRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdRef" ):
                listener.exitIdRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdRef" ):
                return visitor.visitIdRef(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = exampleDslParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = exampleDslParser.ParensExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 30
                self.match(exampleDslParser.PAR_L)
                self.state = 31
                self.expr(0)
                self.state = 32
                self.match(exampleDslParser.PAR_R)
                pass

            elif la_ == 2:
                localctx = exampleDslParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 34
                localctx.value = self.match(exampleDslParser.NUM)
                pass

            elif la_ == 3:
                localctx = exampleDslParser.FunRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 35
                self.functionRef()
                pass

            elif la_ == 4:
                localctx = exampleDslParser.IdRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 36
                self.variableRef()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 47
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 45
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = exampleDslParser.MulDivExprContext(self, exampleDslParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 39
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 40
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==1 or _la==2):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 41
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = exampleDslParser.AddSubExprContext(self, exampleDslParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 42
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 43
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==3 or _la==4):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 44
                        localctx.right = self.expr(6)
                        pass

             
                self.state = 49
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return exampleDslParser.RULE_exprList

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ArgListContext(ExprListContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.ExprListContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(exampleDslParser.ExprContext)
            else:
                return self.getTypedRuleContext(exampleDslParser.ExprContext,i)

        def SEP(self, i:int=None):
            if i is None:
                return self.getTokens(exampleDslParser.SEP)
            else:
                return self.getToken(exampleDslParser.SEP, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgList" ):
                listener.enterArgList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgList" ):
                listener.exitArgList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgList" ):
                return visitor.visitArgList(self)
            else:
                return visitor.visitChildren(self)



    def exprList(self):

        localctx = exampleDslParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_exprList)
        self._la = 0 # Token type
        try:
            localctx = exampleDslParser.ArgListContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.expr(0)
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==8:
                self.state = 51
                self.match(exampleDslParser.SEP)
                self.state = 52
                self.expr(0)
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return exampleDslParser.RULE_variableRef

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class VarExprContext(VariableRefContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.VariableRefContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(exampleDslParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarExpr" ):
                listener.enterVarExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarExpr" ):
                listener.exitVarExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarExpr" ):
                return visitor.visitVarExpr(self)
            else:
                return visitor.visitChildren(self)



    def variableRef(self):

        localctx = exampleDslParser.VariableRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_variableRef)
        try:
            localctx = exampleDslParser.VarExprContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(exampleDslParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return exampleDslParser.RULE_functionRef

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FuncExprContext(FunctionRefContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a exampleDslParser.FunctionRefContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(exampleDslParser.ID, 0)
        def PAR_L(self):
            return self.getToken(exampleDslParser.PAR_L, 0)
        def PAR_R(self):
            return self.getToken(exampleDslParser.PAR_R, 0)
        def exprList(self):
            return self.getTypedRuleContext(exampleDslParser.ExprListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncExpr" ):
                listener.enterFuncExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncExpr" ):
                listener.exitFuncExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncExpr" ):
                return visitor.visitFuncExpr(self)
            else:
                return visitor.visitChildren(self)



    def functionRef(self):

        localctx = exampleDslParser.FunctionRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_functionRef)
        self._la = 0 # Token type
        try:
            localctx = exampleDslParser.FuncExprContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(exampleDslParser.ID)
            self.state = 61
            self.match(exampleDslParser.PAR_L)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3104) != 0):
                self.state = 62
                self.exprList()


            self.state = 65
            self.match(exampleDslParser.PAR_R)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         





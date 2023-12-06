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
        4,1,11,46,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,3,0,15,8,0,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,3,2,25,8,2,1,2,1,2,
        1,2,1,2,1,2,1,2,5,2,33,8,2,10,2,12,2,36,9,2,1,3,1,3,1,4,1,4,1,4,
        1,4,1,5,1,5,1,5,0,1,4,6,0,2,4,6,8,10,0,3,1,0,1,2,1,0,3,4,1,0,5,6,
        43,0,14,1,0,0,0,2,16,1,0,0,0,4,24,1,0,0,0,6,37,1,0,0,0,8,39,1,0,
        0,0,10,43,1,0,0,0,12,15,3,2,1,0,13,15,3,4,2,0,14,12,1,0,0,0,14,13,
        1,0,0,0,15,1,1,0,0,0,16,17,7,0,0,0,17,18,5,10,0,0,18,19,5,7,0,0,
        19,20,3,4,2,0,20,3,1,0,0,0,21,22,6,2,-1,0,22,25,3,6,3,0,23,25,3,
        8,4,0,24,21,1,0,0,0,24,23,1,0,0,0,25,34,1,0,0,0,26,27,10,4,0,0,27,
        28,7,1,0,0,28,33,3,4,2,5,29,30,10,3,0,0,30,31,7,2,0,0,31,33,3,4,
        2,4,32,26,1,0,0,0,32,29,1,0,0,0,33,36,1,0,0,0,34,32,1,0,0,0,34,35,
        1,0,0,0,35,5,1,0,0,0,36,34,1,0,0,0,37,38,3,10,5,0,38,7,1,0,0,0,39,
        40,3,10,5,0,40,41,5,8,0,0,41,42,5,9,0,0,42,9,1,0,0,0,43,44,5,10,
        0,0,44,11,1,0,0,0,4,14,24,32,34
    ]

class TestExprCoreParser ( Parser ):

    grammarFileName = "TestExprCore.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'+'", "'-'", 
                     "'*'", "'/'", "'='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "VAR", "LET", "PLUS", "MINUS", "MULTIPLY", 
                      "DIVIDE", "EQUAL", "OPEN_PAR", "CLOSE_PAR", "ID", 
                      "WS" ]

    RULE_expression = 0
    RULE_assignment = 1
    RULE_simpleExpression = 2
    RULE_variableRef = 3
    RULE_functionRef = 4
    RULE_identifier = 5

    ruleNames =  [ "expression", "assignment", "simpleExpression", "variableRef", 
                   "functionRef", "identifier" ]

    EOF = Token.EOF
    VAR=1
    LET=2
    PLUS=3
    MINUS=4
    MULTIPLY=5
    DIVIDE=6
    EQUAL=7
    OPEN_PAR=8
    CLOSE_PAR=9
    ID=10
    WS=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(TestExprCoreParser.AssignmentContext,0)


        def simpleExpression(self):
            return self.getTypedRuleContext(TestExprCoreParser.SimpleExpressionContext,0)


        def getRuleIndex(self):
            return TestExprCoreParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = TestExprCoreParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_expression)
        try:
            self.state = 14
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 12
                self.assignment()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 13
                self.simpleExpression(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(TestExprCoreParser.ID, 0)

        def EQUAL(self):
            return self.getToken(TestExprCoreParser.EQUAL, 0)

        def simpleExpression(self):
            return self.getTypedRuleContext(TestExprCoreParser.SimpleExpressionContext,0)


        def VAR(self):
            return self.getToken(TestExprCoreParser.VAR, 0)

        def LET(self):
            return self.getToken(TestExprCoreParser.LET, 0)

        def getRuleIndex(self):
            return TestExprCoreParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = TestExprCoreParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_assignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            _la = self._input.LA(1)
            if not(_la==1 or _la==2):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 17
            self.match(TestExprCoreParser.ID)
            self.state = 18
            self.match(TestExprCoreParser.EQUAL)
            self.state = 19
            self.simpleExpression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableRef(self):
            return self.getTypedRuleContext(TestExprCoreParser.VariableRefContext,0)


        def functionRef(self):
            return self.getTypedRuleContext(TestExprCoreParser.FunctionRefContext,0)


        def simpleExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TestExprCoreParser.SimpleExpressionContext)
            else:
                return self.getTypedRuleContext(TestExprCoreParser.SimpleExpressionContext,i)


        def PLUS(self):
            return self.getToken(TestExprCoreParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(TestExprCoreParser.MINUS, 0)

        def MULTIPLY(self):
            return self.getToken(TestExprCoreParser.MULTIPLY, 0)

        def DIVIDE(self):
            return self.getToken(TestExprCoreParser.DIVIDE, 0)

        def getRuleIndex(self):
            return TestExprCoreParser.RULE_simpleExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleExpression" ):
                listener.enterSimpleExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleExpression" ):
                listener.exitSimpleExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleExpression" ):
                return visitor.visitSimpleExpression(self)
            else:
                return visitor.visitChildren(self)



    def simpleExpression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TestExprCoreParser.SimpleExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_simpleExpression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 22
                self.variableRef()
                pass

            elif la_ == 2:
                self.state = 23
                self.functionRef()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 34
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 32
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = TestExprCoreParser.SimpleExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_simpleExpression)
                        self.state = 26
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 27
                        _la = self._input.LA(1)
                        if not(_la==3 or _la==4):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 28
                        self.simpleExpression(5)
                        pass

                    elif la_ == 2:
                        localctx = TestExprCoreParser.SimpleExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_simpleExpression)
                        self.state = 29
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 30
                        _la = self._input.LA(1)
                        if not(_la==5 or _la==6):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 31
                        self.simpleExpression(4)
                        pass

             
                self.state = 36
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class VariableRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(TestExprCoreParser.IdentifierContext,0)


        def getRuleIndex(self):
            return TestExprCoreParser.RULE_variableRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableRef" ):
                listener.enterVariableRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableRef" ):
                listener.exitVariableRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableRef" ):
                return visitor.visitVariableRef(self)
            else:
                return visitor.visitChildren(self)




    def variableRef(self):

        localctx = TestExprCoreParser.VariableRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_variableRef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.identifier()
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

        def identifier(self):
            return self.getTypedRuleContext(TestExprCoreParser.IdentifierContext,0)


        def OPEN_PAR(self):
            return self.getToken(TestExprCoreParser.OPEN_PAR, 0)

        def CLOSE_PAR(self):
            return self.getToken(TestExprCoreParser.CLOSE_PAR, 0)

        def getRuleIndex(self):
            return TestExprCoreParser.RULE_functionRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionRef" ):
                listener.enterFunctionRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionRef" ):
                listener.exitFunctionRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionRef" ):
                return visitor.visitFunctionRef(self)
            else:
                return visitor.visitChildren(self)




    def functionRef(self):

        localctx = TestExprCoreParser.FunctionRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_functionRef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.identifier()
            self.state = 40
            self.match(TestExprCoreParser.OPEN_PAR)
            self.state = 41
            self.match(TestExprCoreParser.CLOSE_PAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(TestExprCoreParser.ID, 0)

        def getRuleIndex(self):
            return TestExprCoreParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def identifier(self):

        localctx = TestExprCoreParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(TestExprCoreParser.ID)
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
        self._predicates[2] = self.simpleExpression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def simpleExpression_sempred(self, localctx:SimpleExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         





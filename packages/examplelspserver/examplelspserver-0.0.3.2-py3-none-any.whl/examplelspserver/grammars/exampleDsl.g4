/**
 *  Copyright (C) 2021 OceanDSL (https://oceandsl.uni-kiel.de)
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Grammars always start with a grammar header. This grammar is called
 *  exampleDsl and must match the filename: exampleDsl.g4
 *
 *  This grammar serves as a test grammar for development.
 *
 *  author Armin Mackensen, Sven Gundlach
 */
grammar exampleDsl;

/** imports include all rules, imported rules are overwritten by existing rules */
import CommonLexerRules; // import CommonLexerRules.g4

/** parser rules start with lowercase letters */

/** The start rule; begin parsing here */
prog:   stat*                                   # startProg // possible empty statement
    ;

stat:   expr NEWLINE                            # printExprStat /** label can be any identifier that doesn't collide with a rule name */
    |   ID EQUAL expr NEWLINE                   # assignStat
    |   NEWLINE                                 # blankStat
    ;

expr:   left=expr op=(OP_MUL|OP_DIV) right=expr # mulDivExpr /** token attributes (e.g. left and right) are reference labels to distinguish ambiguous token instances references */
    |   left=expr op=(OP_ADD|OP_SUB) right=expr # addSubExpr
    |   PAR_L expr PAR_R                        # parensExpr
    |   value=NUM                               # numberExpr
    |   functionRef                             # funRef
    |   variableRef                             # idRef
    ;

exprList :   expr(SEP expr)*                    # argList // list of function arguments
         ;

/** rules to lookup in the symboltable */
variableRef: ID                                 # varExpr
           ;
functionRef: ID PAR_L exprList? PAR_R           # funcExpr // function call like f(), f(x), f(1,2)
           ;


/** lexer rules start with uppercase letters */
OP_MUL  :   '*' ;                                       // assigns token name to '*' used above in grammar
OP_DIV  :   '/' ;
OP_ADD  :   '+' ;
OP_SUB  :   '-' ;
PAR_L   :   '(' ;                                       // match left parenthesis
PAR_R   :   ')' ;                                       // match right parenthesis
EQUAL   :   '=' ;                                       // match equal sign
SEP     :   ',' ;                                       // match separator

/** overwrite CommonLexerRules.g4 */
WS      :   [ \t]+ -> channel(HIDDEN) ;                 // hide spaces and tabs from the parser but generate tokens

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
 *  TestGrammar and must match the filename: TestGrammar.g4
 *
 *  This grammar serves as a test grammar for presentation.
 *
 *  author Sven Gundlach
 */
grammar allstar;

/** parser rules start with lowercase letters */

/** The start rule; begin parsing here */
stat    : expr ';'
        | ID '(' ')' ';'
        ;

expr    : ID '(' ')'
        | INT
        ;

// lexer rules with uppercase letters
ID      :   [a-zA-Z]+ ;                                 // match identifiers <label id="code.tour.expr.3"/>
NUM     :   '-'? ('.' DIG+ | DIG+ ('.' DIG*)? EXP? ) ;  // match numbers
INT :   '0' | [1-9] DIG* ;                              // match integers without leading zeros
/** fragments generate no lexer tokens */
fragment EXP :   [eE] [+\-]? INT ;                      // fragment match exponent
fragment DIG :   [0-9] ;                                // fragment match digits
/** Grammars always start with a grammar header. This grammar is called
 *  TestExpr and must match the filename: TestExpr.g4
 */
grammar TestExpr;

import CommonLexerRules; // includes all rules from CommonLexerRules.g4

/** The start rule; begin parsing here. */
// parser rules start with lowercase letters
prog:   stat+ ;

stat:   expr NEWLINE                # printExpr /** label can be any identifier  that doesn't collide with a rule name **/
    |   ID '=' expr NEWLINE         # assign
    |   NEWLINE                     # blank
    ;

expr:   expr op=('*'|'/') expr      # MulDiv
    |   expr op=('+'|'-') expr      # AddSub
    |   INT                         # int
    |   ID                          # id
    |   '(' expr ')'                # parens
    ;

// lexer rules with uppercase letters
MUL :   '*' ; // assigns token name to '*' used above in grammar
DIV :   '/' ;
ADD :   '+' ;
SUB :   '-' ;
ID  :   [a-zA-Z]+ ;      // match identifiers
INT :   [0-9]+ ;         // match integers
NEWLINE:'\r'? '\n' ;     // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ; // toss out whitespace

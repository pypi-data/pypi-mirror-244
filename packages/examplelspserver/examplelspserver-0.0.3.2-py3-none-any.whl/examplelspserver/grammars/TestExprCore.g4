/** Grammars always start with a grammar header. This grammar is called
 *  TestExprCore and must match the filename: TestExprCore.g4
 */
grammar TestExprCore;

@eader {
/* eslint-disable @typescript-eslint/no-unused-vars, no-useless-escape */
}

/** The start rule; begin parsing here. */
// parser rules start with lowercase letters
expression: assignment | simpleExpression
          ;

assignment: (VAR | LET) ID EQUAL simpleExpression
          ;

simpleExpression: simpleExpression (PLUS | MINUS) simpleExpression
                | simpleExpression (MULTIPLY | DIVIDE) simpleExpression
                | variableRef
                | functionRef
                ;

variableRef: identifier
           ;

functionRef: identifier OPEN_PAR CLOSE_PAR
           ;

identifier: ID
          ;

// lexer rules with uppercase letters
VAR: [vV] [aA] [rR];
LET: [lL] [eE] [tT];

PLUS:      '+'; // assigns token name to '+' used above in grammar
MINUS:     '-';
MULTIPLY:  '*';
DIVIDE:    '/';
EQUAL:     '=';
OPEN_PAR:  '(';
CLOSE_PAR: ')';
ID:        [a-zA-Z] [a-zA-Z0-9_]*;          // match identifiers
WS:        [ \n\r\t] -> channel(HIDDEN);    // hide spaces, carriage returns, newlines and tabs from the parser but generate tokens aka toss out whitespace
/*
 * Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Generated from TestExprCore.g4 by ANTLR 4.13.0
package TestExprCore;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link TestExprCoreParser}.
 */
public interface TestExprCoreListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link TestExprCoreParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(TestExprCoreParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link TestExprCoreParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(TestExprCoreParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link TestExprCoreParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(TestExprCoreParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link TestExprCoreParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(TestExprCoreParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link TestExprCoreParser#simpleExpression}.
	 * @param ctx the parse tree
	 */
	void enterSimpleExpression(TestExprCoreParser.SimpleExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link TestExprCoreParser#simpleExpression}.
	 * @param ctx the parse tree
	 */
	void exitSimpleExpression(TestExprCoreParser.SimpleExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link TestExprCoreParser#variableRef}.
	 * @param ctx the parse tree
	 */
	void enterVariableRef(TestExprCoreParser.VariableRefContext ctx);
	/**
	 * Exit a parse tree produced by {@link TestExprCoreParser#variableRef}.
	 * @param ctx the parse tree
	 */
	void exitVariableRef(TestExprCoreParser.VariableRefContext ctx);
	/**
	 * Enter a parse tree produced by {@link TestExprCoreParser#functionRef}.
	 * @param ctx the parse tree
	 */
	void enterFunctionRef(TestExprCoreParser.FunctionRefContext ctx);
	/**
	 * Exit a parse tree produced by {@link TestExprCoreParser#functionRef}.
	 * @param ctx the parse tree
	 */
	void exitFunctionRef(TestExprCoreParser.FunctionRefContext ctx);
	/**
	 * Enter a parse tree produced by {@link TestExprCoreParser#identifier}.
	 * @param ctx the parse tree
	 */
	void enterIdentifier(TestExprCoreParser.IdentifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link TestExprCoreParser#identifier}.
	 * @param ctx the parse tree
	 */
	void exitIdentifier(TestExprCoreParser.IdentifierContext ctx);
}
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

// Generated from exampleDsl.g4 by ANTLR 4.13.0
package exampleDsl;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link exampleDslParser}.
 */
public interface exampleDslListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by the {@code startProg}
	 * labeled alternative in {@link exampleDslParser#prog}.
	 * @param ctx the parse tree
	 */
	void enterStartProg(exampleDslParser.StartProgContext ctx);
	/**
	 * Exit a parse tree produced by the {@code startProg}
	 * labeled alternative in {@link exampleDslParser#prog}.
	 * @param ctx the parse tree
	 */
	void exitStartProg(exampleDslParser.StartProgContext ctx);
	/**
	 * Enter a parse tree produced by the {@code printExprStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterPrintExprStat(exampleDslParser.PrintExprStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code printExprStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitPrintExprStat(exampleDslParser.PrintExprStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterAssignStat(exampleDslParser.AssignStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitAssignStat(exampleDslParser.AssignStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code blankStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterBlankStat(exampleDslParser.BlankStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code blankStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitBlankStat(exampleDslParser.BlankStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAddSubExpr(exampleDslParser.AddSubExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAddSubExpr(exampleDslParser.AddSubExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code funRef}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterFunRef(exampleDslParser.FunRefContext ctx);
	/**
	 * Exit a parse tree produced by the {@code funRef}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitFunRef(exampleDslParser.FunRefContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNumberExpr(exampleDslParser.NumberExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNumberExpr(exampleDslParser.NumberExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParensExpr(exampleDslParser.ParensExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParensExpr(exampleDslParser.ParensExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMulDivExpr(exampleDslParser.MulDivExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMulDivExpr(exampleDslParser.MulDivExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code idRef}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIdRef(exampleDslParser.IdRefContext ctx);
	/**
	 * Exit a parse tree produced by the {@code idRef}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIdRef(exampleDslParser.IdRefContext ctx);
	/**
	 * Enter a parse tree produced by the {@code argList}
	 * labeled alternative in {@link exampleDslParser#exprList}.
	 * @param ctx the parse tree
	 */
	void enterArgList(exampleDslParser.ArgListContext ctx);
	/**
	 * Exit a parse tree produced by the {@code argList}
	 * labeled alternative in {@link exampleDslParser#exprList}.
	 * @param ctx the parse tree
	 */
	void exitArgList(exampleDslParser.ArgListContext ctx);
	/**
	 * Enter a parse tree produced by the {@code varExpr}
	 * labeled alternative in {@link exampleDslParser#variableRef}.
	 * @param ctx the parse tree
	 */
	void enterVarExpr(exampleDslParser.VarExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code varExpr}
	 * labeled alternative in {@link exampleDslParser#variableRef}.
	 * @param ctx the parse tree
	 */
	void exitVarExpr(exampleDslParser.VarExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link exampleDslParser#functionRef}.
	 * @param ctx the parse tree
	 */
	void enterFuncExpr(exampleDslParser.FuncExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link exampleDslParser#functionRef}.
	 * @param ctx the parse tree
	 */
	void exitFuncExpr(exampleDslParser.FuncExprContext ctx);
}
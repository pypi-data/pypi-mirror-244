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
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class exampleDslLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.0", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		OP_MUL=1, OP_DIV=2, OP_ADD=3, OP_SUB=4, PAR_L=5, PAR_R=6, EQUAL=7, SEP=8, 
		WS=9, ID=10, NUM=11, NEWLINE=12;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"OP_MUL", "OP_DIV", "OP_ADD", "OP_SUB", "PAR_L", "PAR_R", "EQUAL", "SEP", 
			"WS", "ID", "NUM", "INT", "EXP", "DIG", "NEWLINE"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'*'", "'/'", "'+'", "'-'", "'('", "')'", "'='", "','"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "OP_MUL", "OP_DIV", "OP_ADD", "OP_SUB", "PAR_L", "PAR_R", "EQUAL", 
			"SEP", "WS", "ID", "NUM", "NEWLINE"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public exampleDslLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "exampleDsl.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\fn\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b"+
		"\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001"+
		"\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001"+
		"\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001\b\u0004\b1\b\b\u000b"+
		"\b\f\b2\u0001\b\u0001\b\u0001\t\u0004\t8\b\t\u000b\t\f\t9\u0001\n\u0003"+
		"\n=\b\n\u0001\n\u0001\n\u0004\nA\b\n\u000b\n\f\nB\u0001\n\u0004\nF\b\n"+
		"\u000b\n\f\nG\u0001\n\u0001\n\u0005\nL\b\n\n\n\f\nO\t\n\u0003\nQ\b\n\u0001"+
		"\n\u0003\nT\b\n\u0003\nV\b\n\u0001\u000b\u0001\u000b\u0001\u000b\u0005"+
		"\u000b[\b\u000b\n\u000b\f\u000b^\t\u000b\u0003\u000b`\b\u000b\u0001\f"+
		"\u0001\f\u0003\fd\b\f\u0001\f\u0001\f\u0001\r\u0001\r\u0001\u000e\u0003"+
		"\u000ek\b\u000e\u0001\u000e\u0001\u000e\u0000\u0000\u000f\u0001\u0001"+
		"\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005\u000b\u0006\r\u0007\u000f"+
		"\b\u0011\t\u0013\n\u0015\u000b\u0017\u0000\u0019\u0000\u001b\u0000\u001d"+
		"\f\u0001\u0000\u0006\u0002\u0000\t\t  \u0002\u0000AZaz\u0001\u000019\u0002"+
		"\u0000EEee\u0002\u0000++--\u0001\u000009w\u0000\u0001\u0001\u0000\u0000"+
		"\u0000\u0000\u0003\u0001\u0000\u0000\u0000\u0000\u0005\u0001\u0000\u0000"+
		"\u0000\u0000\u0007\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000"+
		"\u0000\u000b\u0001\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000"+
		"\u000f\u0001\u0000\u0000\u0000\u0000\u0011\u0001\u0000\u0000\u0000\u0000"+
		"\u0013\u0001\u0000\u0000\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000"+
		"\u001d\u0001\u0000\u0000\u0000\u0001\u001f\u0001\u0000\u0000\u0000\u0003"+
		"!\u0001\u0000\u0000\u0000\u0005#\u0001\u0000\u0000\u0000\u0007%\u0001"+
		"\u0000\u0000\u0000\t\'\u0001\u0000\u0000\u0000\u000b)\u0001\u0000\u0000"+
		"\u0000\r+\u0001\u0000\u0000\u0000\u000f-\u0001\u0000\u0000\u0000\u0011"+
		"0\u0001\u0000\u0000\u0000\u00137\u0001\u0000\u0000\u0000\u0015<\u0001"+
		"\u0000\u0000\u0000\u0017_\u0001\u0000\u0000\u0000\u0019a\u0001\u0000\u0000"+
		"\u0000\u001bg\u0001\u0000\u0000\u0000\u001dj\u0001\u0000\u0000\u0000\u001f"+
		" \u0005*\u0000\u0000 \u0002\u0001\u0000\u0000\u0000!\"\u0005/\u0000\u0000"+
		"\"\u0004\u0001\u0000\u0000\u0000#$\u0005+\u0000\u0000$\u0006\u0001\u0000"+
		"\u0000\u0000%&\u0005-\u0000\u0000&\b\u0001\u0000\u0000\u0000\'(\u0005"+
		"(\u0000\u0000(\n\u0001\u0000\u0000\u0000)*\u0005)\u0000\u0000*\f\u0001"+
		"\u0000\u0000\u0000+,\u0005=\u0000\u0000,\u000e\u0001\u0000\u0000\u0000"+
		"-.\u0005,\u0000\u0000.\u0010\u0001\u0000\u0000\u0000/1\u0007\u0000\u0000"+
		"\u00000/\u0001\u0000\u0000\u000012\u0001\u0000\u0000\u000020\u0001\u0000"+
		"\u0000\u000023\u0001\u0000\u0000\u000034\u0001\u0000\u0000\u000045\u0006"+
		"\b\u0000\u00005\u0012\u0001\u0000\u0000\u000068\u0007\u0001\u0000\u0000"+
		"76\u0001\u0000\u0000\u000089\u0001\u0000\u0000\u000097\u0001\u0000\u0000"+
		"\u00009:\u0001\u0000\u0000\u0000:\u0014\u0001\u0000\u0000\u0000;=\u0005"+
		"-\u0000\u0000<;\u0001\u0000\u0000\u0000<=\u0001\u0000\u0000\u0000=U\u0001"+
		"\u0000\u0000\u0000>@\u0005.\u0000\u0000?A\u0003\u001b\r\u0000@?\u0001"+
		"\u0000\u0000\u0000AB\u0001\u0000\u0000\u0000B@\u0001\u0000\u0000\u0000"+
		"BC\u0001\u0000\u0000\u0000CV\u0001\u0000\u0000\u0000DF\u0003\u001b\r\u0000"+
		"ED\u0001\u0000\u0000\u0000FG\u0001\u0000\u0000\u0000GE\u0001\u0000\u0000"+
		"\u0000GH\u0001\u0000\u0000\u0000HP\u0001\u0000\u0000\u0000IM\u0005.\u0000"+
		"\u0000JL\u0003\u001b\r\u0000KJ\u0001\u0000\u0000\u0000LO\u0001\u0000\u0000"+
		"\u0000MK\u0001\u0000\u0000\u0000MN\u0001\u0000\u0000\u0000NQ\u0001\u0000"+
		"\u0000\u0000OM\u0001\u0000\u0000\u0000PI\u0001\u0000\u0000\u0000PQ\u0001"+
		"\u0000\u0000\u0000QS\u0001\u0000\u0000\u0000RT\u0003\u0019\f\u0000SR\u0001"+
		"\u0000\u0000\u0000ST\u0001\u0000\u0000\u0000TV\u0001\u0000\u0000\u0000"+
		"U>\u0001\u0000\u0000\u0000UE\u0001\u0000\u0000\u0000V\u0016\u0001\u0000"+
		"\u0000\u0000W`\u00050\u0000\u0000X\\\u0007\u0002\u0000\u0000Y[\u0003\u001b"+
		"\r\u0000ZY\u0001\u0000\u0000\u0000[^\u0001\u0000\u0000\u0000\\Z\u0001"+
		"\u0000\u0000\u0000\\]\u0001\u0000\u0000\u0000]`\u0001\u0000\u0000\u0000"+
		"^\\\u0001\u0000\u0000\u0000_W\u0001\u0000\u0000\u0000_X\u0001\u0000\u0000"+
		"\u0000`\u0018\u0001\u0000\u0000\u0000ac\u0007\u0003\u0000\u0000bd\u0007"+
		"\u0004\u0000\u0000cb\u0001\u0000\u0000\u0000cd\u0001\u0000\u0000\u0000"+
		"de\u0001\u0000\u0000\u0000ef\u0003\u0017\u000b\u0000f\u001a\u0001\u0000"+
		"\u0000\u0000gh\u0007\u0005\u0000\u0000h\u001c\u0001\u0000\u0000\u0000"+
		"ik\u0005\r\u0000\u0000ji\u0001\u0000\u0000\u0000jk\u0001\u0000\u0000\u0000"+
		"kl\u0001\u0000\u0000\u0000lm\u0005\n\u0000\u0000m\u001e\u0001\u0000\u0000"+
		"\u0000\u000e\u000029<BGMPSU\\_cj\u0001\u0000\u0001\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
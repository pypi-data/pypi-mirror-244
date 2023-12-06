"""Port of antlr-c3 typescript symbol table implementation to python"""

from __future__ import annotations

__author__ = 'sgu'

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

# TODO license

# utils import
import asyncio
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, TypeVar, ParamSpec, Set, Coroutine

# antlr4
from antlr4.tree.Tree import ParseTree


class DuplicateSymbolError(Exception):
    pass


class MemberVisibility(Enum):
    # Not specified, default depends on the language and type.
    Unknown = 0
    # Used in Swift, member can be accessed outside of the defining module and extended.
    Open = 1
    # Like Open, but in Swift such a type cannot be extended.
    Public = 2
    # Member is only accessible in the defining class and any derived class.
    Protected = 3
    # Member can only be accessed from the defining class.
    Private = 4
    # Used in Swift, member can be accessed from everywhere in a defining module, not outside however.
    FilePrivate = 5
    # Custom enum for special usage.
    Library = 6


class Modifier(Enum):
    Static = 0
    Final = 1
    Sealed = 2
    Abstract = 3
    Deprecated = 4
    Virtual = 5
    Const = 6
    Overwritten = 7


class TypeKind(Enum):
    """
    Rough categorization of a type.
    """
    Unknown = 0
    Integer = 1
    Float = 2
    Number = 3
    String = 4
    Char = 5
    Boolean = 6
    Class = 7
    Interface = 8
    Array = 9
    Map = 10
    Enum = 11
    Alias = 12


class ReferenceKind(Enum):
    Irrelevant = 0
    # Default for most languages for dynamically allocated memory ('Type*' in C++).
    Pointer = 1
    # 'Type&' in C++
    Reference = 2
    # 'Type' as such and default for all value types.
    Instance = 3


class UnitKind(Enum):
    """
    Rough categorization of a unit from SI units.
    """
    Unknown = 0
    Second = 1
    Metre = 2
    # TODO si unit is kilogram | added to FundamentalUnit
    Gram = 3
    Ampere = 4
    Kelvin = 5
    Mole = 6
    Candela = 7
    # TODO add non si units?
    Pascal = 8
    Joule = 9
    ton = 10


class UnitPrefix:
    """
    Rough categorization of a unit from SI prefixes.
    """
    NoP = 0
    Quetta = 1
    Ronna = 2
    Yotta = 3
    Zetta = 4
    Exa = 5
    Peta = 6
    Tera = 7
    Giga = 8
    Mega = 9
    Kilo = 10
    Hecto = 11
    Deca = 12
    Deci = 13
    Centi = 14
    Mili = 15
    Micro = 16
    Nano = 17
    Pico = 18
    Femto = 19
    Atto = 20
    Zepto = 21
    Yocto = 22
    Ronto = 23
    Quecto = 24


@dataclass
class Unit:
    """
    The root unit. Used for unit symbols
    """
    name: str

    # The super unit of this unit or empty if this is a SI unit such as second.
    # TODO add units
    # TODO add aliases?
    baseTypes: List[Unit]
    prefix: UnitPrefix
    kind: UnitKind
    reference: ReferenceKind


@dataclass
class Type:
    """
    The root type. Used for typed symbols and type aliases.
    """
    name: str

    # The super type of this type or empty if this is a fundamental type.
    # Also used as the target type for type aliases.
    baseTypes: List[Type]
    kind: TypeKind
    reference: ReferenceKind


@dataclass
class SymbolTableOptions:
    allow_duplicate_symbols: Optional[bool] = None


class classproperty(property):
    # TODO use metaclass factory https://stackoverflow.com/q/6760685/
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class FundamentalUnit(Unit):
    """
    A single class for all fundamental units which are mostly SI units. They are distinguished via the kind field.
    """

    def __init__(self, name: str, baseTypes=[], unitPrefix=UnitPrefix.NoP, unitKind=UnitKind.Unknown,
                 referenceKind=ReferenceKind.Irrelevant):
        super().__init__(name=name, baseTypes=baseTypes, kind=unitKind, reference=referenceKind, prefix=unitPrefix)

    @classproperty
    def secondUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="second", unitKind=UnitKind.Second)

    @classproperty
    def metreUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="metre", unitKind=UnitKind.Metre)

    # TODO si unit is kilogram but unitKind has gram
    @classproperty
    def gramUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="gram", unitKind=UnitKind.Gram)

    # TODO si unit is kilogram but unitKind has gram
    @classproperty
    def kilogramUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="kilogram", unitPrefix=UnitPrefix.Kilo, unitKind=UnitKind.Gram)

    @classproperty
    def AmpereUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="ampere", unitKind=UnitKind.Ampere)

    @classproperty
    def KelvinUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Kelvin", unitKind=UnitKind.Kelvin)

    @classproperty
    def MoleUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Mole", unitKind=UnitKind.Mole)

    @classproperty
    def CandelaUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Candela", unitKind=UnitKind.Candela)

    @classproperty
    def PascalUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Pascal", unitKind=UnitKind.Pascal)

    @classproperty
    def JouleUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Joule", unitKind=UnitKind.Joule)

    # TODO si unit is kilogram. unitKind has gram but could include ton
    @classproperty
    def TonUnit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Ton", unitPrefix=UnitPrefix.Mega, unitKind=UnitKind.Gram)


class FundamentalType(Type):
    """
    A single class for all fundamental types. They are distinguished via the kind field.
    """

    def __init__(self, name: str, baseTypes=[], typeKind=TypeKind.Unknown, referenceKind=ReferenceKind.Irrelevant):
        super().__init__(name=name, baseTypes=baseTypes, kind=typeKind, reference=referenceKind)

    @classproperty
    def integerType(self) -> FundamentalType:
        return FundamentalType(name="int", typeKind=TypeKind.Integer)

    @classproperty
    def floatType(self) -> FundamentalType:
        return FundamentalType(name="float", typeKind=TypeKind.Float)

    @classproperty
    def stringType(self) -> FundamentalType:
        return FundamentalType(name="string", typeKind=TypeKind.String)

    @classproperty
    def boolType(self) -> FundamentalType:
        return FundamentalType(name="bool", typeKind=TypeKind.Boolean)


class Symbol:
    """
    The root of the symbol table class hierarchy: a symbol can be any manageable entity (like a block), not only things
    like variables or classes. We are using a class hierarchy here, instead of an enum or similar, to allow for easy
    extension and certain symbols can so provide additional APIs for simpler access to their sub elements, if needed.
    """
    # The name of the scope or empty if anonymous.
    name: str

    # Reference to the parse tree which contains this symbol.
    context: Optional[ParseTree]

    @property
    def modifiers(self) -> Set[int]:
        return set()

    visibility: MemberVisibility = MemberVisibility.Unknown

    __theParent: Optional[Symbol] = None

    def __init__(self, name: str = ''):
        self.name = name
        self.context = None

    def parent(self) -> Optional[Symbol]:
        return self.__theParent

    def firstSibling(self) -> Symbol:
        if isinstance(self.__theParent, ScopedSymbol):
            # expect not to be None
            return self.__theParent.firstChild()

        return self

    def previousSibling(self) -> Optional[Symbol]:
        """
        :return: the symbol before this symbol in its scope.
        """
        if not isinstance(self.__theParent, ScopedSymbol):
            return self

        return self.__theParent.previous_sibling_of(self)

    def nextSibling(self) -> Optional[Symbol]:
        """
        :return: the symbol following this symbol in its scope.
        """
        if not isinstance(self.__theParent, ScopedSymbol):
            return self

        return self.__theParent.next_sibling_of(self)

    def lastSibling(self) -> Symbol:
        if isinstance(self.__theParent, ScopedSymbol):
            # expect not to be None
            return self.__theParent.lastChild()

        return self

    def next(self) -> Optional[Symbol]:
        """
        :return: the next symbol in definition order, regardless of the scope.
        """
        if isinstance(self.__theParent, ScopedSymbol):
            return self.__theParent.next_of(self)

        return None

    def root(self) -> Optional[Symbol]:
        """
        :return: the outermost entity (below the symbol table) that holds us.
        """
        run: Optional[Symbol] = self.__theParent
        while run is not None:
            if run.parent() is None or isinstance(run.parent(), SymbolTable):
                return run
            run = run.parent()

        return run

    def symbolTable(self) -> Optional[SymbolTable]:
        """
        :return: the symbol table we belong too or undefined if we are not yet assigned.
        """
        if isinstance(self, SymbolTable):
            return self

        run: Optional[Symbol] = self.__theParent
        while run is not None:
            if isinstance(run, SymbolTable):
                return run
            run = run.parent()

        return None

    def symbolPath(self) -> List[Symbol]:
        """
        :return: the list of symbols from this one up to root.
        """
        result: List[Symbol] = []

        run: Symbol = self
        while run is not None:
            result.append(run)
            if run.parent() is None:
                break
            run = run.parent()

        return result

    def setParent(self, parent: Optional[Symbol]) -> None:
        """
        The parent is usually a scoped symbol as only those can have children, but we allow any symbol here for special
        scenarios. This is rather an internal method and should rarely be used by external code.

        :param parent: The new parent to use.
        :return:
        """
        self.__theParent = parent

    def remove_from_parent(self) -> None:
        if isinstance(self.__theParent, ScopedSymbol):
            self.__theParent.removeSymbol(self)
            self.__theParent = None

    async def resolve(self, name: str, localOnly: bool = False) -> Optional[Symbol]:
        """
        Asynchronously looks up a symbol with a given name, in a bottom-up manner.

        :param name: The name of the symbol to find.
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A promise resolving to the first symbol with a given name, in the order of appearance in this scope or
        any of the parent scopes (conditionally).
        """

        if isinstance(self.__theParent, ScopedSymbol):
            return await self.__theParent.resolve(name, localOnly)

        return None

    def resolve_sync(self, name: str, localOnly=False) -> Optional[Symbol]:
        """
        Synchronously looks up a symbol with a given name, in a bottom-up manner.

        :param name: The name of the symbol to find.
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: the first symbol with a given name, in the order of appearance in this scope or any of the parent
        scopes (conditionally).
        """
        if isinstance(self.__theParent, ScopedSymbol):
            return self.__theParent.resolve_sync(name, localOnly)

        return None

    def get_parent_of_type(self, t: type) -> Optional[T]:
        """
        :param t: The type of objects to return.
        :return: the next enclosing parent of the given type.
        """
        run = self.__theParent
        while run is not None:
            if isinstance(run, t):
                return run
            run = run.__theParent

        return None

    # TODO <anonymous> special string for empty scope names
    def qualifiedName(self, separator=".", full=False, includeAnonymous=False) -> str:
        """
        Creates a qualified identifier from this symbol and its parent. If `full` is true then all parents are traversed
        in addition to this instance.

        :param separator: The string to be used between the parts.
        :param full: A flag indicating if the full path is to be returned.
        :param includeAnonymous: Use a special string for empty scope names.
        :return: the constructed qualified identifier.
        """
        if not includeAnonymous and len(self.name) == 0:
            return ''

        result: str = '<anonymous>' if len(self.name) == 0 else self.name
        run = self.__theParent
        while run:
            if includeAnonymous or len(run.name) > 0:
                result = ('<anonymous>' if len(run.name) == 0 else run.name) + separator + result

            if not full or run.__theParent is None:
                break

            run = run.__theParent

        return result


P = ParamSpec('P')
T = TypeVar('T', bound=Symbol)


class TypedSymbol(Symbol):
    """
    A symbol with an attached type (variables, fields etc.).
    """
    attached_type: Optional[Type]

    def __init__(self, name: str, attached_type: Type = None):
        super().__init__(name)
        self.attached_type = attached_type


class UnitSymbol(TypedSymbol):
    """
    A symbol with an attached unit (physical units such as second, metre, gram etc.).
    """
    attached_unit: Optional[Unit]

    def __init__(self, name: str, attached_unit: Unit, attached_type: Type = None):
        super().__init__(name, attached_type)
        self.attached_unit = attached_unit


class TypeAlias(Symbol, Type):
    """
    An alias for another type.
    """
    __targetType: Type

    def __init__(self, name: str, target: Type):
        super().__init__(name)
        self.__targetType = target

    def baseTypes(self) -> List[Type]:
        return [self.__targetType]

    def kind(self) -> TypeKind:
        return TypeKind.Alias

    def reference(self) -> ReferenceKind:
        return ReferenceKind.Irrelevant


class ScopedSymbol(Symbol):
    """
    A symbol with a scope (so it can have child symbols).
    """
    # All child symbols in definition order.
    __childSymbols: List[Symbol]

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.__childSymbols = []

    def directScopes(self) -> Coroutine[List[ScopedSymbol]]:
        """
        :return: A promise resolving to all direct child symbols with a scope (e.g. classes in a module).
        """
        return self.get_symbols_of_type(ScopedSymbol)

    def children(self) -> List[Symbol]:
        return self.__childSymbols

    def firstChild(self) -> Optional[Symbol]:
        if len(self.children()) > 0:
            return self.children()[0]

        return None

    def lastChild(self) -> Optional[Symbol]:
        if len(self.children()) > 0:
            return self.children()[len(self.children()) - 1]

        return None

    def clear(self) -> None:
        self.__childSymbols = []

    def addSymbol(self, symbol: Symbol) -> None:
        """
        Adds the given symbol to this scope. If it belongs already to a different scope it is removed from that before
        adding it here.

        :param symbol: The symbol to add as a child.
        :return:
        """
        symbol.remove_from_parent()

        # Check for duplicates first.
        symbolTable = self.symbolTable()
        if symbolTable is None or not symbolTable.options.allow_duplicate_symbols:
            for child in self.children():
                if child == symbol or (len(symbol.name) > 0 and child.name == symbol.name):
                    name = symbol.name
                    if len(name) == 0:
                        name = '<anonymous>'

                    raise DuplicateSymbolError({"message": "Attempt to add duplicate symbol '%s'" % name})

        self.children().append(symbol)
        symbol.setParent(self)

    def removeSymbol(self, symbol: Symbol) -> None:
        if symbol in self.children():
            self.children().remove(symbol)
            symbol.setParent(None)

    async def get_nested_symbols_of_type(self, t: type) -> List[T]:
        """
        Asynchronously retrieves child symbols of a given type from this symbol.

        :param t: The type of the objects to return.
        :return: A promise resolving to all (nested) children of the given type.
        """
        result: List[T] = []

        childPromises: List[Coroutine[List[T]]] = []
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                childPromises.append(child.get_nested_symbols_of_type(t))

        childSymbols = await asyncio.gather(*childPromises)
        for entry in childSymbols:
            result.extend(entry)

        return result

    def get_nested_symbols_of_type_sync(self, t: type) -> List[T]:
        """
        Synchronously retrieves child symbols of a given type from this symbol.

        :param t: The type of the objects to return.
        :return: A list of all (nested) children of the given type.
        """
        result: List[T] = []

        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_nested_symbols_of_type_sync(t))

        return result

    async def get_all_nested_symbols(self, name: str = None) -> List[Symbol]:
        """
        :param name: If given only returns symbols with that name.
        :return: A promise resolving to symbols from this and all nested scopes in the order they were defined.
        """
        result: List[Symbol] = []

        childPromises: List[Coroutine[List[Symbol]]] = []
        for child in self.children():
            if name is None or child.name == name:
                result.append(child)

            if isinstance(child, ScopedSymbol):
                childPromises.append(child.get_all_nested_symbols(name))

        childSymbols = await asyncio.gather(*childPromises)
        for entry in childSymbols:
            result.extend(entry)

        return result

    def get_all_nested_symbols_sync(self, name: str = None) -> List[Symbol]:
        """
        :param name: If given only returns symbols with that name.
        :return: A list of all symbols from this and all nested scopes in the order they were defined.
        """
        result: List[Symbol] = []

        for child in self.children():
            if name is None or child.name == name:
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_all_nested_symbols_sync(name))

        return result

    async def get_symbols_of_type(self, t: type) -> List[T]:
        """
        :param t: The type of the objects to return.
        :return: A promise resolving to direct children of a given type.
        """
        result: List[T] = []
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

        return result

    # TODO: add optional position dependency (only symbols defined before a given caret pos are viable).
    async def get_all_symbols(self, t: type, localOnly=False) -> List[T]:
        """
        :param t: The type of the objects to return.
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A promise resolving to all symbols of the given type, accessible from this scope (if localOnly is
        false), within the owning symbol table.
        """
        result: List[T] = []

        # Special handling for namespaces, which act like grouping symbols in this scope, so we show them as available
        # in this scope.
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, NamespaceSymbol):
                childSymbols = await child.get_all_symbols(t, True)
                result.extend(childSymbols)

        if not localOnly and isinstance(self.parent(), ScopedSymbol):
            childSymbols = await self.get_all_symbols(t, True)
            result.extend(childSymbols)

        return result

    def get_all_symbols_sync(self, t: type, localOnly: bool = False) -> List[T]:
        """
        TODO: add optional position dependency (only symbols defined before a given caret pos are viable).

        :param t: The type of the objects to return.
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A list with all symbols of the the given type, accessible from this scope (if localOnly is false),
        within the owning symbol table.
        """
        result: List[T] = []

        # Special handling for namespaces, which act like grouping symbols in this scope,
        # so we show them as available in this scope.
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, NamespaceSymbol):
                childSymbols = child.get_all_symbols_sync(t, True)
                result.extend(childSymbols)

        if not localOnly and isinstance(self.parent(), ScopedSymbol):
            childSymbols = self.get_all_symbols_sync(t, True)
            result.extend(childSymbols)

        return result

    async def resolve(self, name: str, localOnly=False) -> Optional[Symbol]:
        """
        :param name: The name of the symbol to resolve.
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A promise resolving to the first symbol with a given name, in the order of appearance in this scope or
        any of the parent scopes (conditionally).
        """
        for child in self.children():
            if child.name == name:
                return child

        # Nothing found locally. Let the parent continue.
        if not localOnly and isinstance(self.parent(), ScopedSymbol):
            return await self.parent().resolve(name, False)

        return None

    def resolve_sync(self, name: str, localOnly=False) -> Optional[Symbol]:
        """
        :param name: The name of the symbol to resolve.
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: the first symbol with a given name, in the order of appearance in this scope or any of the parent
        scopes (conditionally).
        """
        for child in self.children():
            if child.name == name:
                return child

        # Nothing found locally. the parent continues.
        if not localOnly and isinstance(self.parent(), ScopedSymbol):
            return self.parent().resolve_sync(name, False)

        return None

    def get_typed_symbols(self, localOnly=True) -> List[TypedSymbol]:
        """
        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: all accessible symbols that have a type assigned.
        """
        result: List[TypedSymbol] = []

        for child in self.children():
            if isinstance(child, TypedSymbol):
                result.append(child)

        if not localOnly and isinstance(self.parent(), ScopedSymbol):
            localList = self.parent().get_typed_symbols(True)
            result.extend(localList)

        return result

    def get_typed_symbol_names(self, localOnly=True) -> List[str]:
        """
        The names of all accessible symbols with a type.

        :param localOnly: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: A list of names.
        """
        result: List[str] = []
        for child in self.children():
            if isinstance(child, TypedSymbol):
                result.append(child.name)

        if not localOnly and isinstance(self.parent(), ScopedSymbol):
            localList = self.parent().get_typed_symbol_names(True)
            result.extend(localList)

        return result

    def symbol_from_path(self, path: str, separator=".") -> Optional[Symbol]:
        """
        :param path: The path consisting of symbol names separator by `separator`.
        :param separator: The character to separate path segments.
        :return: the symbol located at the given path through the symbol hierarchy.
        """
        elements = path.split(separator)
        index = 0
        if elements[0] == self.name or len(elements[0]) == 0:
            index += 1

        result: Symbol = self
        while index < len(elements):
            if not isinstance(result, ScopedSymbol):
                return None

            child: Optional[Symbol] = next(
                filter(lambda candidate: candidate.name == elements[index], result.children()), None)
            if child is None:
                return None

            result = child
            index += 1

        return result

    def indexOfChild(self, child: Symbol) -> int:
        """
        :param child: The child to search for.
        :return: the index of the given child symbol in the child list or -1 if it couldn't be found.
        """
        # two pass org
        # return lambda child,self.children() : self.children().index(child) if child in self.children() else -1
        try:
            return self.children().index(child)
        except ValueError:
            return -1

    def next_sibling_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the sibling symbol after the given child symbol, if one exists.
        """
        index = self.indexOfChild(child)
        if index == -1 or index >= len(self.children()) - 1:
            return None

        return self.children()[index + 1]

    def previous_sibling_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the sibling symbol before the given child symbol, if one exists.
        """
        index = self.indexOfChild(child)
        if index < 1:
            return None

        return self.children()[index - 1]

    def next_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the next symbol in definition order, regardless of the scope.
        """
        if not isinstance(child.parent(), ScopedSymbol):
            return None

        if child.parent() is not self:
            return child.parent().nextOf(child)

        if isinstance(child, ScopedSymbol) and len(child.children()) > 0:
            return child.children()[0]

        sibling = self.next_sibling_of(child)
        if sibling is not None:
            return sibling

        return self.parent().next_of(self)


class NamespaceSymbol(ScopedSymbol):
    pass


class BlockSymbol(ScopedSymbol):
    pass


class VariableSymbol(UnitSymbol):

    def __init__(self, name: str, value=None, attached_type: Type = None):
        super().__init__(name, attached_type)

        self.value = value


class LiteralSymbol(UnitSymbol):

    def __init__(self, name: str, value=None, attached_type: Type = None):
        super().__init__(name, attached_type)

        self._value = value

    @property
    def value(self):
        return self._value


class ParameterSymbol(VariableSymbol):
    pass


class RoutineSymbol(ScopedSymbol):
    """
    A standalone function/procedure/rule.
    """
    returnType: Optional[Type]  # Can be null if result is void.

    def __init__(self, name: str, returnType: Type = None):
        super().__init__(name)
        self.returnType = returnType

    def getVariables(self, localOnly=True) -> Coroutine[List[T]]:
        return self.get_symbols_of_type(VariableSymbol)

    def getParameters(self, localOnly=True) -> Coroutine[List[T]]:
        return self.get_symbols_of_type(ParameterSymbol)


class MethodFlags(Enum):
    NoneFL = 0
    Virtual = 1
    Const = 2
    Overwritten = 4

    # Distinguished by the return type.
    SetterOrGetter = 8

    # Special flag used e.g. in C++ for explicit c-tors.
    Explicit = 16


class MethodSymbol(RoutineSymbol):
    """
    A function which belongs to a class or other outer container structure.
    """
    methodFlags = MethodFlags.NoneFL


class FieldSymbol(VariableSymbol):
    """
    A field which belongs to a class or other outer container structure.
    """
    setter: Optional[MethodSymbol] = None
    getter: Optional[MethodSymbol] = None


class ClassSymbol(ScopedSymbol, Type):
    """
    Classes and structs.
    """
    isStruct: bool
    reference: ReferenceKind

    @property
    def extends(self) -> List[ClassSymbol]:
        """
        Usually only one member, unless the language supports multiple inheritance (like C++).
        """
        return self._extends

    @property
    def implements(self) -> List[tuple[ClassSymbol, InterfaceSymbol]]:
        """
        Typescript allows a class to implement a class, not only interfaces.
        """
        return self._implements

    def __init__(self, name: str, ext: List[ClassSymbol], impl: List[tuple[ClassSymbol, InterfaceSymbol]]):
        super().__init__(name)
        self._extends = ext
        self._implements = impl

        self.isStruct = False
        self.reference = ReferenceKind.Irrelevant

    def baseTypes(self) -> List[Type]:
        return self._extends

    def kind(self) -> TypeKind:
        return TypeKind.Class

    def getMethods(self, includeInherited=False) -> Coroutine[List[T]]:
        """

        :param includeInherited: Not used.
        :return: a list of all methods.
        """
        return self.get_symbols_of_type(MethodSymbol)

    def getFields(self, includeInherited=False) -> Coroutine[List[T]]:
        """
        :param includeInherited: Not used.
        :return: all fields.
        """
        return self.get_symbols_of_type(FieldSymbol)


class InterfaceSymbol(ScopedSymbol, Type):
    reference: ReferenceKind

    def __init__(self, name: str, ext: List[tuple[ClassSymbol, InterfaceSymbol]]):
        super().__init__(name)
        self._extends = ext

        self.reference = ReferenceKind.Irrelevant

    @property
    def extends(self) -> List[tuple[ClassSymbol, InterfaceSymbol]]:
        """
        Typescript allows an interface to extend a class, not only interfaces.
        """
        return self._extends

    def baseTypes(self) -> List[Type]:
        return self._extends

    def kind(self) -> TypeKind:
        return TypeKind.Interface

    def getMethods(self, includeInherited=False) -> Coroutine[List[MethodSymbol]]:
        """
        :param includeInherited: Not used.
        :return: a list of all methods.
        """
        return self.get_symbols_of_type(MethodSymbol)

    def getFields(self, includeInherited=False) -> Coroutine[List[T]]:
        """
        :param includeInherited: Not used.
        :return: all fields.
        """
        return self.get_symbols_of_type(FieldSymbol)


class ArrayType(Symbol, Type):
    __referenceKind: ReferenceKind

    def __init__(self, name: str, referenceKind: ReferenceKind, elemType: Type, size=0):
        super().__init__(name)
        self.__referenceKind = referenceKind
        self._elementType = elemType
        self._size = size

    @property
    def elementType(self) -> Type:
        return self._elementType

    @property
    def size(self) -> int:
        return self._size  # > 0 if fixed length.

    def baseTypes(self) -> List[Type]:
        return []

    def kind(self) -> TypeKind:
        return TypeKind.Array

    def reference(self) -> ReferenceKind:
        return self.__referenceKind


@dataclass
class SymbolTableInfo:
    dependencyCount: int
    symbolCount: int


class SymbolTable(ScopedSymbol):
    """
    The main class managing all the symbols for a top level entity like a file, library or similar.
    """
    #  Other symbol information available to this instance.
    dependencies: Set[SymbolTable]
    options: SymbolTableOptions

    def __init__(self, name: str, options: SymbolTableOptions):
        self.dependencies = set()
        self.options = options
        super().__init__(name)

    def info(self):
        """
        :return: instance information, mostly relevant for unit testing.
        """
        return SymbolTableInfo(len(self.dependencies), len(self.children()))

    def clear(self):
        super().clear()
        self.dependencies.clear()

    def addDependencies(self, *tables: SymbolTable):
        for table in tables:
            self.dependencies.add(table)

    def removeDependency(self, table: SymbolTable):
        if table in self.dependencies:
            self.dependencies.remove(table)

    def add_new_symbol_of_type(self, t: type, parent: Optional[ScopedSymbol] = None, *my_args: P.args or None,
                               **my_kwargs: P.kwargs or None) -> T:
        result = t(*my_args, **my_kwargs)
        if parent is None or parent is self:
            self.addSymbol(result)
        else:
            parent.addSymbol(result)

        return result

    async def add_new_namespace_from_path(self, parent: Optional[ScopedSymbol], path: str,
                                          delimiter=".") -> NamespaceSymbol:
        """
        Asynchronously adds a new namespace to the symbol table or the given parent. The path parameter specifies a
        single namespace name or a chain of namespaces (which can be e.g. "outer.intermittent.inner.final"). If any of
        the parent namespaces is missing they are created implicitly. The final part must not exist however or you'll
        get a duplicate symbol error.

        :param parent: The parent to add the namespace to.
        :param path: The namespace path.
        :param delimiter: The delimiter used in the path.
        :return: The new symbol.
        """
        parts = path.split(delimiter)
        i = 0
        currentParent = self if parent is None else parent
        while i < len(parts) - 1:
            namespace: NamespaceSymbol = await currentParent.resolve(parts[i], True)
            if namespace is None:
                namespace = self.add_new_symbol_of_type(NamespaceSymbol, currentParent, parts[i])

            currentParent = namespace
            i += 1

        return self.add_new_symbol_of_type(NamespaceSymbol, currentParent, parts[len(parts) - 1])

    def add_new_namespace_from_path_sync(self, parent: Optional[ScopedSymbol], path: str, delimiter=".") -> NamespaceSymbol:
        """
        Synchronously adds a new namespace to the symbol table or the given parent. The path parameter specifies a
        single namespace name or a chain of namespaces (which can be e.g. "outer.intermittent.inner.final"). If any of
        the parent namespaces is missing they are created implicitly. The final part must not exist however or you'll
        get a duplicate symbol error.

        :param parent: The parent to add the namespace to.
        :param path: The namespace path.
        :param delimiter: The delimiter used in the path.
        :return: The new symbol.
        """
        parts = path.split(delimiter)
        i = 0
        currentParent = self if parent is None else parent

        while i < len(parts) - 1:
            namespace: NamespaceSymbol = currentParent.resolve_sync(parts[i], True)
            if namespace is None:
                namespace = self.add_new_symbol_of_type(NamespaceSymbol, currentParent, parts[i])

            currentParent = namespace
            i += 1

        return self.add_new_symbol_of_type(NamespaceSymbol, currentParent, parts[len(parts) - 1])

    async def get_all_symbols(self, t: type, localOnly=False) -> List[T]:
        """
        Asynchronously returns all symbols from this scope (and optionally those from dependencies) of a specific type.

        :param t: The type of the symbols to return.
        :param localOnly: If true do not search dependencies.
        :return: A promise which resolves when all symbols are collected.
        """
        result: List[T] = await super().get_all_symbols(t, localOnly)

        if not localOnly:
            # TODO alternative
            # dependencyResults = await asyncio.gather(*[x.getAllSymbols(t, localOnly) for x in self.dependencies])
            dependencyResults = await asyncio.gather(
                *(map((lambda x: x.get_all_symbols(t, localOnly)), self.dependencies)))

            for value in dependencyResults:
                result.extend(value)

        return result

    def get_all_symbols_sync(self, t: type, localOnly=False) -> List[T]:
        """
        Synchronously returns all symbols from this scope (and optionally those from dependencies) of a specific type.

        :param t: The type of the symbols to return.
        :param localOnly: If true do not search dependencies.
        :return: A list with all symbols.
        """
        result: List[T] = super().get_all_symbols_sync(t, localOnly)

        if not localOnly:
            for dependency in self.dependencies:
                result.extend(dependency.get_all_symbols_sync(t, localOnly))

        return result

    async def symbol_with_context(self, context: ParseTree) -> Optional[Symbol]:
        """
        Asynchronously looks for a symbol which is connected with a given parse tree context.

        :param context: The context to search for.
        :return: A promise resolving to the found symbol or undefined.
        """

        def findRecursive(local_symbol: Symbol) -> Optional[Symbol]:
            """
            Local function to find a symbol recursively.

            :param local_symbol: The symbol to search through.
            :return: The symbol with the given context, if found.
            """
            if local_symbol.context == context:
                return local_symbol

            if isinstance(local_symbol, ScopedSymbol):
                for child in local_symbol.children():
                    local_result = findRecursive(child)
                    if local_result is not None:
                        return local_result

            return None

        symbols = await self.get_all_symbols(Symbol)
        for symbol in symbols:
            result = findRecursive(symbol)
            if result is not None:
                return result

        for dependency in self.dependencies:
            symbols = await dependency.get_all_symbols(Symbol)
            for symbol in symbols:
                result = findRecursive(symbol)
                if result is not None:
                    return result

        return None

    def symbol_with_context_sync(self, context: ParseTree) -> Optional[Symbol]:
        """
        Synchronously looks for a symbol which is connected with a given parse tree context.

        :param context: The context to search for.
        :return: The found symbol or undefined.
        """

        def findRecursive(local_symbol: Symbol) -> Optional[Symbol]:
            """
            Local function to find a symbol recursively.

            :param local_symbol: The symbol to search through.
            :return: The symbol with the given context, if found.
            """
            if local_symbol.context is context:
                return local_symbol

            if isinstance(local_symbol, ScopedSymbol):
                for child in local_symbol.children():
                    local_result = findRecursive(child)
                    if local_result is not None:
                        return local_result

            return None

        symbols = self.get_all_symbols_sync(Symbol)
        for symbol in symbols:
            result = findRecursive(symbol)
            if result is not None:
                return result

        for dependency in self.dependencies:
            symbols = dependency.get_all_symbols_sync(Symbol)
            for symbol in symbols:
                result = findRecursive(symbol)
                if result is not None:
                    return result

        return None

    async def resolve(self, name: str, localOnly=False) -> Optional[Symbol]:
        """
        Asynchronously resolves a name to a symbol.

        :param name: The name of the symbol to find.
        :param localOnly: A flag indicating if only this symbol table should be used or also its dependencies.
        :return: A promise resolving to the found symbol or undefined.
        """
        result = await super().resolve(name, localOnly)
        if result is None and not localOnly:
            for dependency in self.dependencies:
                result = await dependency.resolve(name, False)
                if result is not None:
                    return result

        return result

    def resolve_sync(self, name: str, localOnly=False) -> Optional[Symbol]:
        """
        Synchronously resolves a name to a symbol.

        :param name: The name of the symbol to find.
        :param localOnly: A flag indicating if only this symbol table should be used or also its dependencies.
        :return: The found symbol or undefined.
        """
        result = super().resolve_sync(name, localOnly)
        if result is None and not localOnly:
            for dependency in self.dependencies:
                result = dependency.resolve_sync(name, False)
                if result is not None:
                    return result

        return result

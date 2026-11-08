from dependency_injector import containers, providers
from sympy import numbered_symbols


class NumberedSymbolContainer(containers.DeclarativeContainer):
    numbered_symbol_singleton = providers.Singleton(numbered_symbols, "x")

"""Class for a context-free (type 2) Grammar. """
class Grammar:
    def __init__(self, V, terminal, S, P):
        # A grammar is a tuple G=(V, Σ, S, P)
        self._V = V  # array of non terminal symbols
        self._terminal = terminal  # array of terminal symbols
        self._S = S  # a special member contained in V
        self._rules = P  # production rules. A dictionary of variable:[substitutions]

    @property
    def V(self):
        return self._V

    @property
    def terminal(self):
        return self._terminal

    @property
    def S(self):
        return self._S

    @property
    def rules(self):
        return self._rules

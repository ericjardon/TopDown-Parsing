"""Parsing tree's search is deterministic i.e. a single path only"""
from collections import deque

class Node:
    def __init__(self, name, parent):
        self._name=name
        # children es una variable para uso interno ('privada')
        self._children = [] # array of nodes
        self._depth = 0
        self._parent = parent

    def updateDepth(self, childDepth):
        self._depth = max(self._depth, childDepth + 1)
        if self._parent != None:
            self._parent.updateDepth(self._depth)

    def addChild(self, node):
        self._children.append(node)
        self.updateDepth(node.depth)

    @property
    def name(self):
        return self._name

    @property
    def children(self):
        return self._children

    @property
    def depth(self):
        return self._depth

    # str method to print trees (debugging purposes)
    def __str__(self, level=0):
        tree =  "\t"*level + repr(self.name) + "\n"
        for child in self.children:
            tree += child.__str__(level+1)
        return tree

class Parser:
    # Traverses an implicit derivations tree to determine if the given word can be derived.
    def topdown_parse(self, Grammar, word, max):
        root = Node(Grammar.S, None)
        que = deque()       # deque uses append() and popleft()
        que.append(root)
        found = False
        while (len(que)>0 and not found and root.depth <= max):
            # Iteration basis is per-node from the queue
            q = que.popleft()   #   q is the node to analyze
            done = False
            #print("Current node: ", q.name)

            # Decompose q into 'uAv' where A is leftmost non terminal symbol
            leftmost = None
            for i in range(len(q.name)):
                if q.name[i] in Grammar.rules:      # if the symbol is a Head in the Grammar's rules (non-terminal)
                    leftmost = q.name[i]
                    pos = i     # the position of A in uAv
                    break
            #print("Leftmost variable:", leftmost)

            if leftmost == None:
                done = True     # which means we reached a leaf, so we skip to next iteration

            i = 0  # index of production rule of A
            while (not done and not found):
                # Per production rule of leftmost A
                if i >= len(Grammar.rules[leftmost]):
                    done = True     # Finished exploring all production rules of A
                else:
                    #print("Rule", leftmost," ->", Grammar.rules[leftmost][i])
                    j = i+1
                    u = q.name[:pos]    # The substring to the left of A (prefix)
                    #print("u =", u)
                    w = Grammar.rules[leftmost][i]      # The production body
                    #print("w =", w)
                    v = q.name[pos+1:]      # the substring to the right of A
                    #print("v =", v)
                    uwv = u + w + v
                    #print("uwv: ", uwv)
                    wv = w + v          # The suffix wv

                    hasNonTerminal = False
                    #nextpos = len(u) -1     # index to find next nonTerminal symbol in wv
                    nextpos = pos

                    # after producing uvw check if terminal prefix matches a prefix in word, otherwise stop exploring
                    for i in range(pos, len(uwv)):      # for each character after the prefix u
                        if uwv[i] in Grammar.rules:
                            #print("found next variable: ", uwv[i])
                            hasNonTerminal = True
                            nextpos = i
                            break

                    #print("terminal prefix:", uwv[:nextpos])
                    if hasNonTerminal and uwv[:nextpos] == word[:nextpos]:
                        # si no tiene no-terminales y es un prefijo, es un nodo válido para el árbol
                        #print("uwv has non terminal and is valid prefix. enqueuing uwv: ", uwv)
                        node = Node(uwv, q)
                        que.append(node)        # append to tree & updates depth of the tree
                        q.addChild(node)        # enqueue the node to continue BFS

                    if uwv == word:
                        print(word, "was found")
                        q.addChild(Node(word, q))      # appends to tree while updating depth of the tree
                        found = True
                    i = j

        if root.depth > max: print("Maximum Depth Exceeded. Parsing stopped.")

        return found, root
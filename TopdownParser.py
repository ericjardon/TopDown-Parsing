"""Do we really need a tree? search is deterministic i.e. a single path only"""
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
    # getter method using python Properties , we can call node.children

    def __str__(self, level=0):
        tree =  "\t"*level + repr(self.name) + "\n"
        for child in self.children:
            tree += child.__str__(level+1)
        return tree

class Parser:

    # Traverses an implicit tree to determine if the given word can be derived.
    def topdown_parse(self, Grammar, word, max):
        root = Node(Grammar.S, None, )
        que = deque()       # uses append() and popeft()
        que.append(root)
        found = False
        currentLevel = 0
        while (len(que)>0 and not found and root.depth <= max):
            # Per-node iteration
            q = que.popleft()   #   q is the node to analyze: 'uAv' where A is leftmost variable
            #print("Current node: ", q.name)
            done = False
            leftmost = None
            for i in range(len(q.name)):
                if q.name[i] in Grammar.rules:
                    leftmost = q.name[i]
                    pos = i
                    break
            #print("Leftmost variable:", leftmost)

            if leftmost == None:
                done = True

            i = 0  # index of production rule
            while (not done and not found):
                # Per production rule of leftmost
                if i >= len(Grammar.rules[leftmost]):
                    done = True
                else:
                    #print("Rule", leftmost," ->", Grammar.rules[leftmost][i])
                    j = i+1
                    u = q.name[:pos]
                    #print("u =", u)
                    w = Grammar.rules[leftmost][i]
                    #print("w =", w)
                    v = q.name[pos+1:]
                    #print("v =", v)
                    uwv = u + w + v
                    #print("uwv: ", uwv)
                    afterU = w + v
                    # Checa que uwv no tenga más no-terminales Y uwv sea un prefijo de word (p)
                    hasNonTerminal = False
                    nextpos = len(u) -1     # next non terminal symbol position
                    for i in range(len(afterU)):
                        if afterU[i] in Grammar.rules:
                            #print("found next variable: ", afterU[i])
                            hasNonTerminal = True
                            nextpos += i + 1
                            break

                    #print("terminal prefix:", uwv[:nextpos])
                    if hasNonTerminal and uwv[:nextpos] == word[:nextpos]:     # si no tiene no-terminales y es un prefijo,
                        #print("uwv has non terminal and is valid prefix. enqueuing uwv: ", uwv)
                        node = Node(uwv, q)
                        que.append(node)        # append to tree & updates depth of the tree
                        q.addChild(node)        # enqueue the node to continue BFS

                    if uwv == word:
                        print("Word was found")
                        q.addChild(Node(word, q))      # append to tree & updates depth of the tree
                        found = True
                    i = j

        if root.depth > max: print("Maximum Depth Exceeded. Parsing stopped.")

        return found, root
"""Do we really need a tree? search is deterministic i.e. a single path only"""
from collections import deque

class Node:
    def __init__(self, name):
        self._name=name
        # children es una variable para uso interno ('privada')
        self._children = [] # array of nodes

    def addChild(self, node):
        self._children.append(node)

    @property
    def name(self):
        return self._name

    @property
    def children(self):
        return self._children
    # getter method using python Properties , we can call node.children

    def __str__(self, level=0):
        tree =  "\t"*level + repr(self.name) + "\n"
        for child in self.children:
            tree += child.__str__(level+1)
        return tree

class Parser:
    # Traverses an implicit tree to determine if the given word can be derived.
    def topdown_parse(self, Grammar, word):
        root = Node(Grammar.S)
        que = deque()       # uses append() and popeft()
        que.append(root)
        found = False

        while (len(que)>0 and not found):
            # Per-node iteration
            q = que.popleft()   #   q is  the node to analyze: uAv
            print("Current node: ", q.name)
            done = False
            leftmost = None
            for i in range(len(q.name)):
                if q.name[i] in Grammar.rules:
                    leftmost = q.name[i]
                    pos = i
                    break
            print("Leftmost variable:", leftmost)
            if leftmost == None:
                done = True

            i = 0  # index of production rule
            while (not done and not found):
                # Per production rule of leftmost
                if i >= len(Grammar.rules[leftmost]):
                    done = True
                else:
                    print("Rule", leftmost," ->", Grammar.rules[leftmost][i])
                    j = i + 1
                    u = q.name[:pos]
                    print("u =", u)
                    w = Grammar.rules[leftmost][i]
                    print("w =", w)
                    v = q.name[pos+1:]
                    print("v =", v)
                    uwv = u + w + v
                    print("uwv: ", uwv)
                    afterU = w + v
                    # Checa que uwv no tenga más no-terminales Y uwv sea un prefijo de word (p)
                    hasNonTerminal = False
                    nextpos = len(u) -1     # next non terminal symbol position
                    for i in range(len(afterU)):
                        if afterU[i] in Grammar.rules:
                            print("found next variable: ", afterU[i])
                            hasNonTerminal = True
                            nextpos += i + 1
                            break

                    print("terminal prefix:", uwv[:nextpos])
                    if hasNonTerminal and uwv[:nextpos] == word[:nextpos]:     # si no tiene no-terminales y es un prefijo,
                        print("uwv has non terminal and is valid prefix. enqueuing uwv: ", uwv)
                        node = Node(uwv)
                        que.append(node)
                        q.addChild(node)        # enqueue the ndoe and add as child to q

                    if uwv == word:
                        print("Word was found")
                        q.addChild(Node(word))
                        found = True
                    i = j

        return found, root

def printTree(root):
    #todo
    pass



#class DTree:
 #   def __init__(self, root):
  #      self._root = root
#    @property
 #   def root(self):
      #  return self._root
  #  @root.setter
   # def root(self, root):
    #    self._root = root

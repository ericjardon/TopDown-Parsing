"""Principal module that contains the classes for the Parsing process.
    Node is a utility class representing the nodes for the derivations tree.
    Node holds attributes for name (value), children nodes list, height, and parent node.
    Parser is the class that traverses an implicit tree to generate a given word from a Grammar."""

from collections import deque

class Node:
    def __init__(self, name, parent):
        # Leading underscore denotes internal use variables in OOP Python
        self._name=name
        self._children = []
        self._height = 0
        self._parent = parent

    def updateDepth(self, childDepth):
        """Depth of tree is our parameter to stop parsing.
        Height of root is equal to depth of deepest node.
        To know when to stop parsing, we check the height of the root.
        This method updates a tree's depth by updating heights recursively from last added node towards the root.
          childDepth is the height value of the previously updated node in tree"""
        self._height = max(self._height, childDepth + 1)
        # If the node has a parent, update its height too
        if self._parent != None:
            self._parent.updateDepth(self._height)

    # Method to add a child to this node while also updating the depth of the tree
    def addChild(self, node):
        """node is another instance of Node that is attached as child to this Node.
            We append the child to children list of node and update the depth of tree."""
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
        return self._height

    # str method to print trees (debugging purposes, no pretty format)
    def __str__(self, level=0):
        tree =  "\t"*level + repr(self.name) + "\n"
        for child in self.children:
            tree += child.__str__(level+1)
        return tree


class Parser:
    def topdown_parse(self, Grammar, word, max):
        """Traverses an implicit derivations tree to determine if the given word can be derived.
            Grammar is an instance of Grammar class
            word is the string to derive from the grammar
            max is the maximum number of levels in the tree
            Returns a boolean found and the root of the generated tree."""

        root = Node(Grammar.S, None)
        que = deque()
        que.append(root)        # initialize a queue and enqueue the root
        found = False
        while (len(que)>0 and not found and root.depth <= max):
            # Iterations are per-node q popped from the queue
            q = que.popleft()   # q is the node to analyze
            done = False
            # print("Current node: ", q.name)

            # Decompose q into 'uAv' where A is leftmost non terminal symbol
            leftmost = None
            for i in range(len(q.name)):
                if q.name[i] in Grammar.rules:      # if the symbol is a Head in the Grammar's rules (non-terminal)
                    leftmost = q.name[i]
                    pos = i     # the position of A in uAv
                    break

            if leftmost == None:
                done = True     # No A means we reached a leaf; skip to next iteration

            i = 0  # index of current production of head A

            while (not done and not found):
                # Per production rule of leftmost A
                if i >= len(Grammar.rules[leftmost]):
                    done = True     # Finished exploring all production rules of A
                else:
                    j = i+1
                    u = q.name[:pos]    # The substring to the left of A (prefix)
                    #print("u =", u)
                    w = Grammar.rules[leftmost][i]      # The production body
                    #print("w =", w)
                    v = q.name[pos+1:]      # the substring to the right of A
                    #print("v =", v)
                    uwv = u + w + v
                    #print("uwv: ", uwv)

                    hasNonTerminal = False
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
                        # si se compone solo de terminales y es un prefijo, es un nodo válido para el árbol
                        #print("uwv has non terminal and is valid prefix. enqueuing uwv: ", uwv)
                        node = Node(uwv, q)
                        que.append(node)        # append to tree & updates depth of the tree
                        q.addChild(node)        # enqueue the node to continue BFS

                    if uwv == word:
                        q.addChild(Node(word, q))      # appends to tree while updating depth of the tree
                        found = True
                    i = j

        if root.depth > max: print("Maximum Depth Exceeded. Parsing stopped.")

        return found, root
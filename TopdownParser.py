"""Principal module that contains the classes for the Parsing process.
    Node is a utility class representing the nodes for the derivations tree.
    Node holds attributes for name (value), children nodes list, height, and parent node.
    Parser is the class that traverses an implicit tree to generate a given word from a Grammar."""

from collections import deque

class Node:
    def __init__(self, name, parent):
        self._name=name
        self._children = []
        self._height = 0
        self._parent = parent
        # Leading underscore denotes internal use variables in OOP Python

    def updateDepth(self, childDepth):
        """This method updates a tree's depth by updating heights recursively from last added node up to the root.
          childDepth is the height of the previously updated node in tree"""
        self._height = max(self._height, childDepth + 1)
        # If the node has a parent, update its height too
        if self._parent != None:
            self._parent.updateDepth(self._height)
        # Depth of a tree is our parameter to stop parsing.
        # Height of a root is equal to depth of deepest node.
        # To know when to stop parsing, the Parser checks the height of the root.

    # Method to add a child to this node while also updating the depth of the tree
    def addChild(self, node):
        """node is another instance of Node that is attached as child to this Node.
            We append the child to children list of the node and update the depth of tree."""
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
    # Method that traverses an implicit derivations tree to determine if the given word can be derived.
    def topdown_parse(self, Grammar, word, max):
        """Grammar is an instance of Grammar class
            word is the string to derive from the grammar
            max is the maximum number of levels in the tree
            Returns a boolean whether the word was found and the root of the generated tree."""

        # Make S the root of our tree. Initialize a queue and enqueue the root.
        root = Node(Grammar.S, None)
        que = deque()
        que.append(root)

        found = False

        while (len(que)>0 and not found and root.depth <= max):
            # Per-node iterations, q popped from the queue
            q = que.popleft()
            done = False

            # Decompose q into 'uAv' where A is leftmost non-terminal symbol
            leftmost = None
            for i in range(len(q.name)):
                if q.name[i] in Grammar.rules:      # if the symbol is a Head in the Grammar's rules (non-terminal)
                    leftmost = q.name[i]
                    pos = i         # the position of A in uAv
                    break

            if leftmost == None:
                done = True     # If no leftmost it means we reached a leaf; skip to next iteration

            i = 0  # initialize index for current production of Head A

            while not done and not found:
                # Iterations per-production rule of A
                if i >= len(Grammar.rules[leftmost]):
                    done = True     # Finished exploring all production rules of A
                else:
                    j = i+1
                    u = q.name[:pos]    # The substring to the left of A (prefix)
                    w = Grammar.rules[leftmost][i]      # The production body
                    v = q.name[pos+1:]      # the substring to the right of A
                    uwv = u + w + v

                    hasNonTerminal = False
                    nextpos = pos

                    for i in range(pos, len(uwv)):      # for-loop to find next non-terminal symbol
                        if uwv[i] in Grammar.rules:
                            hasNonTerminal = True
                            nextpos = i
                            break

                    if hasNonTerminal and uwv[:nextpos] == word[:nextpos]:
                        # If uwv has a non-terminal and the terminal prefix matches a prefix in word, it is a valid node
                        node = Node(uwv, q)
                        que.append(node)        # append to tree & update depth of the tree
                        q.addChild(node)        # enqueue the node to continue BFS

                    if uwv == word:
                        q.addChild(Node(word, q))      # appends to tree while updating depth of the tree
                        found = True
                    i = j

        if root.depth > max: print("Maximum Depth Exceeded. Parsing stopped.")

        return found, root

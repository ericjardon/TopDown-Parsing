from TopdownParser import Node

class TreePrinter:
    """Class that prints a horizontal tree to console given a
    Node object that represents the root."""
    mid = "├──"
    last = "└──"
    branch = "│"
    tree = ""
    # Characters for horizontal tree formatting

    # Helper method that recursively builds the string representing a Tree
    def printNodes(self, space, character, node, isLast):
        """space is the accumulated whitespace to the left.
                character is the symbol representing the tree's branches
                node is the node to print in this call
                isLast is a boolean that indicates if it is the last child node of previous node"""
        self.tree += "\n"
        self.tree += space
        self.tree += character
        self.tree += node.name

        # Only if the given node has children nodes do we call printNodes recursively
        if (len(node.children) != 0):
            nextSpace = space
            if (isLast):
                nextSpace += "   "
            else:
                nextSpace += "│  "

            for i in range(0, len(node.children) - 1):
                self.printNodes(nextSpace, self.mid, node.children[i], False)

            self.printNodes(nextSpace, self.last, node.children[-1], True)

    # Main method that prints the tree given a root
    def printTree(self, root):
        """root is an instance of the Node class.
            Prints to console the tree built by printNodes helper function"""
        self.tree = root.name
        for i in range(0, len(root.children) - 1):
            self.printNodes("", self.mid, root.children[i], False)

        self.printNodes("", self.last, root.children[-1], True)

        print(self.tree)
from TopdownParser import Node

class TreePrinter:
    mid = "├──"
    last = "└──"
    branch = "│"
    tree = ""

    def printNodes(self, space, character, node, isLast):
            # Recursively build the string representing a Tree without printing to console
            self.tree += "\n"
            self.tree += space
            self.tree += character
            self.tree += node.name

            if (len(node.children) != 0):
                nextSpace = space
                if (isLast):
                    nextSpace += "   "
                else:
                    nextSpace += "│  "

                for i in range(0, len(node.children) - 1):
                    self.printNodes(nextSpace, self.mid, node.children[i], False)

                self.printNodes(nextSpace, self.last, node.children[-1], True)


    def printTree(self, root):
        self.tree = root.name
        for i in range(0, len(root.children) - 1):
            self.printNodes("", self.mid, root.children[i], False)

        self.printNodes("", self.last, root.children[-1], True)

        print(self.tree)
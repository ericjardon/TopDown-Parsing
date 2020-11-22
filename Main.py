from TopdownParser import Parser, Node
from readfile import readGrammar
from TreePrinter import TreePrinter

def main():
    user = 1
    while (user!=0):
        if (user == 1):
            filename = input("Type the Grammar filename: ")
            G = readGrammar(filename)

        word = input("Type the word: ")
        max = int(input("Type maximum depth of parsing tree: "))

        result, tree = Parser().topdown_parse(G, word, max)
        print("------------------------")
        if result:
            print(word, "is accepted")
        else:
            print(word, "is rejected")

        user = int(input("Press:\n1 -- to try another file, \n2 -- to view the Derivations Tree,\n0 -- to exit,\n"
                         "any other -- to try another word: "))

        if (user == 2):
            # print(tree)
            print('=====================')
            TreePrinter().printTree(tree)
            print('=====================')

    print("Bye!")

main()
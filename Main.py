from TopdownParser import Parser, Node
from readfile import readGrammar

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

        user = int(input("Type 1 to try another file, \n2 to view the derivations tree,\n 0 to exit,\n"
                         "any other number to try another word"))

        if (user == 2):
            print(tree)


    print("Bye!")

main()
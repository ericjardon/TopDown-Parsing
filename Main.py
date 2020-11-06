from TopdownParser import Parser, Node
from readfile import readGrammar

def main():
    using = 1
    while (using!=0):
        if (using == 1):
            filename = input("Type the Grammar filename: ")
            G = readGrammar(filename)

        word = input("Type the word: ")

        result, tree = Parser().topdown_parse(G, word)
        print("------------------------")
        if result:
            print(word, "is accepted")
        else:
            print(word, "is rejected")

        using = int(input("Type 1 to try another file, 0 to exit, "
                      "2 to view the derivation tree,"
                      "any other number to try another word"))

        if (using == 2):
            print(tree)
            continue

    print("Bye!")

main()
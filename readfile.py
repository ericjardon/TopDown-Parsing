"""Functional based module for reading the component of a grammar
 from the provided .txt file name"""
from Grammar import Grammar

def readGrammar(filename):
    """filename is the name of the txt file to read.
        Returns a Grammar object based on the information on the txt file."""
    f = open(filename, "r", encoding="UTF-8")
    data = f.readlines()
    file_length = len(data)

    # read basic elements of grammar
    nonterminal = data[0].rstrip().split(',')
    terminal = data[1].rstrip().split(',')
    S = data[2].rstrip()

    rules = {}
    for i in range(3, file_length):
        line = data[i].rstrip()
        args = line.split("->")
        if args[0] in rules:
            rules[args[0]].append(args[1])
        else:
            rules[args[0]] = [args[1]]

    return Grammar(nonterminal, terminal, S, rules)

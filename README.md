# TopDown-Parsing
**Integrative Practice Part 2** 

Bryan Alexis Monroy Álvarez A01026848  
Eric Andrés Jardón Chao A01376748

***

### _Description_:  
A console program  that  reads  from  a  given file the  elements  that  define  a  context-free grammar and apply the top-down parsing process for strings given by the user. 
It also prints the derivation tree to the console, if the user wants to.

### _Modules_:  
- **Main**: Driver program that asks input from the user. User can choose the name of the file of the Grammar, enter the word to parse, print the derivations tree if desired, 
and exit the program.
- **Grammar**: Class for a context-free (type 2) Grammar. According to a grammar definition (A grammar is a tuple G=(V, Σ, S, P)).
- **Read file**: Functional based module for reading the component of a grammar from the provided .txt file name.
- **TopdownParser**: Principal module that contains the classes for the Parsing process. Node is a utility class representing the nodes for the derivations tree. Node holds 
attributes for name (value), children nodes list, height, and parent node. Parser is the class that traverses an implicit tree to generate a given word from a Grammar.
- **TreePrinter**: Class that prints a horizontal tree to console given a node object that represents the root.

### _How do we build the tree?_
We are using a implicit tree (We do not explore all the branches) with a back-tracking condition in which we only append a node to the tree if the terminal prefix of the node 
matches a prefix of the user given word, or if the node exactly matches the node in which case we stopped the tree building process.

### _How do we print the tree?_
We created special characters to print an horizontal tree, which every character represented a specific part of the branches. We used a main method (printTree) that calls another
recursive method (printNode), which checked from a given node if it has children and if that was the case we called the method recursively. At each call in the recursion, the 
space is incremented and the character is chosen depending if the node to print is the last child.

### _How do we determine the left most non-terminal symbol?_ 
At each node the algorithm require us to split the word into uAv where u is equivalent to the terminal symbols part of the word, A is the first non-terminal symbol, and v
is the remaing part of the given word. We process each word in a for loop where we determine the position at which the first non-terminal symbol is, and we use that position to 
split the word into the respective parts, substituting the leftmost 'A' for its current production rule. This allow us to perform the left most derivation, to find the given word.

### _How do we know when to stop?_
The whole derivation loop uses three stopping conditions.
1. If the queue of our algorithm is empty: which means that we do not have any other node to process.
2. If the given word was found: this means we reach the node that contains the word.
3. If the maximum depth was reached: this means the tree depth is equal or larger than the maximum number of levels established by the user. Every time we append a node, we update the
height of the nodes of the tree and thus checking the height of the root is the same as checking the depth of the tree.


#### **Note**
**Sample text files are included**

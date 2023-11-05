"""
Assume you are working as a librarian at a public library in Rome. Some new books have arrived, and you are in charge of putting them on a shelf. Your supervisor will give you some instructions, and you will follow his. Each book has a unique ID, and your boss's instructions can be of the following types: 

- **L N** - place the book with ID = N on the shelf to the left of the leftmost existing book
- **R N** - place the book with ID = N on the shelf to the right of the rightmost existing book
- **? N** - Calculate the minimum number of books you must pop from the left or right to have the book with ID = N as the leftmost or rightmost book on the shelf.
  
You must follow your boss's instructions and report the answers to type 3 instructions to him. He guarantees that if he has a type 3 instruction for a book with a specific ID, the book has already been placed on the shelf. 

Remember that once you've answered a type 3 instruction, the order of the books <ins>does not change</ins>. 

**Input:**

The first line contains a single number, n, representing the number of your boss's instructions. The ith instruction the boss gives can be found at each of the following n lines. 

**Output:**

Print your boss's type 3 instructions in the order they appear in the input. 

"""
#Solution:

#First we import the deque class from the collections module. We do this since deques have the appendleft method, which allows us to add an element to the left of the deque.
from collections import deque

#Here we take the number of instructions from the user.
n = int(input().strip())
#Here we create a deque to store the books on the shelf.
books_on_shelf = deque()

#Here we iterate over the instructions.
for i in range(n):
    #Here we take the instruction and the book id from the user.
    instruction, id = input().strip().split()
    #If the instruction is L, we add the book to the left of the leftmost book on the shelf.
    if instruction == "L":
        books_on_shelf.appendleft(id)
    #If the instruction is R, we add the book to the right of the rightmost book on the shelf.
    elif instruction == "R":
        books_on_shelf.append(id)
    #If the instruction is ?, we calculate the minimum number of books we must pop from the left or right to have the book with ID = N as the leftmost or rightmost book on the shelf.
    elif instruction == "?":
        #Here we find the index of the book with the given id.
        book_index = books_on_shelf.index(id)
        #Here we print the minimum number of books we must pop from the left or right to have the book with ID = N as the leftmost or rightmost book on the shelf.
        #We can see that this only depends on the index ("virtual position") of the book on the shelf and the number of books on the shelf.
        #If we know the position of the book on the shelf, the number of books we must pop from the left is the index itself, since the index is the number of books to the left of the book.
        #On the other side, the number of books we must pop from the right is the number of books on the shelf minus the index minus 1, since the index is the number of books to the left of the book and we must take out the book itself to obtain the number of books to the right of the book.
        print(min(book_index, len(books_on_shelf) - book_index - 1))

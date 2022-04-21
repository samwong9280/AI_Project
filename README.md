# Introduction
There's three different files included here:
Iter1.py
Iter2.py
Iter3.py

## Iter1.py Average: 5.95
Iter1 uses pure constraint programming and nothing else. Randomly guessing from it's current list of possible words.

## Iter2.py Average: 5.62
Iter2 uses constraint programming along with some common wordle stratgies. It always guesses crane first, since this is the best known first guess for Wordle. It makes its 2nd guess based on a heuristic which picks a word that has the most unused letters, no repeated letters, and most unused vowels. After it makes that guess it then implements the constraints it previously found and tries to guess the answer. 

## Iter3.Py Average: 4.34
This is the same as Iter2 but after the 2nd guess it only allows the program to guess 
# Wordle Solver

Clues:

0 - Miss: Letter not in the word<br/>
1 - Hit: Letter in the word but wrong spot<br/>
2 - Match: Letter in the word and in the correct spot

Example run:
```
$ python3 wordle_solver.py
8913 words in repository

Guess 1: arose
Correct (C)? or new clues? 11100

Guess 2: ratio
Correct (C)? or new clues? 11001

Guess 3: loran
Correct (C)? or new clues? 02010

Guess 4: hoard
Correct (C)? or new clues? c
Solved!
hoard
```

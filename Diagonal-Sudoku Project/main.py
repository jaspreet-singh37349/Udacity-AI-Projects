# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:52:05 2020

@author: Jaspreet
"""


"""
Use these examples for testing

*Note => Input must be string and empty space must be '.' .
         Also input string must be of 81 length i.e. 9x9 sudoku board

sudoku = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
hard_sudoku = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
.5.......6.3..24...7.1....38.4.....7.........3.....2.97....1.2...96..7.1.......4.
"""



sudoku = input()

assert len(sudoku)==81

rows = 'ABCDEFGHI'
cols = '123456789'
reverse_cols = cols[::-1]

def cross(a,b):
    return [x+y for x in a for y in b]


Boxes = cross(rows,cols)

row_units = [cross(x,cols) for x in rows]

col_units = [cross(rows,y) for y in cols]

square_units = [cross(x,y) for x in ['ABC','DEF','GHI'] for y in ['123','456','789']]

diagonal_units = [[str(cross(x,y)[0]) for x,y in zip(rows,cols)]] + [[str(cross(x,y)[0]) for x,y in zip(rows,reverse_cols)]]


unit_list = row_units + col_units + square_units + diagonal_units

units = dict((s, [u for u in unit_list if s in u]) for s in Boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in Boxes)



def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in Boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


print('Sudoku Game')

display(dict(zip(Boxes,sudoku)))

def grid(values):
    
    arr=[]
    digits = '123456789'
    for val in values:
        if val=='.':
            arr.append(digits)
        else:
            arr.append(val)
        
    return dict(zip(Boxes,arr))
            

sudoku_dict = grid(sudoku)



print('-----------------------------------\nAfter Solving')

def elimination(values):
    
    solved_val = [box for box in values.keys() if len(values[box])==1]
    
    for box in solved_val:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    
    return values

"""After_Elim = elimination(sudoku_dict)"""

def OnlyChoice(values):
    
    for unit in unit_list:
        for digit in cols:
            places = [box for box in unit if digit in values[box]]
            if(len(places)==1):
                values[places[0]] = digit
    return values

"""After_OnlyC = OnlyChoice(After_Elim)"""


def twins(values):
    
    for unit in unit_list:
        len_two = [box for box in unit if len(values[box])==2]
        for box in len_two:
            same = [x for x in len_two if values[x]==values[box]]
            if len(same)==2:
                len_two.remove(same[0])
                len_two.remove(same[1])
                for y in unit:
                    if(y!=same[0] and y!=same[1]):
                        values[y]=values[y].replace(values[same[0]][0],'')
                        values[y]=values[y].replace(values[same[0]][1],'')
    
    
    return values


def reduce_puzzle(values):
    flag=False
    
    while not flag:
        solved_val_before = len([box for box in values.keys() if len(values[box])==1])
        values = elimination(values)
        values = OnlyChoice(values)
        values = twins(values)
        solved_val_after = len([box for box in values.keys() if len(values[box])==1])
        
        flag = solved_val_before==solved_val_after
        
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        
    return values

def search(values):
    values = reduce_puzzle(values)
    
    if values is False:
        return False
    
    if all(len(values[box])==1 for box in Boxes):
        return values
    
    n,box = min((len(values[box]),box) for box in Boxes if len(values[box])>1)

    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        att = search(new_sudoku)
        
        if att:
            return att;

res = search(sudoku_dict)

display(res)




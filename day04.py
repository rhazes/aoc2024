import re
import itertools

test_mode = False
input_file = "input04_test.txt" if test_mode else "input04.txt"
data = []
with open(input_file,'r') as file:
    for line in file:
        data.append(line.strip())


UL = "upLeft"
UR = "upRight"
DL = "downLeft"
DR = "downRight"
LT = "left"
RT = "right"
UP = "up"
DN = "down"
puzzle = data

def make_puzzle():
    right = len(data[0]) - 1
    bottom = len(data) - 1
    return (right,bottom)

def get_letter(col,row):
    if row < 0 or row > puzzle_bottom:
        print(f"ERROR {row} is not in bounds")
        return None

    if col < 0 or row > puzzle_right:
        print(f"ERROR {col} is not in bounds")
        return None

    return puzzle[row][col]


def prob1():
    coords = []
    for row in range(puzzle_bottom + 1):
        for col in range(puzzle_right + 1):
            coords.append((col,row))
    words = []
    for col, row in coords:
        vectors = get_multidirection_coords(col,row)
        for vs in vectors:
            words.append(extract_letters(vs))
    return words.count('XMAS')

def prob2():
    coords = []
    for row in range(puzzle_bottom + 1):
        for col in range(puzzle_right + 1):
            coords.append((col,row))
    count = 0
    for col, row in coords:
        if get_letter(col,row) == 'A':
            xarm1,xarm2 = get_multidirection_from_center_coords(col,row)
            # print(xarm1,xarm2)
            if extract_letters(xarm1) in ['SAM','MAS'] and extract_letters(xarm2) in ['SAM','MAS']:
                count += 1
    return count


# def check(col,row,direction):
#     word = 'XMAS'
#     match direction:
#         case UP:
#             found = True
#             coords = [ (col,row-j) for j in range(4) ]

#             for ((i,j),letter) in zip(coords,word):
#                 if i < 0 or i > puzzle_right:
#                     found = False
#                     break
#                 if j < 0  or j > puzzle_bottom:
#                     found = False
#                     break
#                 if get_letter(i,j) != letter:
#                     found = False
#                     break

def get_up_coords(col,row,n=4):
   return [ (col,row-j) for j in range(n)]

def get_down_coords(col,row,n=4):
   return [ (col,row+j) for j in range(n) ] 
 
def get_left_coords(col,row,n=4):
   return [ (col-i,row) for i in range(n) ] 

def get_right_coords(col,row,n=4):
   return [ (col+i,row) for i in range(n) ] 

def get_up_left_coords(col,row,n=4):
   return [ (col-i,row-i) for i in range(n) ] 

def get_up_right_coords(col,row,n=4):
   return [ (col+i,row-i) for i in range(n) ] 
   
def get_down_left_coords(col,row,n=4):
   return [ (col-i,row+i) for i in range(n) ] 
   
def get_down_right_coords(col,row,n=4):
   return [ (col+i,row+i) for i in range(n) ] 
   
def get_multidirection_coords(col,row):
    coords = []
    for fn in [get_up_coords,
               get_up_right_coords,
               get_right_coords,
               get_down_right_coords,
               get_down_coords,
               get_down_left_coords,
               get_left_coords,
               get_up_left_coords]:
        coords.append( fn(col,row))
    
    return coords
 
def get_multidirection_from_center_coords(col,row):
    ul_to_br = [(col-1,row-1),
                (col,row),
                (col+1,row+1)]
    ur_to_bl = [(col+1,row-1),
                (col,row),
                (col-1,row+1)]
    return [ul_to_br,ur_to_bl]


def extract_letters(vector):
    word = []
    for x,y in vector:
        if x >= 0 and x <= puzzle_right:
            if y >= 0 and y <= puzzle_bottom:
                word.append(get_letter(x,y))
            else:
                word.append(None)
        else:
            word.append(None)

    if None in word:
        return None
    else:
        return "".join(word)

puzzle_right,puzzle_bottom = make_puzzle()

x_vector = []
for j,row in enumerate(puzzle):
    for i,col in enumerate(row):
        if col == 'X':
            for vector in get_multidirection_coords(i,j):
                x_vector.append(vector)

# coords = []
# for row in range(puzzle_bottom + 1):
#     for col in range(puzzle_right + 1):
#         coords.append((col,row))
# words = []
# for col, row in coords:
#     vectors = get_multidirection_coords(col,row)
#     for vs in vectors:
#         words.append(d.extract_letters(vs))


# print(prob1())
print(prob2())

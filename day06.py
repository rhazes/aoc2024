import re
import bisect
import sys


sys.setrecursionlimit(2000)

TESTING = True

NORTH = 0
EAST =  1
SOUTH = 2
WEST =  3

class Player:
    headings = [NORTH,EAST,SOUTH,WEST]

    def __init__(self,pos):
        self.pos = pos
        self.heading = NORTH
        self.heading_idx = 0
        self.steps = 0
        # self.visited_by_row = {}
        self.visited = set() 

    def mt(self): self.move_and_turn()

    def move_and_turn(self):
        new_pos = find_closest_obj(self.heading)
        delta_col,delta_row = [(new_pos[0]-self.pos[0]),(new_pos[1]-self.pos[1])]
        if delta_col != 0:
            delta_col = (delta_col - 1) if delta_col > 0 else (delta_col + 1)
            range_traveled = [ self.visited_by_row[self.pos[1]].append(col) for col in range(self.pos[0],new_pos[0])]
        if delta_row != 0:
            delta_row = (delta_row - 1) if delta_row > 0 else (delta_row + 1)
            range_traveled = [8]

        print(range_traveled)

        self.steps += abs(delta_row + delta_col)
        self.heading_idx = (self.heading_idx + 1) % 4
        self.heading = Player.headings[self.heading_idx]

        self.pos[0] += delta_col
        self.pos[1] += delta_row


    def heading_str(self):
        return ["north","east","south","west"][self.heading_idx]

    def __repr__(self):
        return f"{self.pos}@ {self.heading_str()};step:{self.steps}"

def in_bounds(pos,dim):
   within_width = pos[0] >= 0 and pos[0]<dim[0]  
   within_height = pos[1] >= 0 and pos[0]<dim[1]  
   return within_height and within_width


def ray_cast(start,dir,board):
    """return the coords of the first hit obj"""
    found = None
    _pos = start

    def step_fn(coord): 
        return coord[0] + dir[0], coord[1] + dir[1]

    # North find the next obstacle above in y
    obstacles_north = by_col[_pos[0]]

    # while found is None and in_bounds(_pos):
        # pass
        
def get_obs_north(pos, col_objs):
    objs_north = [obs for obs in col_objs[pos[0]] if obs[0] == pos[0]\
]    
    objs_north.sort(key = lambda x: x[1])
    return objs_north

def find_closest_obj(dir):
    col,row = player.pos
    obj_in_col = by_col[col]
    obj_in_row = by_row[row]

    if dir in [NORTH,SOUTH] and len(obj_in_col) == 0:
        print(f"EXIT MAZE to {dir}")
        return None

    if dir in [EAST,WEST] and len(obj_in_row) == 0:
        print(f"EXIT MAZE to {dir}")
        return None

    
    match dir:
        case 0: #NORTH
            os = [obj for obj in obj_in_col if obj[1] < row]

            if len(os) == 0:
                print("EXIT MAZE to NORTH")
                return None

            os.sort(key=lambda coord: coord[1])
            closest = os[-1]

        case 2: # SOUTH
            os = [obj for obj in obj_in_col if obj[1] > row]

            if len(os) == 0:
                print("EXIT MAZE to SOUTH")
                return None

            os.sort(key=lambda coord: coord[1])
            closest = os[0]

        case 3: # WEST
            os = [obj for obj in obj_in_row if obj[0] < row]

            if len(os) == 0:
                print("EXIT MAZE to WEST")
                return None

            os.sort(key=lambda coord: coord[0])
            closest = os[-1]

        case 1: # EAST
            os = [obj for obj in obj_in_row if obj[0] > row]

            if len(os) == 0:
                print("EXIT MAZE to EAST")
                return None

            os.sort(key=lambda coord: coord[0])
            closest = os[0]
    return closest

def parse_input():
    cols = None
    rows = 0
    objs = []
    by_row = {}
    by_col = None
    player = None
    with open(['input06.txt','input06_test.txt'][TESTING],'r') as FILE:
        for line in FILE:
            by_row[rows] = []
            line = line.strip()
            if cols is None:
                cols = len(line)

            if by_col is None:
                by_col = {}
                for i in range(cols):
                    by_col[i] = []

            for m in re.finditer("#",line):
                coord = (m.start(),rows)
                objs.append(coord)
                by_row[rows].append(coord[0])
                by_col[m.start()].append(coord[1])
            
            # look for player
            player_match = re.search(r"\^",line)
            if player_match and player_match.span()[1] > 0:
                player = Player([player_match.start(),rows])
            rows += 1

        # sort all of the rows
        for vals in by_row.values():
            vals.sort()
            # vals.sort(key= lambda x: x[0])
            
    return (by_row,by_col,objs,(cols,rows),player)

by_row,by_col,objs,(board_width,board_height),player = parse_input()

def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

pos = player.pos
visited = set()
visited_map = {}

# visited.add((pos[0],pos[1]))
STEP = [(0,-1),(1,0),(0,1),(-1,0)]
HEADING = [NORTH,EAST,SOUTH,WEST]
heading_idx = 0

def walk_to_exit(pos):
    global heading_idx,HEADING,STEP,visited
    if not in_bounds(pos,(board_width,board_height)):
        print("exiting the puzzle")
        return "exit"
    else:
        #if next step in direction is an obstacle turn
        col,row = add(pos,STEP[heading_idx])
        if row < 0 or row >= board_height:
            return "exit"  
        elif col in by_row[row]:
            print("turning...")
            heading_idx = (heading_idx + 1) % 4
            return pos
        else:
            print("\tstepping...")
            col,row = add(STEP[heading_idx],pos)
            visited.add((col,row))
            if not row in visited_map:
                print("creating visited map")
                visited_map[row] = {}
                visited_map[row][col] = None

            if not col in visited_map[row]:
                visited_map[row][col] = None
            
            if HEADING[heading_idx] in [NORTH,SOUTH]:
                curr_dir_symbol = '|'
            else:
                curr_dir_symbol = '-'

            # print(f"keys:{visited_map.keys()}, trying key:{pos[1]} ...f{visited_map[pos[1]].keys()}")
            print(f"pos1:{row} pos0:{col}")
            last_dir_symbol =  visited_map[row][col]
            if last_dir_symbol:
                if last_dir_symbol != '+':
                    if last_dir_symbol != curr_dir_symbol:
                        visited_map[row][col] = '+'
            else:
                visited_map[row][col] = curr_dir_symbol

        return (col,row)

n = 8000
next_pos = None
while n > 0 and next_pos != "exit":
    next_pos = walk_to_exit(pos)
    if next_pos == "exit":
        break
    visited.add(next_pos)
    pos = next_pos
    n -= 1
if n == 0:
    print("!!!the loop bottomed out before completing!!!")
#5243 is too high by 1 ??? Fixed
print(f"ans={len(visited)}")
import re
import bisect
import sys


sys.setrecursionlimit(2000)

TESTING = True

NORTH = 0
EAST =  1
SOUTH = 2
WEST =  3
DIRS = ['north','east','south','west']

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


# def ray_cast(start,dir,board):
#     """return the coords of the first hit obj"""
#     found = None
#     _pos = start

#     def step_fn(coord): 
#         return coord[0] + dir[0], coord[1] + dir[1]

#     # North find the next obstacle above in y
#     obstacles_north = by_col[_pos[0]]

#     # while found is None and in_bounds(_pos):
#         # pass
        
# def get_obs_north(pos, col_objs):
#     objs_north = [obs for obs in col_objs[pos[0]] if obs[0] == pos[0]\
# ]    
#     objs_north.sort(key = lambda x: x[1])
#     return objs_north

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

def step(a,b):
    return (a[0]+b[0],a[1]+b[1])

pos = player.pos
visited = set()
visited_map = {}
patrol_turns = set()

# visited.step((pos[0],pos[1]))
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
        col,row = step(pos,STEP[heading_idx])
        if row < 0 or row >= board_height:
            return "exit"  
        elif col in by_row[row]:
            # print("turning...")
            heading_idx = (heading_idx + 1) % 4
            # store the turn
            patrol_turns.add(pos)
            return pos
        else:
            # print("\tstepping...")
            col,row = step(STEP[heading_idx],pos)
            visited.add((col,row))
            if not row in visited_map:
                # print("creating visited map")
                visited_map[row] = {}
                visited_map[row][col] = None

            if not col in visited_map[row]:
                visited_map[row][col] = None
            
            if HEADING[heading_idx] in [NORTH,SOUTH]:
                curr_dir_symbol = '|'
            else:
                curr_dir_symbol = '-'

            # print(f"pos1:{row} pos0:{col}")
            last_dir_symbol =  visited_map[row][col]
            if last_dir_symbol: # update to a corner location
                if last_dir_symbol != '+':
                    if last_dir_symbol != curr_dir_symbol:
                        visited_map[row][col] = '+'
            else:
                visited_map[row][col] = curr_dir_symbol

            #### 
            # check this step to see if there is an already 
            # traversed path to the right # that leads to an obstacle
            obj_to_right = None
            closest = None
            if heading_idx == NORTH:
                # find obj with higher col
                if not by_row[row] == []:
                    obj_to_right = [ obj_col for obj_col in by_row[row] if obj_col > col ]
                    if obj_to_right != []: 
                        obj_to_right.sort()
                        closest = (obj_to_right[0],row)
                        print(f"found an obj to the east of pos {col},{row} {closest}")

            if heading_idx == SOUTH:
                # find obj with higher col
                if not by_row[row] == []:
                    obj_to_right = [ obj_col for obj_col in by_row[row] if obj_col < col ]
                    if obj_to_right != []:
                        obj_to_right.sort()
                        closest = (obj_to_right[0],row)
                        print(f"found an obj to the west of pos {col},{row} {closest}")

            if not closest is None:
                path = get_path_in_dir((col,row),closest)
                if path is None:
                    print(f"weird that we have a closest and path is none: closest: {closest} to pos: {(col,row)}")
                print(f"path to closest { closest} is {path}...",end=' ')
                all_seen = all( [ coord in visited for coord in path])
                print(f"has been traversed = {all_seen}")

        return (col,row)

def draw_map():
    for row in range(board_height):
        for col in range(board_width):
            if (col,row) in objs:
                print("#",end=' ')
                continue
            if not row in visited_map:
                print(".",end=' ')
                continue
            if not col in visited_map[row]:
                print(".",end=' ')
                continue
            print(visited_map[row][col],end=' ')
        print()

def prob1():
    n = 8000
    next_pos = None
    pos = player.pos
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

# def east_candidates(pos):
#     col = pos[0] + 1
#     row = pos[1] + 1

#     if col < 0 or col >= board_width:
#         return []

#     if row < 0 or row >= board_height:
#         return []

#     candidates = [ (c,row) for c in by_row[row] if c > col]

def get_candidates(dir,pos):
    col = pos[0]
    row = pos[1]
    candidates = None
    candidate = None

    def valid_coord(c,r):
        if c < 0 or c >= board_width:
            return False 
        elif r < 0 or r >= board_height:
            return False
        return True

    match dir:
        case 0: #NORTH
            col += 1
            row -= 1
            if valid_coord(col,row):
                candidates = [ (col,r) for r in by_col[col] if r < row ]
        case 1: #EAST
            col += 1
            row += 1
            if valid_coord(col,row):
                candidates = [ (c,row) for c in by_row[row] if c > col]
        case 2: #SOUTH
            col -= 1
            row += 1
            if valid_coord(col,row):
                candidates = [ (col,r) for r in by_col[col] if r > row ]
        case 3: #WEST
            col -= 1
            row -= 1
            if valid_coord(col,row):
                candidates = [ (c,row) for c in by_row[row] if c < col]

    if candidates in [[],None]:
        candidates = None
    else:
    # if not candidates is None:
        candidates.sort(key= lambda coord: manhattan(pos,coord))
        candidate = candidates[0]

    return candidate #candidates

# def west_candidates(pos):
#     col = pos[0] - 1
#     row = pos[1] - 1 
#     if col < 0 or col >= board_width:
#         return []

#     if row < 0 or row >= board_height:
#         return []

#     candidates = [ (c,row) for c in by_row[row] if c < col]
    
#     if len(candidates) == 0:
#         return None

#     if len(candidates) == 1:
#         return candidates[0]

#     closest = candidates[0]
#     min_dist = manhattan(closest, pos)
#     for coord in candidates:
#         d = manhattan(coord,pos)
#         if d < min_dist:
#             closest = coord
#             min_dist = d 

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1])

# def north_candidates(pos):
#     col = pos[0] + 1 
#     row = pos[1] - 1
#     if col < 0 or col >= board_width:
#         return []

#     if row < 0 or row >= board_height:
#         return []

#     candidates = [ (col,r) for r in by_col[col] if r < row ]

# def south_candidates(pos):
#     col = pos[0] - 1
#     row = pos[1] + 1

#     if col < 0 or col >= board_width:
#         return []

#     if row < 0 or row >= board_height:
#         return []

#     candidates = [ (col,r) for r in by_col[col] if r > row ]

def get_loop_candidates(pos):
    # ret = {}
    ret = { dir:get_candidates(idx,pos) for idx,dir in enumerate(DIRS)}
    return ret

def flatten_candidates(candidates):
    return [ coord for coords in candidates if not coords is None for coord in coords]

def build_loop(dirs,obj_pos):
    """helper function to get the number of non-None entries in loop candidates"""
    if len(dirs) == 0:
        return []
    
    direction = dirs[0]
    # candidates = get_candidates(direction,obj_pos)
    candidate = get_candidates(direction,obj_pos)
    # print(candidate)
    if not candidate is None:
        return [obj_pos] + build_loop(dirs[1:], candidate)
    # if not candidates is None:
        candidate = candidates[0]
        # return [obj_pos] + build_loop(dirs[1:], candidate)
    else:
        return []

def check_loops(obj_pos):
    cycles = [[0,1,2,3],
              [1,2,3,0],
              [2,3,0,1],
              [3,0,1,2]]

    return [ build_loop(cycle,obj_pos) for cycle in cycles]

def get_empty_cells():
    prob1()
    empties = [ (col,row) for row in range(board_height) for col in range(\
                    board_width) if col not in by_row[row]]  
    empty_loops = { coord:get_loop_candidates(coord) for coord in \
                    empties}

def is_loop_closed(loop):
    objs_for_last_elem_in_loop = get_loop_candidates(loop[-1])
    lst = list(objs_for_last_elem_in_loop.values())

    # filter out blank ones
    lst = [l for l in lst if not l is None]

    #True if the first elem of the loop is also connected
    # to the last_elem in the loop
    return loop[0] in lst

def get_turn_dir(coord1,coord2):
    c1,r1 = coord1
    c2,r2 = coord2
    delta_col = c2 - c1
    delta_row = r2 - r1
    if abs(delta_col) == 1:
        # has to be north south
        if delta_row > 0:
            return SOUTH
        else:
            return NORTH
    if abs(delta_row) == 1:
        # has to be east/west
        if delta_col > 0:
            return EAST
        else:
            return WEST

def get_dir_to_close_loop(loop):
    first_dir = get_turn_dir(loop[0],loop[1])
    last_dir = (first_dir - 1) % 4
    return last_dir

def flip_dir(dir):
    return (dir + 2) % 4

def get_points_til_cross(start,end,dir):
    pass

def is_subset(a,b):
    intersection = a.intersection(b)
    return len(intersection) == len(a)

def get_points_to_close_loop(loop):
    c1,c2,c3,c4 = loop
    dir_to_home = get_dir_to_close_loop(loop)
    coords = set()
    if dir_to_home == NORTH:
        # go south til you get to c4_row
        coords = set([ (c1[0],r) for r in range(c1[1],c4[1]+1) ])
    elif dir_to_home == SOUTH:
        # go north til you get to c4
        coords = set([ (c1[0],r) for r in range(c1[1], c4[1]-1) ])
    elif dir_to_home == EAST:
        # go west til you get to c4
        coords = set([ (c,c1[1]) for c in range(c1[0],c4[0]-1) ])
    elif dir_to_home == WEST:
        # go east til you get to c4
        coords = set([ (c,c1[1]) for c in range(c1[0], c4[0]+1) ])
    else:
        print(f"ERROR unknown direction: {dir_to_home}")
    return coords

def get_path_in_dir(coord1,coord2):
    c1,r1 = coord1
    c2,r2 = coord2
    delta_col = c2 - c1
    delta_row = r2 - r1

    col_step = 1 if delta_col > 0 else -1
    row_step = 1 if delta_row > 0 else -1

    print(f"from {c1} to {c2}",end = ' ')
    print(f"from {r1} to {r2}")
    points = None

    if abs(delta_col) > 1:
        row = r1 + delta_row # going east
        points = [ (c,row) for c in range(c1,c2,col_step)]
    elif abs(delta_row) > 1:
        col = c1 + delta_col # going east
        points = [ (col,r) for r in range(r1,r2,row_step)]
    else:
        print(f"ERROR bad points: {coord1} and {coord2}")
    return points



# Part 2 Script
def prob2():
    prob1()
    maybes = [check_loops(o) for o in objs]
    loop_4 = [f for fs in maybes for f in fs if len(f) == 4 ]
    not_closed = [l for l in loop_4 if not is_loop_closed(l) ] 

    potential_paths = [get_points_to_close_loop(l) for l in not_closed]
    validate_paths = [is_subset(path,visited) for path in potential_paths] 
    validate_paths = [p for p in validate_paths if p ]
    print(f"count of valid obstacles that interrupt existing\
         closed loop: {len(validate_paths)}") # 923

    loop_3 = [f for fs in maybes for f in fs if len(f) == 3 ]
    

    return (loop_3,not_closed)
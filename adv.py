from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
# creates the current player
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n','n', 's', 's', 's', 's', 'n','n','e', 'e', 'w', 'w', 'w', 'w']
# traversal_path = ['n', 'n']
traversal_path = []

# TRAVEL GRAPH - bft
visited = {} # { 0: {'n':'?', 's':'?', 'w':'?', 'e':'?'} }
# { 0: {'n':1} }
# { 1: {'n':2, 's':0}
# { 2: {'s':1} }

# FIND OPPOSITE DIRECTION
def get_opposite_direction(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'

# ADD UNVISTED ROOM TO VISITED
def add_to_visited(room_id, exits_list):
    exits_dict = {}
    # iterate through exits,
    for exit in exits_list:
        # add up exits in a {} with '?'
        exits_dict[exit] = '?'
    # add room to visited
    visited[room_id] = exits_dict

# CHECK FOR UNVISTED ROOMS
def check_unvisited(room_id):
    flag = False
    print('test:', visited, room_id)
    if visited[room_id]['n'] == '?':
        flag = True
    if visited[room_id]['s'] == '?':
        flag = True
    if visited[room_id]['e'] == '?':
        flag = True
    if visited[room_id]['w'] == '?':
        flag = True
    return flag

# SAVE EXITS, cur room id
exits_list = player.current_room.get_exits() # ['n'] 
direction = exits_list[-1] # 'n'
# print('starting room:', player.current_room.id, 'starting exists:', exits_list)
# INIT STACK or QUEUE
s = Stack()

# ENQUEUE FIRST ITEM - tuple of direction and previous room - (0, 'n')
s.push( (None, direction) ) # (0, 'n')
# enqueue all cur room exits in tuple (room_id, direction ) (0, 'n')
# for exit in first_exits_list:
#     q.enqueue( (player.current_room.id, exit) )

# loop while queue is not empty
while s.size() > 0:
    # dequeue first room
    room_info = s.pop() # (None, 'n') -> (0, 'n')
    prev_room_id = room_info[0] # None -> 0 
    curr_room_id = player.current_room.id # 0 -> 1
    print('dequeued room info:', room_info) # (None, 'n) -> (0, 'n)
    print('prev_room:', prev_room_id) # None -> 0
    print('cur_room:', curr_room_id) # 0 -> 1

    # ADD TO VISITED IF UNVISITED
    # if room has not been visited,
    if curr_room_id not in visited:
        exits_list = player.current_room.get_exits()
        add_to_visited(curr_room_id, exits_list)
        print('visited1:', visited) # { 0: {'n':'?'} } -> {0: {'n': '?'}, 1: {'n': '?', 's': '?'}}

        # UPDATE PREV ROOM'S DIRECTION AND UPDATE CUR ROOM'S OPPOSITE DIRECTION
        opp_dir = get_opposite_direction(direction)
        if prev_room_id is not None:
            visited[prev_room_id][direction] = curr_room_id
            print('visited after updated:', visited) # 2nd time around: {0: {'n': 1}, 1: {'n': '?', 's': 0}}
        # set cur room's past room
        visited[curr_room_id][opp_dir] = prev_room_id

        # GET EXITS
        exits = player.current_room.get_exits() 
        print('get exits:', exits) # ['n'] -> ['n', 's']

        # ADD TO QUEUE/STACK
        # add new room exits to queue to travel to later
        for direction in exits:
            print('dir:', direction)

            # TRAVEL TO A ROOM
            print('curID:', curr_room_id)
            if visited[curr_room_id][direction] == "?":
                
                # ADD FUTURE ROOMS TO STACK
                s.push((curr_room_id, direction))
                player.travel(direction)
                # curr_room_id = player.current_room.id # 0 
                print('cur_rom id:', curr_room_id)

        # TODO: if room has no ?s - helpfer func
        if check_unvisited(curr_room_id) == True:
            print('here')
            # go backwards, pop off stack

        # BFS to find any unvisited rooms with ?s
            # destination is a room with ?s
            # buid a path to traverse after finding destination

        # step back a room and check that room for more rooms
        # pop from stack to travel
        print('stack after pushed:', s) # [(0, 'n')]


    # ADD TO TRAVERSAL PATH
    traversal_path.append(direction)
    print('.......')



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# TO WALK AROUND
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

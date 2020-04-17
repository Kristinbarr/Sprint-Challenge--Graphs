from room import Room
from player import Player
from world import World
from util import Queue

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
# { 0: {'n':'?'} }
# { 1: {'n':'?', 's':'?'}
# { 2: {'s':'?'}

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

q = Queue()
# enqueue all cur room exits in tuple (room_id, direction ) (0, 'n')
exits_list = player.current_room.get_exits()

for exit in exits_list:
    print('exit:', exit)
    q.enqueue( (player.current_room.id, exit) )
# enqueue first room id - [ {0:[n]}, {1:[n,s]}, {2:[s]} ]
# q.enqueue(player.current_room.id)

# loop while queue is not empty
while q.size() > 0:
    # dequeue first room - (0, 'n')
    room = q.dequeue()
    room_id = room[0]
    print('room:', room, 'roomId:', room_id)
    # save cur room as previous
    prev_room_id = room_id

    # ADD TO VISITED IF UNVISITED
    # if room has not been visited,
    if room_id not in visited:
        add_to_visited(room_id, exits_list)

        # GET EXITS
        # variable for exits direction list
        exits = player.current_room.get_exits()
        # pick last direction in list
        direction = exits[-1]

        # ADD TO QUEUE/STACK
        # add new room to queue so we can travel all it's exits
        q.enqueue((room_id, direction))


        # TRAVEL TO NEW ROOM
        # if value is a ?, travel to it
        if visited[room_id][direction] == "?":
            player.travel(direction)
        # TODO: if no rooms have ?, it's a dead end or been traveled already, start over?

        # UPDATE TRAVELED DIRECTION FOR PREV ROOM
        # update last room's opposite direction to be the cur room
        opp_dir = get_opposite_direction(direction)
        visited[prev_room_id][opp_dir] = player.current_room.id
        # update cur room's cur direction to be the next room
        # next_room_id = player.current_room.get_room_in_direction(direction).id
        # visited[room_id][direction] = next_room_id


        # ADD TO TRAVERSAL PATH
        traversal_path.append(direction)





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

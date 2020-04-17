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

# RANDOM DIRECTION GENERATOR [n, s, e, w]
def random_direction():
    dirs = ['n', 's', 'e', 'w']
    return random.choice(dirs)

# CONSTRUCT A TRAVEL GRAPH - bft
visited = {} # { 0: {'n':'?', 's':'?', 'w':'?', 'e':'?'} }

q = Queue()
# enqueue first room id
print('cur room id:', player.current_room.id)
q.enqueue(player.current_room.id)

# loop while queue is not empty
# maybe loop while room is valid?
while q.size() > 0:
    # dequeue first room
    room = q.dequeue()
    print('room id:', room)
    # pick a random unexplored direction from cur room, unexplored = '?'
    direction = random_direction()
    print('direction:', direction)

    # check if room can be traveled to
    if player.current_room.get_room_in_direction(direction) != None:
        # travel to that room
        player.travel(direction)
        # log that direction
        traversal_path.append(direction)

        # get possible rooms possible
        unvisited = player.current_room.get_exits()
        # print('unvisited:', unvisited) # ['n', 's']

        # save cur rooms to add to visited
        cur_room_dict = {}

        # loop through list of rooms
        for next_room in unvisited:

            # if next_room != '?':
                # add each room to room dict
                cur_room_dict[next_room] = '?'
                print('cur room dict', cur_room_dict)
            # enqueue each room
            q.enqueue(next_room)

        # add cur room to visited
        visited[player.current_room.id] = cur_room_dict
        print('visited dict:', visited)



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

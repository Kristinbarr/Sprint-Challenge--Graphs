from room import Room
from player import Player
from world import World
from graph import Graph

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
# create a new player. room_graph will start player at room 0
player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []
# traversal_path = ['n','n']
# traversal_path = ['n','n','s','s','s','s','n','n','e','e','w','w','w','w']


# BUILD A GRAPH, add to traveral_path similtaneously during building

# instantiate graph
graph = Graph()

# room_graph: {
#     0: [ (3, 5), {'n': 1} ], 
#     1: [ (3, 6), {'s': 0, 'n': 2} ], 
#     2: [ (3, 7), {'s': 1} ],
# }
# graph: { 
#   0:{'n':1}, 
#   1:{'s':0,'n':2}, 
#   2:{'s':1} 
# }

# iterate through room_graph
for room_id in room_graph:
    # check if room is present
    if room_id not in graph.rooms:
        # if not, insert room - do all exits get inserted?
        graph.add_room(room_id, room_graph[room_id][1])
    

    # generate random exit direction
    directions = ['n','s','e','w']
    # print([random.randint(0,3) for i in directions])

    # iterate over exits
        # check if its a valid move
        # add exit direction to traversal list
        # add exit to the graph

# functions to use:
# player.current_room.id
# player.current_room.get_exits()
# player.travel(direction)


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


# WALK AROUND
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

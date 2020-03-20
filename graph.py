from util import Stack, Queue

# {
#     0: [ (3, 5), {'n': 1} ], 
#     1: [ (3, 6), {'s': 0, 'n': 2} ], 
#     2: [ (3, 7), {'s': 1} ],
# }

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.rooms = {}

    def __str__(self):
        return f"{self.rooms}\n"

    def add_room(self, room_id, room_exits):
        """
        Add a room to the graph.
        """
        print('ROOM EXITS:',room_exits)
        # clear all exits: to '?'
        # add room to graph
        self.rooms[room_id] = set()

    # graph w 3 rooms: { 0:{'n':1}, 1:{'s':0,'n':2}, 2:{'s':1} }

    def add_edge(self, r1, r2, direction):
        """
        Add a undirectional edge connecting 2 rooms
        """
        # if rooms contain both r1 and r2,
        if r1 in self.rooms and r2 in self.rooms:
            # r1 is key, r2 is value in the set (.add overrides value?)
            self.rooms[r1].add(r2)
            # self.rooms[r2].add(r2)
        else:
            raise ValueError("vertex does not exist")


    def get_neighbors(self, room_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if room_id in self.room:
            return self.rooms[room_id]
        else:
            # print("ERROR: vertex does not exist")
            raise ValueError("vertex does not exist")


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create a stack
        s = Stack()
        # push the starting vertex
        s.push(starting_vertex)
        # create a set to store visited vertices
        visited = set()
        # while the stack is not empty,
        while s.size() > 0:
            # pop the first vertex
            v = s.pop()
            # check if it's been visited
            # if it hasn't been visited,
            if v not in visited:
                # mark it as visited
                print(v)
                visited.add(v)
                # push all it's neighbors onto the stack
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)


        # iterate through exits?
        # player.current_room.get_exits()
        # add each exit to a room dict, value unknown for now ... { n:?, s:?, e:?, w:? }
        # add cur_room to traversal graph ... { 0: { n:?, s:?, e:?, w:? } }

        # save previous room id



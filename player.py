class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room

    def travel(self, direction, show_rooms = False):
        ''' 
        takes a direction, moves the player
        also take arg show_rooms option, default to false
        if no room in that direction, returns error message
        '''
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room is not None:
            self.current_room = next_room
            if (show_rooms):
                next_room.print_room_description(self)
        else:
            print("You cannot move in that direction.")

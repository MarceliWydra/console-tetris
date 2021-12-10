import random
from getkey import getkey

ALLOWED_SHAPES = [
    {"shape": [(1,1), (2,1), (3,1), (4,1)], "width": 4}, # horizontal I
    {"shape": [(1,1), (2,1), (1,2), (2,2)], "width": 2}, # square
    {"shape": [(1,1), (1,2), (1,3), (2,3)], "width": 3}, # L
    {"shape": [(2,1), (2,2), (2,3), (1,3)], "width": 3}, # J
    {"shape": [(2,1), (2,2), (1,2), (1,3)], "width": 3}, # bolt
]
GAME_WIDTH = 20
GAME_HEIGHT = 20

class Block(object):
    def __init__(self) -> None:
        super().__init__()
        self.shape = None
        self.x = 0
        self.y = 0
        self.rotation = 1
        self.original_shape = None
        self.width = 0
        self.shape_index = None
    
    def generate_new_block(self, range):
        choice = random.choice(ALLOWED_SHAPES)
        start_point = random.randrange(1, range - choice["width"])
        self.shape = [(x[0]+start_point, x[1]-1) for x in choice["shape"]]
        self.x = start_point
        self.y = 0
        self.shape_index = ALLOWED_SHAPES.index(choice)
        self.original_shape = choice["shape"]
        self.width = choice["width"]
    

    def is_valid_move(self, new_move, board):
        try: 
            moves = any([True for x in new_move if x[0] in board[x[1]]])
            return not moves
        except Exception:
            return False


    def relocate(self, direction):
        return [(x[0]+direction, x[1]+1) for x in self.shape]


    def move(self, direction: int, board):
        new_move = self.relocate(direction)
        if self.is_valid_move(new_move, board):
            self.shape = new_move
            self.x += direction
            self.y += 1
            return True
        return False
    
    def rotate(self, direction):
        if self.width != 2: # square shape cannot rotate
            new_shape = []
            if direction == "counter-clock":
                for point in self.original_shape:
                    x = point[1]
                    y = 1 - (point[0] - (self.width - 2))
                    new_shape.append((x,y))
            elif direction == "clock":
                for point in self.original_shape:
                    x = 1 - (point[1] - (self.width - 2))
                    y = point[0]
                    new_shape.append((x,y))
            temp_shape = [(x[0]+self.x, x[1]+self.y+1) for x in new_shape]
            return new_shape, temp_shape
        return None, None

    def move_rotate(self, direction: str, board):
        new_shape, temp_shape = self.rotate(direction)
        if new_shape and self.is_valid_move(temp_shape, board):
            self.original_shape = new_shape
            self.shape = temp_shape
            self.y += 1
            return True
        return False



class Game(object):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.game_over = False
        self.board = []
        self.height = height
        self.width = width
        self.y = 0

        # initialize empty board
        for i in range(height):
            row = [x for x in range(width+2) if (x == 0 or x == width+1)]
            self.board.append(row)
        
        #added last row with bottom border
        last_row = [x for x in range(width+2)]
        self.board.append(last_row)


    def add_to_board(self, shape):
        for point in shape:
            self.board[point[1]].append(point[0])
    
    def remove_from_board(self, shape):
        for point in shape:
            self.board[point[1]].remove(point[0])

    def is_valid_move_exist(self, block: Block):
        move_left = block.is_valid_move(block.relocate(-1),self.board)
        move_right = block.is_valid_move(block.relocate(1),self.board)
        rotate_cc = block.is_valid_move(block.rotate("counter-clock")[1], self.board)    
        rotate_clock = block.is_valid_move(block.rotate("clock")[1], self.board)    
        return move_right or move_left or rotate_cc or rotate_clock

    def draw_board(self):
        for row in self.board:
            printed_row = ["*" if x in row else " " for x in range(self.width+2)]
            print(*printed_row, sep="")



    def main_loop(self):
        block = Block()
        # add first block outside of the game loop
        block.generate_new_block(self.width-2)
        self.add_to_board(block.shape)
        self.draw_board()

        new_move = []
        game_over = False
        while not game_over:
            self.remove_from_board(block.shape)
            if self.is_valid_move_exist(block):
                key = getkey()
                if key: 
                    if key == "d":
                        new_move = block.move(1, self.board)
                    elif key == "a":
                        new_move = block.move(-1, self.board)
                    elif key == "w":
                        new_move = block.move_rotate("counter-clock", self.board)
                    elif key == "s":
                        new_move = block.move_rotate("clock", self.board)

                    if not new_move:
                        pass
            else:
                self.add_to_board(block.shape)
                block.generate_new_block(self.width-1)
                if not self.is_valid_move_exist(block):
                    game_over = True
                    break

            self.add_to_board(block.shape)    
            self.draw_board()





game = Game(GAME_WIDTH,GAME_HEIGHT)
game.main_loop()

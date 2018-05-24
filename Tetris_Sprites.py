"""
    Date: June 7, 2011

    Description: The Tetris Sprites module contains all the sprites that will
    bee used to create the Tetris game. There are nine sprites here that 
    are used.
    
    **NOTE** Only unique things are commented. Any segments of code that have
    a similar structure to other code segments will not be commented.
"""

#Import and initialize
import pygame, random
pygame.init()
pygame.mixer.init()
        
class drawStuff(pygame.sprite.Sprite):
    """This class defines a sprite that will be used to draw the playing
    field for the Tetris game."""
    
    def __init__(self, background):
        """This initializer method accepts the game's surface as an parameter."""
               
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Draws the boundry lines for the Tetris playing field
        pygame.draw.line(background, (0, 60, 130), (0, 0), (0, 520), 17)
        pygame.draw.line(background, (0, 60, 130), (268, 0), (268, 520), 17)
        pygame.draw.rect(background, (0, 60, 130), ((0, 500), (270, 20)))
        
        #Draws the horizontal lines in the Tetris grid
        y_pos = 0
        for num in range(20):            
            pygame.draw.line(background, (0, 90, 130), (10, y_pos), (259, y_pos), 1)
            y_pos += 25
        
        #Draws the vertical lines in the Tetris grid
        x_pos = 35
        for num in range(9):
            pygame.draw.line(background, (0, 90, 130), (x_pos, 0), (x_pos, 498), 1)
            x_pos += 25

class Brick (pygame.sprite.Sprite):
    """This class creates the individual bricks that will build blocks in
    the Tetris game."""
    
    def __init__(self, top, left, colour):
        """This initializer method accepts rect positions and a block colour
        as parameters. It also initializes rect and image attributes for 
        the sprite."""
        
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Possible list of images that will be used
        self.__brick_colours = ["./Images/bluebrick.png","./Images/greenbrick.png",
                                "./Images/orangebrick.png", "./Images/purplebrick.png",
                                "./Images/redbrick.png","./Images/tealbrick.png",
                                "./Images/yellowbrick.png"]
        
        #Creates an image based on the colour passed in
        #Sets image attributes
        self.image = pygame.image.load(self.__brick_colours[colour])
        self.image = self.image.convert()
        
        #Sets rect attributes
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top   
        
class Blocks(pygame.sprite.Sprite):
    """This class creates the blocks in the Tetris game and manages their
    attributes (e.g. rotations)."""
    
    def __init__(self,grid,blocks,lose):
        """This initializer method accepts two lists (grid & blocks) and a 
        variable as parameters. It also creates some variables that will be
        used later on."""
        
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Creates variables that will be used later
        self.__grid = grid
        self.__blocks = blocks
        self.__lose = lose
        self.__length = len(self.__blocks)-1
        self.__stopDropping = False
        self.__rows_destroyed = 0
        self.__total_rows = 0
        
        
    def make_block(self):  
        """This method creates a block that will be seen in the Tetris game"""
        
        #Used to dermine the shape of the block
        self.__shapes = ["I", "J", "L", "O", "S", "T", "Z"]
        self.__shape = str(self.__shapes[random.randint(0,6)])
        
        #Starting position for the block
        block_row = 0
        block_col = 5
        
        #Creates the block based on the shape
        if self.__shape == "I":
            
            #Creates a special starting position (needed for some blocks)
            block_row = 1
            block_col = 3
            
            #Creates the block (actually coordinates that will be used to
            #show the blocks in the game)
            block = []
            for num in range (4):
                self.__grid[block_row][block_col] = 0
                block.append([block_row,block_col])
                block_col += 1            
            self.__blocks.append(block)
            
        elif self.__shape == "J":
            block_row = 1
            block_col = 6
            block = []
            for num in range(4):
                self.__grid[block_row][block_col] = 0
                block.append([block_row,block_col])
                if num == 2:
                    block_row -= 1
                    block_col += 1
                block_col -= 1            
            self.__blocks.append(block)
                
        elif self.__shape == "L":
            block_row = 1
            block_col = 3
            block = []
            for num in range(4):
                self.__grid[block_row][block_col] = 0
                block.append([block_row,block_col])
                if num == 2:
                    block_row -= 1
                    block_col -= 1 
                block_col += 1            
            self.__blocks.append(block)
            
        elif self.__shape == "O":
            block = []
            for num in range(4):
                self.__grid[block_row][block_col] = 0 
                block.append([block_row,block_col])
                if num == 1:
                    block_row -= 2
                    block_col += 1
                block_row += 1            
            self.__blocks.append(block)
            
        elif self.__shape == "Z":
            block = []
            block_col -= 1
            for num in range(4):
                self.__grid[block_row][block_col] = 0 
                block.append([block_row,block_col])
                if num == 1:
                    block_row += 1
                    block_col -= 1
                block_col += 1            
            self.__blocks.append(block)
            
        elif self.__shape == "T":
            block = []
            for num in range(4):
                self.__grid[block_row][block_col] = 0
                block.append([block_row,block_col])
                if num == 0:
                    block_row += 1
                    block_col -= 1
                if num > 0:
                    block_col += 1             
            self.__blocks.append(block)
         
        elif self.__shape == "S":
            block = []
            block_col += 1
            for num in range(4):
                self.__grid[block_row][block_col] = 0 
                block.append([block_row,block_col])
                if num == 1:
                    block_row += 1
                    block_col += 1
                block_col -= 1            
            self.__blocks.append(block)
            
    def drop_block(self):
        """This method will drop the current block"""
        
        #Will be used later to determine if the block will drop or not
        sorted_bricks = []
        will_drop = []
        
        #Creates a sorted version of the blocks list
        for num in range(len(self.__blocks[self.__length])):
            sorted_bricks.append(self.__blocks[self.__length][num])
        sorted_bricks.sort(reverse=True)
        
        #Checks to see if the block will drop
        for num2 in range(len(sorted_bricks)):
            for num in range(len(self.__blocks[self.__length])): 
                if self.__blocks[self.__length][num] == sorted_bricks[num2]:
                    row = self.__blocks[self.__length][num][0]
                    col = self.__blocks[self.__length][num][1]
                    if ((row < 21) and self.__grid[row][col] == 0) and ((self.__grid[row+1][col] == " ") or\
                                                  ([row+1,col] in self.__blocks[self.__length])):
                        will_drop.append([row,col])  
                        sorted_bricks[num2] = [99,99]
           
        #Drops the block if the drop if valid
        if len(will_drop) == 4:
            for num in range(len(will_drop)):
                row = will_drop[num][0]
                col = will_drop[num][1]
                self.__grid[row][col] = " "
                self.__grid[row+1][col] = 0 
            for num2 in range (len(self.__blocks[self.__length])):
                self.__blocks[self.__length][num2][0] += 1
            self.__drop = True
        else:
            self.__drop = False
                             
    def instant_drop(self):  
        """This method drops the current block until it can be dropped no further"""
        
        keepDropping = True
        
        while keepDropping:
            
            #Checks to see if the drop is valid
            sorted_bricks = []
            will_drop = []
            for num in range(len(self.__blocks[self.__length])):
                sorted_bricks.append(self.__blocks[self.__length][num])
            sorted_bricks.sort(reverse=True)
            
            for num2 in range(len(sorted_bricks)):
                for num in range(len(self.__blocks[self.__length])): 
                    if self.__blocks[self.__length][num] == sorted_bricks[num2]:
                        row = self.__blocks[self.__length][num][0]
                        col = self.__blocks[self.__length][num][1]
                        if ((row < 21) and self.__grid[row][col] == 0) and ((self.__grid[row+1][col] == " ") or\
                                                      ([row+1,col] in self.__blocks[self.__length])):
                            will_drop.append([row,col])  
                            sorted_bricks[num2] = [99,99]
             
            #Drops the block if the drop is valid  
            if len(will_drop) == 4:
                for num in range(len(will_drop)):
                    row = will_drop[num][0]
                    col = will_drop[num][1]
                    self.__grid[row][col] = " "
                    self.__grid[row+1][col] = 0 
                for num2 in range (len(self.__blocks[self.__length])):
                    self.__blocks[self.__length][num2][0] += 1
            else:
                keepDropping = False
                           
    def left(self):
        """This method moves the current block to the left."""
        
        #Used to check if the block will move
        sorted_bricks = []
        will_move = []
        
        #Creates a sorted verison of the blocks list
        for num in range(len(self.__blocks[self.__length])):
            sorted_bricks.append(self.__blocks[self.__length][num])
        sorted_bricks.sort(reverse=True)
        
        #Changes the position of the items in the list
        for _ in range(len(sorted_bricks)):
            for num in range(len(sorted_bricks)-1):
                    if sorted_bricks[num][1] > sorted_bricks[num+1][1]:
                            sorted_bricks.insert(num, sorted_bricks.pop(num+1))
        
        #Validates the move
        for num2 in range(len(sorted_bricks)):
            for num in range(len(self.__blocks[self.__length])): 
                if self.__blocks[self.__length][num] == sorted_bricks[num2]:
                    row = self.__blocks[self.__length][num][0]
                    col = self.__blocks[self.__length][num][1]
                    if ((col > 0) and self.__grid[row][col] == 0) and\
                       ((self.__grid[row][col-1] == " ") or ([row,col-1] in self.__blocks[self.__length])):
                        will_move.append([row,col])  
                        sorted_bricks[num2] = [99,99]
             
        #Moves the block to the left if the move is valid
        if len(will_move) == 4:
            for num in range(len(will_move)):
                row = will_move[num][0]
                col = will_move[num][1]
                self.__grid[row][col] = " "
                self.__grid[row][col-1] = 0 
            for num2 in range (len(self.__blocks[self.__length])):
                self.__blocks[self.__length][num2][1] -= 1
    
    def right(self):
        """This method moves the block to the right."""
        
        #***This method has the same structure as the previous one***
        #The only difference is that it makes the block move in the opposite direction
        
        sorted_bricks = []
        will_move = []
        
        for num in range(len(self.__blocks[self.__length])):
            sorted_bricks.append(self.__blocks[self.__length][num])
        sorted_bricks.sort(reverse=True)
        
        for _ in range(len(sorted_bricks)):
            for num in range(len(sorted_bricks)-1):
                    if sorted_bricks[num][1] < sorted_bricks[num+1][1]:
                            sorted_bricks.insert(num, sorted_bricks.pop(num+1))
                            
        for num2 in range(len(sorted_bricks)):
            for num in range(len(self.__blocks[self.__length])): 
                if self.__blocks[self.__length][num] == sorted_bricks[num2]:
                    row = self.__blocks[self.__length][num][0]
                    col = self.__blocks[self.__length][num][1]
                    if ((col < 9) and self.__grid[row][col] == 0) and\
                       ((self.__grid[row][col+1] == " ") or ([row,col+1] in self.__blocks[self.__length])):
                        will_move.append([row,col])  
                        sorted_bricks[num2] = [99,99]
                        
        if len(will_move) == 4:
            for num in range(len(will_move)):
                row = will_move[num][0]
                col = will_move[num][1]
                self.__grid[row][col] = " "
                self.__grid[row][col+1] = 0 
            for num2 in range (len(self.__blocks[self.__length])):
                self.__blocks[self.__length][num2][1] += 1
    
    def rotate(self,turn): 
        """This method rotates the block and accepts a direction as an parameter"""
        
        #Creates a clone of the block (will be used later)
        block_clone = []
        
        #Creates an instance of the parameter
        self.__turn = turn
        
        #Adds to the block clone
        for num in range(len(self.__blocks[self.__length])):
                block_clone.append([int(self.__blocks[self.__length][num][0]),int(self.__blocks[self.__length][num][1])])
    
        if self.__turn == "r":
            
            #Direction is used to make the block rotate left or right
            direction = 1
        else:
            direction = -1
            
        def rotate_I(self):
            """This sub method rotates the block if it is a specific shape."""
            
            #Variables used in making the rotation
            rotation = True        
            state = 0
            
            #Some blocks do not have only two positions so the direction
            #will be used to make it change state from one or the other
            direction = 1
            column = self.__blocks[self.__length][0][1]        
            
            #Checks to see the state of the block (which way it is rotated)
            for col in range(len(self.__blocks[self.__length])):
                if self.__blocks[self.__length][col][1] == column:
                    state += 0
                else:
                    state += 1
              
            #Changes direction based on state
            if state != 0:
                direction = -1
            
            #Rotates the block in the clone
            for num in range(len(block_clone)):
                if num == 0:
                    block_clone[num][0] += 1*direction
                    block_clone[num][1] -= 1*direction
                elif num == 2:
                    block_clone[num][0] -= 1*direction
                    block_clone[num][1] += 1*direction
                elif num == 3:
                    block_clone[num][0] -= 2*direction
                    block_clone[num][1] += 2*direction
             
            #Validation for the actual block rotation
            for num in range(len(block_clone)):
                if block_clone[num][0] > 21 or block_clone[num][1] < 0 or\
                   block_clone[num][1] > 9:
                    rotation = False
                
            #More validation
            for num in range(len(self.__blocks)-1):
                for num2 in range(len(self.__blocks[num])):
                    for num3 in range(len(block_clone)):
                        if num3 != 1:
                            if block_clone[num3] == self.__blocks[num][num2]:
                                rotation = False
            
            #Rotates the block if the rotation is valid
            if rotation:
                
                #Rotates the block based on state
                for num in range(len(self.__blocks[self.__length])):
                    if num == 0:
                        
                        #Updates the new position of the block in the grid
                        self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        
                        #Updates the coordinates of the block
                        self.__blocks[self.__length][num][0] += 1*direction
                        self.__blocks[self.__length][num][1] -= 1*direction
                    elif num == 2:
                        self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] -= 1*direction
                        self.__blocks[self.__length][num][1] += 1*direction
                    elif num == 3:
                        self.__grid[(self.__blocks[self.__length][num])[0]-2*direction][(self.__blocks[self.__length][num])[1]+2*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] -= 2*direction
                        self.__blocks[self.__length][num][1] += 2*direction
                
        #***NOTE*** The following sub methods are similar to the previous one
        #so they will not be commented
                        
        def rotate_J(self):
            rotation = True
            state = 0
            position = 0
            column = self.__blocks[self.__length][2][1]
            
            if turn == "r":
                rotate_range = range(len(self.__blocks[self.__length]))
            else:
                rotate_range = range(len(self.__blocks[self.__length]),-1,-1)
            
            for col in range(len(self.__blocks[self.__length])):
                if self.__blocks[self.__length][col][1] == column:
                    state += 0
                else:
                    state += 1
                    
            if (state == 1) and (self.__blocks[self.__length][3][1] == self.__blocks[self.__length][2][1] - 1):
                position = 1
            elif (state == 2) and (self.__blocks[self.__length][1][1] == self.__blocks[self.__length][2][1] + 1):
                position = 2
            elif (state == 1) and (self.__blocks[self.__length][3][1] == self.__blocks[self.__length][2][1] + 1):
                position = 3
            elif (state == 2) and (self.__blocks[self.__length][1][1] == self.__blocks[self.__length][2][1] - 1):
                position = 4
                
            for num in range(len(block_clone)):
                if position == 1:        
                    if num == 0:
                        block_clone[num][0] += 2
                        block_clone[num][1] += 2*direction
                    elif num == 1:
                        block_clone[num][0] += 1
                        block_clone[num][1] += 1*direction                
                    elif num == 3:
                        block_clone[num][0] -= 1*direction
                        block_clone[num][1] += 1
                        
                elif position == 2:
                    if num == 0:
                            block_clone[num][0] += 2*direction
                            block_clone[num][1] -= 2
                    elif num == 1:
                            block_clone[num][0] += 1*direction
                            block_clone[num][1] -= 1
                    elif num == 3:
                            block_clone[num][0] += 1
                            block_clone[num][1] += 1*direction
                            
                elif position == 3:
                    if num == 0:
                            block_clone[num][0] -= 2
                            block_clone[num][1] -= 2*direction
                    elif num == 1:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                    elif num == 3:
                            block_clone[num][0] += 1*direction
                            block_clone[num][1] -= 1
                            
                elif position == 4:
                    if num == 0:
                            block_clone[num][0] -= 2*direction
                            block_clone[num][1] += 2
                    elif num == 1:
                            block_clone[num][0] -= 1*direction
                            block_clone[num][1] += 1
                    elif num == 3:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                            
            for num in range(len(block_clone)):
                if block_clone[num][0] > 21 or block_clone[num][1] < 0 or\
                   block_clone[num][1] > 9:
                    rotation = False
                    
            for num in range(len(self.__blocks)-1):
                for num2 in range(len(self.__blocks[num])):
                    for num3 in range(len(block_clone)):
                        if num3 != 2:
                            if block_clone[num3] == self.__blocks[num][num2]:
                                rotation = False
            
            if rotation:
                for num in rotate_range:
                    if position == 1:        
                        if num == 0:
                            self.__grid[(self.__blocks[self.__length][num])[0]+2][(self.__blocks[self.__length][num])[1]+2*direction] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 2
                            self.__blocks[self.__length][num][1] += 2*direction
                        elif num == 1:
                            self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 1
                            self.__blocks[self.__length][num][1] += 1*direction                
                        elif num == 3:
                            self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] -= 1*direction
                            self.__blocks[self.__length][num][1] += 1
                            
                    elif position == 2:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]+2*direction][(self.__blocks[self.__length][num])[1]-2] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 2*direction
                                self.__blocks[self.__length][num][1] -= 2
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1*direction
                                self.__blocks[self.__length][num][1] -= 1
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1
                                self.__blocks[self.__length][num][1] += 1*direction
                                
                    elif position == 3:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]-2][(self.__blocks[self.__length][num])[1]-2*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 2
                                self.__blocks[self.__length][num][1] -= 2*direction
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1*direction
                                self.__blocks[self.__length][num][1] -= 1
                                
                    elif position == 4:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]-2*direction][(self.__blocks[self.__length][num])[1]+2] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 2*direction
                                self.__blocks[self.__length][num][1] += 2
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1*direction
                                self.__blocks[self.__length][num][1] += 1
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                
        def rotate_L(self):
            rotation = True
            state = 0
            position = 0
            column = self.__blocks[self.__length][2][1]
            
            if turn == "r":
                rotate_range = range(len(self.__blocks[self.__length]),-1,-1)
            else:
                rotate_range = range(len(self.__blocks[self.__length]))
            
            for col in range(len(self.__blocks[self.__length])):
                if self.__blocks[self.__length][col][1] == column:
                    state += 0
                else:
                    state += 1
                    
            if (state == 1) and (self.__blocks[self.__length][3][1] == self.__blocks[self.__length][2][1] + 1):
                position = 1
            elif (state == 2) and (self.__blocks[self.__length][1][1] == self.__blocks[self.__length][2][1] + 1):
                position = 2
            elif (state == 1) and (self.__blocks[self.__length][3][1] == self.__blocks[self.__length][2][1] - 1):
                position = 3
            elif (state == 2) and (self.__blocks[self.__length][1][1] == self.__blocks[self.__length][2][1] - 1):
                position = 4
                
            for num in range(len(block_clone)):
                if position == 1:        
                    if num == 0:
                        block_clone[num][0] += 2
                        block_clone[num][1] += 2*direction
                    elif num == 1:
                        block_clone[num][0] += 1
                        block_clone[num][1] += 1 *direction               
                    elif num == 3:
                        block_clone[num][0] += 1*direction
                        block_clone[num][1] -= 1
                        
                elif position == 2:
                    if num == 0:
                            block_clone[num][0] += 2*direction
                            block_clone[num][1] -= 2
                    elif num == 1:
                            block_clone[num][0] += 1*direction
                            block_clone[num][1] -= 1
                    elif num == 3:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                            
                elif position == 3:
                    if num == 0:
                            block_clone[num][0] -= 2
                            block_clone[num][1] -= 2*direction
                    elif num == 1:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                    elif num == 3:
                            block_clone[num][0] -= 1*direction
                            block_clone[num][1] += 1
                            
                elif position == 4:
                    if num == 0:
                            block_clone[num][0] -= 2*direction
                            block_clone[num][1] += 2
                    elif num == 1:
                            block_clone[num][0] -= 1*direction
                            block_clone[num][1] += 1
                    elif num == 3:
                            block_clone[num][0] += 1
                            block_clone[num][1] += 1*direction
                            
            for num in range(len(block_clone)):
                if block_clone[num][0] > 21 or block_clone[num][1] < 0 or\
                   block_clone[num][1] > 9:
                    rotation = False
                    
            for num in range(len(self.__blocks)-1):
                for num2 in range(len(self.__blocks[num])):
                    for num3 in range(len(block_clone)):
                        if num3 != 2:
                            if block_clone[num3] == self.__blocks[num][num2]:
                                rotation = False
            
            if rotation:
                for num in rotate_range:
                    if position == 1:        
                        if num == 0:
                            self.__grid[(self.__blocks[self.__length][num])[0]+2][(self.__blocks[self.__length][num])[1]+2*direction] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 2
                            self.__blocks[self.__length][num][1] += 2*direction
                        elif num == 1:
                            self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 1
                            self.__blocks[self.__length][num][1] += 1 *direction               
                        elif num == 3:
                            self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 1*direction
                            self.__blocks[self.__length][num][1] -= 1
                            
                    elif position == 2:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]+2*direction][(self.__blocks[self.__length][num])[1]-2] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 2*direction
                                self.__blocks[self.__length][num][1] -= 2
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1*direction
                                self.__blocks[self.__length][num][1] -= 1
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                                
                    elif position == 3:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]-2][(self.__blocks[self.__length][num])[1]-2*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 2
                                self.__blocks[self.__length][num][1] -= 2*direction
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1*direction
                                self.__blocks[self.__length][num][1] += 1
                                
                    elif position == 4:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]-2*direction][(self.__blocks[self.__length][num])[1]+2] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 2*direction
                                self.__blocks[self.__length][num][1] += 2
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1*direction
                                self.__blocks[self.__length][num][1] += 1
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1
                                self.__blocks[self.__length][num][1] += 1*direction                    
                                                    
        def rotate_S(self):
            rotation = True
            state = 0
            direction = 1
        
            if self.__blocks[self.__length][1][0] == self.__blocks[self.__length][2][0] - 1:
                state = 0
                num_range = range(len(self.__blocks[self.__length]))
            else:
                state = 1
                num_range = range(len(self.__blocks[self.__length]),-1,-1)
                    
            if state != 0:
                direction = -1
            
            for num in range(len(block_clone)):
                if num == 0:
                    block_clone[num][0] += 2*direction
                elif num == 1:
                    block_clone[num][0] += 1*direction
                    block_clone[num][1] += 1*direction
                elif num == 3:
                    block_clone[num][0] -= 1*direction
                    block_clone[num][1] += 1*direction
                    
            for num in range(len(block_clone)):
                if block_clone[num][0] > 21 or block_clone[num][1] < 0 or\
                   block_clone[num][1] > 9:
                    rotation = False
                    
            for num in range(len(self.__blocks)-1):
                for num2 in range(len(self.__blocks[num])):
                    for num3 in range(len(block_clone)):
                        if num3 != 2:
                            if block_clone[num3] == self.__blocks[num][num2]:
                                rotation = False
            
            if rotation:
                for num in num_range:
                    if num == 0:
                        self.__grid[(self.__blocks[self.__length][num])[0]+2*direction][(self.__blocks[self.__length][num])[1]] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] += 2*direction
                    elif num == 1:
                        self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] += 1*direction
                        self.__blocks[self.__length][num][1] += 1*direction
                    elif num == 3:
                        self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] -= 1*direction
                        self.__blocks[self.__length][num][1] += 1*direction
                    
        def rotate_Z(self):
            rotation = True
            state = 0
            direction = 1
        
            if self.__blocks[self.__length][1][0] == self.__blocks[self.__length][2][0] - 1:
                state = 0
                num_range = range(len(self.__blocks[self.__length]),-1,-1)        
            else:
                state = 1        
                num_range = range(len(self.__blocks[self.__length]))
                    
            if state != 0:
                direction = -1
            
            for num in range(len(block_clone)):
                if num == 0:
                    block_clone[num][1] += 2*direction
                elif num == 1:
                    block_clone[num][0] += 1*direction
                    block_clone[num][1] += 1*direction
                elif num == 3:
                    block_clone[num][0] += 1*direction
                    block_clone[num][1] -= 1*direction
                    
            for num in range(len(block_clone)):
                if block_clone[num][0] > 21 or block_clone[num][1] < 0 or\
                   block_clone[num][1] > 9:
                    rotation = False
                    
            for num in range(len(self.__blocks)-1):
                for num2 in range(len(self.__blocks[num])):
                    for num3 in range(len(block_clone)):
                        if num3 != 2:
                            if block_clone[num3] == self.__blocks[num][num2]:
                                rotation = False
                    
            if rotation:
                for num in num_range:
                    if num == 0:
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]+2*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][1] += 2*direction
                    elif num == 1:
                        self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] += 1*direction
                        self.__blocks[self.__length][num][1] += 1*direction
                    elif num == 3:
                        self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                        self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                        self.__blocks[self.__length][num][0] += 1*direction
                        self.__blocks[self.__length][num][1] -= 1*direction
                  
        def rotate_T(self):
            rotation = True
            position = 0
            column1 = self.__blocks[self.__length][0][1]
            column2 = self.__blocks[self.__length][2][1]
            row1 = self.__blocks[self.__length][0][0]
            row2 = self.__blocks[self.__length][2][0]
            brick_numbers = [3,0,1]
            
            if turn == "l":
                brick_numbers.reverse()
                        
            if (column1 == column2) and (row1 == row2 - 1):
                position = 1
            elif (column1 == column2 + 1) and (row1 == row2):
                position = 2
            elif (column1 == column2) and (row1 == row2 + 1):
                position = 3
            elif (column1 == column2 - 1) and (row1 == row2):
                position = 4
                
            for num in range(len(block_clone)):
                if position == 1:        
                    if num == 0:
                        block_clone[num][0] += 1
                        block_clone[num][1] += 1*direction
                    elif num == 1:
                        block_clone[num][0] -= 1*direction
                        block_clone[num][1] += 1                
                    elif num == 3:
                        block_clone[num][0] += 1*direction
                        block_clone[num][1] -= 1
                        
                elif position == 2:
                    if num == 0:
                            block_clone[num][0] += 1*direction
                            block_clone[num][1] -= 1
                    elif num == 1:
                            block_clone[num][0] += 1
                            block_clone[num][1] += 1*direction
                    elif num == 3:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                            
                elif position == 3:
                    if num == 0:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                    elif num == 1:
                            block_clone[num][0] += 1*direction
                            block_clone[num][1] -= 1
                    elif num == 3:
                            block_clone[num][0] -= 1*direction
                            block_clone[num][1] += 1
                            
                elif position == 4:
                    if num == 0:
                            block_clone[num][0] -= 1*direction
                            block_clone[num][1] += 1
                    elif num == 1:
                            block_clone[num][0] -= 1
                            block_clone[num][1] -= 1*direction
                    elif num == 3:
                            block_clone[num][0] += 1
                            block_clone[num][1] += 1*direction
                
            for num in range(len(block_clone)):
                if block_clone[num][0] > 21 or block_clone[num][1] < 0 or\
                   block_clone[num][1] > 9:
                    rotation = False
                    
            for num in range(len(self.__blocks)-1):
                for num2 in range(len(self.__blocks[num])):
                    for num3 in range(len(block_clone)):
                        if num3 != 2:
                            if block_clone[num3] == self.__blocks[num][num2]:
                                rotation = False
              
            if rotation:
                for number in range(3):
                    num = brick_numbers[number]
                    if position == 1:        
                        if num == 0:
                            self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 1
                            self.__blocks[self.__length][num][1] += 1*direction
                        elif num == 1:
                            self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] -= 1*direction
                            self.__blocks[self.__length][num][1] += 1                
                        elif num == 3:
                            self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                            self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                            self.__blocks[self.__length][num][0] += 1*direction
                            self.__blocks[self.__length][num][1] -= 1
                            
                    elif position == 2:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1*direction
                                self.__blocks[self.__length][num][1] -= 1
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1
                                self.__blocks[self.__length][num][1] += 1*direction
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                                
                    elif position == 3:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1*direction][(self.__blocks[self.__length][num])[1]-1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1*direction
                                self.__blocks[self.__length][num][1] -= 1
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1*direction
                                self.__blocks[self.__length][num][1] += 1
                                
                    elif position == 4:
                        if num == 0:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1*direction][(self.__blocks[self.__length][num])[1]+1] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1*direction
                                self.__blocks[self.__length][num][1] += 1
                        elif num == 1:
                                self.__grid[(self.__blocks[self.__length][num])[0]-1][(self.__blocks[self.__length][num])[1]-1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] -= 1
                                self.__blocks[self.__length][num][1] -= 1*direction
                        elif num == 3:
                                self.__grid[(self.__blocks[self.__length][num])[0]+1][(self.__blocks[self.__length][num])[1]+1*direction] = 0        
                                self.__grid[(self.__blocks[self.__length][num])[0]][(self.__blocks[self.__length][num])[1]] = " "
                                self.__blocks[self.__length][num][0] += 1
                                self.__blocks[self.__length][num][1] += 1*direction
          
        #Rotates the block based on shape
        if self.__shape == "I":
            rotate_I(self)
        elif self.__shape == "J":
            rotate_J(self)    
        elif self.__shape == "L":
            rotate_L(self) 
        elif self.__shape == "T":
            rotate_T(self) 
        elif self.__shape == "S":
            rotate_S(self) 
        elif self.__shape == "Z":
            rotate_Z(self)        
               
    def destroy_and_drop(self):
        """This method is used to verify if a row of blocks has been completed.
        If a row has been completed, the blocks are destroyed and those above
        it dropped."""
        
        #Used to verify if there are [more] blocks to be dropped
        verifying = True
        
        #Used to keep track of the number of rows destroyed
        counter = 0
        
        while verifying == True:   
            
            #Variables used to verify and destroy the rows
            verify = 0
            delete = []    
            block_copy = []
            
            #Checks to see which rows are filled
            for row in range(21,-1,-1):        
                for col in range(10):
                    for num in range(len(self.__blocks)):
                        for num2 in range(len(self.__blocks[num])):
                            if [row,col] == self.__blocks[num][num2]:
                                verify += 1
                if verify == 10:
                    delete.append(row)
                verify = 0
             
            if bool(delete):
                
                #Adds to number of rows destroyed
                counter += 1
                
                #Destroys the blocks in the row
                for col in range(10):
                    self.__grid[delete[0]][col] = " "
                    for num in range(len(self.__blocks)):
                        try:
                            self.__blocks[num].remove([delete[0],col])
                        except ValueError:
                            filler = None
                        
                for num in range(len(self.__blocks)):
                    for num2 in range(len(self.__blocks[num])):
                        if self.__blocks[num][num2][0] < delete[0]:
                            block_copy.append([self.__blocks[num][num2][0],self.__blocks[num][num2][1]])
                block_copy.sort(reverse=True)
                        
                #Drops the blocks above the destroyed row
                for num in range(len(block_copy)):
                    self.__grid[block_copy[num][0] + 1][block_copy[num][1]] = 0
                    self.__grid[block_copy[num][0]][block_copy[num][1]] = " "
                    for num2 in range(len(self.__blocks)):
                        for num3 in range(len(self.__blocks[num2])):
                            if self.__blocks[num2][num3] == block_copy[num]:
                                self.__blocks[num2][num3][0] += 1
                                
            else:
                #Exits the game loop if there are no more filled rows
                verifying = False
          
        #Variables used to keep track of score and rows destroyed
        self.__rows_destroyed = counter
        self.__total_rows += self.__rows_destroyed
                            
    def get_lost(self):
        """This method is used to determine if the user has lost the game"""
        
        #Defaults the loss to false
        self.__lose = False
        
        #Checks if the user lost the game
        for num in range(len(self.__blocks[self.__length])):
            if self.__blocks[self.__length][num][0] == 0:
                self.__lose = True     
         
        #Returns whether the user has lost or not
        return self.__lose
    
    def get_blocks(self):
        """This method returns the blocks list."""
        
        return self.__blocks
        
    def get_grid(self):
        """This method returns the grid list."""
        
        return self.__grid
    
    def get_drop(self):
        """This method returns whether the blocks have stopped dropping or not."""
        
        return self.__drop
    
    def get_rows_destroyed(self):
        """This method returns the current number of rows destroyed."""
        
        return self.__rows_destroyed
    
    def get_total_rows(self):
        """This method returns the total number of rows destroyed."""
        
        return self.__total_rows
                  
class Scorekeeper(pygame.sprite.Sprite):
    """This class defines the scorekeeper sprite for the breakout game."""
    
    def __init__(self, screen):
        """This initializer method accepts a screen surface as a parameter.
        It also initializes instance variables for score, the screen, and
        a font."""
        
        #Calls the parent __init__()
        pygame.sprite.Sprite.__init__(self) 
        
        #Creates instance variables
        self.__font = pygame.font.Font("./Fonts/Tetris.ttf", 30)
        self.__score = 0
        self.__screen = screen
    
    def scored(self, points):
        """This method accepts an integer for points as a parameter. This method
        is used to update the score."""
        
        #Adds scored points to the current score
        self.__score += points
        

    def get_score(self):
        """This method is used to return the users current score. This method
        will be used later."""
        
        return self.__score
        
    def update(self):
        """This method will be called automatically to display the current score
        on the screen."""
        
        #Creates the message that will be displayed
        self.__message = "Current Score: " + str(self.__score)
        
        #Sets the image attribute for the scorekeeper sprite
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        
        #Sets the rect attributes for the sprite
        self.rect = self.image.get_rect()
        self.rect.top = 25
        self.rect.left = self.__screen.get_width()/2 - 50
        
class Label(pygame.sprite.Sprite):
    """This class creates a stationary label used to display information."""
    
    def __init__(self, message, font, size, pos_x, pos_y):
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Creates a font based on the font passed as an parameter
        self.__font = pygame.font.Font(font, size)
        
        #Creates a message based on the message passed as an parameter
        self.__message = message
         
        #Sets the image attribute
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        
        #Sets the rect attributes
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        
    def get_rect(self):
        """This method retuns the Label sprite's rect attributes allowing it
        to be used as a "clickable" button."""
        
        return self.rect
    
class Message(pygame.sprite.Sprite):
    """This class defines the messages sprite for the breakout game."""
    
    def __init__(self, screen, rows, numbers):
        """This initializer method accepts a screen surface as a parameter."""
        
        #Calls the parent __init__()
        pygame.sprite.Sprite.__init__(self)
        
        #Instance variables that will be used later
        self.__numbers = []
        for num in range(len(numbers)):
            self.__numbers.append(int(numbers[num]))
        self.__numbers.reverse()
        self.__screen = screen
        self.__rows_destroyed = rows
        
        #Creates a font
        self.__font = pygame.font.Font("./Fonts/Tetris.ttf", 20)
        
        #Creates a message that determines when the game speed will increase
        for num in range(len(self.__numbers)):
            if self.__rows_destroyed < self.__numbers[num]:
                self.__message = "Speed Increases in " + str(self.__numbers[num] - self.__rows_destroyed) + " rows"
                
    def get_rows_destroyed(self, rows):
        """This method is used to update the number of rows destoryed."""
        
        self.__rows_destroyed = rows
            
    def update(self):
        """This method will be called automatically to display the 'speed'
        message on the screen."""
        
        #Creates a message that determines when the game speed will increase
        for num in range(len(self.__numbers)):
            if self.__rows_destroyed < self.__numbers[num]:
                self.__message = "Speed Increases in " + str(self.__numbers[num] - self.__rows_destroyed) + " rows"
                
        #Sets the image attribute for the messages sprite
        self.image = self.__font.render(self.__message, 1 , (255,255,255))
        
        #Sets the rect attributes for the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (self.__screen.get_width()/2 + 100,200)
        
class Pause(pygame.sprite.Sprite):
    """This class allows the game to be paused"""
    
    def __init__(self, screen):
        """This intializer method accepts the screen as an parameter. In addition,
        it creates instance variables and calls on the Label sprite."""
        
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Creates instace variables
        self.__screen = screen
        self.__pause = True
        
        #Creates a clock to determine when to update the screen so that events
        #can be detected
        self.__clock = pygame.time.Clock()
        
        #Creates special music for when the game is paused
        self.__music = pygame.mixer.Sound("./Music/pause.ogg")
        self.__music.set_volume(1)
        self.__channel = pygame.mixer.Channel(2)
        self.__channel.play(self.__music,loops=-1)
        
        #Defaults the music to being paused
        self.__channel.pause()
        
        #Creates a label sprite and its group to display a message telling the
        #player how to unpause the game
        label = Label("Press any key to unpause","./Fonts/Tetris.ttf",46,self.__screen.get_width()/2,self.__screen.get_height()/2)
        self.__labelSprite = pygame.sprite.Group(label)
        
    def pause(self):
        #Unpauses the music
        self.__channel.unpause()
        
        #Event handling
        while self.__pause:        
            self.__clock.tick(6)
            for event in pygame.event.get():
                
                #Checks to see if a key is pressed
                if event.type == pygame.KEYDOWN:
                    
                    #Pauses the music
                    self.__channel.pause()
                    
                    #Stops the pause loop
                    self.__pause = False     
            self.__labelSprite.draw(self.__screen)
            
            #Displays the label on the screen
            pygame.display.flip()
        self.__pause = True                   
     
#***NOTE*** The next two classes do not use proper encapsulation to improve
#code redability in addition to making the code easier to make

class Instructions(pygame.sprite.Sprite):
    """This class defines the instruction screen that is show when the 
    "Instructions" button on the menu is clicked."""
    
    def __init__(self):
        """This initializer creates a main gaming loop to display the instructions."""
        
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # I - Initialize
        screen = pygame.display.set_mode((670, 520),pygame.FULLSCREEN)
        
        # E - Entities
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        
        #Messages for lables that will be created
        message = open("instructions.txt", "r")
        messages = []
        
        line = message.readline().strip()
        
        while line != "":
            messages.append(line)
            line = message.readline().strip()           
            
        message.close() 
        
        labels = []
        
        #Creates label sprites to show instructions
        for num in range(19):
            if num == 0 or num == 1 or num == 7 or num == 8 or num == 17 or num == 18:
                label = Label(messages[num],"./Fonts/Tetris.ttf",30,screen.get_width()/2,num*25 +25)
            else:
                label = Label(messages[num],"./Fonts/Bits.ttf",10,screen.get_width()/2,num*25 + 21)
            labels.append(label)
          
        #Creates a sprite group used for updating later
        allSprites = pygame.sprite.Group(labels)
          
        
        #Assign = ALTER
        clock = pygame.time.Clock()
        keepGoing = True
        
        #Main gaming loop for the class
        while keepGoing:         
        
            clock.tick(30)
         
            # E - Event handling                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #Returns to the main menu
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:               
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False   
                elif event.type == pygame.MOUSEBUTTONDOWN:               
                    if labels[18].get_rect().collidepoint(pygame.mouse.get_pos()):
                        
                        #Allows the user to return to the main menu when they click
                        #the "Return" label
                        keepGoing = False
                
            # R - Refresh display       
            allSprites.clear(screen,background)   
            allSprites.update()
            allSprites.draw(screen) 
            pygame.display.flip()
          
        #Clears the screen so that no sprites will be shown after the sprite exits
        allSprites.clear(screen,background)
            
 
class Play(pygame.sprite.Sprite):
    """This class defines the actual Tetris game that will be played."""
    
    def __init__(self):
        """This initializer creates a main gaming loop to run the actual game."""
        
        pygame.sprite.Sprite.__init__(self)
        # I - Import and Initialize
        screen = pygame.display.set_mode((670, 520),pygame.FULLSCREEN)
         
        # E - Entities
        
        #Creates the grid for the blocks
        grid = []
        for row in range(22):
            grid.append([])
            for col in range(10):
                grid[row].append(" ")
        
        #Variables that will be used later
        total_rows = 0
        blocks = []
        colours = []
        lose = False
        
        #Variables used to increase game speed
        speed = 5
        increase = 5
        number = 0
        numbers = [] 
        for _ in range(10):
            number += increase
            numbers.append(number)
            increase += 5
        
        #Creates a block sprite
        block = Blocks(grid,blocks,lose)
                                                
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        
        #Creates special music for the game
        bgm = pygame.mixer.Sound("./Music/bgm.ogg")
        bgm.set_volume(1)
        channel = pygame.mixer.Channel(0)
        channel.play(bgm,loops=-1)
        
        #Creates the first block that will be displayed
        block.make_block()
        grid = block.get_grid()
        blocks = block.get_blocks()
        bricks = []
        colour_num = 0
        
        #Determines block colour
        colour = random.randint(0,6)        
        colours.append(colour)
        
        #Creates the block thaw will be DISPLAYED in the game
        for num in range(len(blocks)):
            for num2 in range(len(blocks[num])):               
                row_pos = (blocks[num][num2][0])*25 - 50
                col_pos = (blocks[num][num2][1])*25 + 10
                brick = Brick(row_pos,col_pos,colours[colour_num])
                bricks.append(brick)
                
            colour = random.randint(0,6)        
            colours.append(colour)
            colour_num +=1
        
        #Creates messages for label sprites that will be displayed to 
        #show how scoring works
        message = open("points.txt", "r")
        messages = []
        
        line = message.readline().strip()
        
        while line != "":
            messages.append(line)
            line = message.readline().strip()           
            
        message.close() 
        
        #Creates label sprites to show scoring
        labels = []
        
        for num in range(4):            
            label = Label(messages[num],"./Fonts/Tetris.ttf",20,screen.get_width()/2 + 100, num*25 + 400)
            labels.append(label)
         
        #Creates sprites
        speed_message = Message(screen,block.get_total_rows(),numbers)
        brickSprites = pygame.sprite.Group(bricks)
        draw_stuff = drawStuff(background)
        scorekeeper = Scorekeeper(screen)
        pause = Pause(screen)
        game_over = Label("GAME OVER","./Fonts/Tetris.ttf",50,screen.get_width()/2, screen.get_height()/2)
        
        #Creates sprite groups
        loseSprite = pygame.sprite.Group(game_over)
        allSprites = pygame.sprite.Group(brickSprites,scorekeeper, labels, speed_message)
        
        # A - Action (broken into ALTER steps)
         
            # A - Assign values to key variables
        clock = pygame.time.Clock()
        keepGoing = True        
            # L - Loop
        while keepGoing:                      
                                       
            # T - Timer to set frame rate
            clock.tick(speed)
         
            # E - Event handling               
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #Returns the user to the main menu
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        block.rotate("l")
                    elif event.key == pygame.K_x:
                        block.rotate("r")
                    elif event.key == pygame.K_LEFT:
                        block.left()
                    elif event.key == pygame.K_RIGHT:
                        block.right()
                    elif event.key == pygame.K_DOWN:               
                        block.drop_block()
                    elif event.key == pygame.K_SPACE:
                        block.instant_drop()                
                    elif event.key == pygame.K_p:
                        
                        #Pauses the current music so music will not overlap with
                        #pause game music
                        channel.pause()
                        
                        #Pauses the game
                        pause.pause()
                        
                        #Unpauses music after the game has resumed
                        channel.unpause()                
                    elif event.key == pygame.K_ESCAPE:
                        
                        #Returns to the main menu
                        keepGoing = False               
            
            #Regulates the speed at which blocks drop
            for num in range(100000):
                if num == 99999:
                    block.drop_block()     
                    drop = block.get_drop()
                
            if drop == False:   
                
                #Checks to see if rows are filled AFTER the current block has
                #finished dropping
                block.destroy_and_drop() 
                
                #Used to determine when to increase game speed (speed at which blocks drop)
                total_rows += block.get_rows_destroyed()
                
                #Increases game speed
                if total_rows == numbers[0]:
                    speed += 1
                    numbers.insert(len(numbers)-1, numbers.pop(0))
                    
                #Updates the current number for rows destroyed for the speed increase message
                speed_message.get_rows_destroyed(block.get_total_rows())
                
                #Updates the current points
                points = block.get_rows_destroyed()
                points *= points * 100
                scorekeeper.scored(points)
                lose = block.get_lost()                       
                                  
            if lose:
                
                #Returns to the main menu if the user lost the game
                keepGoing = False
                
            else:
                #Otherwise, a new block will be created
                if drop == False:
                    block.make_block()            
                 
                #Recreates the blocks on the screen
                bricks = []
                colour_num = 0
                for num in range(len(blocks)):
                    for num2 in range(len(blocks[num])):               
                        row_pos = (blocks[num][num2][0])*25 - 50
                        col_pos = (blocks[num][num2][1])*25 + 10
                        brick = Brick(row_pos,col_pos,colours[colour_num])
                        bricks.append(brick)
                    
                    colour = random.randint(0,6)        
                    colours.append(colour)
                    colour_num += 1
             
            #Recreates the sprite group of Brick classes
            brickSprites = pygame.sprite.Group(bricks)            
                        
            # R - Refresh display
            
            #Clears the screen
            screen.blit(background, (0, 0))
            allSprites.clear(screen,background)   
            
            #Recreates the sprite group used for updating
            allSprites = pygame.sprite.Group(brickSprites,scorekeeper, labels, speed_message)
            allSprites.update()
            allSprites.draw(screen) 
            pygame.display.flip()    
           
        #Displays a "Game Over" message when the user loses the game
        loseSprite.draw(screen)
        pygame.display.flip()
        
        #Fades out the music
        channel.fadeout(3000) 
        
        #Allows for the music to fade before returning to the main menu
        pygame.time.delay(3000)  
        
        #Used to clear the screen
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        allSprites.clear(screen,background)

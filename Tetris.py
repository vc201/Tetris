""" 
    Date: June 7, 2011

    Description: The Tetris game simulates the one created by Alexey Pajitnov.
    Everything is displayed in a single separate window (to the Python Shell) 
    in fullscreen mode and is made using sprites. This game is singleplayer.
    The game is fully controlled with the keyboard. On the other hand, the
    menu is controlled by the mouse. Features of this game include:
    a menu, gradually increasing game speed, score, an instruction screen,
    and music. The game will start when the user clicks "play" in the main menu
    and will return to the menu after the player has lost the game. The goal
    of this game is to make as many rows of blocks as you can before they reach
    the top of the screen.
    
    **NOTE** This main program is only the menu. It calls on the game which 
    is located in the "Tetris_Sprites" module. This is done for code efficiency
    and to make it a little easier to build the game.
"""

# I - Import and Initialize
import random, pygame, Tetris_Sprites
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((670, 520),pygame.FULLSCREEN)
 
def main():
    '''This function defines the 'mainline logic' for the breakout game.'''
    
    # E - Entities
    #Creates music that will be played and that can be resumed later
    music = pygame.mixer.Sound("./Music/title.ogg")
    music.set_volume(1)
    channel = pygame.mixer.Channel(1)
    channel.play(music,loops=-1)
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    #Creates a "title screen" image
    picture = pygame.image.load("./Images/tetris.jpg")
    picture = picture.convert()
    screen.blit(picture, (0, 0))
    pygame.display.flip()
    
    #Makes the mouse invisible while the "title screen" image is shown
    pygame.mouse.set_visible(False)
    pygame.time.delay(5000)
    
    #Removes the "title screen"
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    #Sets the mouse to visible after the "title screen" disappears
    pygame.mouse.set_visible(True)
    
    #Creates an image that will be used later
    loading = pygame.image.load("./Images/loading.jpg")
    
    #Creates the "buttons" for the menu
    messages = ["Play", "Instructions", "Quit"]
    label_1 = Tetris_Sprites.Label(messages[0],"./Fonts/Tetris.ttf",50,screen.get_width()/2,100)
    label_2 = Tetris_Sprites.Label(messages[1],"./Fonts/Tetris.ttf",50,screen.get_width()/2,250)
    label_3 = Tetris_Sprites.Label(messages[2],"./Fonts/Tetris.ttf",50,screen.get_width()/2,400)
    allSprites = pygame.sprite.Group(label_1, label_2, label_3)
    
    #Assign = ALTER
    clock = pygame.time.Clock()
    keepGoing = True
    
    #Main gaming loop for the program
    while keepGoing:         
    
        clock.tick(30)
     
        # E - Event handling        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:               
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False   
            #Used to detect if a "button" is being clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if label_3.get_rect().collidepoint(pygame.mouse.get_pos()):
                    #Stops the game loop if the "Quit" button is pressed
                    keepGoing = False
                elif label_2.get_rect().collidepoint(pygame.mouse.get_pos()):
                    #Creates and navigates to the instruction screen
                    instructions = Tetris_Sprites.Instructions()
                elif label_1.get_rect().collidepoint(pygame.mouse.get_pos()):
                    #Sets the mouse to invisible
                    pygame.mouse.set_visible(False)
                    
                    #Shows an image that says loading 
                    #NOTE: Does not actually wait for anything to know
                    #just notifies the user that there will be a delay before
                    #the game starts
                    screen.blit(loading, (0, 0))
                    pygame.display.flip()
                    
                    #Keeps the miage on the screen for five seconds
                    pygame.time.delay(5000)
                    
                    #Pauses the music
                    channel.pause()
                    
                    #Creates and navigates to the game
                    play = Tetris_Sprites.Play()
                    
                    #Unpauses the music after the game has finished
                    channel.unpause()
                    
                    #Sets the mouse to visible
                    pygame.mouse.set_visible(True)                
          
        # R - Refresh display
        allSprites.clear(screen,background)   
        allSprites.update()
        allSprites.draw(screen) 
        pygame.display.flip()
      
    #Quits pygame if the main gaming loop is exited
    pygame.quit()
    
#Calls the main function
main()

import pygame

class Screen:
    """
    Manages the screen
    """
    def __init__(self):
        #create the display and set it's size
        self.display = pygame.display.set_mode((1980,1080))
        #set the display's name
        pygame.display.set_caption("Pokemon")
        #creates a clock
        self.clock = pygame.time.Clock()
        #serts framerate to 120
        self.framerate = 120


    def update(self):
        #show display
        pygame.display.flip()
        #update display
        pygame.display.update()
        #refresh at the framerate speed
        self.clock.tick(self.framerate)
        #fill the screen with black every frame
        self.display.fill((0, 0, 0))


    def get_size(self):
        #return screen size
        return self.display.get_size()
    
    def get_display(self):
        #return display
        return self.display
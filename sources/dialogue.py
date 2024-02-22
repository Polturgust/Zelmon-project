import pygame.rect

import SQL_requests

class Dialogue():

    def __init__(self,dialogue,screen,map):
        self.textedonne=dialogue
        self.screen=screen
        self.map=map
        self.texte=[]
        while len(self.textedonne)>45:
            self.texte.append(self.textedonne[:45])
            self.textedonne=self.textedonne[45:]
        self.texte.append(self.textedonne)
        self.pressed={}
        print(len(self.texte),self.texte)
        self.cooldown=0

    def afficher(self):
        i=0
        while i<len(self.texte):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return None
                if event.type==pygame.KEYDOWN :
                    self.pressed[event.key]=True
                elif event.type==pygame.KEYUP:
                    self.pressed[event.key]=False

            if len(self.texte)-i>2:
                self.surface = pygame.Surface((self.screen.get_size()[0], 100))
                self.surface.fill((255, 255, 255))
                self.screen.update()
                self.map.update()
                self.screen.get_display().blit(self.surface, (0, self.screen.get_size()[1] - 150))
                self.screen.get_display().blit(
                    pygame.font.SysFont('Comic Sans MS', 20).render(self.texte[i], False, (0, 0, 0)),
                    (40, self.screen.get_display().get_size()[1] - 140))
                self.screen.get_display().blit(
                    pygame.font.SysFont('Comic Sans MS', 20).render(self.texte[i+1], False, (0, 0, 0)),
                    (40, self.screen.get_display().get_size()[1] - 90))

            else:
                self.surface=pygame.Surface((self.screen.get_size()[0],100))
                self.surface.fill((255,255,255))
                self.screen.update()
                self.map.update()
                self.screen.get_display().blit(self.surface,(0,self.screen.get_size()[1]-150))
                self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 20).render(self.texte[i], False, (0, 0, 0)),
                                           (40, self.screen.get_display().get_size()[1] - 120))
            if self.cooldown>0:
                self.cooldown-=1
            if self.pressed.get(pygame.K_RETURN)==True and self.cooldown<=0:
                i+=2
                self.cooldown=30

import pygame
import math
import random

class Player:
    def __init__(self, screen):
        self.pos = pygame.Vector2(screen.get_width()/6, screen.get_height()*3/5 + 20)
        self.dpos = pygame.Vector2(0, 0)
        self.hitbox_size = pygame.Vector2(32,32)
        self.hitbox = pygame.Rect(self.pos, self.hitbox_size)
        self.jumping = False

    def apply_gravity(self, gravity, floor_pos, delta):
        
        self.dpos.y += gravity*delta

        if self.pos.y > floor_pos:
            self.pos.y = floor_pos    
            self.dpos.y = 0
            self.jumping = False

    
    def eval(self, keys, delta):

        if keys[pygame.K_w]:
            if self.jumping == False:
                self.dpos.y = -80
                self.jumping = True
    
        self.pos = self.pos + (self.dpos * delta)
        new_pos = pygame.Vector2(self.pos.x, self.pos.y+keys[pygame.K_s]*self.hitbox_size.y/2)
        new_size = pygame.Vector2(self.hitbox_size.x, self.hitbox_size.y/(keys[pygame.K_s]+1))
        self.hitbox.update(new_pos, new_size) 

    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.hitbox)


class Obstacle:
    def __init__(self):
        self.speed = -32
        self.pos = pygame.Vector2(0,0)
        self.hitbox = pygame.Rect(0,0,0,0)
        self.hitbox_size = pygame.Vector2(0,0)
        self.delete_me = False
    
    def eval(self, delta):
        self.pos.x += self.speed * delta
        self.hitbox.update(self.pos, self.hitbox_size)
        if self.pos.x < -128:
            self.delete_me = True
    
    def draw(self, surface):
        pygame.draw.rect(surface, "red", self.hitbox)

if __name__ == '__main__':
    
    pygame.init()
    screen = pygame.display.set_mode((400,200))
    pygame.display.set_caption('the runner')
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    random.seed()

    thefont = pygame.font.Font('./IHateComicSans.ttf', size=32)
    background = pygame.image.load('./background.png')

    score = 0
    speed = 128
    max_speed = 320
    gravity = 128
    floor_pos = screen.get_height()*3/5 + 20

    player = Player(screen)
    obstacles = []

    while running:
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #eval
        keys = pygame.key.get_pressed()

        player.eval(keys, dt) 
        player.apply_gravity(gravity, floor_pos, dt)
       
        if len(obstacles) == 0:
           spawn_obstacle = True

        for obstacle in obstacles:
            if obstacle.pos.x < screen.get_width()/2:
                spawn_obstacle = True
            else:
                spawn_obstacle = False

        if spawn_obstacle == True:
            if random.randint(1,60) == 1:
                obstacle = Obstacle()
                obstacle.speed = -1*speed
                obstacle.pos.x = screen.get_width()+64
                if random.randint(1,2) == 1:
                    obstacle.hitbox_size = pygame.Vector2(32,16)
                    obstacle.pos.y = floor_pos+16
                else:
                    obstacle.pos.y = floor_pos-20
                    obstacle.hitbox_size = pygame.Vector2(32,32)
                obstacles.append(obstacle)

        for obstacle in obstacles:
            obstacle.speed = -1*speed
            obstacle.eval(dt)
            if obstacle.delete_me == True:
               obstacles.remove(obstacle)
            if obstacle.hitbox.colliderect(player.hitbox):
                running = False


        speed += .001*max_speed
        if speed > max_speed:
            speed = max_speed

        score += math.floor(speed/32)

        #draw
        screen.fill("white")
        
        screen.blit(background, pygame.Vector2(0,0))

        player.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        renderedfont = thefont.render("score: %s" % score, False, "black")

        screen.blit(renderedfont, pygame.Vector2(screen.get_width()/2-renderedfont.get_width()/2,0))

        pygame.display.flip()
        
        dt = clock.tick(60)/1000
    
    print("your score is: %s" % score)
    pygame.quit()

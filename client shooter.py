import pygame
from sys import exit
import random
import socket
import threading


PORT = 7070

FORMAT = "utf_8"

HEADER = 64



SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

client.connect((SERVER , PORT))

    
WIDTH , HEIGHT = 600 , 600

SPEED = 3

goingup = False
goingdown = False
goingright = False
goingleft = False

class Player:
    def __init__(self , x , y , radius ,color ):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.goingup = False
        self.goingdown = False
        self.goingright = False
        self.goingleft = False

    def player_move(self):
        count = 0
        for i in [self.goingup , self.goingdown , self.goingright , self.goingleft]:
            if i == True:
                count += 1

        if count == 2:
            if self.goingup and self.goingright:
                self.x += SPEED
                self.y -= SPEED
            if self.goingup and self.goingleft:
                self.x -= SPEED
                self.y -= SPEED
            if self.goingdown and self.goingright:
                self.x += SPEED
                self.y += SPEED
            if self.goingdown and self.goingleft:
                self.x -= SPEED
                self.y += SPEED
        if count == 1:
            if self.goingup:
                self.y -= (2*(SPEED**2))**0.5
            if self.goingdown:
                self.y += (2*(SPEED**2))**0.5
            if self.goingright:
                self.x += (2*(SPEED**2))**0.5
            if self.goingleft:
                self.x -= (2*(SPEED**2))**0.5

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x , self.y), self.radius)
        
player_2 = Player(400 , 400 , 10 , "red")

def res():
    while True:
        msg = client.recv(2048).decode(FORMAT)
        if msg != " ":
            m = msg.split(",")
            player_2.x = int(m[0][:3])
            player_2.y = int(m[1][:3])


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send((send_length))
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))


        
        
thread = threading.Thread(target=res)
thread.start()  



pygame.init()
screen = pygame.display.set_mode( (WIDTH , HEIGHT) )
shade_screen = pygame.Surface( (WIDTH , HEIGHT) , pygame.SRCALPHA )
shade_screen.fill((0 , 0 , 0, 75))
shade_rect = shade_screen.get_rect(topleft = (0 , 0))
pygame.display.set_caption("online shooter")
clock = pygame.time.Clock()

player = Player(300 , 300 , 10 , "white")

while True:
    p = f"{player.x},{player.y}"
    send(p)
    screen.blit(shade_screen , shade_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.goingup = True
            if event.key == pygame.K_s :
                player.goingdown = True
            if event.key == pygame.K_d :
                player.goingright = True
            if event.key == pygame.K_a :
                player.goingleft = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit() 
        if event.type  == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.goingup = False
            if event.key == pygame.K_s:
                player.goingdown = False
            if event.key == pygame.K_d:
                player.goingright = False
            if event.key == pygame.K_a:
                player.goingleft = False        
                
    player.player_move()
    player.draw()
    player_2.player_move()
    player_2.draw()
    pygame.display.update()
    clock.tick(60)
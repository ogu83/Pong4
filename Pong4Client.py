import socket
import json
import pygame
import GameState as gs

global global_game_state 
global_game_state = gs.GameState()

### Colors
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)

#Colors of players
py1_Color = RED
py2_Color = GREEN
py3_Color = BLUE       
py4_Color = YELLOW

### Variables
wt = 10 #thread update wait time  

'''
The Player That Client has to Command
Player1 = RED PLayer
Player2 = GREEN PLayer
Player3 = BLUE Player
Player4 = YELLOW Player
'''
Player = "Player2"

def client(ip, port, message, onInit=True, screen=None, font=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:        
        sock.sendall(bytes(message.encode('ascii')))
        response = sock.recv(4096)
        if (message == "GameState"):
            game_state_str = response.decode('ascii')
            game_state = gs.GameState.from_json(game_state_str)
            if onInit:
                onInitGameState(game_state)
                onInit = False   
            else:
                updateGlobalGameState(game_state,screen,font)

    finally:
        sock.close()

### Functions
def drawpaddle(screen,x, y, w, h, color=WHITE):
    pygame.draw.rect(screen, color, (x, y, w, h))

def drawball(screen, x, y, bw):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), int(bw))

def drawscore(screen, font, H, FourPlayers):    
    screen.blit(font.render("Score", False, WHITE), (30,30))
    
    screen.blit(font.render(f"{global_game_state.p1score}",False,py1_Color),(H/5,30))
    screen.blit(font.render(f"{global_game_state.p2score}",False,py2_Color),(2*H/5,30))
    
    if FourPlayers:
        screen.blit(font.render(f"{global_game_state.p3score}",False,py3_Color),(3*H/5,30))
        screen.blit(font.render(f"{global_game_state.p4score}",False,py4_Color),(4*H/5,30))

def updateGlobalGameState(game_state, screen, font):
    global_game_state = game_state

    screen.fill(BLACK)

    drawscore(screen, font, global_game_state.H, global_game_state.FourPlayers)
    drawball(screen, global_game_state.bx, global_game_state.by, global_game_state.bw)

    drawpaddle(screen,global_game_state.p1x, global_game_state.p1y, global_game_state.paddle_width_v, global_game_state.paddle_height_v, py1_Color) 
    drawpaddle(screen,global_game_state.p2x, global_game_state.p2y, global_game_state.paddle_width_v, global_game_state.paddle_height_v, py2_Color)

    if global_game_state.FourPlayers:
        drawpaddle(screen,global_game_state.p3x, global_game_state.p3y, global_game_state.paddle_width_h, global_game_state.paddle_height_h, py3_Color)
        drawpaddle(screen,global_game_state.p4x, global_game_state.p4y, global_game_state.paddle_width_h, global_game_state.paddle_height_h, py4_Color)

    pygame.display.flip()  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_LEFT:
                str = f"{Player}:LEFT_DOWN"
                print(str)
                client(ip, port, str)
            if event.key == pygame.K_RIGHT:
                str = f"{Player}:RIGHT_DOWN"
                print(str)
                client(ip, port, str)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                str = f"{Player}:LEFT_UP"
                print(str)
                client(ip, port, str)
            if event.key == pygame.K_RIGHT:
                str = f"{Player}:RIGHT_UP"
                print(str)
                client(ip, port, str)

    pygame.time.wait(wt)
    client(ip, port,  "GameState", False, screen, font)

def onInitGameState(game_state):
    global_game_state = game_state

    ### PY GAME FONT
    pygame.font.init()
    comic = pygame.font.SysFont('Comic Sans MS', 15)

    ### Initialize
    screen = pygame.display.set_mode((global_game_state.W, global_game_state.H))

    playerCount = 2
    if global_game_state.FourPlayers:
        playerCount = 4   
    pygame.display.set_caption(f'Pong Client for {playerCount} Players')

    screen.fill(BLACK)
    pygame.display.flip()

    ip, port = socket.gethostname(), 9009
    client(ip, port,  "GameState", False, screen, comic)

ip, port = socket.gethostname(), 9009
client(ip, port,  "GameState")
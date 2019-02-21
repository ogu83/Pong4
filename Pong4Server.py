import socket
import threading
import socketserver as SocketServer
import pygame
import json
import GameState as gs

if __name__ == "__main__":    
    game_state = gs.GameState() 
       
    class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            data = str(self.request.recv(4096), 'ascii')        
            cur_thread = threading.current_thread()                
            print("Recieved:", "{}: {}".format(cur_thread.name, data))

            if (data == "GameState"):
                game_state_str = game_state.toJSON().encode('ascii')
                self.request.sendall(game_state_str)
            else:
                player_name = data.split(':')[0]
                key = data.split(':')[1]
                if player_name == "Player1":  #RED PLAYER                 
                    if key == "LEFT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w))
                    elif key == "LEFT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_w))
                    elif key == "RIGHT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
                    elif key == "RIGHT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_s))
                elif player_name == "Player2": #GREEN PLAYER
                    if key == "LEFT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
                    elif key == "LEFT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
                    elif key == "RIGHT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
                    elif key == "RIGHT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))
                elif player_name == "Player3": #BLUE PLAYER                   
                    if key == "LEFT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
                    elif key == "LEFT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_a))
                    elif key == "RIGHT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
                    elif key == "RIGHT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_d))
                elif player_name == "Player4": #YELLOW PLAYER                   
                    if key == "LEFT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
                    elif key == "LEFT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
                    elif key == "RIGHT_DOWN":
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
                    elif key == "RIGHT_UP":
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))

    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

    HOST, PORT = socket.gethostname(), 9009
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # start a thread with the server. 
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)

    # exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Pong 4 server loop running in thread:", server_thread.name)  
    
    ####GAME####

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

    ### Constants
    game_state.W = 600 # Width of the game table
    game_state.H = game_state.W # Height of the game table Game should be a square always to be fair for 4 player game

    game_state.FourPlayers = True ## 2 Players or 4 Players mode    

    ### PY GAME FONT
    pygame.font.init()
    comic = pygame.font.SysFont('Comic Sans MS', 15)

    ### Variables
    wt = 10 #thread update wait time 

    #Player Coordinates
    game_state.p1x = game_state.W/30
    game_state.p1y = game_state.H/2 - ((game_state.W/60)**2)/2

    game_state.p2x = game_state.W-(game_state.W/30)
    game_state.p2y = game_state.H/2 - ((game_state.W/60)**2)/2

    if game_state.FourPlayers:
        game_state.p3x = game_state.W/2 - ((game_state.H/60)**2)/2
        game_state.p3y = game_state.H/30

        game_state.p4x = game_state.W/2 - ((game_state.H/60)**2)/2
        game_state.p4y = game_state.H-(game_state.H/30)

    game_state.ball_thrower = 0 #No player is ball thrower in the first run, to get score the corresponding player should throw the ball, it is a little bit different in my game original one because of 4 play rules.

    #Player Scores
    game_state.p1score = 0
    game_state.p2score = 0
    if game_state.FourPlayers:
        game_state.p3score = 0
        game_state.p4score = 0 

    # W-S Key Params
    w_p = False
    s_p = False
    wsr = False
    # Up-Down Key Params
    up_p = False
    down_p = False
    udr = False
    if game_state.FourPlayers:
        # A-D Key Params
        a_p = False
        d_p = False
        adr = False
        # Left-Right Key Params
        left_p = False
        right_p = False
        lrr = False

    ##Screen Margins for Paddles
    game_state.dmH = game_state.H/40
    game_state.dmW = game_state.W/40

    #Vertical Players Paddle Size (Players which stands right and left)
    game_state.paddle_width_v = game_state.W/60
    game_state.paddle_height_v = game_state.paddle_width_v**2

    #Horizontal Players Paddle Size (Players which stands up and down)
    game_state.paddle_height_h = game_state.H/60
    game_state.paddle_width_h = game_state.paddle_height_h**2

    ## Ball Geometry
    game_state.bx = game_state.W/2 #Ball X Position
    game_state.by = game_state.H/2 #Ball Y Position
    game_state.bw = game_state.W/65 #Ball diameter

    ## Ball Velocity 
    game_state.velocity_raito = 240 #Initial velocity ratio (bigger makes the game slower, smaller makes the game faster)
    game_state.bxv = -game_state.H/game_state.velocity_raito # Ball X Velocity
    game_state.byv = 0 #Ball Y Velocity

### Functions
def drawpaddle(x, y, w, h, color=WHITE):
    pygame.draw.rect(screen, color, (x, y, w, h))

def drawball(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), int(game_state.bw))

''' 
Updates Player Locations
''' 
def uploc():
    global p1y
    global p2y
    
    if game_state.FourPlayers:
        global p3x
        global p4x    

    p1y = game_state.p1y
    p2y = game_state.p2y

    if game_state.FourPlayers:
        p3x = game_state.p3x
        p4x = game_state.p4x

    if w_p:
        if p1y-(game_state.dmH) < 0:
            py1 = 0
        else:
            p1y -= game_state.dmH
    elif s_p:
        if p1y+(game_state.dmH)+game_state.paddle_height_v > game_state.H:
            p1y = game_state.H-game_state.paddle_height_v
        else:
            p1y += game_state.dmH

    if up_p:
        if p2y-(game_state.dmH) < 0:
            p2y = 0
        else:
            p2y -= game_state.dmH
    elif down_p:
        if p2y+(game_state.dmH)+game_state.paddle_height_v > game_state.H:
            p2y = game_state.H-game_state.paddle_height_v
        else:
            p2y += game_state.dmH

    if game_state.FourPlayers:
        if a_p:
            if p3x-(game_state.dmW)<0:
                p3x = 0
            else:
                p3x -= game_state.dmW
        elif d_p:
            if p3x+(game_state.dmW)+game_state.paddle_width_h>game_state.W:
                p3x = game_state.W-game_state.paddle_width_h
            else:
                p3x += game_state.dmW

        if left_p:
            if p4x-(game_state.dmW)<0:
                p4x = 0
            else:
                p4x -=game_state.dmW
        elif right_p:
            if p4x+(game_state.dmW)+game_state.paddle_width_h>game_state.W:
                p4x = game_state.W-game_state.paddle_width_h
            else:
                p4x += game_state.dmW

    game_state.p1y= p1y                
    game_state.p2y= p2y

    if game_state.FourPlayers:
       game_state.p3x= p3x
       game_state.p4x= p4x
''' 
Updates Ball And Game Scores
''' 
def upblnv():

    global ball_thrower
    ball_thrower = game_state.ball_thrower

    global bx
    global bxv
    global by
    global byv    
    bx = game_state.bx
    bxv = game_state.bxv
    by = game_state.by
    byv = game_state.byv

    if game_state.FourPlayers:
        global p3score
        global p4score        
        p3score = game_state.p3score
        p4score = game_state.p4score

    global p1score
    global p2score
    p1score = game_state.p1score
    p2score = game_state.p2score
        
    '''
    Updates score according to the last ball thrower
    '''
    if game_state.FourPlayers:
        def update_score(p1score, p2score,p3score,p4score,ball_thrower): 
            if ball_thrower == 1:
                p1score += 1
            elif ball_thrower == 2:
                p2score += 1
            elif ball_thrower == 3:
                p3score += 1
            elif ball_thrower == 4:
                p4score += 1

            ball_thrower = 0 #Set Ball thrower 0 to be fair, when the corresponding player throws then begin to score it.

            return p1score,p2score,p3score,p4score,ball_thrower
    else:
        def update_score(p1score, p2score,ball_thrower): 
            if ball_thrower == 1:
                p1score += 1
            elif ball_thrower == 2:
                p2score += 1            

            ball_thrower = 0 #Set Ball thrower 0 to be fair, when the corresponding player throws then begin to score it.

            return p1score,p2score,ball_thrower
    
    if (bx+bxv < game_state.p1x+game_state.paddle_width_v) and ((game_state.p1y < game_state.by+game_state.byv+game_state.bw) and (game_state.by+game_state.byv-game_state.bw < game_state.p1y+game_state.paddle_height_v)):
        bxv = -bxv
        byv = ((game_state.p1y+(game_state.p1y+game_state.paddle_height_v))/2)-by
        byv = -byv/((5*game_state.bw)/7)
        ball_thrower = 1
    elif bx+bxv < 0:
        if game_state.FourPlayers:
            p1score,p2score,p3score,p4score,ball_thrower = update_score(p1score,p2score,p3score,p4score,ball_thrower)
        else:
            p1score,p2score,ball_thrower = update_score(p1score,p2score,ball_thrower)

        bx = game_state.W/2
        bxv = game_state.H/game_state.velocity_raito
        by = game_state.H/2
        byv = 0

    if (bx+bxv > game_state.p2x) and ((game_state.p2y < by+byv+game_state.bw) and (by+byv-game_state.bw < game_state.p2y+game_state.paddle_height_v)):
        bxv = -bxv
        byv = ((game_state.p2y+(game_state.p2y+game_state.paddle_height_v))/2)-by
        byv = -byv/((5*game_state.bw)/7)
        ball_thrower = 2
    elif bx+bxv > game_state.W:
        if game_state.FourPlayers:
            p1score,p2score,p3score,p4score,ball_thrower = update_score(p1score,p2score,p3score,p4score,ball_thrower)
        else:
            p1score,p2score,ball_thrower = update_score(p1score,p2score,ball_thrower)
        bx = game_state.W/2
        bxv = -game_state.H/game_state.velocity_raito
        by = game_state.H/2
        byv = 0

    
    if game_state.FourPlayers:##4 Player Mode        
        if (by+byv < game_state.p3y+game_state.paddle_height_h) and ((game_state.p3x < bx+bxv+game_state.bw) and (bx+bxv-game_state.bw < p3x+game_state.paddle_width_h)):
            byv = -byv
            bxv = ((p3x+(p3x+game_state.paddle_width_h))/2)-bx
            bxv = -bxv/((5*game_state.bw)/7)
            ball_thrower = 3
        elif by+byv < 0:
            p1score,p2score,p3score,p4score,ball_thrower = update_score(p1score,p2score,p3score,p4score,ball_thrower)
            by = game_state.H/2
            byv = game_state.W/game_state.velocity_raito
            bx = game_state.W/2
            bxv = 0

        if (by+byv > game_state.p4y) and ((game_state.p4x < bx+bxv+game_state.bw) and (bx+bxv-game_state.bw < p4x+game_state.paddle_width_h)):
            byv = -byv
            bxv = ((game_state.p4x+(game_state.p4x+game_state.paddle_width_h))/2)-bx
            bxv = -bxv/((5*game_state.bw)/7)
            ball_thrower = 4
        elif by+byv > game_state.H:
            p1score,p2score,p3score,p4score,ball_thrower = update_score(p1score,p2score,p3score,p4score,ball_thrower)
            by = game_state.H/2
            byv = -game_state.W/game_state.velocity_raito
            bx = game_state.W/2
            bxv = 0
    else:##2 Player Mode    
        if by+byv > game_state.H or by+byv < 0:
            byv = -byv
        
    bx += bxv
    by += byv

    game_state.bx = bx
    game_state.by = by
    game_state.bxv = bxv
    game_state.byv = byv
    game_state.ball_thrower = ball_thrower
    game_state.p1score = p1score
    game_state.p2score = p2score
    game_state.p3score = p3score
    game_state.p4score = p4score

def drawscore():    
    screen.blit(comic.render("Score", False, WHITE), (30,30))
    
    screen.blit(comic.render(f"{p1score}",False,py1_Color),(game_state.H/5,30))
    screen.blit(comic.render(f"{p2score}",False,py2_Color),(2*game_state.H/5,30))
    
    if game_state.FourPlayers:
        screen.blit(comic.render(f"{p3score}",False,py3_Color),(3*game_state.H/5,30))
        screen.blit(comic.render(f"{p4score}",False,py4_Color),(4*game_state.H/5,30))

### Initialize
screen = pygame.display.set_mode((game_state.W, game_state.H))

playerCount = 2
if game_state.FourPlayers:
    playerCount = 4   
pygame.display.set_caption(f'Pong Server for {playerCount} Players')

screen.fill(BLACK)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                w_p = True
                if s_p == True:
                    s_p = False
                    wsr = True
            if event.key == pygame.K_s:
                s_p = True
                if w_p == True:
                    w_p = False
                    wsr = True
            if event.key == pygame.K_UP:
                up_p = True
                if down_p == True:
                    down_p = False
                    udr = True
            if event.key == pygame.K_DOWN:
                down_p = True
                if up_p == True:
                    up_p = False
                    udr = True

            if game_state.FourPlayers:
                if event.key == pygame.K_a:
                    a_p = True
                    if d_p == True:
                        a_p = False
                        adr = True
                if event.key == pygame.K_d:
                    d_p = True
                    if a_p == True:
                        d_p = False
                        adr = True
                if event.key == pygame.K_LEFT:
                    left_p = True
                    if right_p == True:
                        left_p = False
                        lrr = True
                if event.key == pygame.K_RIGHT:
                    right_p = True
                    if left_p == True:
                        right_p = False
                        lrr = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_p = False
                if wsr == True:
                    s_p = True
                    wsr = False
            if event.key == pygame.K_s:
                s_p = False
                if wsr == True:
                    w_p = True
                    wsr = False
            if event.key == pygame.K_UP:
                up_p = False
                if udr == True:
                    down_p = True
                    udr = False
            if event.key == pygame.K_DOWN:
                down_p = False
                if udr == True:
                    up_p = True
                    udr = False

            if game_state.FourPlayers:
                if event.key == pygame.K_a:
                    a_p = False
                    if adr == True:
                        d_p = True
                        adr = False
                if event.key == pygame.K_d:
                    d_p = False
                    if adr == True:
                        a_p = True
                        adr = False
                if event.key == pygame.K_LEFT:
                    left_p = False
                    if lrr == True:
                        right_p = True
                        lrr = False
                if event.key == pygame.K_RIGHT:
                    right_p = False
                    if lrr == True:
                        left_p = True
                        lrr = False

    screen.fill(BLACK)
    uploc()
    upblnv()
    drawscore()
    drawball(game_state.bx, game_state.by)

    drawpaddle(game_state.p1x, game_state.p1y, game_state.paddle_width_v, game_state.paddle_height_v, py1_Color) 
    drawpaddle(game_state.p2x, game_state.p2y, game_state.paddle_width_v, game_state.paddle_height_v, py2_Color)

    if game_state.FourPlayers:
        drawpaddle(game_state.p3x, game_state.p3y, game_state.paddle_width_h, game_state.paddle_height_h, py3_Color)
        drawpaddle(game_state.p4x, game_state.p4y, game_state.paddle_width_h, game_state.paddle_height_h, py4_Color)

    pygame.display.flip()
    pygame.time.wait(wt)
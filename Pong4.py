import pygame

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
W = 600 # Width of the game table
H = W # Height of the game table Game should be a square always to be fair for 4 player game

### PY GAME FONT
pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 15)

### Variables
wt = 10 #thread update wait time 
mplay = False

#Player Coordinates
p1x = W/30
p1y = H/2 - ((W/60)**2)/2

p2x = W-(W/30)
p2y = H/2 - ((W/60)**2)/2

p3x = W/2 - ((H/60)**2)/2
p3y = H/30

p4x = W/2 - ((H/60)**2)/2
p4y = H-(H/30)

#Player Scores
p1score = 0
p2score = 0
p3score = 0
p4score = 0 

# W-S Key Params
w_p = False
s_p = False
wsr = False
# Up-Down Key Params
up_p = False
down_p = False
udr = False
# A-D Key Params
a_p = False
d_p = False
adr = False
# Left-Right Key Params
left_p = False
right_p = False
lrr = False

##Screen Margins for Paddles
dmH = H/40
dmW = W/40

#Vertical Players Paddle Size (Players which stands right and left)
paddle_width_v = W/60
paddle_height_v = paddle_width_v**2

#Horizontal Players Paddle Size (Players which stands up and down)
paddle_height_h = H/60
paddle_width_h = paddle_height_h**2

## Ball Geometry
bx = W/2 #Ball X Position
by = H/2 #Ball Y Position
bw = W/65 #Ball diameter

## Ball Velocity 
velocity_raito = 240 #Initial velocity ratio (bigger makes the game slower, smaller makes the game faster)
bxv = -H/velocity_raito # Ball X Velocity
byv = 0 #Ball Y Velocity

### Functions
def drawpaddle(x, y, w, h, color=WHITE):
    pygame.draw.rect(screen, color, (x, y, w, h))

def drawball(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), int(bw))

''' 
Updates Player Locations
''' 
def uploc():
    global p1y
    global p2y
    
    global p3x
    global p4x


    if w_p:
        if p1y-(dmH) < 0:
            py1 = 0
        else:
            p1y -= dmH
    elif s_p:
        if p1y+(dmH)+paddle_height_v > H:
            p1y = H-paddle_height_v
        else:
            p1y += dmH

    if up_p:
        if p2y-(dmH) < 0:
            p2y = 0
        else:
            p2y -= dmH
    elif down_p:
        if p2y+(dmH)+paddle_height_v > H:
            p2y = H-paddle_height_v
        else:
            p2y += dmH


    if a_p:
        if p3x-(dmW)<0:
            p3x = 0
        else:
            p3x -=dmW
    elif d_p:
        if p3x+(dmW)+paddle_width_h>W:
            p3x = W-paddle_width_h
        else:
            p3x += dmW

    if left_p:
        if p4x-(dmW)<0:
            p4x = 0
        else:
            p4x -=dmW
    elif right_p:
        if p4x+(dmW)+paddle_width_h>W:
            p4x = W-paddle_width_h
        else:
            p4x += dmW

 
''' 
Updates Ball And Game Scores
''' 
def upblnv():

    global bx
    global bxv
    global by
    global byv

    global p4score
    global p3score
    global p2score
    global p1score
    
    if (bx+bxv < p1x+paddle_width_v) and ((p1y < by+byv+bw) and (by+byv-bw < p1y+paddle_height_v)):
        bxv = -bxv
        byv = ((p1y+(p1y+paddle_height_v))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv < 0:
        p2score += 1
        bx = W/2
        bxv = H/velocity_raito
        by = H/2
        byv = 0

    if (bx+bxv > p2x) and ((p2y < by+byv+bw) and (by+byv-bw < p2y+paddle_height_v)):
        bxv = -bxv
        byv = ((p2y+(p2y+paddle_height_v))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv > W:
        p1score += 1
        bx = W/2
        bxv = -H/velocity_raito
        by = H/2
        byv = 0

    ##2 Player Mode
    #if by+byv > H or by+byv < 0:
    #    byv = -byv

    ##4 Player Mode
    if (by+byv < p3y+paddle_height_h) and ((p3x < bx+bxv+bw) and (bx+bxv-bw < p3x+paddle_width_h)):
        byv = -byv
        bxv = ((p3x+(p3x+paddle_width_h))/2)-bx
        bxv = -bxv/((5*bw)/7)
    elif by+byv < 0:
        p4score += 1
        by = H/2
        byv = W/velocity_raito
        bx = W/2
        bxv = 0

    if (by+byv > p4y) and ((p4x < bx+bxv+bw) and (bx+bxv-bw < p4x+paddle_width_h)):
        byv = -byv
        bxv = ((p4x+(p4x+paddle_width_h))/2)-bx
        bxv = -bxv/((5*bw)/7)
    elif by+byv > H:
        p3score += 1
        by = H/2
        byv = -W/velocity_raito
        bx = W/2
        bxv = 0
        
    bx += bxv
    by += byv

def drawscore():    
    screen.blit(comic.render("Score", False, WHITE), (30,30))
    screen.blit(comic.render(f"{p1score}",False,py1_Color),(H/5,30))
    screen.blit(comic.render(f"{p2score}",False,py2_Color),(2*H/5,30))
    screen.blit(comic.render(f"{p3score}",False,py3_Color),(3*H/5,30))
    screen.blit(comic.render(f"{p4score}",False,py4_Color),(4*H/5,30))

### Initialize
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Pong for 4 Players')
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
    drawball(bx, by)

    drawpaddle(p1x, p1y, paddle_width_v, paddle_height_v, py1_Color) 
    drawpaddle(p2x, p2y, paddle_width_v, paddle_height_v, py2_Color)
    drawpaddle(p3x, p3y, paddle_width_h, paddle_height_h, py3_Color)
    drawpaddle(p4x, p4y, paddle_width_h, paddle_height_h, py4_Color)

    pygame.display.flip()
    pygame.time.wait(wt)

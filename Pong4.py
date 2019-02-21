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
H = W # Height of the game table Game should be a square always to be fair

pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 30)

### Variables
wt = 10 #thread update wait time 
mplay = False

#Player Coordinates
p1x = W/30
p1y = H/2 - ((W/60)**2)/2

p2x = W-(W/30)
p2y = H/2 - ((W/60)**2)/2

p3x = H/30
p3y = W/2 - ((H/60)**2)/2

p4x = H-(H/30)
p4y = W/2 - ((H/60)**2)/2

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
u_p = False
d_p = False
udr = False
# A-D Key Params
a_p = False
d_p = False
adr = False
# Left-Right Key Params
l_p = False
r_p = False
lrr = False

dm = H/40

#Vertical Players Paddle Size (Players which stands right and left)
paddle_width_v = W/60
paddle_height_v = paddle_width_v**2

#Horizontal Players Paddle Size (Players which stands up and down)
paddle_height_h = H/60
paddle_widht_h = paddle_height_h**2

bsd = 1

bx = W/2 #Ball X Position
by = H/2 #Ball Y Position
bw = W/65 #Ball diameter

velocity_raito = 120 #Initial velocity ratio
bxv = -H/velocity_raito # Ball X Velocity
byv = 0 #Ball Y Velocity

### Functions
def drawpaddle(x, y, w, h, color=WHITE):
    pygame.draw.rect(screen, color, (x, y, w, h))

def drawball(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), int(bw))

def uploc():
    global p1y
    global p2y
    if w_p:
        if p1y-(dm) < 0:
            py1 = 0
        else:
            p1y -= dm
    elif s_p:
        if p1y+(dm)+paddle_height_v > H:
            p1y = H-paddle_height_v
        else:
            p1y += dm
    if u_p:
        if p2y-(dm) < 0:
            p2y = 0
        else:
            p2y -= dm
    elif d_p:
        if p2y+(dm)+paddle_height_v > H:
            p2y = H-paddle_height_v
        else:
            p2y += dm

def upblnv():
    global bx
    global bxv
    global by
    global byv
    global p4score
    global p3score
    global p2score
    global p1score

    #2 Player Mode
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
    if by+byv > H or by+byv < 0:
        byv = -byv

    bx += bxv
    by += byv

def drawscore():
    scoreStr = f"Score"
    score = comic.render(scoreStr, False, WHITE)
    screen.blit(score, (30,30))
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
                u_p = True
                if d_p == True:
                    d_p = False
                    udr = True
            if event.key == pygame.K_DOWN:
                d_p = True
                if u_p == True:
                    u_p = False
                    udr = True
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
                u_p = False
                if udr == True:
                    d_p = True
                    udr = False
            if event.key == pygame.K_DOWN:
                d_p = False
                if udr == True:
                    u_p = True
                    udr = False

    screen.fill(BLACK)
    uploc()
    upblnv()
    drawscore()
    drawball(bx, by)

    drawpaddle(p1x, p1y, paddle_width_v, paddle_height_v, py1_Color) 
    drawpaddle(p2x, p2y, paddle_width_v, paddle_height_v, py2_Color)

    pygame.display.flip()
    pygame.time.wait(wt)

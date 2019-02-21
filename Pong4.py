import pygame

### Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

### Constants
W = 600
H = 600
pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 30)

### Variables
wt = 10
mplay = False

p1x = W/30
p1y = H/2 - ((W/60)**2)/2

p2x = W-(W/30)
p2y = H/2 - ((W/60)**2)/2

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

paddle_width = W/60
paddle_height = paddle_width**2

bsd = 1

bx = W/2
by = H/2
bw = W/65
bxv = H/60
bxv = -bxv
byv = 0

### Functions
def drawpaddle(x, y, w, h):
    pygame.draw.rect(screen, WHITE, (x, y, w, h))

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
        if p1y+(dm)+paddle_height > H:
            p1y = H-paddle_height
        else:
            p1y += dm
    if u_p:
        if p2y-(dm) < 0:
            p2y = 0
        else:
            p2y -= dm
    elif d_p:
        if p2y+(dm)+paddle_height > H:
            p2y = H-paddle_height
        else:
            p2y += dm

def upblnv():
    global bx
    global bxv
    global by
    global byv
    global p2score
    global p1score

    if (bx+bxv < p1x+paddle_width) and ((p1y < by+byv+bw) and (by+byv-bw < p1y+paddle_height)):
        bxv = -bxv
        byv = ((p1y+(p1y+paddle_height))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv < 0:
        p2score += 1
        bx = W/2
        bxv = H/60
        by = H/2
        byv = 0
    if (bx+bxv > p2x) and ((p2y < by+byv+bw) and (by+byv-bw < p2y+paddle_height)):
        bxv = -bxv
        byv = ((p2y+(p2y+paddle_height))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv > W:
        p1score += 1
        bx = W/2
        bxv = -H/60
        by = H/2
        byv = 0
    if by+byv > H or by+byv < 0:
        byv = -byv

    bx += bxv
    by += byv

def drawscore():
    score = comic.render(str(p1score) + " - " + str(p2score), False, WHITE)
    screen.blit(score, (W/2,30))

### Initialize
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake ML v.1.0.0')
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
    drawpaddle(p1x, p1y, paddle_width, paddle_height)
    drawpaddle(p2x, p2y, paddle_width, paddle_height)
    pygame.display.flip()
    pygame.time.wait(wt)

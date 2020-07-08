import pygame, random, math

pink = (255,182,193)
black = (0, 0, 0)
white = (255, 255, 255)
light_blue = (152,245,255)
light_green = (0,201,87)
light_yellow = (255,236,139)
red = (255, 0, 0)


class Ball(pygame.sprite.Sprite):
    dx = 0
    dy = 0
    x = 0
    y = 0
    direction = 0
    speed = 0

    def __init__(self, sp, srx, sry, radium, color):
        pygame.sprite.Sprite.__init__(self)
        self.speed = sp
        self.x = srx
        self.y = sry
        self.image = pygame.Surface([radium*2, radium*2])
        self.image.fill(black)
        pygame.draw.circle(self.image, color, (radium, radium), radium, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (srx, sry)
        self.direction = random.randint(20,70)

    def update(self):
            radian = math.radians(self.direction)
            self.dx = self.speed * math.cos(radian)
            self.dy = -self.speed * math.sin(radian)
            self.x += self.dx
            self.y += self.dy
            self.rect.x = self.x
            self.rect.y = self.y
            if self.rect.left <= 0 or self.rect.right >= screen.get_width()-10:
                self.bouncelr()
            elif self.rect.top <= 10:
                self.rect.top = 10
                self.bouncetop()
            if self.rect.bottom >= screen.get_height()-10:
                return True
            else:
                return False

    def bouncetop(self):
        self.direction = 360 - self.direction

    def bouncelr(self):
        self.direction = (180 - self.direction) % 360


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([38, 13])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Pad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([65, 13])
        self.image.fill(pink)
        self.rect = self.image.get_rect()
        self.rect.x = int((screen.get_width()-self.rect.width)/2)
        self.rect.y = int(screen.get_height() - self.rect.height - 20)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]-30
        if self.rect.x > screen.get_width()-self.rect.width:
            self.rect.x = screen.get_width() - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0


def gameover(message):
    global running
    text = font_end.render(message, 1, red)
    screen.blit(text, (screen.get_width()/2-60, screen.get_height()/2-20))
    pygame.display.update()
    running = False


pygame.init()
score = 0
font = pygame.font.SysFont("Arial", 20)
font_end = pygame.font.SysFont("Arial", 32)
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Brick Breaker Challenge")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
allsprite = pygame.sprite.Group()
bricks = pygame.sprite.Group()
ball = Ball(9, 300, 350, 9, white)
allsprite.add(ball)
pad = Pad()
allsprite.add(pad)
clock = pygame.time.Clock()
for row in range(0,4):
    for column in range(0,15):
        if row == 0 or row == 1 :
            brick = Brick(light_blue, column*40+1, row*15+1)
        if row == 2 or row == 3 :
            brick = Brick(light_green, column*40+1, row*15+1)
        bricks.add(brick)
        allsprite.add(bricks)
msgstr = "Left click to start!"
playing = False
running = True
exit_program = False

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        playing = True
    if playing:
        screen.blit(background, (0,0))
        fail = ball.update()
        if fail:
            gameover("Failed...")
        pad.update()
        hitbrick = pygame.sprite.spritecollide(ball, bricks, True)
        if len(hitbrick) > 0:
            score+=len(hitbrick)
            ball.rect.y += 20
            ball.bouncetop()
            if len(bricks)==0:
                gameover("Congratulations!")
        hitpad = pygame.sprite.collide_rect(ball, pad)
        if hitpad:
            ball.bouncetop()
        allsprite.draw(screen)
        msgstr = "Points: "+str(score)
    msg = font.render(msgstr, 1, light_yellow)
    screen.blit(msg, (screen.get_width()/2-60, screen.get_height()-20))
    pygame.display.update()

while not exit_program:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True


pygame.quit()







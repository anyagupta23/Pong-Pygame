import pygame, sys
FPS = 45
FPSCLOCK = pygame.time.Clock()
pygame.init()
screen_size = width, height = 500, 400
screen = pygame.display.set_mode(screen_size)
gamename = "Pong"
b_font = pygame.font.Font('freesansbold.ttf', 100)
s_font = pygame.font.Font('freesansbold.ttf', 18)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
GREEN = (0, 225, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)

class Ball:
    def __init__(self, canvas, paddle, computer_paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.computer_paddle = computer_paddle
        self.color = color
        start = [150, 200]
        r = 8
        self.radius=8
        self.id = pygame.draw.circle(self.canvas, self.color, start, self.radius, 0)
        rect = (start [0] - r, start[1] - r, start[0] + r, start[1] + r)
        self.xspeed = 3
        self.yspeed = 3
        self.x = self.xspeed
        self.y = self.yspeed
        self.hit_bottom_or_top = False
        self.width = 100
        self.height=10
        rect = (start[0], start[1], self.width, self.height)
        self.id = pygame.draw.rect(self.canvas, self.color, rect, 0)

    def hit_paddle(self):
        b, p = self.id, self.paddle.id
        if b.right >= p.left and b.left <= p.right:
            if b.bottom >= p.top and b.bottom<=p.bottom:
                return True
        return False

    def draw(self):
        width, height = self.canvas.get_size()
        if self.id.bottom >= height or self.id.top <=0:
            self.hit_bottom_or_top = True
        if self.hit_paddle():
            self.y = -self.yspeed
            self.x = self.edge_hit(self.id, self.paddle)
        if self.hit_computer_paddle():
            self.y = self.yspeed
            self.x = self.xspeed
        if self.id.left <= 0 or self.id.right >= width:
            self.x = -(self.x)
        pos = [self.id.centerx + self.x, self.id.centery + self.y]
        self.id = pygame.draw.circle(self.canvas, self.color, pos, self.radius, 0)

    def edge_hit(self, pos, paddle):
        b_x = pos.centerx
        p_x = paddle.id.centerx
        direction = 0
        speed = abs(self.x)
        if (speed !=0):
            direction = self.x/speed
        distance = 25
        if b_x < p_x - distance:
            direction = -1
            speed+=1
        if b_x > p_x + distance:
            direction = 1
            speed+=1
        return int (direction * speed)

    def hit_computer_paddle(self):
        b, p = self.id, self.computer_paddle.id
        if b.right >= p.left and b.left <= p.right:
            if b.top >= p.top and b.top <= p.bottom:
                return True
        return False

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        start = [200, 300]
        self.width = 100
        self.height = 10
        rect = (start[0], start[1], start[0] + self.width, self.height)
        self.id = pygame.draw.rect(self.canvas, self.color, rect, 0)
        self.x = 0
        self.speed = 3
       
    def draw(self, direction):
        p, width = self.id, self.canvas.get_width()
        if direction == 'left' and p.left>=self.speed:
            self.x = -self.speed
        elif direction == 'right' and p.right<=width - self.speed:
            self.x = self.speed
        else:
            self.x = 0
        rect = [p.left + self.x, p.top, self.width, self.height]
        self.id=pygame.draw.rect(self.canvas, self.color, rect, 0)

    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed

class Computer_Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        start = [200, 50]
        self.width = 100
        self.height = 10
        rect = (start[0], start[1], start[0] + self.width, self.height)
        self.id = pygame.draw.rect(self.canvas, self.color, rect, 0)
        self.x = 0
        self.speed = 3

    def draw(self, ball):
        p, b, width = self.id, ball.id, self.canvas.get_width()
        if p.centerx<b.centerx and p.right<= width - self.speed:
            self.x=self.speed
        elif p.centerx>b.centerx and p.left>=self.speed:
            self.x = -self.speed
        else:
            self.x = 0
        rect = [p.left + self.x, p.top, self.width, self.height]
        self.id = pygame.draw.rect(self.canvas, self.color, rect, 0)
            
def main():
    pygame.display.set_caption(gamename)
    showStartScreen()
    while True:
        runGame()
        showGameOver()

def runGame():
    paddle = Paddle(screen, GREEN)
    computer_paddle = Computer_Paddle(screen, BLUE)
    ball = Ball(screen, paddle, computer_paddle, RED)
    direction = ' '
    while ball.hit_bottom_or_top == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                elif event.key == pygame.K_ESCAPE:
                    terminate()
        screen.fill(BLACK)
        ball.draw()
        paddle.draw(direction)
        computer_paddle.draw(ball)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

def showPressKey():
    text = s_font.render('Press a key to play.', True, GREEN)
    rect = text.get_rect()
    rect.center = (width/2, height - 50)
    screen.blit(text, rect)

def checkForKeyPress():
    if len(pygame.event.get(pygame.QUIT))>0:
        terminate()
    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def keypress(event):
    global keyPressed
    keyPressed = True

def showStartScreen():
    text = b_font.render(gamename, True, WHITE, DARKGREEN)
    degrees = 0
    while True:
        screen.fill(BLACK)
        rText = pygame.transform.rotate(text, degrees)
        rect = rText.get_rect()
        rect.center = (width/2, height/2)
        screen.blit(rText, rect)
        showPressKey()
        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees += 3

def showGameOver():
    gameText = b_font.render('Game', True, WHITE)
    overText = b_font.render('Over', True, WHITE)
    gameRect = gameText.get_rect()
    overRect = overText.get_rect()
    gameRect.midtop = (width/2, height/2 - 100)
    overRect.midtop = (width/2, height/2)
    screen.blit(gameText, gameRect)
    screen.blit(overText, overRect)
    showPressKey()
    pygame.display.update()
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def terminate():
    pygame.quit()
    sys.exit()

if __name__== '__main__':
    main()

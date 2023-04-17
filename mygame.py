import pygame as pg
import os
import math

pg.init()
screen = pg.display.set_mode()

clock = pg.time.Clock()
split = os.path.split(os.path.abspath(__file__))[0]
maindir = os.path.join(split, "mygamedata")


def load_image(name, sc, colorkey=None):
    imagepath = os.path.join(maindir, name)
    image = pg.image.load(imagepath)
    image = pg.transform.scale(image, sc)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


class Pscore(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.p = "score" + str(ball.count) + ".png"
        self.image, self.rect = load_image(self.p, (200, 200), -1)

    def update(self):
        self.p = "score" + str(ball.count) + ".png"
        self.image, self.rect = load_image(self.p, (200, 200), -1)


class Bscore(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.p = "score" + str(ball.count2) + ".png"
        self.image, self.rect = load_image(self.p, (200, 200), -1)
        self.rect.right = (screen.get_width() - 50)
        self.rect.top = (screen.get_height() - 50)

    def update(self):
        self.p = "score" + str(ball.count2) + ".png"
        self.image, self.rect = load_image(self.p, (200, 200), -1)
        self.rect.right = (screen.get_width() - 50)
        self.rect.top = (screen.get_height() - 860)


class Ball(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("ball.png",(50,50), -1)
        self.rect.y = 1
        self.rect.x = 1000
        self.original = self.rect
        self.image = self.image.convert()
        self.xspeed = -20
        self.yspeed = -15
        self.count = 0
        self.count2 = 0

    def update(self):
        if (self.rect.top < screen.get_rect().top
                or self.rect.bottom > screen.get_rect().bottom):
            self.yspeed = -self.yspeed
        if self.rect.colliderect(paddle.rect) or self.rect.colliderect(
                paddle2.rect):
            self.xspeed = -self.xspeed
        if self.rect.left < screen.get_rect().left:
            self.rect = self.original
            self.count2 = self.count2 + 1
        if self.rect.right > screen.get_rect().right:
            self.rect = self.original
            self.count = self.count + 1
        newpos = self.rect.move((self.xspeed, self.yspeed))
        self.rect = newpos


class Paddle(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("paddle.png",(20,200))
        self.image = self.image.convert()
        self.speed = 20
        self.up = False
        self.down = False

    def moveup(self):
        self.up = True

    def movedown(self):
        self.down = True

    def uplifted(self):
        self.up = False

    def downlifted(self):
        self.down = False

    def update(self):
        newpos = None
        if self.down == True:
            newpos = self.rect.move((0, self.speed))
            self.rect = newpos
            if self.rect.bottom > screen.get_rect().bottom:
                self.rect.bottom = screen.get_rect().bottom
        elif self.up == True:
            newpos = self.rect.move((0, -self.speed))
            self.rect = newpos
            if self.rect.top < screen.get_rect().top:
                self.rect.top = screen.get_rect().top


class Paddle2(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("paddle.png",(20, 200))
        self.image = self.image.convert()
        self.rect.right = screen.get_rect().right
        self.rect.midright = screen.get_rect().midright
        self.ballup = False
        self.balldown = False
        self.speed = 20

    def update(self):
        if self.ballup == True:
            newpos = self.rect.move((0, -self.speed))
            self.rect = newpos
        if self.balldown == True:
            newpos = self.rect.move((0, self.speed))
            self.rect = newpos


paddle = Paddle()
ball = Ball()
paddle2 = Paddle2()
pscore = Pscore()
bscore = Bscore()
screen.fill("green")
sprites = pg.sprite.RenderPlain((paddle, pscore, paddle2, bscore, ball))

while True:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN and event.key == pg.K_s:
            paddle.down = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_w:
            paddle.up = True
        elif event.type == pg.KEYUP and event.key == pg.K_w:
            paddle.uplifted()
        elif event.type == pg.KEYUP and event.key == pg.K_s:
            paddle.downlifted()
    if abs(ball.rect.right - paddle2.rect.left) <= 1000:
        if (ball.rect.bottom < paddle2.rect.top):
            paddle2.ballup = True
            paddle2.balldown = False
        elif (ball.rect.top > paddle2.rect.top):
            paddle2.balldown = True
            paddle2.ballup = False
    else:
        paddle2.balldown = False
        paddle2.ballup = False
    sprites.update()
    screen.fill("green")
    sprites.draw(screen)
    pg.display.flip()
    if (ball.count == 5 or ball.count2 == 5):
        overdir = os.path.join(maindir, "gameover.png")
        windir = os.path.join(maindir, "youwin.png")
        if (ball.count2 == 5):
            over = pg.image.load(overdir)
        elif (ball.count == 5):
            over = pg.image.load(windir)
        over = pg.transform.scale(over, (screen.get_size()))
        over = over.convert()
        while True:
            screen.blit(over, (0, 0))
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.flip()

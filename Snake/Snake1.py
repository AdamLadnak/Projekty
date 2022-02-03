from pyglet import app
from pyglet import image
from pyglet.window import Window
from pyglet import clock
from pyglet.window import key

window = Window(750, 750)

velkost_bunky = 25

snake_x = window.width // velkost_bunky // 2 * velkost_bunky
snake_y = window.height // velkost_bunky // 2 * velkost_bunky

snake_dx, snake_dy = 0, 0
@window.event
def on_draw():
    window.clear()
    nakresli_stvorec(snake_x, snake_y, velkost_bunky, colour = (0,255,0,0))

def nakresli_stvorec(x, y, size, colour = (255,255,255,0)):
    img = image.create(size,size,image.SolidColorImagePattern(colour))
    img.blit(x, y)

@window.event
def on_key_press(symbol, modifiers):
    global snake_dx, snake_dy
    if symbol == key.LEFT:
        snake_dx = -velkost_bunky
        snake_dy = 0
    elif symbol == key.RIGHT:
        snake_dx = velkost_bunky
        snake_dy = 0
    elif symbol == key.UP:
        snake_dx = 0
        snake_dy = velkost_bunky
    elif symbol == key.DOWN:
        snake_dx = 0
        snake_dy = -velkost_bunky
def obnovenie(dt):
    global snake_x, snake_y
    snake_x += snake_dx
    snake_y += snake_dy

clock.schedule_interval(obnovenie, 1/10)

app.run()
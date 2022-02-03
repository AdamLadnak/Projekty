from pyglet import app
from pyglet import image
from pyglet.window import Window

window = Window(750, 750)

velkost_bunky = 25

snake_x = window.width // velkost_bunky // 2 * velkost_bunky
snake_y = window.height // velkost_bunky // 2 * velkost_bunky

@window.event
def on_draw():
    window.clear()
    nakresli_stvorec(snake_x, snake_y, velkost_bunky, colour = (0,255,0,0))

def nakresli_stvorec(x, y, size, colour = (255,255,255,0)):
    img = image.create(size,size,image.SolidColorImagePattern(colour))
    img.blit(x, y)


app.run()
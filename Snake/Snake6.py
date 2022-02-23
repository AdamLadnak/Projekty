from pyglet import app
from pyglet import image
from pyglet.window import Window
from pyglet import clock
from pyglet.window import key
from random import randint
from pyglet import text
from pyglet import graphics
from pyglet import resource
from pyglet import media

window = Window(750, 750)

velkost_bunky = 25
chvost = []
snake_x = window.width // velkost_bunky // 2 * velkost_bunky
snake_y = window.height // velkost_bunky // 2 * velkost_bunky

eat = resource.media('sound/eating_sound.wav', streaming=False)
naburanie = resource.media('sound/Bonk_sound_effect.wav')
hudba_na_pozadi = resource.media('sound/background_music.mp3')
drink = resource.media('sound/drinking_sound.mp3', streaming=False)

snake_dx, snake_dy = 0, 0
jedlo_x, jedlo_y = 0, 0
jedlo1_x, jedlo1_y = 0, 0

koniec_hry = False

@window.event
def on_draw():
    window.clear()

    nakresli_stvorec(jedlo_x, jedlo_y, velkost_bunky, colour = (255,0,0,0))
    nakresli_stvorec(jedlo1_x, jedlo1_y, velkost_bunky, colour=(0, 0, 255, 0))

    for suradnice in chvost:
        nakresli_stvorec(suradnice[0], suradnice[1], velkost_bunky, colour = (50,200,50,50))
    nakresli_stvorec(snake_x, snake_y, velkost_bunky, colour=(0, 255, 0, 0))
    if koniec_hry:
        napis_game_over()

def nova_hra():
    global snake_x, snake_y, snake_dx, snake_dy, koniec_hry, chvost

    snake_x = window.width // velkost_bunky // 2 * velkost_bunky
    snake_y = window.height // velkost_bunky // 2 * velkost_bunky
    snake_dx, snake_dy = 0, 0
    chvost = []

    nakresli_jedlo()
    nakresli_jedlo1()

    koniec_hry = False
    player.play()

def nakresli_stvorec(x, y, size, colour = (255,255,255,0)):
    img = image.create(size,size,image.SolidColorImagePattern(colour))
    img.blit(x, y)

def nakresli_jedlo():
    global jedlo_x, jedlo_y
    jedlo_x = randint(0, (window.width // velkost_bunky) - 1) * velkost_bunky
    jedlo_y = randint(0, (window.height // velkost_bunky) - 1) * velkost_bunky

def nakresli_jedlo1():
    global jedlo1_x, jedlo1_y
    jedlo1_x = randint(0, (window.width // velkost_bunky) - 1) * velkost_bunky
    jedlo1_y = randint(0, (window.height // velkost_bunky) - 1) * velkost_bunky

def napis_game_over():
    game_over = text.Label(f'GAME OVER\n Skóre: {len(chvost)}\n (Klikni space pre reštart)', font_size=36,
                           x=window.width//2, y=window.height//2, width=window.width, align='center',
                           anchor_x='center', anchor_y='center', multiline=True)
    game_over.draw()

@window.event
def on_key_press(symbol, modifiers):
    global snake_dx, snake_dy, koniec_hry
    if not koniec_hry:
        if symbol == key.LEFT:
            if snake_dx == 0:
                snake_dx = -velkost_bunky
                snake_dy = 0
        elif symbol == key.RIGHT:
            if snake_dx == 0:
                snake_dx = velkost_bunky
                snake_dy = 0
        elif symbol == key.UP:
            if snake_dy == 0:
                snake_dy = velkost_bunky
                snake_dx = 0
        elif symbol == key.DOWN:
            if snake_dy == 0:
                snake_dy = -velkost_bunky
                snake_dx = 0
    else:
        if symbol == key.SPACE:
            nova_hra()

def obnovenie(dt):
    global snake_x, snake_y, jedlo_x, jedlo_y, jedlo_x, jedlo1_y, koniec_hry

    if koniec_hry:
        return
    if stav_koniec_hry():
        koniec_hry = True
        naburanie.play()
        player.pause()
        return

    chvost.append((snake_x, snake_y))

    snake_x += snake_dx
    snake_y += snake_dy

    if snake_x == jedlo_x and snake_y == jedlo_y:
        eat.play()
        nakresli_jedlo()
    else:
        chvost.pop(0)

    if snake_x == jedlo1_x and snake_y == jedlo1_y:
        if snake_x == jedlo1_x and snake_y == jedlo1_y and chvost > []:
            drink.play()
            chvost.pop(0)
        else:
            koniec_hry = True
            naburanie.play()
            player.pause()
            return
        nakresli_jedlo1()

def stav_koniec_hry():
    podmienka1 = snake_x + snake_dx < 0 or snake_x + snake_dx > window.width - velkost_bunky or snake_y + snake_dy < 0 or snake_y + snake_dy > window.height - velkost_bunky
    podmienka2 = (snake_x, snake_y) in chvost
    podmienka3 = snake_x == jedlo1_x and snake_y == jedlo1_y and chvost == []
    return podmienka1 or podmienka2 or podmienka3

nakresli_jedlo()
nakresli_jedlo1()

player = media.Player()
player.loop = True
player.queue(hudba_na_pozadi)
player.play()
player.volume = 0.1
nova_hra()

clock.schedule_interval(obnovenie, 1/10)

app.run()
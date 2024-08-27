import arcade
import random
import math

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Typing Game"

class Confetti:
    def __init__(self, x, y):
        self.confetti = [
            arcade.SpriteSolidColor(10, 10, arcade.color.PURPLE_MOUNTAIN_MAJESTY),
            arcade.SpriteSolidColor(10, 10, arcade.color.FUCHSIA_PINK),
            arcade.SpriteSolidColor(10, 10, arcade.color.LIGHT_SALMON),
            arcade.SpriteSolidColor(10, 10, arcade.color.KHAKI),
        ]
        for sprite in self.confetti:
            sprite.center_x = x
            sprite.center_y = y
        self.y = y + 50
        self.animation_time = -2
        self.directions_x = [random.random() * -10 for _ in self.confetti]
        self.speeds = [random.random() * 2 + 2 for _ in self.confetti]
    
    def draw(self):
        for c in self.confetti:
            c.draw()
            
    def update(self, dt):
        self.animation_time += dt * 20
        for c, d, s in zip(self.confetti, self.directions_x, self.speeds):
            c.center_y = self.y - self.animation_time ** 2 * s
            c.center_x += d * dt * 10

class Game:
    def __init__(self):
        self.words = ["SONNE", "MOND", "STERNE", "KOMET", "VENUS", "RAKETE", "STRAHLUNG", "ALIENS", "MILCHSTRASSE", "DISTANZ"]
        
    def new_round(self):
        self.word = random.choice(self.words)
        
    def check_key(self, character):
        if character == self.word[0]:
            self.word = self.word[1:]
            return True
        return False

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.game = Game()
        self.characters = None
        self.confetti = None
        self.laser = None
        self.stars = None
        self.shake_animation_time = 0
        
    def setup(self):
        arcade.load_font("assets/joystix monospace.otf")

        self.laser = arcade.ShapeElementList()
        self.laser.append(arcade.create_line(SCREEN_WIDTH / 5, 0, SCREEN_WIDTH / 5, SCREEN_HEIGHT, arcade.color.FUCHSIA_PINK, 2))
        
        self.stars = arcade.SpriteList()
        for _ in range(20):
            star = arcade.SpriteSolidColor(4, 4, arcade.color.PURPLE_MOUNTAIN_MAJESTY)
            star.center_x = random.randint(0, SCREEN_WIDTH)
            star.center_y = random.randint(0, SCREEN_HEIGHT)
            self.stars.append(star)
        
        self.start_new_round()
        
    def start_new_round(self):
        self.game.new_round()
        self.characters = []
        self.confetti = []
        x = SCREEN_WIDTH
        y = random.randint(SCREEN_HEIGHT / 4, SCREEN_HEIGHT / 4 * 3)
        for t in self.game.word:
            character = arcade.Text(t, x, y, arcade.color.YELLOW, 24, anchor_x="center", font_name="Joystix")
            self.characters.append(character)
            x += 32
        
    def on_draw(self):
        self.clear()
        self.laser.draw()
        self.stars.draw()
        for character in self.characters:
            character.draw()
        for c in self.confetti:
            c.draw()
            
    def on_update(self, dt):
        for c in self.characters:
            c.x -= 100 * dt
        if self.characters and self.characters[0].x < SCREEN_WIDTH / 5 + 12:
            self.start_new_round()
        for c in self.confetti:
            c.update(dt)
        if self.shake_animation_time > 0:
            self.shake_animation_time -= dt
            self.characters[0].rotation = math.sin(self.shake_animation_time * 50) * 20
        else:
            if self.characters:
                self.characters[0].rotation = 0
        for s in self.stars:
            s.center_x += dt * 20
            if s.center_x > SCREEN_WIDTH:
                s.center_x = 0
            
    def on_key_press(self, key, modifiers):
        character = chr(key).upper()
        if self.game.check_key(character):
            if self.characters:
                first_char = self.characters.pop(0)
                if not self.game.word:  # word complete
                    self.start_new_round()
                self.confetti.append(Confetti(first_char.x, first_char.y))
        else:
            self.shake_animation_time = 0.3  # 300 ms

window = GameWindow()
window.setup()
arcade.run()

import arcade
import random
import math
import array, tempfile, os, wave

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "산성비"

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
        self.directions_x = [random.random() * -10 + 5 for _ in self.confetti]
        self.speeds = [random.random() * 2 + 2 for _ in self.confetti]
    
    def draw(self):
        for c in self.confetti:
            c.draw()
            
    def update(self, dt):
        self.animation_time += dt * 20
        for c, d, s in zip(self.confetti, self.directions_x, self.speeds):
            c.center_y = self.y - self.animation_time ** 2 * s
            c.center_x += d * dt * 10

class Word:
    def __init__(self, text, x, y):
        self.text = text
        self.sprite = arcade.Text(text, x, y, arcade.color.WHITE, 24, font_name="LanaPixel")
        self.speed = random.uniform(50, 170)
        self.lifetime = 0
        self.is_dead = False

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.y -= self.speed * dt
        self.lifetime += dt


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE)
        
        self.words = []
        self.confetti = []
        self.input_box = ""
        self.shake_time = 0
        self.score = 1024
        self.igt = 0

        self.word_list = ["헬로월드", "빵형의 개발도상국", "구독과 좋아요"]

        self.correct_sound = arcade.Sound("assets/correct_sound.wav")
        self.wrong_sound = arcade.Sound("assets/wrong_sound.wav")

    def setup(self):
        arcade.load_font("assets/LanaPixel.ttf")
        self.score = 1024

    def add_word(self):
        # if len(self.words) < 10 and random.random() < 0.1:
        if self.igt > 3 and random.random() < 0.25:
            word = random.choice(self.word_list)
            x = random.randint(0, SCREEN_WIDTH - 100)
            new_word = Word(word, x, SCREEN_HEIGHT)
            self.words.append(new_word)

    def on_draw(self):
        self.clear()
        
        for word in self.words:
            word.draw()
        
        for c in self.confetti:
            c.draw()
        
        # 입력 상자 그리기
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 30, SCREEN_WIDTH, 60, arcade.color.LIGHT_GRAY)
        arcade.draw_text("빵형의 개발도상국", SCREEN_WIDTH // 2, 30, arcade.color.BLACK, 20, anchor_x="center", font_name="LanaPixel")
        
        # 점수 표시
        arcade.draw_text(f"점수: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18, font_name="LanaPixel")

        # 화면 흔들기 효과
        if self.shake_time > 0:
            arcade.set_viewport(
                -random.randint(0, 5), SCREEN_WIDTH + random.randint(0, 5),
                -random.randint(0, 5), SCREEN_HEIGHT + random.randint(0, 5)
            )
        else:
            arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_update(self, delta_time):
        self.igt += delta_time
        self.add_word()
        
        for word in self.words:
            word.update(delta_time)
            
            if not word.is_dead and word.lifetime > 3:
                word.is_dead = True
                self.confetti.append(Confetti(word.sprite.x, word.sprite.y))
                self.words.remove(word)
                self.wrong_sound.play()
                self.shake_time = 0.3
        
        self.words = [word for word in self.words if word.sprite.y > 0]
        
        for c in self.confetti:
            c.update(delta_time)
        
        self.confetti = [c for c in self.confetti if c.animation_time < 100]
        
        if self.shake_time > 0:
            self.shake_time -= delta_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.input_box = self.input_box[:-1]
        elif key == arcade.key.ENTER:
            self.check_input()
        elif key == arcade.key.SPACE:
            self.input_box += " "

    def on_text(self, text):
        self.input_box += text

    def check_input(self):
        for word in self.words:
            if word.text == self.input_box.strip():
                self.words.remove(word)
                self.confetti.append(Confetti(word.sprite.x, word.sprite.y))
                self.score += len(word.text)
                self.input_box = ""
                self.correct_sound.play()
                return
        
        # 일치하는 단어가 없으면 화면 흔들기
        self.shake_time = 0.3
        self.input_box = ""
        self.wrong_sound.play()


window = Game()
window.setup()
arcade.run()

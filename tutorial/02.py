import arcade
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "산성비"

class Word:
    def __init__(self, text, x, y):
        self.text = text
        self.sprite = arcade.Text(text, x, y, arcade.color.WHITE, 18, font_name="LanaPixel")
        self.speed = random.uniform(30, 70)

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.y -= self.speed * dt

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.load_font("LanaPixel.ttf")

        arcade.set_background_color(arcade.color.DARK_BLUE)

        self.words = []
        self.word_list = ["헬로월드", "빵형의개발도상국", "구독과좋아요", "파이썬", "아케이드", "게임", "프로그래밍", "타자연습", "재미있다", "산성비"]

### 02 ###
        self.input_box = ""
### /02 ###

    def on_update(self, dt):
        if len(self.words) < 10 and random.random() < 0.02:
            word = random.choice(self.word_list)
            x = random.randint(100, SCREEN_WIDTH - 100)
            new_word = Word(word, x, SCREEN_HEIGHT)
            self.words.append(new_word)

        for word in self.words:
            word.update(dt)

    def on_draw(self):
        self.clear()

        for word in self.words:
            word.draw()

            if word.sprite.y < 0:
                self.words.remove(word)

### 02 ###
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 30, SCREEN_WIDTH, 60, arcade.color.LIGHT_GRAY)
        arcade.draw_text(self.input_box, SCREEN_WIDTH // 2, 30, arcade.color.BLACK, 24, anchor_x="center", font_name="LanaPixel")
### /02 ###

### 02 ###
    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.input_box = self.input_box[:-1]
        elif key == arcade.key.ENTER:
            for word in self.words:
                if word.text == self.input_box.strip():
                    self.words.remove(word)
                    self.input_box = ""
                    return

            self.input_box = ""
        elif key == arcade.key.SPACE:
            self.input_box += " "

    def on_text(self, text):
        self.input_box += text
### /02 ###


window = Game()
arcade.run()

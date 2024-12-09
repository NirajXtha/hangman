import mysql.connector
from re import M
from kivy.uix.behaviors import button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from random import choice
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.app import MDApp
import widgets.keyboard
import widgets.dynamicwidget
import random

from Dict import data
from session import load_session

Builder.load_file('screens/gamescreen.kv')


class GameScreen(Screen):
    word = str()
    word_list = list(word)
    category = ""

    guess = str()
    keyboard_reference = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.username = load_session().get('username', 'Guest')
        except:
            self.username = None
        db = mysql.connector.connect(
            host="localhost",
            user="Akanshya",
            password="1234",
            database="hangman"
        )
        cursor = db.cursor()

        cursor.execute(f"SELECT level, score, life FROM users WHERE username = '{self.username}'")
        result = cursor.fetchone()

        if result:
            self.level, self.score, self.lives = result
        else:
            self.level = 1
            self.score = 0
            self.lives = 3

        db.close()
        self.choose_word()
        widgets.keyboard.KeyBoard.game_screen_reference = self
    
    def on_enter(self, *args):
        db = mysql.connector.connect(
            host="localhost",
            user="Akanshya",
            password="1234",
            database="hangman"
        )
        cursor = db.cursor()

        cursor.execute(f"SELECT level, score, life FROM users WHERE username = '{self.username}'")
        result = cursor.fetchone()

        if result:
            self.level, self.score, self.lives = result
            self.update_ui()
        else:
            self.level = 1
            self.score = 0
            self.lives = 3

        db.close()
    
    def update_ui(self):
        self.ids.lives_label.text = "💜" * self.lives
        self.ids.score_label.text = str(self.score)
        self.ids.level_label.text = "Level: " + str(self.level)
        self.ids.category.text = "Category: " + str(GameScreen.category).upper()
        self.save_user_data()

    def save_user_data(self, *args):
        db = mysql.connector.connect(
            host="localhost",
            user="Akanshya",
            password="1234",
            database="hangman"
        )
        cursor = db.cursor()

        cursor.execute(f"""
            UPDATE users 
            SET level = {self.level}, score = {self.score}, life = {self.lives} 
            WHERE username = '{self.username}'
        """)
        db.commit()
        db.close()

    def choose_word(self):
        GameScreen.category = random.choice(list(data.keys()))
        GameScreen.word = random.choice(data[GameScreen.category][self.level])
        
        GameScreen.word_list = list(GameScreen.word)
        GameScreen.guess = "_" * len(GameScreen.word)
        print(f"Category: {GameScreen.category}, Word: {GameScreen.word}, Word List: {GameScreen.word_list}")

    def next_game(self):
        if self.lives == 0 or self.level == 6:
            self.save_user_data()
        self.clear_hangman()
        self.choose_word()
        self.ids.guess_label.text = GameScreen.guess

    def clear_hangman(self):
        for instr in widgets.dynamicwidget.DynamicLineWidget.on_canvas:
            self.ids.drawing_area.canvas.remove(instr)

        widgets.dynamicwidget.DynamicLineWidget.on_canvas.clear()
        widgets.dynamicwidget.DynamicLineWidget.instructions.clear()

    def quit_gamescreen(self):
        cancel_button = MDFillRoundFlatIconButton(
            text="NO", icon="close")

        return_main = MDFillRoundFlatIconButton(
            text="Quit", icon="arrow-left")

        dialog = MDDialog(title="Return To Main Screen?",
                          text="Sure Want to Quit the Game?",
                          buttons=[return_main, cancel_button],
                          auto_dismiss=False)

        dialog.open()
        cancel_button.bind(on_press=dialog.dismiss)

        # return_main.bind(on_press=self.save_user_data)
        return_main.bind(on_press=dialog.dismiss)

        app_root = MDApp.get_running_app().root
        tr = app_root.transition
        return_main.bind(
            on_press=lambda *args: setattr(tr, 'direction', "right"))
        return_main.bind(
            on_press=lambda *args: setattr(app_root, 'current', "_main_screen_"))
        return_main.bind(
            on_press=lambda *args: GameScreen.keyboard_reference.reset())

    def reset_game(self):
        self.next_game()

        self.lives = 3
        self.level = 1
        self.score = 0

        self.ids.lives_label.text = "💜" * self.lives
        self.ids.score_label.text = str(self.score)
        self.ids.level_label.text = "Level: " + str(self.level)
        self.ids.category.text = "Category: " + str(GameScreen.category)

    def update_guess(self, btn_text):
        guess_list = list(GameScreen.guess)
        for pos, letter in enumerate(GameScreen.word):
            if(letter.lower() == btn_text.lower()):
                print(f"Letter {letter} found at position {pos}")
                guess_list[pos] = btn_text
                GameScreen.word_list.remove(letter) 
                print(f"After update: Letter = {letter}, Word List = {GameScreen.word_list}")
                print(f"btn_text = {btn_text.lower()}")
        GameScreen.guess = self.ids.guess_label.text = "".join(guess_list)
        print(GameScreen.guess, GameScreen.word_list, GameScreen.word)

    def update_win(self):
        self.score += 100 * self.level
        self.level += 1

        if self.level == 6:
            app_root = MDApp.get_running_app().root
            self.reset_game()
            self.save_user_data()
            setattr(app_root, 'current', '_win_screen_')
        else:
            self.ids.score_label.text = str(self.score)
            self.ids.level_label.text = "Level: " + str(self.level)
            self.save_user_data()

    def update_lose(self):
        if self.score >= 10 * self.level:
            self.score -= 10 * self.level
        else:
            self.score = 0

        self.lives -= 1

        if self.lives == 0:
            app_root = MDApp.get_running_app().root
            self.reset_game()
            self.save_user_data()
            setattr(app_root, 'current', '_lose_screen_')
        else:
            self.ids.score_label.text = str(self.score)
            self.ids.lives_label.text = "💜" * self.lives

    def hint_popup(self):
        hint_button = MDFillRoundFlatIconButton(
            text="Take Hint", icon="key")

        cancel_button = MDFillRoundFlatIconButton(
            text="Cancel", icon="arrow-left")

        dialog = MDDialog(
            title="Buy a Hint?", text="50 points will be deducted from the score",
            buttons=[cancel_button, hint_button], auto_dismiss=False)

        dialog.open()
        cancel_button.bind(on_press=dialog.dismiss)

        hint_button.bind(on_press=lambda *args: self.credit_check())
        hint_button.bind(on_press=dialog.dismiss)

    def credit_check(self):
        if self.score < 50:
            self.insuff_credit()
        else:
            self.take_hint()
    
    def insuff_credit(self):
        ok_button = MDFillRoundFlatIconButton(text="OK", icon="")

        dialog = MDDialog(title="Insufficient Credit", 
        text="Score must be atleast 50 to buy a hint", buttons=[ok_button], 
        auto_dismiss=False)

        dialog.open()
        ok_button.bind(on_press=dialog.dismiss)

    def take_hint(self):
        letter = GameScreen.word_list[0]
        GameScreen.keyboard_reference.ids[letter.upper()].background_color = [1, 1, 1, 1]
        GameScreen.keyboard_reference.ids[letter.upper()].color = [0, 0, 0, 1]

        self.score -= 50
        self.ids.score_label.text = str(self.score)
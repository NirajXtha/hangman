from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
import json
from session import load_session
import mysql.connector

Builder.load_file('screens/sharescreen.kv')


class ShareScreen(Screen):
    username = StringProperty("N/A")
    level = StringProperty("N/A")
    life = StringProperty("N/A")
    status = StringProperty("N/A")

    def __init__(self, **kwargs):
        super(ShareScreen, self).__init__(**kwargs)
        self.load_user_data()

    def load_user_data(self):
        level = 1
        score = 0
        lives = 3
        try:
            with open('session.json', 'r') as f:
                user_data = json.load(f)
                self.username = user_data.get("username", "N/A")
                if(self.username != "N/A"):
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
                        level, score, lives = result
                    self.level = str(level)
                    self.life = str(lives)
                    self.status = str(score)
                    db.close()
                
        except FileNotFoundError:
            print("Profile file not found. Using default values.")

    def build(self):
        return ShareScreen

if __name__ == '__main__':
    ShareScreen().run()

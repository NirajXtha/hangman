from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from session import load_session

from screens.loginscreen import LoginScreen
from screens.signupscreen import SignupScreen
from screens.mainscreen import MainScreen
from screens.gamescreen import GameScreen
from screens.sharescreen import ShareScreen
from screens.winscreen import WinScreen
from screens.titlescreen import TitleScreen
from screens.losescreen import LoseScreen

class RootScreenManager(ScreenManager):
    pass


class HangManApp(MDApp):
    def build(self):
         root = RootScreenManager()
         session_data = load_session()
         if session_data and session_data != None:
            root.current = '_main_screen_'
         else:
            root.current = 'login'
         return root


if __name__ == '__main__':
    HangManApp().run()

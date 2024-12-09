from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton

from session import load_session, clear_session

Builder.load_file('screens/mainscreen.kv')

class MainScreen(Screen):
    def on_pre_enter(self):
        session_data = load_session()
        login_button = self.ids.login_button
        profile_button = self.ids.profile

        if session_data:
            login_button.text = 'Logout'
            login_button.icon = 'logout'
            login_button.on_release = self.logout
            profile_button.disabled = False
            profile_button.opacity = 1
        else:
            login_button.text = 'Login'
            login_button.icon = 'login'
            login_button.on_release = self.login
            profile_button.disabled = True
            profile_button.opacity = 0

    def login(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'

    def logout(self):
        clear_session()
        self.ids.login_button.text = 'Login'
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'

    def show_confirmation_dialog(self):
        cancel_button = MDFillRoundFlatIconButton(text="Cancel", icon="refresh")
        exit_button = MDFillRoundFlatIconButton(text="OK", icon="close-circle")
        dialog = MDDialog(title="Do you really want to exit?",
                          type="confirmation",
                          buttons=[exit_button, cancel_button], auto_dismiss=False)

        dialog.open()
        cancel_button.bind(on_press=dialog.dismiss)
        exit_button.bind(on_press=MDApp.get_running_app().stop)

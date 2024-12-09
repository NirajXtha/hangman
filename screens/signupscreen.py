from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.app import MDApp
from db import create_user

Builder.load_file('screens/signupscreen.kv')

class SignupScreen(Screen):
    def validate_signup(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if not username or not password:
            self.show_dialog("Error", "All fields are required.")
        elif len(password) < 6:
            self.show_dialog("Error", "Password must be at least 6 characters.")
        else:
            create_user(username, password)
            self.show_dialog("Success", "Account created successfully!")
            app_root = MDApp.get_running_app().root
            app_root.current = 'login'

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title, 
            text=text, 
            buttons=[MDFillRoundFlatIconButton(text="OK", on_release=lambda *args: dialog.dismiss())]
        )
        dialog.open()

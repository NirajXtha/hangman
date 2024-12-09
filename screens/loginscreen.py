from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.app import MDApp
from db import verify_user
from session import save_session

Builder.load_file('screens/loginscreen.kv')

class LoginScreen(Screen):
    def validate_login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        if not username or not password:
            self.show_dialog("Error", "Username and Password are required.")
        else:
            user = verify_user(username, password)
            if user:
                self.show_dialog("Success", "Login successful!")
                save_session({"username": username})
                app_root = MDApp.get_running_app().root
                app_root.current = '_main_screen_'
            else:
                self.show_dialog("Error", "Invalid username or password.")

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title, 
            text=text, 
            buttons=[MDFillRoundFlatIconButton(text="OK", on_release=lambda *args: dialog.dismiss())]
        )
        dialog.open()

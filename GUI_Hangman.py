############################ GUI PART ##########################################################
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class WelcomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass
    login_username_text_input = ObjectProperty()
    login_password_text_input = ObjectProperty()

    def login_func(self):
        print("DIAG: username is: ", self.login_username_text_input.text)

class MenuScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation
#################################################################################################
########################## BASE APP PART ########################################################




if __name__ == "__main__":
    MainApp().run()
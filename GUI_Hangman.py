#################################################################################################
########################## BASE APP PART ########################################################
class login_data(object):

    users_index = 0
    username = "guest"








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
    login_username_text_input = ObjectProperty()
    login_password_text_input = ObjectProperty()
    main_menu = ObjectProperty()

    def login_func(self):
        username = self.login_username_text_input.text
        print("DIAG: username is: ", username )

        ### Base App
        import os
        if os.path.isfile("users.txt"):
            print("USERS FILE EXISTS")
            with open('users.txt', 'r') as saved_users:
                users = saved_users.read().splitlines()
                print("DIAG: Users list initialized from file as: ", users)
        else:
            print("USERS FILE DOES NOT EXIST.")

        if username in users:
            print("Diagnostics: USER FOUND!")
            login_data.username = username
        else:
            print("Diagnostics: USER NOT FOUND!")
        ###

        self.manager.current = 'MenuScreen'


class MenuScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation




if __name__ == "__main__":
    MainApp().run()
#################################################################################################
########################## BASE APP PART ########################################################
class login_data(object):

    users_index = 0
    username = "guest"

class MainSinglegameClass:

    target_word = None
    target_word_len = None
    char_found = 0
    word_print = []
    wrong_used_char = []
    total_used_char = []
    gu_left = 6
    match_found = False
    user_gu_accepted = False
    input_error_msg = None # errors from gu_validity_check for user char input, if there are any

    def set_target_word(self, target_word):
        self.target_word = target_word
        self.target_word = target_word
        self.target_word_len = len(target_word)
        print("MPIKA set_target_word function!!!!!!!")

        for i in range(0, self.target_word_len):
            self.word_print.append("_")

    def get_input_error_msg(self):
        return self.input_error_msg

    def get_input_valid_status(self):
        return self.user_gu_accepted

    def gu_validity_check(self, char_gu, total_used_char, res_dict):

        try:  #
            char_gu = int(char_gu)  # checks if the user input
            # print("DIAGNOSTICS: INPUT IS not str")  #is a string or not. This prevents
            string = False  #
        except ValueError:  # the user from entering a number
            # print("DIAGNOSTICS: INPUT IS str")      #
            string = True  #

        if string is True:
            if len(char_gu) > 1:
                single = False
            else:
                single = True

            if char_gu in total_used_char:
                unique = False
            else:
                unique = True

            if char_gu.isalpha():
                letter = True
            else:
                letter = False

        res_dict["string"] = string
        res_dict["single"] = single
        res_dict["unique"] = unique
        res_dict["letter"] = letter

        return




    def get_user_guess(self, gu_char):
        gu_char = gu_char.upper()

        self.user_gu_accepted = False #reset class fields
        self.input_error_msg = None      #reset class fields
        v_res_dict = {}               #validity_result_dictionary

        self.gu_validity_check(gu_char, self.total_used_char, v_res_dict)

        if v_res_dict["string"] is True and v_res_dict["single"] is True and v_res_dict["unique"] is True  and v_res_dict["letter"] is True:
            #user guess entry is valid and is accepted by the game
            self.user_gu_accepted = True
        else:
            # user guess entry is INVALID and is rejected by the game
            # appropriate error message should be displayed
            self.input_error_msg = "Error: \n"
            if v_res_dict["string"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter a character as input.\n"
            if v_res_dict["single"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter a single character as input.\n"
            if v_res_dict["unique"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! You have entered this character during a previous guess.\n"
            if v_res_dict["letter"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter an alphabetic letter.\n"

        self.game_state(gu_char)

    def game_state(self, gu_char):

        match_found = False
        self.total_used_char.append(gu_char)

        for i in range(0, self.target_len):
            if self.target_word[i] == gu_char:
                match_found = True
                self.char_found += 1
                self.word_print[i] = gu_char

        if match_found is False:
            print("\n\nWrong guess!")
            self.gu_msg = "Wrong guess!"
            self.wrong_used_char.append(gu_char)
            self.gu_left = self.gu_left - 1

    def check_win_status(self):
        if self.char_found < self.target_word_len:
            return False
        elif self.char_found == self.target_word_len and self.gu_left >= 0:
            return True







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
            self.manager.current = 'MenuScreen'
        else:
            print("Diagnostics: USER NOT FOUND!")
        ###


class MenuScreen(Screen):

    def on_pre_enter(self, *args):
        self.change_button1_text()

    def change_button1_text(self):
        self.ids.menu_option1.text = "Start a new singleplayer game as " + login_data.username


class SingleplayerGameScreen(Screen):
    word_list = []
    target_word = None
    # word_print = None
    guess_input = ObjectProperty()

    def on_pre_enter(self, *args):

        with open("1.txt", 'r') as dictionary:  # settings[1] contains the file name (name.txt)
            self.word_list = dictionary.read().upper().splitlines()
            print('diag: word_list is: ', self.word_list)
        import random
        self.target_word = random.choice(self.word_list)
        print("diag: target_word is: ", self.target_word)


    def on_enter(self, *args):
        game_instance = MainSinglegameClass()
        game_instance.set_target_word(self.target_word)
        word_str = ''.join(game_instance.word_print) #convert word_print array to string
        self.ids.word_display.text = word_str





class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation




if __name__ == "__main__":
    MainApp().run()
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
    # target_word = None
    # word_print = None
    guess_input = ObjectProperty()

    def entry_check(choice, total_used_char):

        verified = False

        while verified == False:

            try:  #
                choice = int(choice)  # checks if the user input
                # print("DIAGNOSTICS: INPUT IS not str")  #is a string or not. This prevents
                string = False  #
            except ValueError:  # the user from entering a number
                # print("DIAGNOSTICS: INPUT IS str")      #
                string = True  #

            if string == True:
                if len(choice) > 1:
                    single = False
                else:
                    single = True

                if choice in total_used_char:
                    unique = False
                else:
                    unique = True

                if choice.isalpha():
                    letter = True
                else:
                    letter = False

            if string == True and single == True and unique == True and letter == True:
                verified = True
                return choice
            else:
                if string == False:
                    print("Wrong entry! Please enter a character as input.")
                elif single == False:
                    print("Wrong entry! Please enter a single character as input.")
                elif unique == False:
                    print("Wrong entry! You have entered this character during a previous guess.")
                elif letter == False:
                    print("Wrong entry! Please enter an alphabetic letter.")

                choice = input("Please enter your guess: ")
                choice = choice.upper()

    def char_entry_func(self, char_queue, total_used_char, fn):  # MULTIPLAYER##
        import sys
        import os
        sys.stdin = os.fdopen(fn)  # open stdin in this process
        print("DIAG: multiplayer char_entry_func!!!!!!!!")

        print("Please enter a single character as your guess: ")
        while True:
            if self.guess_input.text != "":
                char_gu = self.guess_input.text
                break
        char_gu = char_gu.upper()
        char_gu = self.entry_check(char_gu, total_used_char)
        char_queue.put(char_gu)

        # import sys

        # read = sys.stdin.read(1)
        # print("DIAG: read is: ",read)

        # print("DIAG MPIKA")
        # print(sys.stdin.read(2) != " ")
        # char_queue.put(sys.stdin.read(1))


        return

    def main_game_func(self, menu_choice, settings, target, username, unique_id):

        com_array = []

        char_found = 0
        word_print = []
        wrong_used_char = []
        total_used_char = []
        gu_left = 6
        match_found = False


        if menu_choice == 5 or menu_choice == 6:  # multiplayer mode
            multiplayer = 1
        else:
            multiplayer = 0  # single player mode

            ### multiplayer == 2 --->stop game!

        print("Diagnostics: Target word is:", target)
        target_len = len(target)

        for i in range(0, target_len):
            word_print.append("_")

        for i in range(0,
                       target_len):  # Emfanizw se oles tis theseis tis lexis ta grammata poy einai idia me to proto gramma.
            if target[0] == target[i]:
                total_used_char.append(target[0])
                word_print[i] = target[0]
                char_found += 1

        ##### MAIN GAME ######
        while gu_left > 0 and char_found < target_len and multiplayer != 2:

            print(hangman_art[6 - gu_left])

            for i in range(0, target_len):
                print(word_print[i], end=" ")  # Prints on the same line
            print("\n")

            if wrong_used_char:  # checks if list is NOT empty
                print(wrong_used_char)

            print("You have", gu_left, "guesses left.")

            #####################  SINGLEPLAYER  ################################

            if menu_choice != 5 and menu_choice != 6:
                import multiprocessing
                char_queue = multiprocessing.Queue(maxsize=5)  # ftiaxnw oura

                # h eisagogi xaraktira ginetai me parallili epexergasia me thread oste na mporoyn
                # na prosthethoyn mellontika
                # leitoyrgies opos px xronometrisi kai time limit.

                create_process = True  # flag gia na xekinisei process MONO stin proti ektelesi tis loopas
                import time  # TEMPORARY?
                while True:

                    import sys

                    if create_process == True:
                        print("DIAG: Initializing char_entry_func parallel process!...")

                        import sys
                        fn = sys.stdin.fileno()  # get original file descriptor
                        print("DIAG: fn is: ", fn)
                        import multiprocessing
                        char_input_process = multiprocessing.Process(target=self.char_entry_func,
                                                                     args=(char_queue, total_used_char, fn))
                        char_input_process.start()

                        create_process = False

                    if not char_queue.empty():
                        # char_input_thread.exit()
                        print("EFTASA 4")
                        print("H OYRA EXEI XARAKTIRA STI LOOPA")
                        given_char = char_queue.get()  ##pairnw ton char poy edwse o user
                        char_input_process.terminate()
                        break
                    time.sleep(1)

            #####################  MULTIPLAYER  ################################
            #
            #
            # if menu_choice == 5 or menu_choice == 6:
            #     import multiprocessing
            #     char_queue = multiprocessing.Queue(maxsize=5)  # ftiaxnw oura
            #
            #     create_process = True  # flag gia na xekinisei process MONO stin proti ektelesi tis loopas
            #     import time  # TEMPORARY?
            #
            #     #######################################################################################################
            #     while True:
            #
            #         import sys
            #
            #         if create_process == True:
            #             print("DIAG: Initializing char_entry_func parallel process!...")
            #
            #             import sys
            #             fn = sys.stdin.fileno()  # get original file descriptor
            #             print("DIAG: fn is: ", fn)
            #             import multiprocessing
            #             char_input_process = multiprocessing.Process(target=char_entry_func,
            #                                                          args=(char_queue, total_used_char, fn))
            #             char_input_process.start()
            #
            #             create_process = False
            #
            #         ## elegxw gia niki apo allon client
            #
            #         win_check_array = client_win_check_func()
            #         print("ELAVA win_check_array[0]: ", win_check_array[0])
            #         if win_check_array[0] == "end_game":
            #             print("EFTASA 3")
            #             print("DIAG: end_game STI LOOPA")
            #             print("O NIKITIS ENTOPISTIKE OS: ", win_check_array[1], win_check_array[2])
            #             multiplayer = 2  # stop game
            #             char_input_process.terminate()
            #             break
            #
            #         if not char_queue.empty():
            #             # char_input_thread.exit()
            #             print("EFTASA 4")
            #             print("H OYRA EXEI XARAKTIRA STI LOOPA")
            #             given_char = char_queue.get()  ##pairnw ton char poy edwse o user
            #             char_input_process.terminate()
            #             break
            #         time.sleep(1)

            ####################################################################################################

            # if multiplayer != 2:  # multiplayer == 2 --->stop game!
            #     total_used_char.append(given_char)
            #     for i in range(0, target_len):
            #         if target[i] == given_char:
            #             match_found = True
            #             char_found += 1
            #             word_print[i] = given_char
            #
            #     if match_found == False:
            #         print("\n\nWrong guess!")
            #         wrong_used_char.append(given_char)
            #         gu_left = gu_left - 1
            #
            #     match_found = False
            #     print("\n")
            # else:
            #     print("*** GAME OVER! Client", win_check_array[1], win_check_array[2], "has won the game!!! ***\n\n")

        ###################################################

        if char_found != target_len and multiplayer != 2:
            print("You are out of guesses!")
            print("The word was:", target)
            print("   *** GAME OVER ***")
        elif char_found == target_len:
            for i in range(0, target_len):
                print(word_print[i], end=" ")  # Prints on the same line
            print("\n")
            print("Congratulations! YOU HAVE WON !")

            # if menu_choice == 5 or menu_choice == 6:
            #     ##SEND "WIN SIGNAL" TO SERVER!
            #     import socket
            #     # create a socket object
            #
            #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     # get local machine name
            #     host = socket.gethostname()
            #     port = 9998
            #     # connection to hostname on the port.
            #     s.connect((host, port))
            #
            #     print("DIAG: in main_game_func winner username: ", username)
            #     # SENDING "win" MESSAGE TO SERVER USING ARRAY!
            #     # message format is: "win"/username/unique_id
            #     import pickle
            #     com_array.append("win")
            #     com_array.append(username)
            #     com_array.append(unique_id)
            #
            #     s.send(pickle.dumps(com_array))

        # score = score_func(settings, target_len, gu_left)
        # print("Your score is:", score)
        # print("Would you like to save your score?")
        # print("Would you like to start a new game?")
        # choice = input("Please enter Yes or No: ")
        # while choice != "Yes" and choice != "No":
        #     print("Wrong entry!")
        #     choice = input("Please enter Yes or No:")
        #
        # if choice == "No":
        #     print("DIAG mpika sto NO2")
        #     print("\n\n\n\n\n\n\n\n")
        #     print("DIAG: welcome_func apo to simeio 3!")
        #
        #     menu_choice = welcome_func(login_data.username)
        #     return menu_choice
        # elif choice == "Yes":
        #     print("$$$UNDER CONSTRUCTION! ")

    def on_pre_enter(self, *args):

        with open("1.txt", 'r') as dictionary:  # settings[1] contains the file name (name.txt)
            self.word_list = dictionary.read().upper().splitlines()
            print('diag: word_list is: ', self.word_list)
        import random
        self.target_word = random.choice(self.word_list)
        print("diag: target_word is: ", self.target_word)
        #self.ids.word_display.text = self.target_word



class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation




if __name__ == "__main__":
    MainApp().run()
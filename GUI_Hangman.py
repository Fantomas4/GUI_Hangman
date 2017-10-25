#################################################################################################
########################## BASE APP PART ########################################################


class LoginData(object):
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
    input_error_msg = "" # errors from gu_validity_check for user char input, if there are any

    winner_username = ""
    winner_id = None

    def set_target_word(self, target_word):
        self.word_print = []
        self.target_word = target_word
        self.target_word = target_word
        self.target_word_len = len(target_word)
        print("MPIKA set_target_word function!!!!!!!")

        for i in range(0, self.target_word_len):
            self.word_print.append("_ ") # adds _ with space to hidden word.

    def reset_input_error_msg(self):
        self.input_error_msg = ""

    def reset_gu_left(self):
        self.gu_left = 6

    def reset_used_char(self):
        self.wrong_used_char = []
        self.total_used_char = []

    def reset_game(self):
        self.reset_gu_left()
        self.reset_used_char()
        self.reset_input_error_msg()

    def get_cur_word(self):   #get current word (example A _ B _ _)
        return ''.join(self.word_print) # returns the word_print array in string form

    def get_input_error_msg(self):
        return self.input_error_msg

    def get_input_valid_status(self):
        return self.user_gu_accepted

    def get_gu_left(self):
        return str(self.gu_left) #returns gu_left converting it from int to string

    def gu_validity_check(self, char_gu, total_used_char, res_dict):

        single = True
        alpha = True
        eng = True
        unique = True

        if len(char_gu) > 1:
            single = False

        if char_gu.isalpha() is False:
            alpha = False

        if char_gu in total_used_char:
            unique = False

        res_dict["single"] = single
        res_dict["alpha"] = alpha
        res_dict["eng"] = eng
        res_dict["unique"] = unique

        return

    def get_wrong_used_char(self):
        return str(self.wrong_used_char)

    def set_user_guess(self, gu_char):
        gu_char = gu_char.text # converts input from GUI input to text
        gu_char = gu_char.upper()
        print("get_user_guess got from GUI: ",gu_char)

        self.user_gu_accepted = False #reset class fields
        self.input_error_msg = None      #reset class fields
        v_res_dict = {}               #validity_result_dictionary

        self.gu_validity_check(gu_char, self.total_used_char, v_res_dict)

        if v_res_dict["single"] is True and v_res_dict["alpha"] is True and v_res_dict["unique"] is True:
            #user guess entry is valid and is accepted by the game
            self.user_gu_accepted = True
            self.total_used_char.append(gu_char)
        else:
            # user guess entry is INVALID and is rejected by the game
            # appropriate error message should be displayed
            self.input_error_msg = "Error: \n"
            if v_res_dict["single"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter a single character as input.\n"

            if v_res_dict["alpha"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter an alphabetic character as input.\n"

            if v_res_dict["unique"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! You have entered this character during a previous guess.\n"

        self.game_state(gu_char, self.user_gu_accepted)

    def game_state(self, gu_char, user_gu_accepted):

        match_found = False

        if user_gu_accepted is True:
            for i in range(0, self.target_word_len):
                if self.target_word[i] == gu_char:
                    match_found = True
                    self.char_found += 1
                    self.word_print[i] = gu_char

            if match_found is False:
                print("\n\nWrong guess!")
                self.gu_msg = "Wrong guess!"
                self.wrong_used_char.append(gu_char)
                self.gu_left = self.gu_left - 1

    def check_game_status(self):
        # returns: -1 for loss, 0 for in progress, 1 for win
        if self.gu_left <= 1:
            return -1
        elif self.char_found < self.target_word_len:
            return 0
        elif self.char_found == self.target_word_len and self.gu_left > 0:
            return 1
#############################################################################################


class ServerGameHostClass:
    winner_username = None
    winner_id = None

    def initialize_server(self):

        import sys

        # first a random word is picked from the word txt file.
        with open("1.txt", 'r') as dictionary:  # settings[1] contains the file name (name.txt)
            word_list = dictionary.read().upper().splitlines()
            print('diag: word_list is: ', word_list)
        import random
        self.target_word = random.choice(word_list)
        print("diag: target_word is: ", self.target_word)

        import random
        self.target_word = random.choice(word_list)

        used_id = []
        win_status = False  # no client has won yet

        import socket


        print("DIAG: gethostname(): ", socket.gethostname(), file=sys.stderr)
        PORT = 9999

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('', PORT))
        listen_socket.listen(5)
        print('Serving HTTP on port %s ...' % PORT, file=sys.stderr)

        while True:
            client_connection, client_address = listen_socket.accept()
            print("Got a connection from %s" % str(client_address), file=sys.stderr)
            request = client_connection.recv(1024)
            # print("Server got the request: ",request.decode('ascii'),file=sys.stderr)

            # receive and DECODE array through socket!
            import pickle  # serialize array that will be send over socket
            com_array = pickle.loads(request)  # serialize array that will be send over socket

            if com_array[0] == "join_request":
                import random
                unique_id = random.randrange(0,5000)
                while unique_id in used_id:
                    unique_id = random.randrange(0, 5000)
                used_id.append(unique_id)

                import pickle
                com_array = []
                com_array.append(unique_id)
                client_connection.send(pickle.dumps(com_array))

            elif com_array[0] == "word_request":
                print("DIAG: Server shares word with client!",file=sys.stderr)
                print("DIAG: SERVER WORD: ", self.target_word, file=sys.stderr)
                ##SENDING "word_request" MESSAGE TO SERVER USING ARRAY!
                import pickle
                com_array = []
                com_array.append(self.target_word)
                client_connection.send(pickle.dumps(com_array))
                # client_connection.close()

            elif com_array[0] == "win_status":
                if win_status is True:
                    # out_request = "end_game"

                    import pickle
                    com_array = []  # empties array?
                    com_array.append("end_game")
                    com_array.append(self.winner_username)
                    com_array.append(self.winner_id)
                    client_connection.send(pickle.dumps(com_array))

                elif win_status is False:
                    out_request = "pending_game"

                    import pickle
                    com_array = []  # empties array?
                    com_array.append(out_request)
                    client_connection.send(pickle.dumps(com_array))

            elif com_array[0] == "win":
                win_status = True
                self.winner_username = com_array[1]
                self.winner_id = com_array[2]
                print(" Server_win_check received winner: ", self.winner_username, self.winner_id)
                ## edw prepei na stelnei se oloys toys client ton nikiti
                listen_socket.close()
                break


class MainMultigameClass:

    target_word = None
    target_word_len = None
    char_found = 0
    word_print = []
    wrong_used_char = []
    total_used_char = []
    gu_left = 6
    match_found = False
    user_gu_accepted = False
    input_error_msg = ""  # errors from gu_validity_check for user char input, if there are any

    unique_id = None  # client id given by server

    def set_target_word(self, target_word):
        self.word_print = []
        self.target_word = target_word
        self.target_word = target_word
        self.target_word_len = len(target_word)
        print("MPIKA set_target_word function!!!!!!!")

        for i in range(0, self.target_word_len):
            self.word_print.append("_ ") # adds _ with space to hidden word.

    def reset_input_error_msg(self):
        self.input_error_msg = ""

    def reset_gu_left(self):
        self.gu_left = 6

    def reset_used_char(self):
        self.wrong_used_char = []
        self.total_used_char = []

    def reset_game(self):
        self.reset_gu_left()
        self.reset_used_char()
        self.reset_input_error_msg()

    def get_cur_word(self):   #get current word (example A _ B _ _)
        return ''.join(self.word_print) # returns the word_print array in string form

    def get_input_error_msg(self):
        return self.input_error_msg

    def get_input_valid_status(self):
        return self.user_gu_accepted

    def get_gu_left(self):
        return str(self.gu_left) #returns gu_left converting it from int to string

    def gu_validity_check(self, char_gu, total_used_char, res_dict):

        single = True
        alpha = True
        eng = True
        unique = True

        if len(char_gu) > 1:
            single = False

        if char_gu.isalpha() is False:
            alpha = False

        if char_gu in total_used_char:
            unique = False

        res_dict["single"] = single
        res_dict["alpha"] = alpha
        res_dict["eng"] = eng
        res_dict["unique"] = unique

        return

    def get_wrong_used_char(self):
        return str(self.wrong_used_char)

    def set_user_guess(self, gu_char):
        gu_char = gu_char.text # converts input from GUI input to text
        gu_char = gu_char.upper()
        print("get_user_guess got from GUI: ",gu_char)

        self.user_gu_accepted = False #reset class fields
        self.input_error_msg = None      #reset class fields
        v_res_dict = {}               #validity_result_dictionary

        self.gu_validity_check(gu_char, self.total_used_char, v_res_dict)

        if v_res_dict["single"] is True and v_res_dict["alpha"] is True and v_res_dict["unique"] is True:
            #user guess entry is valid and is accepted by the game
            self.user_gu_accepted = True
            self.total_used_char.append(gu_char)
        else:
            # user guess entry is INVALID and is rejected by the game
            # appropriate error message should be displayed
            self.input_error_msg = "Error: \n"
            if v_res_dict["single"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter a single character as input.\n"

            if v_res_dict["alpha"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! Please enter an alphabetic character as input.\n"

            if v_res_dict["unique"] is False:
                self.input_error_msg = self.input_error_msg + "Wrong entry! You have entered this character during a previous guess.\n"

        self.game_state(gu_char, self.user_gu_accepted)

    def game_state(self, gu_char, user_gu_accepted):

        match_found = False

        if user_gu_accepted is True:
            for i in range(0, self.target_word_len):
                if self.target_word[i] == gu_char:
                    match_found = True
                    self.char_found += 1
                    self.word_print[i] = gu_char

            if match_found is False:
                print("\n\nWrong guess!")
                self.gu_msg = "Wrong guess!"
                self.wrong_used_char.append(gu_char)
                self.gu_left = self.gu_left - 1

    def check_game_status(self):
        # returns: -1 for loss, 0 for in progress, 1 for win
        if self.gu_left <= 1:
            return -1
        elif self.char_found < self.target_word_len:
            return 0
        elif self.char_found == self.target_word_len and self.gu_left > 0:
            return 1
###############################################################################

    def client_win_check_func(self):

        com_array = []

        import socket
        # create a socket object

        win_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get local machine name
        host = socket.gethostname()
        port = 9999
        # connection to hostname on the port.
        win_socket.connect((host, port))

        ##SENDING "win_status" MESSAGE TO SERVER USING ARRAY!
        import pickle
        send_msg = "win_status"
        com_array.append(send_msg)
        win_socket.send(pickle.dumps(com_array))

        received_msg = win_socket.recv(1024)
        # receive and DECODE array through socket!
        import pickle
        com_array = pickle.loads(received_msg)

        # print("Client got answer from server: ", received_msg,file=sys.stderr)
        print("Client got answer from server using array: ", com_array[0])

        win_socket.close()

        return com_array

    def initialize_client(self):
        com_array = []

        import socket
        # create a socket object

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get local machine name
        host = socket.gethostname()
        port = 9999
        # connection to hostname on the port.
        s.connect((host, port))

        # SENDING "join_request" MESSAGE TO SERVER USING ARRAY!
        import pickle
        send_msg = "join_request"
        com_array.append(send_msg)
        s.send(pickle.dumps(com_array))

        # Receive no more than 1024 bytes
        in_request = s.recv(1024)
        import pickle
        com_array = pickle.loads(in_request)
        self.unique_id = com_array[0]
        print("CLIENT WAS GIVEN UNIQUE ID $$$ : ", self.unique_id)
        # close socket
        s.close()

        # create a socket object again!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        ##SENDING "word_request" MESSAGE TO SERVER USING ARRAY!
        import pickle
        com_array = []
        send_msg = "word_request"
        com_array.append(send_msg)
        s.send(pickle.dumps(com_array))

        # Receive no more than 1024 bytes
        in_request = s.recv(1024)

        import pickle
        com_array = pickle.loads(in_request)

        s.close()

        self.target_word = com_array[0]








############################ GUI PART ##########################################################
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ObjectProperty


class WelcomeScreen(Screen):

    def guest_login(self):
        LoginData.username = "Guest"
        self.manager.current = "MenuScreen"


class RegisterScreen(Screen):
    username_text_input = ObjectProperty()
    password_text_input = ObjectProperty()
    user_error_msg = ObjectProperty()

    users = []

    def on_pre_enter(self, *args):  #read users.txt file
        import os
        if os.path.isfile("users.txt"):
            print("USERS FILE EXISTS")
            with open('users.txt', 'r') as users_file:
                self.users = users_file.read().splitlines()
                print("DIAG: Users list initialized from file as: ", self.users)
        else:
            print("USERS FILE DOES NOT EXIST.")

    def register_user(self):
        print("DIAG: self.users: ", self.users)
        if self.username_text_input.text in self.users:
            print("$$$ USERNAME ALREADY EXISTS! $$$")
            self.user_error_msg.text = "Error: Username already exists!"
        else:
            print("### USER REGISTERED SUCCESSFULLY")
            self.users.append(self.username_text_input.text)
            LoginData.username = self.username_text_input.text
            print(" 1-> users is: ", self.users)
            users_index = len(self.users)
            print("DIAG: User_index is: ", len(self.users))
            with open('users.txt', 'w') as users_file:  ### SAVES USERS TO TEXT FILE!
                for i in range(0, users_index):
                    print("DIAG: LOOP TYPOSIS SE ARXEIO")
                    print("DIAG: users", self.users)
                    users_file.write(self.users[i])
                    users_file.write("\n")
            self.manager.current = 'MenuScreen'


class LoginScreen(Screen):
    username_text_input = ObjectProperty()
    password_text_input = ObjectProperty()
    user_error_msg = ObjectProperty()
    users = []

    def on_pre_enter(self, *args):
        import os
        if os.path.isfile("users.txt"):
            print("USERS FILE EXISTS")
            with open('users.txt', 'r') as users_file:
                self.users = users_file.read().splitlines()
                print("DIAG: Users list initialized from file as: ", self.users)
        else:
            print("USERS FILE DOES NOT EXIST.")

    def login_func(self):
        username = self.username_text_input.text
        print("DIAG: username is: ", username )

        ### Base App
        if username in self.users:
            print("Diagnostics: USER FOUND!")
            LoginData.username = username
            self.manager.current = 'MenuScreen'
        else:
            print("Diagnostics: USER NOT FOUND!")
            self.user_error_msg.text = "Error: User does not exist!"
        ###


class MenuScreen(Screen):

    def on_pre_enter(self, *args):
        self.change_button1_text()

    def change_button1_text(self):
        self.ids.menu_option1.text = "Start a new singleplayer game as " + LoginData.username


class SingleplayerGameScreen(Screen):
    word_list = []
    target_word = None
    # word_print = None
    guess_input = ObjectProperty()
    word_output = ObjectProperty()
    gu_left_output = ObjectProperty()
    wrong_used_char_output = ObjectProperty()
    game_instance = MainSinglegameClass()
    error_msg_output = ObjectProperty()

    def on_pre_enter(self, *args):

        with open("1.txt", 'r') as dictionary:  # settings[1] contains the file name (name.txt)
            self.word_list = dictionary.read().upper().splitlines()
            print('diag: word_list is: ', self.word_list)
        import random
        self.target_word = random.choice(self.word_list)
        print("diag: target_word is: ", self.target_word)

        self.game_instance.set_target_word(self.target_word)
        self.word_output.text = self.game_instance.get_cur_word()
        self.gu_left_output.text = "You have " + self.game_instance.get_gu_left() + " guesses left"

    def on_enter(self, *args):
        pass

    def run_game(self, gu_input):  # gets called when user presses "Submit" button.

        if self.game_instance.check_game_status() == -1:  # player has lost the game -> gameover
            self.gu_left_output.text = "No guesses left!"  # updates guesses left text shown
            self.error_msg_output.text = "GAME OVER! " + "The word was: " + self.target_word

        elif self.game_instance.check_game_status() == 0:  # no win yet!
            print(" MPIKA MPIKA MPIKA MPIKA !!!!!@@#")
            self.game_instance.set_user_guess(gu_input)  # passes user guess input to methods of game_instance
            self.word_output.text = self.game_instance.get_cur_word()  # updates word shown
            if self.game_instance.wrong_used_char: #checks if list is empty so as not to print it
                self.wrong_used_char_output.text = "Wrong guesses: " + self.game_instance.get_wrong_used_char() #updates GUI list of wrong char guesses
            self.gu_left_output.text = "You have " + self.game_instance.get_gu_left() + " guesses left"  # updates guesses left text shown
            if self.game_instance.get_input_valid_status() is True:
                pass
            else:
                self.error_msg_output.text = self.game_instance.get_input_error_msg()

            if self.game_instance.check_game_status() == 1:
                self.error_msg_output.text = "You have WON!"
                self.gu_left_output.text = ""

        self.guess_input.text = ""  # clears guess input after character input from user

    def on_leave(self, *args):
        self.game_instance.reset_game()
        self.wrong_used_char_output.text = ""
        self.error_msg_output.text = ""


class MultiplayerGameScreen(Screen):
    word_list = []
    target_word = None
    # word_print = None
    guess_input = ObjectProperty()
    word_output = ObjectProperty()
    gu_left_output = ObjectProperty()
    wrong_used_char_output = ObjectProperty()
    game_instance = MainSinglegameClass()
    error_msg_output = ObjectProperty()

    def on_pre_enter(self, *args):
        pass

        # then a server thread is initialized


    def on_enter(self, *args):
        pass

    def run_game(self, gu_input):  # gets called when user presses "Submit" button.

        if self.game_instance.check_game_status() == -1:  # player has lost the game -> gameover
            self.gu_left_output.text = "No guesses left!"  # updates guesses left text shown
            self.error_msg_output.text = "GAME OVER! " + "The word was: " + self.target_word

        elif self.game_instance.check_game_status() == 0:  # no win yet!
            print(" MPIKA MPIKA MPIKA MPIKA !!!!!@@#")
            self.game_instance.set_user_guess(gu_input)  # passes user guess input to methods of game_instance
            self.word_output.text = self.game_instance.get_cur_word()  # updates word shown
            if self.game_instance.wrong_used_char:  # checks if list is empty so as not to print it
                self.wrong_used_char_output.text = "Wrong guesses: " + self.game_instance.get_wrong_used_char()  # updates GUI list of wrong char guesses
            self.gu_left_output.text = "You have " + self.game_instance.get_gu_left() + " guesses left"  # updates guesses left text shown
            if self.game_instance.get_input_valid_status() is True:
                pass
            else:
                self.error_msg_output.text = self.game_instance.get_input_error_msg()

            if self.game_instance.check_game_status() == 1:
                self.error_msg_output.text = "You have WON!"
                self.gu_left_output.text = ""

        self.guess_input.text = ""  # clears guess input after character input from user

    def on_leave(self, *args):
        self.game_instance.reset_game()
        self.wrong_used_char_output.text = ""
        self.error_msg_output.text = ""


class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")


class MainApp(App):
    def build(self):
        return presentation


if __name__ == "__main__":
    MainApp().run()

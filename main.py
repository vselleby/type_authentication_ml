from user_handler import UserHandler

if __name__ == "__main__":
    uh = UserHandler()
    cancel = False
    while not cancel:
        option = input("What would you like to do?\n"
                       "1: Authenticate user\n"
                       "2: Register new user\n"
                       "3: Exit\n")

        if option == str(1):
            uh.authenticate_user()
        elif option == str(2):
            uh.new_user()
        elif option == str(3):
            cancel = True
            break
        else:
            print("Select 1, 2 or 3")

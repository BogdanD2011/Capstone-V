# function bellow take the parameters from Capstone_V.py and try to validate the log in details
# it allow the user to input 7 times wrong log in details and after that it exit the program 
def log_in(user, password):
    user_match = 'admin' #change if need to change log in details
    password_match = 'Admin'
    user_try_count = 7 # counting log in attempts
    if user == user_match and password == password_match:
        return True
    else: #  Try to validate the log in details up to 7 times , else will exit the program 
        while user != user_match or password != password_match:
            print("Incorect user name or password! Try again!")
            user = input("User name: ").lower()
            password = input("Password: ")
            user_try_count -= 1
            if user_try_count == 0:
                break
        if user == user_match and password == password_match:
            return True 
        else: 
            print("To many attempts! Log in disabled!")
            return False      
                
       
        
            


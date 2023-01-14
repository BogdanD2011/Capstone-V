# importing libraries 
from log_in import log_in
import sqlite3
import os
import platform

# define clear screen function
def clear():
    sys = platform.uname()
    # for windows
    if sys[0] == 'Windows':
        os.system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')
# function bellow display diferent meniu depoend of which section 
# of code will required 
def display_menu(menu):
    clear()
    if menu == 1:
        print('''
   Main Menu
--------------
1. Enter book
2. Update book
3. Delete book
4. Search books
5. Display all books
0. Exit
            ''')
    elif menu == 2:
          print('''
    Which field would you like to update ?
    --------------------------------------
    1. Update ID
    2. Update Title
    3. Update Author
    4. Update Quantity
    5. Update All values
    0. Back to main menu
            ''')
    elif menu == 3:
          print('''
    By which field would you like to search ? 
    ----------------------------------------
    1. Search by ID
    2. Search by Title
    3. Search by Author
    4. Search by Quantity
    0. Back to main menu
            ''')

# function bellow take the menu selection input from user and validat it
# it take 2 paramater max_option depend of how many options are in the menu
# and menu is the display message which can be adjusted for each function call
def user_menu_selection(max_option, menu):

    while True:
        try:
            option_select = int(input(menu))
            while option_select < 0 or option_select > max_option:
                print(f"Please select one option from 1 to {max_option} !")
                option_select = int(input(menu))
            break
        except ValueError:
            print("Your selection need to ne an integer number!")
    return option_select

# function bellow add a new book to database or return exception if not posible
# field ID and title need to be unique 
def add_to_database(cursor, db):
    confirm = True
    while True:
        try: 
            id_input = int(input("Book ID: "))
            title_input = input("Book Title: ")
            author_input = input("Book Author: ")
            quantity_input = int(input("Book Quantity: "))
            break
        except ValueError:
            print(" Field ID and Quantity need to be integer value!")

    try:
       cursor.execute( ''' INSERT INTO books(id, title, author, quantity)
                            Values(?, ?, ?, ?)''', (
                                                id_input,
                                                title_input,
                                                author_input,
                                                quantity_input
                                                   )
                  )
       db.commit()
    except sqlite3.DatabaseError as e:
        print(e)
        confirm = False
        db.rollback()
    if confirm:
        print("Book entered successfuly! Press enter to continue!")
    else:
        print("The book has not be entered in to database! ")
    cont = input()

# this function allow to update a field in database
# it allow the user to search the book by title or by id and then offer
# different option to change one field or all for that record
def update_database(cursor, db):
    clear()
    indicator = False
    book_name = input("What book title would you like to update? or press 'i' to enter book id :")
    if book_name == 'i': # if user whant to locate the record by id
        try:
            book_id = int(input("Enter book id number: "))
        except ValueError:
            print("You need to enter an integer value!")
        indicator = True
    #this block display the located record with curent values 
    if indicator == False:
        cursor.execute('''SELECT * FROM books WHERE title=? COLLATE NOCASE''', [book_name])
    else:
        cursor.execute('''SELECT * FROM books WHERE id=?''',  [book_id])
    if len(cursor.fetchall()) == 0:
        print("No book with this criteria exits in database! \n")
        cont = input("Press enter to continue! ")
    else:
        try:
            display_menu(2)
            for row in cursor:
                print("Updating curent values:\n | book ID: ", row[0], " | book title: ", row[1], end='')
                print(" | book author: ", row[2], " | book quantity: ", row[3])
            menu_select = user_menu_selection(5, message)
            # this block below procees the option based on user selection
            if menu_select == 1:
                try:
                    up_id = int(input("Enter new ID: "))
                except ValueError:
                    print("You need to enter an integer value!")
                if indicator == False:
                    cursor.execute('''UPDATE books SET id=? WHERE title=? COLLATE NOCASE''', 
                                                        (up_id,       book_name)
                                    )
                else:
                    cursor.execute('''UPDATE books SET id=? WHERE id=?''', 
                                                        (up_id,       book_id)
                                    )
            elif menu_select == 2:
                up_title = input("Enter new book title: ")
                if indicator == False:
                        cursor.execute('''UPDATE books SET title=? WHERE title=? COLLATE NOCASE''', 
                                                        (up_title,       book_name)
                                    )
                else:
                        cursor.execute('''UPDATE books SET title=? WHERE id=?''', 
                                                        (up_title,       book_id)
                                    )
            elif menu_select == 3:
                up_author = input("Enter new book author: ")
                if indicator == False:
                        cursor.execute('''UPDATE books SET author=? WHERE title=? COLLATE NOCASE''', 
                                                        (up_author,       book_name)
                                    )
                else:
                        cursor.execute('''UPDATE books SET author=? WHERE id=?''', 
                                                        (up_author,       book_id)
                                    )
            elif menu_select == 4:
                try:
                    up_quantity = int(input("Enter new book quantity: "))
                except ValueError:
                    print("You need to enter an integer value!")
                if indicator == False:
                    cursor.execute('''UPDATE books SET quantity=? WHERE title=? COLLATE NOCASE''', 
                                                        (up_quantity,       book_name)
                                    )
                else:
                    cursor.execute('''UPDATE books SET quantity=? WHERE id=?''', 
                                                        (up_quantity,       book_id)
                                        )
            # this block bellow allow the user to change all fields of a record 
            elif menu_select == 5:
                    try:
                        up_id = int(input("Enter new ID: "))
                        up_title = input("Enter new book title: ")
                        up_author = input("Enter new book author: ")
                        up_quantity = int(input("Enter new book quantity: "))
                    except ValueError:
                        print("You need to enter an integer value in id and quantity field!")
                    if indicator == False:
                        cursor.execute('''UPDATE books SET id=?, title=?, author=?, quantity=? WHERE title=? COLLATE NOCASE''', 
                                        (up_id, up_title, up_author, up_quantity,       book_name)
                                    )
                    else:
                        cursor.execute('''UPDATE books SET id=?, title=?, author=?, quantity=? WHERE id=?''', 
                                        (up_id, up_title, up_author, up_quantity,      book_id)
                                    )
            cont = input("Sussecffully updated! Press enter to continue! ")
            db.commit()
        except sqlite3.DatabaseError as e:
            print(e)
            cont = input("Can not execute this update! Press enter to continue!")
            

#this function bellow allow user to delete a record from table
# it locate the bock by title or by id 
def delete_book(cursor, db):
    indicator = False
    book_name = input("What book title would you like to delete? or press 'i' to enter book id :")
    if book_name == 'i':
        book_id = int(input("Enter book id number: "))
        indicator = True
    if indicator == False:
        cursor.execute('''SELECT id, title, author, quantity FROM books WHERE title=? COLLATE NOCASE''', [book_name])
    else:
        cursor.execute('''SELECT id, title, author, quantity FROM books WHERE id=?''',[book_id])
    book =  cursor.fetchone()
    print(f"Are you sure you whant to delete {book}?")
    y_n = input("Y / N ?").lower()
    if y_n == 'y':
        if indicator == False:
            cursor.execute('''DELETE FROM books WHERE title=? COLLATE NOCASE''', [book_name])
        else:
            cursor.execute('''DELETE FROM books WHERE id=?''',[book_id])
        print("The book was successfuly deleted!")
    
    db.commit()
    display_menu(1)

# this function bellow alow the user to search for a book by one of the chosen fields 
def search_book(cursor, db):
    display_menu(3)
    menu_select = user_menu_selection(4, message)
    if menu_select == 1:
        search_id = int(input("Enter book id: "))
        cursor.execute('''SELECT * FROM books WHERE id=?''', [search_id])
        book = cursor.fetchone()
        print(book)
    elif menu_select == 2:
        search_title = input("Enter book title: ")
        cursor.execute('''SELECT * FROM books WHERE title=? COLLATE NOCASE''', [search_title])
        book = cursor.fetchone()
        print(book)
    elif menu_select == 3:
        search_author = input("Enter book author: ")
        cursor.execute('''SELECT * FROM books WHERE author=? COLLATE NOCASE''', [search_author])
        book = cursor.fetchone()
        print(book)
    elif menu_select == 4:
        search_quantity = int(input("Enter book current quantity: "))
        cursor.execute('''SELECT * FROM books WHERE quantity=?''', [search_quantity])
        book = cursor.fetchone()
        print(book)
    else:
        display_menu(1)
    cont = input("\n Press enter to go back to main menu!  ")

#this function bellow display all data from the table in a friendly format 
def display_all(cursor, db):
    cursor.execute('''SELECT id, title, author, quantity  FROM books ''')
    print("-" * 130)
    print("  ID   ", end='   ')
    print(" "*33, "Title", " "*33, end='   ') 
    print(" "*12, "Author "," "*12, end='   ')
    print("Quantity")
    for row in cursor:
        tab1 = round(2 - (len(str(row[0])))/2) 
        tab2 = round(35 - (len(row[1])) / 2)
        tab3 = round(15 - (len(row[2])) / 2)
        tab4 = round(4 - round(len(str(row[3])))/2) 
        print("-"*6,"+","-"*72, "+", "-"*32, "+", "-"*10, "+")
        print(" "*int(tab1), row[0], " "*int(tab1), end='   ')
        print(" "*int(tab2), row[1], " "*int(tab2), end='   ') 
        print(" "*int(tab3), row[2], " "*int(tab3), end='   ') 
        print(" "*int(tab4), row[3], " "*int(tab4))  
    
    cont = input("\n Press enter to go back to main menu!  ")
    display_menu(1)

# ============================= main  block ==================================
 # this is the message displayed when user is asked to enter selection from menu 
message = 'Select option and press enter:  '

clear() #clear display screen 
print('''
************************************************************
Welcom to your book store! Please enter your log in details! 
************************************************************\n''')
# asking for log in details 
user_input = input("User name: ").lower()
password_input = input("Password: ")

# function log_in is located in log_in.py file. It validate the log in details 
# in maximum of 7 attempts - please open log_in.py to see comments 
log_in_validator = log_in(user_input, password_input)

if log_in_validator :
    try:
        # connect to database or create if not exist
        db = sqlite3.connect('bookstore')
        # set cursor 
        cursor=db.cursor()
        print("Connected to book store database! \n")
        #create tabel if not exist
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS books(   id INTEGER PRIMARY KEY UNIQUE, 
                                                    title TEXT UNIQUE,
                                                    author TEXT,
                                                    quantity INTEGER
                                                )
                        ''')
        db.commit()
        # navigating through main menu - each option call a function 
        menu_selection = -1
        while menu_selection !=0:
            display_menu(1)
            menu_selection = user_menu_selection(5, message)
            if menu_selection == 1:
                add_to_database(cursor, db)
            elif menu_selection == 2:
                update_database(cursor, db)
            elif menu_selection == 3:
                delete_book(cursor, db)
            elif menu_selection == 4:
                search_book(cursor, db)
            elif menu_selection == 5:
                display_all(cursor, db)
            elif menu_selection == 0:
                exit()
    except sqlite3.DatabaseError as e: # return error if connection not possible
        print(e)
    finally:
        db.close()
# exit program if was over 7 log in attempts
else:
    print("Database will be disabled. Please restart the program !")
    exit()



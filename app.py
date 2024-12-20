import sqlite3
import os
import time
from tabulate import tabulate
import logging


logging.basicConfig(filename='library.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_name = 'Library.db'
password = 'admin1'

def pause(n):
    time.sleep(n)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class LibraryManager:
    def __init__(self):
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS books
                         (name TEXT NOT NULL,
                         author TEXT NOT NULL,
                         status TEXT DEFAULT "avaible")''')
        self.db.commit()
    


    def check_book(self,name=None):
        if not name:
            print("Error - Invalid Syntax : (Empty Syntax)")
            pause(2)
            clear()
            return
        self.cur.execute('SELECT name FROM books')
        names = [name[0] for name in self.cur.fetchall()]
        if name in names:
            return 0
        else:
            return 1



    def add_book(self,name=None,author=None):
        if not name and not author:
            print("Enter A Valid Name / Author !")
            pause(2)
            clear()
            return
        if self.check_book(name):
            print("Book Is Already Exists !")
            pause(2)
            clear()
            return
        try:
            self.db.execute("INSERT INTO books VALUES(?,?)",(name,author))
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            logging.error(f"Error while Adding Book '{name}' : {e}")
            print(f"Connot Adding Book - Error : {e}")
            pause(2)
            clear()
        else:
            logging.info(f"Book '{name}' Added To {db_name}")
            print(f"Book With Name '{name}' Added Successfuly !")
            pause(2)
            clear()
    


    def remove_book(self,name=None):
        if not name:
            print("Enter A Valid Name !")
            pause(2)
            clear()
            return
        if self.check_book(name):
            self.cur.execute("DELETE FROM books WHERE name=?",(name,))
        else:
            print(f"Book With Name {name} Not Found !")
            pause(2)
            clear()
        try:
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            logging.error(f"Error while Removing Book '{name}' : {e}")
            print(f"Connot Remove Book - Error : {e}")
            pause(2)
            clear()
        else:
            logging.info(f"Book '{name}' Removed From {db_name}")
            print(f"Book With Name '{name}' Removed Successfuly !")
            pause(2)
            clear()



    def update_book(self,name=None,name1=None,author=None):
        if not name:
            print("Invalid Syntax : (Empty Syntax)")
            pause(2)
            clear()
            return
        if not self.check_book(name):
            print(f"Book With Name {name} Not Found !")
            pause(2)
            clear()
            return
        row = self.cur.execute('SELECT * FROM books WHERE name=?',(name,)).fetchall()
        name0 = row[0][0]
        author0 = row[0][1]
        if not name1:
            name1 = name0
        if not author:
            author = author0
        self.cur.execute("UPDATE books SET name=?, author=? WHERE name=?",(name1,author,name))
        try:
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            logging.error(f"Error while Updating Book '{name}' : {e}")
            print(f"Connot Updating Book - Error : {e}")
            pause(2)
            clear()
        else:
            logging.info(f"Book '{name}' Updated To {name1}")
            print(f"Book With Name '{name}' Updated Successfuly !")
            pause(2)
            clear()



    def find_book(self,name=None):
        if not name:
            print("Error - Invalid Syntax : (Empty Syntax) !")
            pause(2)
            clear()
            return
        if not self.check_book(name):
            print(f"Book With Name '{name}' Not Found In Our Library !")
            return
        print("Book Found !")
        self.headers = ["NAME","AUTHOR","STATUS"]
        self.row = self.cur.execute('SELECT * FROM books WHERE name=?',(name,)).fetchall()
        print(tabulate(self.row, headers=self.headers, tablefmt='grid'))
    


    def view_books(self):
        self.headers = ["NAME","AUTHOR","STATUS"]
        rows = self.cur.execute("SELECT * FROM books")
        print(tabulate(rows, headers=self.headers, tablefmt='grid'))
    


    def borrow(self,name=None):
        if not name:
            print("Error - Invalid Syntax : (Empty Syntax)")
            pause(2)
            clear()
            return
        if not self.check_book(name):
            print(f"Book With Name {name} Not Found In Our Library!")
            pause(2)
            clear()
            return
        self.cur.execute('UPDATE books SET status="unavaible" WHERE name=?',(name,))
        try:
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            logging.error(f"Error while Borrowing Book '{name}' : {e}")
            print(f"Connot Borrowing Book - Error : {e}")
            pause(2)
            clear()
        else:
            logging.info(f"Book '{name}' Marked As unavaible")
            print(f"Book With Name '{name}' Marked As Unavaible")
            pause(2)
            clear()



    def return_book(self,name=None):
        if not name:
            print("Invalid Syntax : (Empty Syntax)")
            pause(2)
            clear()
            return
        if not self.check_book(name):
            print("Book Not Found !")
            pause(2)
            clear()
            return
        self.cur.execute('UPDATE books SET status="avaible" WHERE name=?',(name,))
        try:
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            logging.error(f"Error while Returning Book '{name}' : {e}")
            print(f"Connot Borrowing Book - Error : {e}")
            pause(2)
            clear()
        else:
            logging.info(f"Book '{name}' Marked As avaible")
            print("Book Marked As Avaible !")
            pause(2)
            clear()
    


    def MainMenu(self):
        
        first_time = True
        logged = False
        while True:
            if not logged:
                login = input(f"Enter The Admin Panel Password : ")
                if login == password:
                    print("Password Correct !")
                    pause(1.5)
                    clear()
                else:
                    print("Password Incorrect !")
                    pause(2)
                    clear()
                    continue
            logged = True
            if first_time:
                print(f"Welcome {login} To Our Digital Library Admin Panel")
            print("1. Add Book")
            pause(0.5)
            print("2. Remove Book")
            pause(0.5)
            print("3. Update Book")
            pause(0.5)
            print("4. Find Book")
            pause(0.5)
            print("5. View All Books")
            pause(0.5)
            print("6. Borrow Book")
            pause(0.5)
            print("7. Return Book")
            pause(0.5)
            print("8. Exit")
            pause(0.5)

            try:
                option = int(input("Choose An option From Above (1-7): "))
            except ValueError:
                print("Enter A Valid Number !")
                pause(2)
                clear()
                continue
            if option == 1:
                print("============ ADD BOOK ============")
                name = input("Enter The Book Name : ")
                author = input("Enter The Book Author : ")
                self.add_book(name,author)
            elif option == 2:
                print("============ REMOVE BOOK ============")
                name = input("Enter The Book Name To Delete: ")
                self.remove_book(name)
            elif option == 3:
                print("============ UPDATE BOOK ============")
                name = input("Enter The Name Of The Book To Update")
                if self.check_book(name):
                    name1 = input("Enter The New Book Name (keep it empty for no change): ")
                    author = input("Enter The New Book Author (keep it empty for no change): ")
                    self.update_book(name,name1,author)
            elif option == 4:
                print("============ FIND BOOK ============")
                name = input("Enter The nma Of The Book To Search : ")
                self.find_book(name)
            elif option == 5:
                print("============ ALL BOOKS ============")
                self.view_books()
            elif option == 6:
                print("============ BORROW BOOK ============")
                name = input("Enter The Name Of The Book To Borrow : ")
                self.borrow(name)
            elif option == 7:
                print("============ RETURN BOOK ============")
                name = input("Enter The Name Of The Book To Return")
                self.return_book(name)
            elif option == 8:
                print("Closing Program ...")
                pause(3)
                clear()
                break
            first_time = False
    

    def __del__(self):
        if self.db:
            self.db.close()
            logging.info("Database Connection Closed.")

if __name__ == '__main__':
    Library = LibraryManager()
    Library.MainMenu()
class library():
    def __init__(self):
        self.book = ['java', 'python', 'philosophy', 'rework', 'atomic habits']

    def add_book(self, book_name=None):
        if book_name is None:
            book_name = input('Enter the name of the book you want to add: ')
        self.book.append(book_name)

    def borrow_book(self, borrow_book = None):
        if borrow_book is None:
            borrow_book = input('Enter the name of the book you want to borrow: ')
            if borrow_book in self.book:
                print(f'You have successfully borrowed the {borrow_book}. Enjoy reading!')
                self.book.remove(borrow_book)
            else:
                print('Sorry! This book is not available in our library.')

    def return_book(self, return_book = None):
        if return_book is None:
            return_book = input('Enter the name of the book you want to return: ')
            self.book.append(return_book)
            print('Thanks for returning the book. Hope you enjoyed reading it!')
        
    def display_book(self):
        print('The availablle books in our library are: ')
        for book in self.book:
            print(f"-> {book}")



def main():
        while True:
            print('''
Welcome to the Library Management System!
Please choose an option:
1. Add Book                     
2. Borrow Book
3. Return Book
4. Display Available Books  
5. Exit
                  ''')
            
            choice = input('Enter your choice (1-5): ')

            lib = library()
            if choice == '1':
                lib.add_book()
            elif choice == '2':
                lib.borrow_book()
            elif choice == '3':
                lib.return_book()
            elif choice == '4':
                lib.display_book()
            elif choice == '5':
                print('Thank you for using the Library Management System. Goodbye!')
                break
            else:
                print('Invalid choice! Please enter a number between 1 and 5.')

        
if __name__ == "__main__":
    main()


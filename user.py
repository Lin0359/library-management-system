from models.book import Book

class Person:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password

class User(Person):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.borrowed_books = []

    def borrow(self, book: Book):
        if book.copies - book.borrowed > 0:
            self.borrowed_books.append(book.book_id)
            book.borrowed += 1
            return True
        return False

    def return_book(self, book: Book):
        if book.book_id in self.borrowed_books:
            self.borrowed_books.remove(book.book_id)
            book.borrowed -= 1
            return True
        return False

    def report_damage(self, book: Book, message: str):
        book.damage_reports.append(f"{self.name} reports: {message}")

class Admin(Person):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)

    def add_book(self, books_dict, book: Book):
        books_dict[book.book_id] = book

    def remove_book(self, books_dict, book_id):
        if book_id in books_dict:
            del books_dict[book_id]

    def view_users(self, users_data):
        print("\nRegistered Users and Their Borrowed Books:")
        for uid, info in users_data.items():
            if info["role"] == "user":
                print(f"{uid} - {info['name']} | Borrowed: {info.get('borrowed_books', [])}")

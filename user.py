"""User roles and library actions."""

from book import Book


class Person:
    def __init__(self, user_id: str, name: str, password: str = ""):
        self.user_id = user_id
        self.name = name
        # Authentication hashes are stored by the application, not this domain model.
        self.password = password


class User(Person):
    def __init__(self, user_id: str, name: str, password: str = ""):
        super().__init__(user_id, name, password)
        self.borrowed_books = []

    def borrow(self, book: Book) -> bool:
        if book.available_copies < 1 or book.book_id in self.borrowed_books:
            return False
        self.borrowed_books.append(book.book_id)
        book.borrowed += 1
        return True

    def return_book(self, book: Book) -> bool:
        if book.book_id not in self.borrowed_books or book.borrowed < 1:
            return False
        self.borrowed_books.remove(book.book_id)
        book.borrowed -= 1
        return True

    def report_damage(self, book: Book, message: str) -> bool:
        message = message.strip()
        if not message:
            return False
        book.damage_reports.append(f"{self.name}: {message}")
        return True


class Admin(Person):
    def add_book(self, books_dict: dict, book: Book) -> bool:
        if book.book_id in books_dict:
            return False
        books_dict[book.book_id] = book
        return True

    def remove_book(self, books_dict: dict, book_id: str) -> bool:
        book = books_dict.get(book_id)
        if book is None or book.borrowed:
            return False
        del books_dict[book_id]
        return True

    def view_users(self, users_data: dict) -> None:
        print("\nRegistered customers and borrowed books:")
        for user_id, info in users_data.items():
            if info.get("role") == "user":
                borrowed = info.get("borrowed_books", [])
                name = info.get("name", "(no name)")
                print(user_id + " - " + name + " | Borrowed: " + str(borrowed))

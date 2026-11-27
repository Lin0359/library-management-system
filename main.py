"""Command-line entry point for the library management system."""

import hashlib
import hmac
import secrets

from book import Book
from data_handler import load_books, load_users, log_damage, save_books, save_users
from user import Admin, User


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, expected = stored.split("$", 1)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000)
        return hmac.compare_digest(digest.hex(), expected)
    except (ValueError, TypeError):
        return False


def create_account(users: dict, role: str) -> bool:
    user_id = input("Choose a user ID: ").strip()
    if not user_id or user_id in users:
        print("Enter a non-empty, unused user ID.")
        return False
    name = input("Name: ").strip()
    password = input("Set a password (at least 8 characters): ")
    if not name or len(password) < 8:
        print("Name is required and the password must have at least 8 characters.")
        return False
    users[user_id] = {
        "user_id": user_id,
        "name": name,
        "password_hash": hash_password(password),
        "role": role,
        "borrowed_books": [],
    }
    save_users(users)
    print(f"{role.title()} account created.")
    return True


def main() -> None:
    books = load_books()
    users = load_users()

    # Create the first staff account on first launch.
    while not any(info.get("role") == "admin" for info in users.values()):
        print("First launch: create the initial staff account.")
        create_account(users, "admin")

    print("\nWelcome to the Library Management System")
    while True:
        print("\n1. Log in\n2. Register as a customer\n0. Exit")
        choice = input(">> ").strip()
        if choice == "0":
            return
        if choice == "2":
            create_account(users, "user")
            continue
        if choice != "1":
            print("Choose a listed option.")
            continue

        user_id = input("User ID: ").strip()
        password = input("Password: ")
        record = users.get(user_id)
        if not record or not verify_password(password, record.get("password_hash", "")):
            print("Invalid user ID or password.")
            continue

        is_admin = record.get("role") == "admin"
        user = Admin(user_id, record["name"], password) if is_admin else User(user_id, record["name"], password)
        user.borrowed_books = record.get("borrowed_books", [])

        while True:
            print("\n1. View catalog")
            print("2. Add book\n3. Remove book\n4. View customer borrowing status" if is_admin else "2. Borrow a book\n3. Return a book\n4. Report damage")
            print("0. Log out")
            action = input(">> ").strip()
            if action == "0":
                save_books(books)
                break
            if action == "1":
                if not books:
                    print("The catalog is empty.")
                for book in books.values():
                    print(f"{book.book_id}: {book.title} — {book.available_copies}/{book.copies} available")
            elif action == "2" and is_admin:
                book_id = input("Book ID: ").strip()
                if not book_id or book_id in books:
                    print("Enter a new, non-empty book ID.")
                    continue
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                year = input("Year: ").strip()
                category = input("Category: ").strip()
                try:
                    copies = int(input("Number of copies: "))
                    if copies < 1:
                        raise ValueError
                    books[book_id] = Book(book_id, title, author, year, category, copies)
                    save_books(books)
                    print("Book added.")
                except ValueError:
                    print("Copies must be a positive whole number.")
            elif action == "3" and is_admin:
                book_id = input("Book ID to remove: ").strip()
                book = books.get(book_id)
                if not book:
                    print("Book not found.")
                elif not Admin.remove_book(user, books, book_id):
                    print("Return all borrowed copies before removing this title.")
                else:
                    save_books(books)
                    print("Book removed.")
            elif action == "4" and is_admin:
                for customer_id, info in users.items():
                    if info.get("role") == "user":
                        name = info.get("name", "(no name)")
                        borrowed = info.get("borrowed_books", [])
                        print(customer_id + " — " + name + " | Borrowed: " + str(borrowed))
            elif action == "2" and not is_admin:
                book = books.get(input("Book ID to borrow: ").strip())
                if book and user.borrow(book):
                    record["borrowed_books"] = user.borrowed_books
                    save_users(users)
                    save_books(books)
                    print("Book borrowed.")
                else:
                    print("Borrow failed. Check the ID, availability, and your current loans.")
            elif action == "3" and not is_admin:
                book = books.get(input("Book ID to return: ").strip())
                if book and user.return_book(book):
                    record["borrowed_books"] = user.borrowed_books
                    save_users(users)
                    save_books(books)
                    print("Book returned.")
                else:
                    print("That book is not in your account.")
            elif action == "4" and not is_admin:
                book_id = input("Book ID: ").strip()
                message = input("Describe the damage: ").strip()
                book = books.get(book_id)
                if book and user.report_damage(book, message):
                    log_damage(f"{user.name} reported damage to {book_id}: {message}")
                    save_books(books)
                    print("Damage report recorded.")
                else:
                    print("Enter an existing book ID and a description.")
            else:
                print("Choose an available option.")


if __name__ == "__main__":
    main()

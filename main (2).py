from models.book import Book
from models.user import User, Admin
from storage.data_handler import load_books, save_books, log_damage, load_users, save_users

books = load_books()
users_data = load_users()

# log in and register
print("Welcome to the Library System!")
while True:
    print("\n1. Login\n2. Register as User\n0. Exit")
    choice = input(">> ")

    if choice == "1":
        uid = input("Enter your user ID: ")
        pwd = input("Enter your password: ")
        if uid in users_data and users_data[uid]['password'] == pwd:
            name = users_data[uid]['name']
            role = users_data[uid]['role']
            if role == "admin":
                user = Admin(uid, name, pwd)
                is_admin = True
            else:
                user = User(uid, name, pwd)
                user.borrowed_books = users_data[uid].get("borrowed_books", [])
                is_admin = False
            break
        else:
            print("Invalid ID or password.")

    elif choice == "2":
        uid = input("Choose a user ID: ")
        if uid in users_data:
            print("User ID already exists.")
            continue
        name = input("Enter your name: ")
        pwd = input("Set your password: ")
        users_data[uid] = {"user_id": uid, "name": name, "password": pwd, "role": "user", "borrowed_books": []}
        save_users(users_data)
        print("User registered successfully. Please log in.")

    elif choice == "0":
        exit()

# main system
while True:
    print("\nSelect an option:")
    print("1. View all books")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Report book damage")
    if is_admin:
        print("5. Add book\n6. Remove book\n7. Register new Admin\n8. View Users")
    print("0. Exit")

    choice = input(">> ")
    if choice == "1":
        for b in books.values():
            print(f"{b.book_id}: {b.title} ({b.borrowed}/{b.copies} borrowed)")
    elif choice == "2" and not is_admin:
        bid = input("Enter book ID: ")
        if bid in books and user.borrow(books[bid]):
            print("Book borrowed successfully!")
            user.borrowed_books.append(bid)
            users_data[user.user_id]["borrowed_books"] = user.borrowed_books
            save_users(users_data)
        else:
            print("Borrow failed. Book may be unavailable.")
    elif choice == "3" and not is_admin:
        bid = input("Enter book ID to return: ")
        if bid in books and user.return_book(books[bid]):
            print("Returned successfully.")
            user.borrowed_books.remove(bid)
            users_data[user.user_id]["borrowed_books"] = user.borrowed_books
            save_users(users_data)
        else:
            print("Return failed.")
    elif choice == "4" and not is_admin:
        bid = input("Book ID: ")
        msg = input("Damage description: ")
        if bid in books:
            user.report_damage(books[bid], msg)
            log_damage(f"{user.name} reported on {bid}: {msg}")
            print("Damage reported.")
    elif choice == "5" and is_admin:
        bid = input("New book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        year = input("Year: ")
        cat = input("Category: ")
        copies = int(input("Copies: "))
        new_book = Book(bid, title, author, year, cat, copies)
        user.add_book(books, new_book)
        print("Book added.")
    elif choice == "6" and is_admin:
        bid = input("Enter book ID to remove: ")
        user.remove_book(books, bid)
        print("Book removed.")
    elif choice == "7" and is_admin:
        uid = input("New admin ID: ")
        if uid in users_data:
            print("ID already exists.")
            continue
        name = input("Name: ")
        pwd = input("Password: ")
        users_data[uid] = {"user_id": uid, "name": name, "password": pwd, "role": "admin"}
        save_users(users_data)
        print("New admin registered.")
    elif choice == "8" and is_admin:
        user.view_users(users_data)
    elif choice == "0":
        break
    else:
        print("Invalid choice.")

save_books(books)
print("Session ended.")

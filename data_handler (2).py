import os
import json
from models.book import Book

DATA_FOLDER = "data"

def load_books():
    path = os.path.join(DATA_FOLDER, "books.json")
    if not os.path.exists(path): return {}
    with open(path, 'r') as f:
        data = json.load(f)
    return {bid: Book.from_dict(bdict) for bid, bdict in data.items()}

def save_books(books):
    path = os.path.join(DATA_FOLDER, "books.json")
    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(path, 'w') as f:
        json.dump({bid: b.to_dict() for bid, b in books.items()}, f, indent=2)

def log_damage(message):
    path = os.path.join(DATA_FOLDER, "logs.txt")
    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(path, 'a') as f:
        f.write(message + "\n")

def load_users():
    path = os.path.join(DATA_FOLDER, "users.json")
    if not os.path.exists(path): return {}
    with open(path, 'r') as f:
        return json.load(f)

def save_users(users):
    path = os.path.join(DATA_FOLDER, "users.json")
    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(users, f, indent=2)
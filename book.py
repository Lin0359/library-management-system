import json

class Book:
    def __init__(self, book_id, title, author, year, category, copies=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.copies = copies
        self.borrowed = 0
        self.damage_reports = []

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "category": self.category,
            "copies": self.copies,
            "borrowed": self.borrowed,
            "damage_reports": self.damage_reports
        }

    @staticmethod
    def from_dict(data):
        book = Book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            category=data["category"],
            copies=data["copies"]
        )
        book.borrowed = data.get("borrowed", 0)
        book.damage_reports = data.get("damage_reports", [])
        return book
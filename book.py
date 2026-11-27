"""Book inventory model."""


class Book:
    def __init__(self, book_id, title, author, year, category, copies=1):
        if copies < 0:
            raise ValueError("copies cannot be negative")
        self.book_id = str(book_id)
        self.title = str(title)
        self.author = str(author)
        self.year = str(year)
        self.category = str(category)
        self.copies = int(copies)
        self.borrowed = 0
        self.damage_reports = []

    @property
    def available_copies(self):
        return self.copies - self.borrowed

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "category": self.category,
            "copies": self.copies,
            "borrowed": self.borrowed,
            "damage_reports": self.damage_reports,
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            category=data["category"],
            copies=int(data["copies"]),
        )
        book.borrowed = int(data.get("borrowed", 0))
        book.damage_reports = list(data.get("damage_reports", []))
        if not 0 <= book.borrowed <= book.copies:
            raise ValueError(f"Invalid inventory count for book {book.book_id}")
        return book

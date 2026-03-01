import pytest
from models.book import Book
from models.user import User

def test_borrow_and_return():
    user = User("u002", "Bob")
    book = Book("b100", "Python", "Author", "2020", "Tech", 2)
    assert user.borrow(book) == True
    assert book.borrowed == 1
    assert user.return_book(book) == True
    assert book.borrowed == 0

def test_fail_borrow():
    user = User("u003", "Charlie")
    book = Book("b200", "Unavailable", "Author", "2019", "Drama", 0)
    assert user.borrow(book) == False


def test_report_damage():
    user = User("u004", "Dora")
    book = Book("b300", "Broken Book", "Author", "2018", "Mystery", 1)
    user.report_damage(book, "Pages torn")
    assert len(book.damage_reports) == 1
    assert "Pages torn" in book.damage_reports[0]
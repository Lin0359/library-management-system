"""Tests for book inventory and borrowing behavior."""

from book import Book
from user import User


def test_borrow_and_return():
    user = User("u002", "Bob")
    book = Book("b100", "Python", "Author", "2020", "Tech", 2)
    assert user.borrow(book)
    assert book.borrowed == 1
    assert book.available_copies == 1
    assert user.return_book(book)
    assert book.borrowed == 0
    assert book.available_copies == 2


def test_customer_cannot_borrow_unavailable_book():
    user = User("u003", "Charlie")
    book = Book("b200", "Unavailable", "Author", "2019", "Drama", 0)
    assert not user.borrow(book)


def test_customer_cannot_borrow_same_book_twice():
    user = User("u004", "Dora")
    book = Book("b300", "Limited", "Author", "2018", "Mystery", 1)
    assert user.borrow(book)
    assert not user.borrow(book)
    assert book.borrowed == 1


def test_damage_report_is_saved_on_book():
    user = User("u005", "Evan")
    book = Book("b400", "Broken Book", "Author", "2018", "Mystery", 1)
    assert user.report_damage(book, "Pages torn")
    assert len(book.damage_reports) == 1
    assert "Pages torn" in book.damage_reports[0]
    assert not user.report_damage(book, "   ")

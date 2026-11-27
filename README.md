# Library Management System

A Python command-line application for managing a small library catalog, customer loans, staff accounts, and damage reports. This began as a Spring 2025 course final project and has been organized into a runnable, documented repository.

## Features

- Staff can add or remove titles and review customer borrowing status.
- Customers can borrow and return books, and submit damage reports.
- Inventory availability is checked before a loan is recorded.
- The first launch guides the operator through creating the initial staff account.
- Account passwords are stored as salted PBKDF2-HMAC-SHA256 hashes.
- Catalog and account records are saved as local JSON files.

## Run locally

Requires Python 3.9 or later. The application has no third-party runtime dependencies.

```bash
python main.py
```

On first launch, create an initial staff account. After signing in, staff can add books; customers can register from the welcome menu. The application creates its `data/` directory and JSON files as needed.

## Project structure

- `main.py`: command-line menus and account sign-in
- `book.py`: book inventory model
- `user.py`: customer and staff actions
- `data_handler.py`: local JSON persistence and damage-report logging
- `test_system.py`: tests for borrowing, availability, duplicate loans, and damage reports

Run the tests with `python -m pytest` after installing pytest.

## Data and scope

This is a local educational project. It uses JSON files rather than a database, has no network service or multi-user concurrency, and should not be treated as production library software. User records are stored on the machine running the application.

## Original project context

Created by Lin Han for a Spring 2025 course project. The repository cleanup focuses on making the existing CLI easier to understand and run while preserving its original scope.

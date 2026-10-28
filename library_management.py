"""
SMART LIBRARY MANAGEMENT SYSTEM
Python Programming (IBM) - Unit 2 Mini Project
Topics: Lists, Dictionaries, Sets, Tuples, Functions, JSON file handling
Run: python library_management.py
"""

import json
import os
from datetime import datetime

DATA_FILE = "library_data.json"

# List of dictionaries: each dictionary represents one book.
books = []
# Set gives fast duplicate-ID checking.
book_ids = set()
# List of dictionaries stores issue transactions.
transactions = []


def load_data():
    """Load saved book and transaction data from JSON."""
    global books, book_ids, transactions
    if not os.path.exists(DATA_FILE):
        books, transactions = [], []
        book_ids = set()
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        books = data.get("books", [])
        transactions = data.get("transactions", [])
        book_ids = {book["book_id"] for book in books}
    except (json.JSONDecodeError, OSError, TypeError):
        print("Warning: Saved data could not be read. Starting with empty records.")
        books, transactions, book_ids = [], [], set()


def save_data():
    """Save current records so they remain available next time."""
    data = {"books": books, "transactions": transactions}
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def find_book(book_id):
    """Return a book dictionary by ID, or None if it does not exist."""
    for book in books:
        if book["book_id"].casefold() == book_id.strip().casefold():
            return book
    return None


def add_book():
    print("\n--- Add Book ---")
    book_id = input("Book ID: ").strip()
    if not book_id:
        print("Book ID cannot be empty.")
        return
    if book_id.casefold() in {item.casefold() for item in book_ids}:
        print("This Book ID already exists.")
        return

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    category = input("Category: ").strip() or "General"
    if not title or not author:
        print("Title and author cannot be empty.")
        return
    try:
        copies = int(input("Total copies: ").strip())
        if copies < 1:
            print("Copies must be at least 1.")
            return
    except ValueError:
        print("Please enter a whole number for copies.")
        return

    # Tuple stores the fixed descriptive fields for this book.
    book_details = (book_id, title, author, category)
    new_book = {
        "book_id": book_details[0],
        "title": book_details[1],
        "author": book_details[2],
        "category": book_details[3],
        "total_copies": copies,
        "available_copies": copies,
    }
    books.append(new_book)
    book_ids.add(book_id)
    save_data()
    print(f"Book '{title}' added successfully.")


def display_books():
    print("\n--- All Books ---")
    if not books:
        print("No books found.")
        return
    print(f"{'ID':<10} {'TITLE':<25} {'AUTHOR':<20} {'CATEGORY':<15} {'TOTAL':>5} {'AVAILABLE':>9}")
    print("-" * 88)
    for book in books:
        print(f"{book['book_id']:<10} {book['title'][:24]:<25} "
              f"{book['author'][:19]:<20} {book['category'][:14]:<15} "
              f"{book['total_copies']:>5} {book['available_copies']:>9}")


def search_book():
    keyword = input("Enter Book ID, title, author, or category: ").strip().casefold()
    if not keyword:
        print("Search text cannot be empty.")
        return
    matches = [
        book for book in books
        if keyword in book["book_id"].casefold()
        or keyword in book["title"].casefold()
        or keyword in book["author"].casefold()
        or keyword in book["category"].casefold()
    ]
    if not matches:
        print("No matching book found.")
        return
    for book in matches:
        print(f"\nID: {book['book_id']} | Title: {book['title']} | Author: {book['author']}")
        print(f"Category: {book['category']} | Available: {book['available_copies']}/{book['total_copies']}")


def issue_book():
    book_id = input("Book ID to issue: ").strip()
    book = find_book(book_id)
    if book is None:
        print("Book ID not found.")
        return
    if book["available_copies"] <= 0:
        print("This book is currently out of stock.")
        return
    student = input("Student name: ").strip()
    if not student:
        print("Student name cannot be empty.")
        return

    book["available_copies"] -= 1
    # Transaction is a dictionary; date/time is saved for the record.
    transactions.append({
        "book_id": book["book_id"],
        "student": student,
        "action": "ISSUED",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    save_data()
    print(f"'{book['title']}' issued to {student}. Copies left: {book['available_copies']}.")


def return_book():
    book_id = input("Book ID to return: ").strip()
    book = find_book(book_id)
    if book is None:
        print("Book ID not found.")
        return
    if book["available_copies"] >= book["total_copies"]:
        print("All copies are already in the library; no return is pending.")
        return

    student = input("Student name returning the book: ").strip()
    if not student:
        print("Student name cannot be empty.")
        return
    book["available_copies"] += 1
    transactions.append({
        "book_id": book["book_id"],
        "student": student,
        "action": "RETURNED",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    save_data()
    print(f"'{book['title']}' returned. Copies available: {book['available_copies']}.")


def show_categories():
    # Set stores unique category names.
    categories = {book["category"] for book in books}
    if not categories:
        print("No categories available yet.")
        return
    print("\nUnique categories:")
    for category in sorted(categories, key=str.casefold):
        print("-", category)


def show_transactions():
    print("\n--- Recent Transactions ---")
    if not transactions:
        print("No transactions recorded.")
        return
    for record in transactions[-20:]:
        # A tuple is used for a compact, fixed display record.
        row = (record["timestamp"], record["action"], record["book_id"], record["student"])
        print(f"{row[0]} | {row[1]:<8} | Book: {row[2]} | Student: {row[3]}")


def main():
    load_data()
    while True:
        print("\n========== SMART LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Add book")
        print("2. Display all books")
        print("3. Search book")
        print("4. Issue book")
        print("5. Return book")
        print("6. Show unique categories")
        print("7. Show recent transactions")
        print("8. Exit")
        choice = input("Choose (1-8): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            show_categories()
        elif choice == "7":
            show_transactions()
        elif choice == "8":
            save_data()
            print("Data saved. Thank you for using the Library Management System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()

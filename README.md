# Smart Library Management System
## Python Programming (IBM) — Unit 2 Mini Project

### Objective
Build a simple console-based library application using Python advanced data structures and file handling.

### Features
- Add books with unique IDs and validate input.
- Display all books and available copy counts.
- Search by book ID, title, author, or category.
- Issue books to students and prevent issuing when stock is zero.
- Return books and prevent the available count exceeding total copies.
- Display unique categories using a set.
- Store transaction history.
- Save and load records using a JSON file.

### Data structures used
- **List:** stores the book records and transactions.
- **Dictionary:** stores each book and each transaction as key-value pairs.
- **Set:** tracks unique Book IDs and unique categories.
- **Tuple:** stores fixed book details and fixed transaction display fields.

### Files
- `library_management.py` — complete Python source code.
- `library_data.json` — created automatically after saving data.
- `Project_Report.docx` — project report and test cases.

### How to run
1. Install Python 3.
2. Open a terminal in this folder.
3. Run: `python library_management.py`
4. Choose an option from the menu and follow the prompts.

On an Android phone, you can run the code in a Python app that supports Python 3, or use an online Python IDE. For GitHub, upload the `.py`, `README.md`, and report file.

### Sample test cases
| Test | Input/action | Expected result |
|---|---|---|
| Add book | ID B101, Python Basics, Author A, 2 copies | Book is added |
| Duplicate ID | Add B101 again | Duplicate ID is rejected |
| Search | Search `Python` | Matching title is displayed |
| Issue | Issue B101 when 2 copies are available | Available copies becomes 1 |
| Issue out of stock | Issue until available copies become 0 | Further issue is blocked |
| Return | Return an issued copy | Available count increases by 1 |
| Invalid copies | Enter `abc` for copies | Error shown; program continues |
| Empty library | Display before adding a book | “No books found” is shown |

### Conclusion
The project demonstrates how Python collections can organize library data, validate operations, and maintain a basic transaction history. JSON persistence keeps records between runs.

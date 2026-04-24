from database import SessionLocal, engine
from model import Base, Library , Book ,Member, Issue , Fine
import csv
from datetime import timedelta , datetime

Base.metadata.create_all(bind=engine)

session = SessionLocal()

current_library = None


def register():
    name = input("Library Name: ")
    email = input("Email: ")
    password = input("Password: ")

    lib = Library(name=name, email=email, password=password)
    session.add(lib)
    session.commit()

    print("Library registered successfully")


def login():
    global current_library

    email = input("Email: ")
    password = input("Password: ")

    lib = session.query(Library).filter_by(email=email, password=password).first()

    if lib:
        current_library = lib
        print(f"Logged in as {lib.name}")
    else:
        print("Invalid credentials")

#! Book managment functions 

def add_book(current_library):
    title = input("Title: ")
    author = input("Author: ")
    genre = input("Genre: ")

    try:
        total = int(input("Total copies: "))
    except:
        print("Invalid number")
        return

    isbn = input("ISBN: ")
    year = input("Publication Year: ")
    shelf = input("Shelf location: ")

    book = Book(
        title=title,
        author=author,
        genre=genre,
        total_copies=total,
        available_copies=total,
        isbn=isbn,
        publication_year=year,
        shelf_location=shelf,
        library_id=current_library.id
    )

    session.add(book)
    session.commit()

    print("Book added successfully")


def remove_book(current_library):
    book_id = input("Enter Book ID: ")

    book = session.query(Book).filter_by(
        id=book_id,
        library_id=current_library.id
    ).first()

    if not book:
        print("Book not found")
        return

    # Edge case: book currently issued
    issued = session.query(Issue).filter_by(
        book_id=book.id,
        return_date=None
    ).first()

    if issued:
        print("Cannot delete, book is currently issued")
        return

    session.delete(book)
    session.commit()

    print("Book removed")

def update_book(current_library):
    book_id = input("Enter Book ID: ")

    book = session.query(Book).filter_by(
        id=book_id,
        library_id=current_library.id
    ).first()

    if not book:
        print("Book not found")
        return

    print("Leave blank to keep old value")

    title = input(f"Title ({book.title}): ")
    author = input(f"Author ({book.author}): ")
    genre = input(f"Genre ({book.genre}): ")

    if title:
        book.title = title
    if author:
        book.author = author
    if genre:
        book.genre = genre

    session.commit()
    print("Book updated")

def view_all_books(current_library):
    books = session.query(Book).filter_by(
        library_id=current_library.id
    ).all()

    if not books:
        print("No books found")
        return

    for b in books:
        print(f"""
ID: {b.id}
Title: {b.title}
Author: {b.author}
Genre: {b.genre}
Available: {b.available_copies}/{b.total_copies}
ISBN: {b.isbn}
Location: {b.shelf_location}
-------------------------
""")

def view_available_books(current_library):
    books = session.query(Book).filter(
        Book.library_id == current_library.id,
        Book.available_copies > 0
    ).all()

    if not books:
        print("No available books")
        return

    for b in books:
        print(f"{b.id} - {b.title} ({b.available_copies} available)")

def view_books_by_genre(current_library):
    genre = input("Enter genre: ")

    books = session.query(Book).filter_by(
        genre=genre,
        library_id=current_library.id
    ).all()

    if not books:
        print("No books found in this genre")
        return

    for b in books:
        print(f"{b.id} - {b.title} by {b.author}")

def import_books_csv(current_library):
    file_path = input("Enter CSV file path: ")

    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                book = Book(
                    title=row["title"],
                    author=row["author"],
                    genre=row["genre"],
                    total_copies=int(row["total_copies"]),
                    available_copies=int(row["total_copies"]),
                    isbn=row["isbn"],
                    publication_year=row["publication_year"],
                    shelf_location=row["shelf_location"],
                    library_id=current_library.id
                )
                session.add(book)

            session.commit()
            print("Books imported successfully")

    except Exception as e:
        print("Error importing CSV:", e)


def book_menu():
    while True:
        print("\n--- Book Management ---")
        print("1. Add new book")
        print("2. Remove book")
        print("3. Update book")
        print("4. View all books")
        print("5. View available books")
        print("6. View by genre")
        print("7. Import CSV")
        print("8. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book(current_library)
        elif choice == "2":
            remove_book(current_library)
        elif choice == "3":
            update_book(current_library)
        elif choice == "4":
            view_all_books(current_library)
        elif choice == "5":
            view_available_books(current_library)
        elif choice == "6":
            view_books_by_genre(current_library)
        elif choice == "7":
            import_books_csv(current_library)
        elif choice == "8":
            break

#!Here create the functions for member managment

def register_member(current_library):
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")

    membership_type = input("Type (Student/Teacher/External): ").capitalize()

    if membership_type not in ["Student", "Teacher", "External"]:
        print("Invalid membership type")
        return

    join_date = datetime.today().date()

    # Example expiry logic (1 year)
    expiry_date = join_date + timedelta(days=365)

    member = Member(
        name=name,
        phone=phone,
        email=email,
        membership_type=membership_type,
        join_date=join_date,
        expiry_date=expiry_date,
        is_active=True,
        library_id=current_library.id
    )

    session.add(member)
    session.commit()

    print("Member registered successfully")

def remove_member(current_library):
    member_id = input("Enter Member ID: ")

    member = session.query(Member).filter_by(
        id=member_id,
        library_id=current_library.id
    ).first()

    if not member:
        print("Member not found")
        return

    # Optional: prevent delete if books issued
    active_issue = session.query(Issue).filter_by(
        member_id=member.id,
        return_date=None
    ).first()

    if active_issue:
        print("Cannot delete member with issued books")
        return

    session.delete(member)
    session.commit()

    print("Member removed")

def update_member(current_library):
    member_id = input("Enter Member ID: ")

    member = session.query(Member).filter_by(
        id=member_id,
        library_id=current_library.id
    ).first()

    if not member:
        print("Member not found")
        return

    print("Leave blank to keep old value")

    name = input(f"Name ({member.name}): ")
    phone = input(f"Phone ({member.phone}): ")
    email = input(f"Email ({member.email}): ")

    if name:
        member.name = name
    if phone:
        member.phone = phone
    if email:
        member.email = email

    session.commit()
    print("Member updated")

def view_all_members(current_library):
    members = session.query(Member).filter_by(
        library_id=current_library.id
    ).all()

    if not members:
        print("📭 No members found")
        return

    for m in members:
        print(f"""
ID: {m.id}
Name: {m.name}
Phone: {m.phone}
Type: {m.membership_type}
Active: {m.is_active}
Expiry: {m.expiry_date}
-------------------------
""")

def view_member_profile(current_library):
    member_id = input("Enter Member ID: ")

    member = session.query(Member).filter_by(
        id=member_id,
        library_id=current_library.id
    ).first()

    if not member:
        print("Member not found")
        return

    print(f"""
===== MEMBER PROFILE =====
Name: {member.name}
Type: {member.membership_type}
Active: {member.is_active}
Join Date: {member.join_date}
Expiry Date: {member.expiry_date}
""")

    # Issued Books
    issues = session.query(Issue).filter_by(
        member_id=member.id,
        return_date=None
    ).all()

    print("Currently Issued Books:")
    if not issues:
        print("None")
    else:
        for i in issues:
            book = session.query(Book).filter_by(id=i.book_id).first()
            print(f"- {book.title} (Due: {i.due_date})")

    # Fines
    fines = session.query(Fine).filter_by(
        member_id=member.id,
        is_paid=False
    ).all()

    total_fine = sum(f.amount for f in fines)

    print(f"Pending Fine: {total_fine}")

def toggle_member_status(current_library):
    member_id = input("Enter Member ID: ")

    member = session.query(Member).filter_by(
        id=member_id,
        library_id=current_library.id
    ).first()

    if not member:
        print("Member not found")
        return

    member.is_active = not member.is_active
    session.commit()

    status = "Active" if member.is_active else "Inactive"
    print(f"Member is now {status}")

def member_menu():
    while True:
        print("\n--- Member Management ---")
        print("1. Register member")
        print("2. Remove member")
        print("3. Update member")
        print("4. View all")
        print("5. Profile")
        print("6. Activate/Deactivate")
        print("7. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            register_member(current_library)
        elif choice == "2":
            remove_member(current_library)
        elif choice == "3":
            update_member(current_library)
        elif choice == "4":
            view_all_members(current_library)
        elif choice == "5":
            view_member_profile(current_library)
        elif choice == "6":
            toggle_member_status(current_library)
        elif choice == "7":
            break

#! here create the functions for teh issue and return managment

def get_limit(membership_type):
    return {
        "Student": 2,
        "Teacher": 5,
        "External": 1
    }.get(membership_type, 0)


def issue_book(current_library):
    member_id = input("Enter Member ID: ")
    book_id = input("Enter Book ID: ")

    member = session.query(Member).filter_by(
        id=member_id,
        library_id=current_library.id
    ).first()

    book = session.query(Book).filter_by(
        id=book_id,
        library_id=current_library.id
    ).first()

    if not member or not book:
        print("Invalid member or book")
        return

    if not member.is_active:
        print("Member is inactive")
        return

    if member.expiry_date < datetime.today().date():
        print("Membership expired")
        return

    unpaid_fine = session.query(Fine).filter_by(
        member_id=member.id,
        is_paid=False
    ).first()

    if unpaid_fine:
        print("Clear pending fines first")
        return

    if book.available_copies <= 0:
        print("No copies available")
        return

    existing = session.query(Issue).filter_by(
        member_id=member.id,
        book_id=book.id,
        return_date=None
    ).first()

    if existing:
        print("Member already has this book")
        return

    active_books = session.query(Issue).filter_by(
        member_id=member.id,
        return_date=None
    ).count()

    if active_books >= get_limit(member.membership_type):
        print("Book limit reached")
        return

    issue_date = datetime.today().date()
    due_date = issue_date + timedelta(days=7)

    issue = Issue(
        book_id=book.id,
        member_id=member.id,
        issue_date=issue_date,
        due_date=due_date,
        library_id=current_library.id
    )

    book.available_copies -= 1

    session.add(issue)
    session.commit()

    print(f"Book issued. Due date: {due_date}")

def return_book(current_library):
    member_id = input("Enter Member ID: ")
    book_id = input("Enter Book ID: ")

    issue = session.query(Issue).filter_by(
        member_id=member_id,
        book_id=book_id,
        return_date=None
    ).first()

    if not issue:
        print("This book was not issued to this member")
        return

    today = datetime.today().date()
    issue.return_date = today

    book = session.query(Book).filter_by(id=book_id).first()
    book.available_copies += 1

    overdue_days = (today - issue.due_date).days

    if overdue_days > 0:
        fine_amount = 0

        for day in range(1, overdue_days + 1):
            if day <= 30:
                fine_amount += 5
            else:
                fine_amount += 10

        fine = Fine(
            member_id=member_id,
            amount=fine_amount,
            is_paid=False,
            reason="Late return",
            library_id=current_library.id
        )

        session.add(fine)
        print(f"Fine generated: ₹{fine_amount}")

    session.commit()
    print("Book returned successfully")

def renew_book(current_library):
    member_id = input("Enter Member ID: ")
    book_id = input("Enter Book ID: ")

    issue = session.query(Issue).filter_by(
        member_id=member_id,
        book_id=book_id,
        return_date=None
    ).first()

    if not issue:
        print("No active issue found")
        return

    if issue.is_renewed:
        print("Already renewed once")
        return

    issue.due_date += timedelta(days=7)
    issue.is_renewed = True

    session.commit()
    print(f"Renewed. New due date: {issue.due_date}")

def view_issued_books(current_library):
    issues = session.query(Issue).filter_by(
        library_id=current_library.id,
        return_date=None
    ).all()

    if not issues:
        print("No issued books")
        return

    for i in issues:
        print(f"""
Member ID: {i.member_id}
Book ID: {i.book_id}
Issue Date: {i.issue_date}
Due Date: {i.due_date}
------------------------
""")

def view_overdue_books(current_library):
    today = datetime.today().date()

    issues = session.query(Issue).filter(
        Issue.library_id == current_library.id,
        Issue.return_date == None,
        Issue.due_date < today
    ).all()

    if not issues:
        print("No overdue books")
        return

    for i in issues:
        overdue_days = (today - i.due_date).days

        fine = 0
        for day in range(1, overdue_days + 1):
            if day <= 30:
                fine += 5
            else:
                fine += 10

        print(f"""
Member ID: {i.member_id}
Book ID: {i.book_id}
Due Date: {i.due_date}
Overdue Days: {overdue_days}
Fine: ₹{fine}
------------------------
""")

def issue_menu():
    while True:
        print("\n--- Issue & Return ---")
        print("1. Issue")
        print("2. Return")
        print("3. Renew")
        print("4. View issued")
        print("5. Overdue")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            issue_book(current_library)
        elif choice == "2":
            return_book(current_library)
        elif choice == "3":
            renew_book(current_library)
        elif choice == "4":
            view_issued_books(current_library)
        elif choice == "5":
            view_overdue_books(current_library)
        elif choice == "6":
            break


def fine_menu():
    while True:
        print("\n--- Fine & Payments ---")
        print("1. Check fine")
        print("2. Pay fine")
        print("3. Pending fines")
        print("4. History")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            break


def report_menu():
    while True:
        print("\n--- Reports & Search ---")
        print("1. Search book")
        print("2. Search member")
        print("3. Top books")
        print("4. Highest fines")
        print("5. Dead stock")
        print("6. Monthly report")
        print("7. Overdue report")
        print("8. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            pass
        elif choice == "7":
            pass
        elif choice == "8":
            break


def admin_menu():
    while True:
        print("\n--- Admin Settings ---")
        print("1. Change fine rate")
        print("2. Change max days")
        print("3. Change limits")
        print("4. Stats")
        print("5. Backup")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            break


def main():
    global current_library

    while True:
        if not current_library:
            print("\n1. Register")
            print("2. Login")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                register()
            elif choice == "2":
                login()
            elif choice == "0":
                break

        else:
            print("\n====== LIBRARY MANAGEMENT SYSTEM ======")
            print("1. Book Management")
            print("2. Member Management")
            print("3. Issue & Return")
            print("4. Fine & Payments")
            print("5. Reports & Search")
            print("6. Admin Settings")
            print("7. Logout")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                book_menu()
            elif choice == "2":
                member_menu()
            elif choice == "3":
                issue_menu()
            elif choice == "4":
                fine_menu()
            elif choice == "5":
                report_menu()
            elif choice == "6":
                admin_menu()
            elif choice == "7":
                current_library = None
            elif choice == "0":
                break


if __name__ == "__main__":
    main()
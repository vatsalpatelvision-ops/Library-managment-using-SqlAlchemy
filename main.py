from database import SessionLocal, engine
from model import Base, Library

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
            break


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


# ------------------ MAIN LOOP ------------------
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
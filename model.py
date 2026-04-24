from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base


# ------------------ LIBRARY (TENANT) ------------------
class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    books = relationship("Book", back_populates="library")
    members = relationship("Member", back_populates="library")


# ------------------ BOOK ------------------
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)

    total_copies = Column(Integer)
    available_copies = Column(Integer)

    isbn = Column(String)
    publication_year = Column(Integer)
    shelf_location = Column(String)

    library_id = Column(Integer, ForeignKey("libraries.id"))

    library = relationship("Library", back_populates="books")


# ------------------ MEMBER ------------------
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    phone = Column(String)
    email = Column(String)

    membership_type = Column(String)  # Student / Teacher / External
    join_date = Column(Date)
    expiry_date = Column(Date)

    is_active = Column(Boolean, default=True)

    library_id = Column(Integer, ForeignKey("libraries.id"))

    library = relationship("Library", back_populates="members")


# ------------------ ISSUE ------------------
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)

    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))

    issue_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)

    is_renewed = Column(Boolean, default=False)

    library_id = Column(Integer, ForeignKey("libraries.id"))


# ------------------ FINE ------------------
class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True)

    member_id = Column(Integer, ForeignKey("members.id"))
    amount = Column(Integer)

    is_paid = Column(Boolean, default=False)
    reason = Column(String)

    library_id = Column(Integer, ForeignKey("libraries.id"))

class AdminSettings(Base):
    __tablename__ = "admin_settings"

    id = Column(Integer, primary_key=True)

    fine_rate_7_days = Column(Integer, default=5)
    fine_rate_30_days = Column(Integer, default=10)
    max_issue_days = Column(Integer, default=7)

    max_books_student = Column(Integer, default=2)
    max_books_teacher = Column(Integer, default=5)
    max_books_external = Column(Integer, default=1)

    library_id = Column(Integer, ForeignKey("libraries.id"), unique=True)
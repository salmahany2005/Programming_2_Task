from abc import ABC, abstractmethod
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
class NotificationService(ABC):
    @abstractmethod
    def notify(self, member, message):
        pass
class EmailNotification(NotificationService):
    def notify(self, member, message):
        print(f"Email to {member.name}: {message}")
class SMSNotification(NotificationService):
    def notify(self, member, message):
        print(f"SMS to {member.name}: {message}")
class LibraryInventory:
    def __init__(self):
        self.books = []
    def add_book(self, book):
        self.books.append(book)
    def remove_book(self, book):
        self.books.remove(book)
    def list_books(self):
        return [f"{book.title} by {book.author}" for book in self.books]
class LoanService(ABC):
    @abstractmethod
    def loan_book(self, member, book):
        pass
    @abstractmethod
    def return_book(self, member, book):
        pass
class BasicLoanService(LoanService):
    def __init__(self):
        self.loans = {}
    def loan_book(self, member, book):
        if member not in self.loans:
            self.loans[member] = []
        self.loans[member].append(book)
        print(f"{book.title} loaned to {member.name}.")
    def return_book(self, member, book):
        if member in self.loans and book in self.loans[member]:
            self.loans[member].remove(book)
            print(f"{book.title} returned by {member.name}.")
        else:
            print(f"{member.name} does not have {book.title}.")
class LibraryService:
    def __init__(self, inventory: LibraryInventory, loan_service: LoanService, notifier: NotificationService):
        self.inventory = inventory
        self.loan_service = loan_service
        self.notifier = notifier
    def add_book_to_inventory(self, book):
        self.inventory.add_book(book)
        print(f"{book.title} added to the library.")
    def loan_book_to_member(self, member, book):
        if book in self.inventory.books:
            self.loan_service.loan_book(member, book)
            self.inventory.remove_book(book)
            self.notifier.notify(member, f"You have loaned '{book.title}'.")
        else:
            print(f"'{book.title}' is not available in the inventory.")

    def return_book_from_member(self, member, book):
        self.loan_service.return_book(member, book)
        self.inventory.add_book(book)
        self.notifier.notify(member, f"Thank you for returning '{book.title}'.")
inventory = LibraryInventory()
notifier = EmailNotification()
loan_service = BasicLoanService()
library_service = LibraryService(inventory, loan_service, notifier)
book1 = Book("Clean Code", "Robert C. Martin", 2008)
book2 = Book("The Pragmatic Programmer", "Andrew Hunt", 1999)
book3 = Book("Design Patterns", "Gang of Four", 1994)
member1 = Member("Alice", "M001")
member2 = Member("Bob", "M002")
library_service.add_book_to_inventory(book1)
library_service.add_book_to_inventory(book2)
library_service.add_book_to_inventory(book3)
library_service.loan_book_to_member(member1, book1)
library_service.loan_book_to_member(member2, book2)
library_service.return_book_from_member(member1, book1)
library_service.return_book_from_member(member2, book2)
print("Books currently in inventory:")
for book in inventory.list_books():
    print(book)

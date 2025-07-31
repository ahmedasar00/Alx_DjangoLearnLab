import os
import django

# ربط إعدادات المشروع
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# استدعاء الموديلات
from relationship_app.models import Author, Book, Library, Librarian

# حذف البيانات القديمة (اختياري)
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# إنشاء مؤلفين
orwell = Author.objects.create(name="George Orwell")
rowling = Author.objects.create(name="J.K. Rowling")

# إنشاء كتب
book1 = Book.objects.create(title="1984", author=orwell)
book2 = Book.objects.create(title="Animal Farm", author=orwell)
book3 = Book.objects.create(title="Harry Potter 1", author=rowling)
book4 = Book.objects.create(title="Harry Potter 2", author=rowling)

# إنشاء مكتبات
central = Library.objects.create(name="Central Library")
community = Library.objects.create(name="Community Library")

# ربط الكتب بالمكتبات
central.books.add(book1, book2, book3)
community.books.add(book2, book4)

# إضافة أمناء مكتبات
Librarian.objects.create(name="Mr. Smith", library=central)
Librarian.objects.create(name="Ms. Johnson", library=community)

print("✅ Sample data loaded successfully.")

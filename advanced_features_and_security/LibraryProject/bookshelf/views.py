# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article,Book
from .forms import BookSearchForm, ExampleForm

#! Task2 ----> 

def search_books(request):
    form = ExampleForm(request.GET)
    books = []
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(title__icontains=query)  # Safe query using ORM
    return render(request, 'bookshelf/search_results.html', {'form': form, 'books': books})


#! Task one ----> Permission

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def article_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        article = Article.objects.create(title=title, content=content, author=request.user)
        return render(request, 'article_detail.html', {'article': article})
    return render(request, 'article_form.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.save()
        return render(request, 'article_detail.html', {'article': article})
    return render(request, 'article_form.html', {'article': article})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        article.delete()
        return render(request, 'article_list.html')
    return render(request, 'article_confirm_delete.html', {'article': article})

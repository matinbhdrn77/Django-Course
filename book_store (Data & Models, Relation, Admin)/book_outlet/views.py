from django.shortcuts import get_object_or_404, render
from django.db.models import Avg, Min
from .models import Book
# Create your views here.


def index(request):
    books = Book.objects.all().order_by('-rating')
    total = books.count()
    avg_min_rating = books.aggregate(Avg('rating'), Min('rating'))
    return render(request, 'book_outlet/index.html', {
        'books': books,
        'total': total,
        'avg_min': avg_min_rating
    })


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book_outlet/book_detail.html', {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestselling": book.is_bestSelling
    })

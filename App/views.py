from django.contrib import messages
from django.db.models import ProtectedError, Count, Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from App.models import Author, Books, Orders


def index(request):
    data = {
        'title': '首頁',
    }

    return render(request, 'index.html', context=data)


def author(request):
    authors = Author.objects.all()
    author_list = []
    for author in authors:
        book_count = author.books_set.all().count()
        author_list.append(
            {
                'id': author.id,
                'name': author.author_name,
                'book_count': book_count,
            }
        )
    data = {
        'title': '作者管理',
        'author_list': author_list,
    }
    return render(request, 'author/author.html', context=data)


def author_add(request):
    if request.method == 'GET':
        data = {
            'title': '新增作者'
        }
        return render(request, 'author/author_add.html', context=data)
    elif request.method == 'POST':
        author_name = request.POST.get('author_name')
        authors = Author()
        authors.author_name = author_name
        authors.save()
        return redirect(reverse('bookstore:author_list'))


def author_edit(request, pk):
    author = get_object_or_404(Author, id=pk)
    if request.method == 'GET':
        data = {
            'title': '修改作者',
            'pk': author.id,
            'author_name': author.author_name,
        }
        return render(request, 'author/author_edit.html', context=data)
    elif request.method == 'POST':
        author_name = request.POST.get('author_name')
        author.author_name = author_name
        author.save(update_fields=['author_name'])
        return redirect(reverse('bookstore:author_list'))


def author_delete(request, pk):
    try:
        Author.objects.get(pk=pk).delete()
        messages.add_message(request, messages.INFO, '已刪除作者')
        return redirect(reverse('bookstore:author_list'))
    except ProtectedError:
        messages.add_message(request, messages.INFO, '此作者還有著作無法刪除')
        return redirect(reverse('bookstore:author_list'))


def books(request):
    books = Books.objects.all()
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'name': book.book_name,
            'author_name': book.author.author_name,
            'price': book.price,
        })
    data = {
        'title': '書籍管理',
        'books_list': books_list,
    }
    return render(request, 'books/books.html', context=data)


def books_add(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        author_option = []
        for author in authors:
            author_option.append({
                'pk': author.id,
                'name': author.author_name,
            })
        data = {
            'title': '新增書籍',
            'author_option': author_option,
        }
        return render(request, 'books/books_add.html', context=data)
    elif request.method == 'POST':
        author_id = request.POST.get('author_id')
        book_name = request.POST.get('book_name')
        price = request.POST.get('price')
        books = Books()
        books.author = Author.objects.get(id=author_id)
        books.book_name = book_name
        books.price = price
        books.save()
        return redirect(reverse('bookstore:books_list'))


def books_edit(request, pk):
    book = get_object_or_404(Books, id=pk)
    if request.method == 'GET':
        authors = Author.objects.all()
        author_option = []
        for author in authors:
            author_option.append({
                'pk': author.id,
                'name': author.author_name,
            })
        data = {
            'title': '新增書籍',
            'author_option': author_option,
            'pk': book.id,
            'name': book.book_name,
            'price': book.price,
            'author_pk': book.author.id,
            'author_name': book.author.author_name,
        }
        return render(request, 'books/books_edit.html', context=data)
    elif request.method == 'POST':
        author_id = request.POST.get('author_id')
        book_name = request.POST.get('book_name')
        price = request.POST.get('price')
        book.author = Author.objects.get(id=author_id)
        book.book_name = book_name
        book.price = price
        book.save(update_fields=['author', 'book_name', 'price'])
        return redirect(reverse('bookstore:books_list'))


def books_delete(request, pk):
    try:
        Books.objects.get(pk=pk).delete()
        messages.add_message(request, messages.INFO, '已刪除此書籍')
        return redirect(reverse('bookstore:books_list'))
    except ProtectedError:
        messages.add_message(request, messages.INFO, '此書籍有訂單無法刪除')
        return redirect(reverse('bookstore:books_list'))


def order(request):
    orders = Orders.objects.all()
    order_list = []
    for order in orders:
        order_list.append({
            'pk': order.id,
            'book_name': order.books.book_name,
            'book_price': order.books.price,
            'amount': order.amount,
            'total_price': order.books.price * order.amount,
        })
    data = {
        'title': '訂單管理',
        'order_list': order_list,
    }
    return render(request, 'order/order.html', context=data)


def order_add(request):
    if request.method == 'GET':
        books = Books.objects.all()
        book_option = []
        for book in books:
            book_option.append({
                'pk': book.id,
                'name': book.book_name,
            })
        data = {
            'title': '新增訂單',
            'book_option': book_option,
        }
        return render(request, 'order/order_add.html', context=data)
    elif request.method == 'POST':
        book_id = request.POST.get('book_id')
        amount = request.POST.get('amount')
        order = Orders()
        order.books = Books.objects.get(id=book_id)
        order.amount = amount
        order.save()
    return redirect(reverse('bookstore:order_list'))


def rank(request):
    amount_sum = Orders.objects.values('books__author__author_name').annotate(Sum('amount'))
    price_sum = Orders.objects.values('books__author__author_name').annotate(Sum('books__price'))
    price_total = Orders.objects.values('books__author__author_name').annotate(prod=F('books__price') * F(amount_sum))

    data = {
        'price_total': price_total,
        'price_sum': price_sum,
    }
    return render(request, 'rank/rank.html', context=data)

from django.urls import path, include

from App import views

app_name = 'bookstore'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('author/', views.author, name='author_list'),
    path('author/add/', views.author_add, name='author_add'),
    path('author/<slug:pk>/edit/', views.author_edit, name='author_edit'),
    path('author/<slug:pk>/delete/', views.author_delete, name='author_delete'),
    path('books/', views.books, name='books_list'),
    path('books/add/', views.books_add, name='books_add'),
    path('books/<slug:pk>/edit/', views.books_edit, name='books_edit'),
    path('books/<slug:pk>/delete/', views.books_delete, name='books_delete'),
    path('order/', views.order, name='order_list'),
    path('order/add/', views.order_add, name='order_add'),
    path('rank/', views.rank, name='rank'),

]

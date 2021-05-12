from django.db import models


# Create your models here.
class Author(models.Model):
    author_name = models.CharField(
        max_length=10,
    )


class Books(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
    )
    book_name = models.CharField(
        max_length=20,
    )
    price = models.IntegerField(
        default=0,
    )


class Orders(models.Model):
    books = models.ForeignKey(
        Books,
        on_delete=models.PROTECT,
    )
    amount = models.IntegerField(
        default=0,
    )

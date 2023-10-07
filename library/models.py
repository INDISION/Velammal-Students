from django.db import models

# Create your models here.
class AuthorAndOrganization(models.Model):
    name = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return self.name

class Genre(models.Model):
    genre = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return self.genre
    
class Book(models.Model):
    name = models.CharField(max_length=250, unique=True)
    by = models.ForeignKey(AuthorAndOrganization, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre)
    publication = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class BookId(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        NotAVAILABLE = 'notavailable', 'Not Available'
    book_id = models.CharField(max_length=50, unique=True)
    name = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.AVAILABLE)
    def __str__(self):
        return self.book_id + " " + str(self.name)
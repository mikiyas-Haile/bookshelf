from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Book(models.Model):
    title = models.CharField(max_length=40)
    body = models.TextField()
    # cover_img = models.ImageField()
    discription = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True,related_name="book_likes")
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def liked(self):
        return self.likes.all()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
            return '%s - %s - %s' % (self.author, self.title, self.date_added)

class Comment(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    likes = models.ManyToManyField(User, blank=True,related_name="comment_likes")
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def liked(self):
        return self.likes.all()

    def total_likes(self):
        return self.likes.count()
    
    @property
    def is_reply(self):
        return self.parent != None

    def __str__(self):
        return '%s - %s - %s' % (self.author, self.book.title, self.body)
from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True,)
    
    def __str__(self):
        return self.category_name

class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_article")
    reporter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name="reporter_article")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return self.title


    
    
class Image(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.ImageField(upload_to="images/")


class Comment(models.Model):
    article = models.ForeignKey(
        Article, related_name="comment", on_delete=models.CASCADE
    )
    commentor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name="commentor")
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

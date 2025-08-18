from django.db import models
from html.parser import HTMLParser
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True,help_text='Category name')
    slug = models.SlugField(max_length=200,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100,unique=True,help_text='Tag name')
    slug = models.SlugField(max_length=200,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Blog(models.Model):

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
        ('disabled','Disabled'),
    )

    title = models.CharField(max_length=200,unique=True,help_text='Blog title')
    content = HTMLField(help_text='Blog content')
    image = models.ImageField(upload_to='blog/image',help_text='Blog image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    author = models.ForeignKey(
        get_user_model(),on_delete=models.CASCADE,related_name='blog_posts',null=True,blank=True
                               )
    categories = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blogs',blank=True)
    tag = models.ManyToManyField(Tag,related_name='blogs',blank=True)
    comments_count = models.PositiveIntegerField(default=0,editable=False,help_text='Comments count')
    share_count = models.PositiveIntegerField(default=0,editable=False,help_text='Share count')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft',help_text='Blog status')

    def update_comments_count(self):
        """Update the count of comments for this blog."""
        self.comments_count = Comment.objects.filter(blog=self).count()  # Comment modelidan foydalaning
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=100,help_text='Commenter name')
    email = models.EmailField(help_text='Commenter email')
    message = HTMLField(help_text='Comment message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"
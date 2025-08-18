from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import *
import bleach
from django.views import View

def truncate_html(context,length):
    allowed_tags = ['p', 'u', 'br', 'strong', 'em', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul']

    truncated_context = bleach.clean(context, tags=allowed_tags, strip=True)

    if len(truncated_context) > length:
        truncated_context = truncated_context[:length] + '...'

    return truncated_context

class BlogListView(View):
    def get(self, request):
        blogs = Blog.objects.filter(status='published').order_by('-created_at')

        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')

        if tag_slug:
            blogs = blogs.filter(tag__slug=tag_slug)

        if category_slug:
            blogs = blogs.filter(categories__slug=category_slug)

        for blog in blogs:
            blog.truncated_content = truncate_html(blog.content, 150)
        context = {}
        context['recent_posts'] = Blog.objects.filter(status='published').order_by('-created_at')[:5]
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        context['blogs'] = blogs
        return render(request, 'blog.html', context)



class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog-details.html'
    context_object_name = 'blog'

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Comment.objects.create(blog=blog, name=name, email=email, message=message)
            return redirect('blog_detail', slug=blog.slug)

    def get_queryset(self):
        return Blog.objects.filter(status='published')

    def get_object(self, queryset=None):
        slug  = self.kwargs.get('slug')
        return self.get_queryset().get(slug=slug)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Blog.objects.filter(status='published').order_by('-created_at')[:15]
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        context['comments'] = Comment.objects.filter(blog=self.object).order_by('-created_at')
        return context

class BlogSearchView(ListView):
    model = Blog
    template_name = 'search.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Blog.objects.filter(title__icontains=query, status='published')

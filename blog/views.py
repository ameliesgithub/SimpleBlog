from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CreatePostForm, PostUpdateForm
from blog.models import Category, Post, UserProfile, Comments
from blog.utils import create_user
import pandas as pd


def index(request):
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'categories': categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'blog/category.html', {'category': category})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post.html', {'post': post})

def create_category(request):
    if request.method == 'POST':
        name = request.POST['category_name']
        category = Category.objects.create(name=name)
        return redirect('category_detail', category_id=category.id)
    return render(request, 'blog/create_category.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# create view is not used often because it is hard to customize
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('post_list')

# Update und Create View werden vom Generic View vererbt deshalb muss man nur model und template
# und fields angeben (oder in der upgedateten version mit forms). Die success url gibt an
# zu welcher Seite man redirected wird wenns geklappt hat.
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostUpdateForm
    success_url = reverse_lazy('post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        github_url = request.POST['github_url']
        linkedin_url = request.POST['linkedin_url']

        create_user(username, password, first_name, last_name, email, github_url, linkedin_url)

        return redirect('login')
    return render(request, 'registration/register.html')

def create_users(request):
    if request.method == 'POST' and request.FILES['names_file']:
        names_file = request.FILES['names_file']
        fs = FileSystemStorage()
        filename = fs.save(names_file.name, names_file) # save file to media folder
        uploaded_file_url = fs.url(filename)
        uploaded_file_path = fs.path(filename)
        print(uploaded_file_path)
        excel_read = pd.read_excel(uploaded_file_path)
        print(excel_read)
        data = pd.DataFrame(excel_read, columns=['username',
                                                 'password',
                                                 'first_name',
                                                 'last_name',
                                                 'email',
                                                 'github',
                                                 'linkedin'])
        usernames=data['username'].to_list()
        passwords = data['password'].to_list()
        first_names = data['first_name'].to_list()
        last_names = data['last_name'].to_list()
        emails = data['email'].to_list()
        github_urls = data['github'].to_list()
        linkedin_urls = data['linkedin'].to_list()
        for username, password, first_name, last_name, email, github_url, linkedin_url in zip(usernames, passwords, first_names, last_names, emails, github_urls, linkedin_urls):
            try:
                user = User.objects.get(username=username)
                user.delete()
                create_user(username, password, first_name, last_name, email, github_url, linkedin_url)
            except User.DoesNotExist:
                create_user(username, password, first_name, last_name, email, github_url, linkedin_url)

        print(data)
        return render(request, 'blog/create_users.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'blog/create_users.html')

def likes_unlikes(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail_view', pk=post_id)

def add_comments(request, post_id):
    if request.method == 'POST':
        comment_body = request.POST['comment_body']
        comment = Comments.objects.create(user=request.user, post=Post.objects.get(id=post_id), comment_body=comment_body)
        return redirect('post_detail_view', pk=post_id)


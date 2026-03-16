from django.shortcuts import render

from blog.models import Category


# Create your views here.
def index(request):
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'categories': categories})

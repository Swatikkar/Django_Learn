from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

vlogs = [
        {
            'title':'My First Blog',
            'author':'Phula',
            'content':'This is my first blog',
            'date_created' : '2022-01-01',
        },
        {
            'title':'My 2nd Blog',
            'author':'Paida',
            'content':'This is my second blog',
            'date_created' : '2022-01-10',
        }
]

def home(request):
    # return HttpResponse("<h1>Hello Bloggers! Welcome to the Blog World </h1>")
    contexts = {'vlogs':vlogs}
    return render(request,'blog/home.html',contexts)

def about(request):
    # return HttpResponse("<h1>This is the about page</h1>")
    return render(request,'blog/about.html')
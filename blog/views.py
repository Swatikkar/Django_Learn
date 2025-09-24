from django.shortcuts import render , redirect
# from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    dummy = [
    {
        "title": "10 Tips for Effective Remote Work",
        "author": "Alice Johnson",
        "image": "photo1.jpg",
        "content": "Remote work has become the new normal for many. In this post, we explore 10 practical tips to stay productive and healthy while working from home.",
        "date_posted": "2025-09-15 10:00"
    },
    {
        "title": "The Future of Artificial Intelligence in Healthcare",
        "author": "Bob Smith",
        "image": "photo2.jpg",
        "content": "AI is transforming healthcare. From diagnostics to personalized medicine, here's how AI is reshaping the industry.",
        "date_posted": "2025-09-14 14:30"
    },
    {
        "title": "Beginner's Guide to Django Web Development",
        "author": "Carol Lee",
        "image": "photo3.jpg",
        "content": "Django is a powerful web framework. This guide covers the basics for beginners who want to build their first web app.",
        "date_posted": "2025-09-13 09:20"
    },
    {
        "title": "Top 5 Travel Destinations for 2025",
        "author": "David Kim",
        "image": "photo4.jpg",
        "content": "Looking for your next adventure? Discover the top 5 must-visit travel destinations for 2025.",
        "date_posted": "2025-09-12 18:45"
    },
    {
        "title": "How to Build a Successful Personal Brand",
        "author": "Eva Green",
        "image": "photo5.jpg",
        "content": "Personal branding is key in today's digital world. Learn how to craft and grow your brand effectively.",
        "date_posted": "2025-09-11 11:10"
    },
    {
        "title": "Understanding Blockchain and Cryptocurrencies",
        "author": "Frank Wright",
        "image": "photo6.jpg",
        "content": "An introductory look at blockchain technology and how cryptocurrencies are changing the financial landscape.",
        "date_posted": "2025-09-10 16:00"
    },
    {
        "title": "Healthy Eating: Tips for a Balanced Diet",
        "author": "Grace Hall",
        "image": "photo7.jpg",
        "content": "Eating healthy doesn't have to be hard. Here are simple tips to maintain a balanced and nutritious diet.",
        "date_posted": "2025-09-09 08:30"
    },
    {
        "title": "The Impact of Social Media on Mental Health",
        "author": "Henry Clark",
        "image": "photo8.jpg",
        "content": "Social media can affect mental well-being in many ways. This post discusses the pros and cons and how to manage usage.",
        "date_posted": "2025-09-08 19:00"
    },
    {
        "title": "Start Coding Today: Resources for Beginners",
        "author": "Isabel Turner",
        "image": "photo9.jpg",
        "content": "Want to learn coding? Discover the best resources and tips for beginners to start programming effectively.",
        "date_posted": "2025-09-07 13:15"
    },
    {
        "title": "Sustainable Living: How to Reduce Your Carbon Footprint",
        "author": "Jackie Wilson",
        "image": "photo10.jpg",
        "content": "Sustainability matters. Learn practical ways to live greener and lower your carbon footprint in daily life.",
        "date_posted": "2025-09-06 10:45"
    }
]
    Vlogs = {"dummy":dummy}
    return render(request,'blog/home.html',Vlogs)

def about(request):
    # return HttpResponse("<h1>This is the about page</h1>")
    return render(request,'blog/about.html')
def myfeeds(request):
    return render(request,'blog/myfeeds.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        bio = request.POST.get('bio')
        profile_pic = request.POST.get('profile_pic')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        temp = User.objects.create_user(username=username, email=email)
        temp.set_password(password)

        user = UserProfile.objects.create(user=temp, full_name=full_name, bio = bio)
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'blog/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(request, 'blog/login.html')

    return render(request, 'blog/login.html')



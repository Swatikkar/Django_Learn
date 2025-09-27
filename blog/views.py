from django.shortcuts import render , redirect
# from django.http import HttpResponse
from .models import Post,UserProfile
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .dummy_data import dummy_posts
from django.conf import settings
def home(request):
    query = request.GET.get('q', '').strip()
    db_posts = Post.objects.all().values('title', 'author__user__username', 'image', 'content', 'date_posted')
    posts = []
    fixed_dummy_posts = []
    for post in dummy_posts:
        img = post['image']
        post_copy = post.copy()
        if img and not img.startswith(settings.MEDIA_URL):   # Prevent double prefix
            post_copy['image'] = settings.MEDIA_URL + 'post_pics/' + img
        fixed_dummy_posts.append(post_copy)
    for post in db_posts:
        image_url = settings.MEDIA_URL + post['image'] if post['image'] else ''
        posts.append({
            "title": post['title'],
            "author": post['author__user__username'],
            "image": image_url,  # Might need to build URL separately
            "content": post['content'],
            "date_posted": post['date_posted'].strftime("%Y-%m-%d %H:%M") if post['date_posted'] else ""
        })
    final_posts = posts + fixed_dummy_posts

    if query:
        q_lower = query.lower()
        final_posts = [post for post in final_posts if q_lower in post['title'].lower() or q_lower in post['content'].lower()]
    Vlogs = {"final_posts":final_posts}
    return render(request,'blog/home.html',Vlogs)

def about(request):
    # return HttpResponse("<h1>This is the about page</h1>")
    return render(request,'blog/about.html')

@login_required
def myfeeds(request):
    db_posts = Post.objects.filter(author=request.user.userprofile).order_by('-date_posted')
    print(f"Posts for user: {len(db_posts)}")
    posts = []
    for post in db_posts:
        image_url = settings.MEDIA_URL + post.image.name if post.image else ''
        posts.append({
            "title": post.title,
            "author": post.author.user.username,
            "image": image_url,
            "content": post.content,
            "date_posted": post.date_posted.strftime("%Y-%m-%d %H:%M") if post.date_posted else ""
    })
    final_posts = posts
    vlogs = {"final_posts":final_posts}
    return render(request,'blog/myfeeds.html',vlogs)

@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title or not content:
            messages.error(request, "Title and Content are required.")
            return render(request, 'blog/add_post.html')

        post = Post(title=title, content=content, author=request.user.userprofile)
        if image:
            post.image = image
        post.save()
        messages.success(request, "Post created successfully!")
        return redirect('home')

    return render(request, 'blog/add_post.html')
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('profile_pic')

        User = get_user_model()

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        temp_user = User.objects.create_user(username=username, email=email,password=password)

        user_profile = UserProfile.objects.create(user=temp_user, full_name=full_name, bio = bio)
        if profile_pic:
            user_profile.profile_pic = profile_pic
            user_profile.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login_page')

    return render(request, 'blog/register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Redirecting to Home")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_page')

    return render(request, 'blog/login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog_Category,contact_info,Subscribe
from .forms import Blog_Form, BlogPost_Form, blog_post, CommentForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Comment


# Create your views here.
def home(request):
    # return HttpResponse('<h1>This is Home page</h1>')
    X=Blog_Category.objects.all()
    print (X)
    return render(request,'myblog/home.html',{"category":X})



def contact(request):
    # return HttpResponse('<h1>This is contact page</h1>')
    if request.method == 'GET':
        return render(request,'myblog/contact.html')
    elif request.method == 'POST':
        email = request.POST.get('user_email')
        message = request.POST.get('message')
        x = contact_info(u_email = email,u_message = message)
        x.save()
        print (email)
        print (message)

        return render(request,'myblog/contact.html')

def blog(request):
    x = Blog_Form()  
    if request.method == "GET":
        return render(request,'myblog/blog.html',{"x":x})
    else:
        print("hi")
        form = Blog_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("hi")
            return redirect('home')
        else:
            context = {
                "x":x
            }
            return render(request,'myblog/blog.html',context)

def sub(request):
    if request.method == 'GET':
        return render(request,'myblog/sub.html')
    elif request.method == 'POST':
        email = request.POST.get('use_email')
        if(Subscribe.objects.filter(u_email = email).exists()):
            return render(request,'myblog/sub.html',{'feedback':'Already Subscribed'})
        else:
            x = Subscribe(u_email = email)
            x.save()
            return render(request,'myblog/sub.html',{'feedback':'Thank You for subscribing our page '})


def ck(request):
    x = BlogPost_Form()
    return render(request,'myblog/ck.html',{"x":x})


def allblogs(request):
    y=blog_post.objects.all()
    paginator = Paginator(y, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'myblog/allblogs.html',{"y":page_obj})

def search(request):
    if request.method == "POST":
        search = request.POST['S_value']
        searchresults = blog_post.objects.filter(blog_name__icontains = search)
        return render(request, 'myblog/allblogs.html',{"y":searchresults})   
    else:
        return redirect("home") 


def blog_details(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    form = CommentForm()
    print(obj)
    print(blog_id)
    z=obj.view_count
    z=z+1
    obj.view_count=z
    obj.save()
    return render(request,'myblog/blog_details.html', {"obj":obj, "form":form})
    # return HttpResponse('blog_details')

def blog_cat(request, blog_cat):
    # print(blog_cat)
    x = Blog_Category.objects.get(blog_cat= blog_cat)
    a = blog_post.objects.filter(blog_cat=x)
    return render(request,'myblog/allblogs.html',{"y":a})
    # return HttpResponse('blog_details')



def loginuser(request):
    if request.method == 'GET':
        return render(request,'myblog/loginuser.html',{'form':AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username=a,password=b)
        if user is None:
            return render(request,'myblog/loginuser.html',{'form':AuthenticationForm(), 'error':'Invalid Credentials'})
        else:
            login(request,user)
            return redirect('home')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'myblog/signupuser.html',{'form':UserCreationForm()})
    else:
        user = request.POST.get('username')
        pas = request.POST.get('password1')
        pasv = request.POST.get('password2')
        if pas == pasv:
            # Check wether user exists
            if (User.objects.filter(username = user)):
                return render(request, 'myblog/signupuser.html', {'SignupForm': UserCreationForm(), 'Error': "Username already exist! (Try again with different username)"})
            else:
                user = User.objects.create_user(username = user, password = pas)
                user.save()
                login(request, user)
                return redirect('/')
        else:
            # if password verification fails
            return render(request, 'myblog/signupuser.html', {'SignupForm': UserCreationForm(), 'Error': "Make sure both password is same!"})


def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')

@login_required
def add_like(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    print (obj.like_count)
    y=obj.like_count
    y=y+1
    obj.like_count=y
    obj.save()
    return redirect('blog_details', obj.id)


def add_comment(request, blog_id):
    post = get_object_or_404(blog_post, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_details', blog_id=post.id)
    

def delete_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('blog_details', blog_id=blog_id)

def edit_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(blog_post, pk=blog_id)
            comment.author = request.user
            comment.save()
            return redirect('blog_details', blog_id=blog_id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'myblog/edit_comment.html', {'form': form})

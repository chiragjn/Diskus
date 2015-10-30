from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found, server_error
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from Diskus.models import *
from django.contrib.auth.models import User
from itertools import chain
from datetime import datetime
import hashlib
import logging
import math
from django.contrib.auth.decorators import login_required

log = logging.getLogger(__name__)
posts_per_page = 15
threads_per_page = 15


def anonymous_required(view_function, redirect_to=None):
    return AnonymousRequired(view_function, redirect_to)


class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            redirect_to = '/'
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__( self, request, *args, **kwargs ):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)



def home(request):
    """Renders the home page with all categories.
    Categories are sorted by number of posts under them in descending order.
    Most recently active two threads are shown under each category.

    :param request: Request object
    :return: rendered page
    """
    context_dict = {}
    categories = []
    general_category = Category.objects.get_or_create(name="General Discussion")[0]
    if general_category:
        categories_qs = Category.objects.exclude(slug="general-discussion").annotate(num_threads=Count('thread')).order_by('-num_threads')
        top_threads = {}
        for category in chain([general_category], categories_qs):
            categories.append(category)
            top_threads[str(category.pk)] = [[thread, str(thread.post_set.count() - 1)] for thread in Thread.objects.filter(category=category, visible=True).order_by('-last_modified')[:2]]
        context_dict['categories'] = categories
        context_dict['top_threads'] = top_threads
        if request.user.is_authenticated():
            member = Member.objects.get(user=request.user)
            if member:
                context_dict['member'] = member
        return render(request, 'home.html', context_dict)
    else:
        return server_error(request)


def get_all_category_threads(request, slug):
    """Renders a category page with all threads paginated.
    Threads are sorted by pinned and then by most recently active.

    :param request: Request object
    :param slug: Category slug
    :return: rendered page
    """
    context_dict = {}
    category = Category.objects.filter(slug=slug)
    if category:
        page = request.GET.get('page')
        context_dict['categories'] = category
        threads = Thread.objects.filter(category=category, visible=True).order_by('-pinned', '-last_modified')
        paginator = Paginator(threads, threads_per_page)  # Show 15 threads per page
        try:
            threads = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            threads = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            threads = paginator.page(paginator.num_pages)
        context_dict['threads'] = [[thread, str(thread.post_set.count() - 1)] for thread in threads]
        context_dict['paginated_threads'] = threads
    else:
        return page_not_found(request)
    return render(request, 'category.html', context_dict)


def get_thread(request, slug_cat, slug_thread):
    """Renders a thread page with all posts paginated.
    Posts are sorted by date in ascending order.

    :param request: Request object
    :param slug_cat: Category slug
    :param slug_thread: thread slug
    :return: rendered page
    """
    context_dict = {}
    thread = Thread.objects.get(slug=slug_thread)
    if thread and thread.category.slug == slug_cat:
        page = request.GET.get('page')
        context_dict['thread'] = thread
        posts = Post.objects.filter(thread=thread).order_by('date')
        if posts:
            context_dict['first_post_pk'] = posts[0].pk
        paginator = Paginator(posts, posts_per_page)  # Show 15 threads per page
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)
        context_dict['posts'] = posts
    else:
        return page_not_found(request)
    if request.user.is_authenticated():
        member = Member.objects.get(user=request.user)
        if member:
            context_dict['member'] = member
    return render(request, 'thread.html', context_dict)


def make_post(request):
    """Responds to AJAX request for posting a reply to a thread.

    :param request: Request object
    :return: HttpResponse 200 or 500
    """
    if request.user.is_authenticated() and request.POST:
        member = Member.objects.get(user=request.user)
        thread_id = request.POST.get('thread_id', -1)
        content = request.POST.get('content', -1)
        if thread_id != -1 and content != -1 and member:
            post = Post()
            post.author = member
            post.thread = Thread.objects.get(pk=thread_id)
            post.content = content
            post.save()
            return HttpResponse(200)
        else:
            return server_error(request)
    else:
        return server_error(request)


@login_required(login_url='/login/')
def start_new_thread(request):
    context_dict = {}
    context_dict['selected_category'] = -1
    if request.user.is_authenticated():
        member = Member.objects.get(user=request.user)
        if member:
            context_dict['member'] = member
        categories = Category.objects.all()
        context_dict['categories'] = categories
        category_slug = request.GET.get('category',-1)
        if category_slug != -1:
            context_dict['selected_category'] = Category.objects.filter(slug=category_slug)[0].pk
        return render(request, 'newthread.html', context_dict)
    else:
        return server_error(request)
        
@login_required(login_url='/login/')
def post_new_thread(request):
    if request.user.is_authenticated() and request.POST:
        member = Member.objects.get(user=request.user)
        category_slug = request.POST.get('category_slug',-1)
        thread_title = request.POST.get('thread_title',-1)
        content = request.POST.get('content', -1)
        log.error(category_slug + " " + thread_title + " " + content)
        if category_slug != -1 or thread_title != -1 or content != -1:
            category = Category.objects.get(slug=category_slug)
            thread = Thread()
            thread.category = category
            thread.op = member
            thread.title = thread_title
            thread.save()
            thread_slug = thread.slug
            post = Post()
            post.author = member
            post.thread = thread
            post.content = content
            post.save()
            return HttpResponse('category/'+category_slug+'/thread/'+thread_slug)
        else:
            return server_error(request)
    else:
        return server_error(request)


#Paren's Code Begins
@anonymous_required
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            member = Member.objects.get(user=user)
            if user.is_active and not member.banned:
                login(request, user)
                redir = '/' if 'next' not in request.POST else request.POST['next']
                return redirect(redir)
            elif not user.is_active:
                return render(request, 'login.html', {'error': 'Account not activated,check email',
                                                      'resend_email_form': True, 'user_username': user.username})
            else:
                return render(request, 'login.html', {'error': 'You account has been banned!,Contact Admin'})
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})
    elif request.method == 'GET':
        context_dict = {'next': '/'}
        if 'status' in request.session:
            context_dict['status'] = request.session['status']
            del request.session['status']
        if 'next' in request.GET:
            context_dict['next'] = request.GET['next']
        return render(request, 'login.html', context_dict)
    else:
        return server_error(request)


@anonymous_required
def register_user(request):
    context_dict = {}
    if request.method == 'POST':
        check_user = User.objects.filter(username=request.POST['username'], email=request.POST['email'])
        if check_user:
            context_dict["error"] = "User Already Exists!"
            return render(request, 'register.html', context_dict)
        else:
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'], password=request.POST['password'])
            user.is_active = False
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.save()
            member = Member()
            member.user = user
            member.date_of_birth = datetime.strptime(request.POST['dob'], '%d/%m/%y')
            member.details_visible = 'visible' in request.POST
            member.bio = request.POST['bio']
            member.location = request.POST['location']
            member.save()
            send_verification_email(request, user)
            request.session['status'] = "Registration Successful.Verification link sent to your email address"
            redirect_to = '/' if 'next' not in request.POST else request.POST['next']
            return redirect('/login?next='+redirect_to)
    elif request.method == 'GET':
        if 'next' in request.GET:
            context_dict['next'] = request.GET['next']
        return render(request, 'register.html', context_dict)
    else:
        return server_error(request)


@anonymous_required
def forgot_password(request):
    if request.method == 'GET':
        if 'user' in request.GET and 'hash' in request.GET:
            return render(request, 'changeforgot.html', {'username': request.GET['user'], 'hash': request.GET['hash']})
        else:
            return render(request, 'forgot.html')
    elif request.method == 'POST':
        if 'forgot' in request.POST:
            user = None
            if request.POST['username'] != "":
                user = User.objects.get(username=request.POST['username'])
            elif request.POST['email'] != "":
                user = User.objects.get(email=request.POST['email'])
            else:
                return render(request, 'forgot.html', {'error': 'Some Error Occurred'})

            if user is not None:
                url = reverse('forgot-password') + '?user=' + user.username + '&hash=' + hashlib.md5(user.password.encode('utf-8')).hexdigest()
                url = request.build_absolute_uri(url)
                message = "Hi " + user.first_name + ",\n"
                message += "Please visit following link to reset password\n" + url
                send_mail('Reset Password', message, 'diskusforums@gmail.com', [user.email])
                return render(request, 'forgot.html', {'status': 'Please check your email for reset password link'})
            else:
                return render(request, 'forgot.html', {'error': 'No such user or email address'})

        elif 'change' in request.POST:
            user = User.objects.get(username=request.POST['username'])
            if request.POST['hash'] == hashlib.md5(user.password.encode('utf-8')).hexdigest():
                user.set_password(request.POST['password'])
                user.save()
                request.session['status'] = "Successfully Changed Password"
                return redirect('/login/')
            else:
                return redirect('/')
        else:
            return render(request, 'forgot.html')
    else:
        return server_error(request)


@login_required(login_url='/login/')
def profile(request, slug):
    member = Member.objects.get(slug=slug)
    self = request.user.is_authenticated() and request.user == member.user
    threads = Thread.objects.filter(op=member, visible=True).order_by('-date')[:5]
    posts = Post.objects.filter(author=member).order_by('-date')[:5]
    return render(request, 'profile.html', {'member': member, 'self': self, 'threads': threads, 'posts': posts})


@login_required(login_url='/login/')
def profile_edit(request, slug):
    if request.method == 'GET':
        if request.user.is_authenticated() and request.user == Member.objects.get(slug=slug).user:
            return render(request, 'edit.html', {'member': Member.objects.get(slug=slug)})
        return redirect('/')
    elif request.method == 'POST':
        if 'change' in request.POST:
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            member = Member.objects.get(user=user)
            member.date_of_birth = request.POST['dob']
            member.location = request.POST['location']
            member.bio = request.POST['bio']
            member.details_visible = 'visible' in request.POST
            user.save()
            member.save()
            return redirect('/profile/'+member.slug)
        return render(request, 'profile.html',  {'error': 'Some error occurred'})
    else:
        return server_error(request)


def verify_user(request):
    if request.method == 'GET':
        if 'user' in request.GET and 'hash' in request.GET:
            user = User.objects.get(username=request.GET['user'])
            if request.GET['hash'] == hashlib.md5(user.password.encode('utf-8')).hexdigest():
                user.is_active = True
                user.save()
                request.session['status'] = "Account Verified!"
                return redirect('/login/')
        else:
            return redirect('/')
    elif request.method == 'POST':
        user = User.objects.get(username=request.POST['user_username'])
        if user is not None:
            send_verification_email(request, user)
            request.session['status'] = "Verification link sent!"
            return redirect('/login/')
        else:
            return server_error(request)
    else:
        return server_error(request)


def send_verification_email(request, user):
    url = reverse('verify_user') + '?user=' + user.username + '&hash=' + hashlib.md5(user.password.encode('utf-8')).hexdigest()
    url = request.build_absolute_uri(url)
    message = "Hi " + user.username + ",\n"
    message += "Please visit following link to verify your account \n" + url
    send_mail('Verify your Diskus Account!', message, 'diskusforums@gmail.com', [user.email])


@login_required(login_url='/login/')
def view_post(request, slug_cat, slug_thread, post_number, relative_post_number):
    thread = Thread.objects.get(slug=slug_thread)
    if thread and thread.category.slug == slug_cat:
        page_number = int(math.ceil(int(relative_post_number)/threads_per_page)) + 1
        return redirect('/category/' + slug_cat + '/thread/' + slug_thread + '?page=' + str(page_number))
    else:
        return page_not_found(request)


@login_required(login_url='/login/')
def delete_post(request, slug_cat, slug_thread, post_number):
    if request.user.is_authenticated():
        post = Post.objects.get(pk=post_number)
        member = Member.objects.get(user=request.user)
        if post and member and (member.type > 0 or post.author == member):
            thread = Thread.objects.get(slug=slug_thread)
            if thread and thread.category.slug == slug_cat:
                post.visible = False
                post.save()
                return redirect('/category/' + slug_cat + '/thread/' + slug_thread + '?page=' + 1)
            else:
                return server_error(request)
        else:
            return server_error(request)
    else:
        return redirect('/login/')


@login_required(login_url='/login/')
def edit_post(request, slug_cat, slug_thread, post_number):
    if request.user.is_authenticated():
        post = Post.objects.get(pk=post_number)
        member = Member.objects.get(user=request.user)
        if post and member and (member.type > 0 or post.author == member):
            thread = Thread.objects.get(slug=slug_thread)
            if thread and thread.category.slug == slug_cat:
                return render(request, 'editpost.html',  {'post': post, 'member': post.author,'category_slug': slug_cat,'thread_slug': slug_thread})
            else:
               return server_error(request)
        else:
            return server_error(request)
    else:
        return redirect('/login/')


@login_required(login_url='/login/')
def save_edited_post(request, slug_cat, slug_thread, post_number):
    if request.user.is_authenticated() and request.POST:
        post = Post.objects.get(pk=post_number)
        member = Member.objects.get(user=request.user)
        if post and member and (member.type > 0 or post.author == member):
            post.content = request.POST['content']
            post.save()
            return HttpResponse('category/' + slug_cat + '/thread/' + slug_thread + '?page=1')
        else:
            return server_error(request)
    else:
        return server_error(request)


@login_required(login_url='/login/')
def add_category(request):
    if request.user.is_authenticated() and request.POST:
        member = Member.objects.get(user=request.user)
        if member and member.type==2:
            category = Category()
            category.name = request.POST['category']
            category.save()
            return redirect('/')
        else:
            return server_error(request)
    else:
        return server_error(request)
            

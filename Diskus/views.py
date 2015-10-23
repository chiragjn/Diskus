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
import logging

log = logging.getLogger(__name__)

#TO DO
#Add vaidation to Register Form
#Send email for verification
#Improve code in Paren's methods
#Profile Page
#Edit Profile
#Profile Image

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
            return HttpResponseRedirect( self.redirect_to)
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
        paginator = Paginator(threads, 15)  # Show 15 threads per page
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
    thread = Thread.objects.filter(slug=slug_thread)[0]
    if thread and thread.category.slug == slug_cat:
        page = request.GET.get('page')
        context_dict['thread'] = thread
        posts = Post.objects.filter(thread=thread, visible=True).order_by('date')
        if posts:
            context_dict['first_post_pk'] = posts[0].pk
        paginator = Paginator(posts, 15)  # Show 15 threads per page
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
        member = Member.objects.filter(user=request.user)
        if member:
            member = member[0]
            context_dict['member'] = member
    return render(request, 'thread.html', context_dict)


def make_post(request):
    """Responds to AJAX request for posting a reply to a thread.

    :param request: Request object
    :return: HttpResponse 200 or 500
    """
    if request.user.is_authenticated() and request.POST:
        member = Member.objects.filter(user=request.user)
        thread_id = request.POST.get('thread_id', -1)
        content = request.POST.get('content', -1)
        if thread_id != -1 and content != -1 and member:
            member = member[0]
            post = Post()
            post.author = member
            post.thread = Thread.objects.filter(pk=thread_id)[0]
            post.content = content
            post.save()
            return HttpResponse(200)
        else:
            return server_error(request)
    else:
        return server_error(request)


def start_new_thread(request):
    context_dict = {}
    context_dict['selected_category'] = -1
    if request.user.is_authenticated():
        member = Member.objects.filter(user=request.user)
        if member:
            member = member[0]
            context_dict['member'] = member
        categories = Category.objects.all()
        context_dict['categories'] = categories
        category_slug = request.GET.get('category',-1)
        if category_slug != -1:
            context_dict['selected_category'] = Category.objects.filter(slug=category_slug)[0].pk
        return render(request,'newthread.html',context_dict)
    else:
        return server_error(request)
        
    

def post_new_thread(request):
    if request.user.is_authenticated() and request.POST:
        member = Member.objects.filter(user=request.user)[0]
        category_slug = request.POST.get('category_slug',-1)
        thread_title = request.POST.get('thread_title',-1)
        content = request.POST.get('content', -1)
        log.error(category_slug + " " + thread_title + " " + content)
        if category_slug != -1 or thread_title != -1 or content != -1:
            category = Category.objects.filter(slug=category_slug)[0]
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


@anonymous_required
def login_user(request):
    # if request.user.is_authenticated():
    #     return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                redir = '/' if 'next' not in request.POST else request.POST['next']
                return redirect(redir)
            else:
                return render(request, 'login.html', {'error': 'You have been Blocked, Contact Admins'})
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})
    else:
        context_dict = {'next': '/'}
        if 'status' in request.session:
            context_dict['status'] = request.session['status']
            del request.session['status']
        if 'next' in request.GET:
            context_dict['next'] = request.GET['next']
        return render(request, 'login.html', context_dict)


@anonymous_required
def register_user(request):
    # if request.user.is_authenticated():
    #     return redirect('/')
    context_dict = {}
    if request.method == 'POST':
        check_user = User.objects.filter(username=request.POST['username'],email=request.POST['email'])
        log.error(check_user)
        if check_user:
            context_dict["error"] = "User Already Exists!"
            return render(request, 'register.html', context_dict)
        else:
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'], password=request.POST['password'])
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.save()
            member = Member()
            member.user = user
            member.date_of_birth = datetime.strptime(request.POST['dob'], '%d/%m/%Y')
            member.details_visible = 'visible' in request.POST
            member.bio = request.POST['bio']
            member.save()
            request.session['status'] = "Registration Successful"
            redirect_to = '/' if 'next' not in request.POST else request.POST['next']
            return redirect('/login?next='+redirect_to)
    else:
        if 'next' in request.GET:
            context_dict['next'] = request.GET['next']
        return render(request, 'register.html', context_dict)


@anonymous_required
def forgot_password(request):
    # if request.user.is_authenticated():
    #     return redirect('/')
    if request.method == 'GET':
        if 'user' in request.GET and 'hash' in request.GET:
            return render(request, 'changeforgot.html', {'username': request.GET['user'],'hash': request.GET['hash']})
        else:
            return render(request, 'forgot.html')
    else:
        if 'forgot' in request.POST:
            if request.POST['username'] != "":
                user = User.objects.get(username=request.POST['username'])
                url = reverse('forgot-password') + '?user=' + user.username + '&hash=' + user.password
                url = request.build_absolute_uri(url)
                message = "Hi " + user.first_name + ",\n"
                message += "Please visit following link to reset password\n" + url
                send_mail('Reset Password', message, 'diskusforums@gmail.com', [user.email])
                return render(request, 'forgot.html', {'status': 'Please check your email for reset password link'})
            elif request.POST['email'] != "":
                user = User.objects.get(email=request.POST['email'])
                url = reverse('forgot-password') + '?user=' + user.username + '&hash=' + user.password
                url = request.build_absolute_uri(url)
                message = "Hi " + user.first_name + ",\n"
                message += "Username: " + user.username + "\n"
                message += "Please visit following link to reset password\n" + url
                send_mail('Reset Password', message, 'diskusforums@gmail.com', [user.email])
                return render(request, 'forgot.html', {'status': 'Please check your email for reset password link'})
            else:
                return render(request, 'forgot.html', {'error': 'Some Error Occurred'})
        elif 'change' in request.POST:
            user = User.objects.get(username=request.POST['username'])
            if '+'.join(request.POST['hash'].split(' ')) == user.password:  # hack because request replaced + with ' '
                user.set_password(request.POST['password'])
                user.save()
                request.session['status'] = "Successfully Changed Password"
                return redirect('/login/')
            else:
                return redirect('/')
        else:
            return render(request, 'forgot.html')


def profile(request, slug):
    member = Member.objects.get(slug=slug)
    return render(request, 'profile.html', {'member': member})

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found, server_error
from Diskus.models import *
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain


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
        paginator = Paginator(posts, 15) # Show 15 threads per page
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
        thread_id = request.POST.get('thread_id', '-1')
        content = request.POST.get('content', '-1')
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